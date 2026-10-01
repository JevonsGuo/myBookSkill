# 02 - 工作流跳步与状态机防绕过 (Workflow & State Machine Bypass)

## 一、 核心概念与审查准则

- **状态机不可越步（Strict State Machine Transitions）**：
  - 任何具有业务生命周期的实体（订单、结算单、凭证、审批流），必须拥有**明确、封闭的状态转移白名单矩阵**。
  - 严禁仅靠客户端跳转步骤来控制流程；**服务端必须在执行任何业务动作前，强校验当前实体的实际持久化状态**。
- **防止逆向/越级扭转（Prevent Reverse & Illegal Transitions）**：
  - 已完成终态的单据（如 `SETTLED` 已结算、`CLOSED` 已关闭），绝不允许被普通业务接口反向更新为初始态。
  - 严禁跳步调用：例如跳过“待清算对账核对”环节，直接调用“清算确认执行”接口。
- **前置条件强断言（Preconditions Enforcement）**：
  - 每一个状态流转接口，必须首先执行前置断言（Guards）：
    1. 当前状态是否在允许的源状态集合中？
    2. 相关联的附属单据（如支付流水）是否已确认为终态？

---

## 二、 状态扭转合法性决策树 (Decision Tree)

| 触发动作 | 当前数据库持久化状态 | 审查与执行动作 |
| :--- | :--- | :--- |
| **发起对账核对** | `PENDING_RECONCILIATION` (待对账) | **允许**：执行核对逻辑，更新为 `RECONCILED` 或 `DIFF_DETECTED` |
| **发起对账核对** | `SETTLED` (已结算) / `CANCELLED` (已作废) | **坚决拒绝（409 Conflict）**：终态单据禁止重复触发核对 |
| **执行清算结算** | `PENDING_RECONCILIATION` (尚未对账) | **坚决拒绝（400/409）**：禁止跳步！必须先完成对账才能结算 |
| **申请差错对冲/调整** | `SETTLED` (已结算) | **允许但必须走独立冲销流**：生成新调整单，原单状态变更为 `ADJUSTING`，禁止直接原地篡改原始金额 |

---

## 三、 典型状态机反模式 (Anti-patterns)

- **反模式 1：接口只管执行，不管前置状态（Blind State Execution）**
  - *表现*：结算确认接口只接收 `order_id`，直接执行 SQL：`UPDATE orders SET status='SETTLED' WHERE id=order_id`，没有检查当前 `status` 是不是 `PENDING_SETTLEMENT`。
  - *危害*：已退款、已取消甚至未支付的订单被直接强制置为“已结算”，引发资金错配。
- **反模式 2：依赖前端多步骤向导（Wizard Step Trusting）**
  - *表现*：系统有 3 个页面：Step 1 录入 $\to$ Step 2 审批 $\to$ Step 3 放款。后端 Step 3 接口没有校验审批记录是否真正通过，直接信任了前端的请求。
  - *危害*：用户直接抓包向 Step 3 发送 POST 请求，彻底绕过业务审批。
- **反模式 3：终态单据原地覆写（In-place Overwrite of Terminal Records）**
  - *表现*：已经对账完毕的月结单，当后续发现补差时，直接 `UPDATE` 原账单的金额和日期字段。
  - *危害*：丢失审计线索，导致前序财务快照与历史报表全部失真。

---

## 四、 Do & Don't 对比

### 场景：结算确认接口的状态机控制

```python
# ❌ DON'T: 原地直接更新，未断言前置状态，未检查并发冲突
@app.route('/api/settlement/confirm', methods=['POST'])
def confirm_settlement():
    data = request.json or {}
    record_id = data.get("record_id")
    
    # 致命缺陷：如果该记录已结算或已被撤销，依然会执行更新
    db.execute("UPDATE biz_settlement SET status = 'CONFIRMED' WHERE id = %s", (record_id,))
    return {"ok": True}

# ✅ DO: 状态白名单断言 + 乐观条件更新（行锁或状态防线）
@app.route('/api/settlement/confirm', methods=['POST'])
def confirm_settlement():
    data = request.json or {}
    record_id = data.get("record_id")
    if not record_id:
        return {"ok": False, "error": "MISSING_ID"}, 400

    # 允许流转到 CONFIRMED 的前置合法状态
    ALLOWED_SOURCE_STATUSES = ('PENDING_CONFIRM', 'VERIFIED_OK')

    with db_transaction() as tx:
        record = tx.query_one("SELECT id, status FROM biz_settlement WHERE id = %s FOR UPDATE", (record_id,))
        if not record:
            return {"ok": False, "error": "RECORD_NOT_FOUND"}, 404
            
        if record["status"] not in ALLOWED_SOURCE_STATUSES:
            return {
                "ok": False, 
                "error": "ILLEGAL_STATE_TRANSITION",
                "message": f"当前状态 {record['status']} 不允许执行结算确认，仅允许 {ALLOWED_SOURCE_STATUSES}"
            }, 409

        # 原子更新状态与确认时间
        affected = tx.execute(
            "UPDATE biz_settlement SET status = 'CONFIRMED', confirmed_at = NOW() WHERE id = %s AND status = %s",
            (record_id, record["status"])
        )
        if affected == 0:
            return {"ok": False, "error": "CONCURRENT_MODIFICATION"}, 409

    return {"ok": True, "status": "CONFIRMED"}
```
