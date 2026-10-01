# 04 - 幂等性设计与防重放攻击 (Idempotency & Replay Defense)

## 一、 核心概念与审查标准

- **幂等性定义（Idempotency Standard）**：
  - **一个操作无论被请求 1 次还是重复请求 100 次，系统产生的业务结果和副作用必须完全一致**。
  - 特别是在涉及“扣款、退款、打款、生成结算单、第三方回调”等场景中，**缺乏幂等性是最高危的业务设计缺陷**。
- **重放场景源头（Sources of Duplication）**：
  1. *用户端双击/多重提交*：前端未做防抖，或用户网络卡顿时连续点击。
  2. *网关/微服务自动重试*：网络超时导致客户端重试，前序请求实际已在服务端执行。
  3. *第三方回调重推*：飞猪、携程、美团或支付宝等支付渠道在未收到 200 回应前会定时重发同一笔回调消息。
- **唯一幂等键原则（Idempotency Key & Unique Constraint）**：
  - **最可靠的幂等防线永远是数据库唯一索引（Unique Constraint）**，而不是应用层查询（SELECT）。
  - 必须由业务唯一标识（如 `biz_identifier`、`ota_order_no`、或客户端生成的 `idempotency_key`）构成唯一约束。

---

## 二、 幂等处理与防重决策树 (Decision Tree)

```text
接收到修改资产/结算请求
│
├── 1. 唯一凭证提取
│   ├── 请求是否携带业务唯一键（如 biz_identifier / ota_order_no）？
│   │   ├── 否 ──► 驳回请求，要求提供唯一流水标识
│   │   └── 是 ──► 进入去重判定
│
├── 2. 状态查询与并发拦截
│   ├── 查询幂等记录表（或唯一单据状态）：
│   │   ├── 状态为 SUCCESS（已处理成功） ──► 直接返回上次成功的结果快照，不重复执行
│   │   ├── 状态为 PROCESSING（正在处理中） ──► 返回 409 / 提示正在处理中，拒绝并发重复穿透
│   │   └── 不存在记录 ──► 进入第 3 步
│
└── 3. 事务执行与原子占位
    └── 开启事务，向幂等记录表插入 (biz_identifier, status='PROCESSING') 唯一记录：
        ├── 插入触发唯一键冲突 ──► 说明并发命中，回滚并拦截
        └── 插入成功 ──► 执行实际结算核心逻辑，执行完毕后将状态更新为 SUCCESS
```

---

## 三、 典型重放反模式 (Anti-patterns)

- **反模式 1：查表判断是否存在（Check-then-Insert Anti-pattern）**
  - *表现*：先 `SELECT * FROM settlement WHERE biz_identifier = %s`，如果为空才执行插入；但数据库没有在 `biz_identifier` 上建 `UNIQUE KEY`。
  - *危害*：两个完全相同的回调同时打入，两边都查出“不存在”，随后双双插入成功，导致同一笔订单结算两次。
- **反模式 2：内存 Set / 缓存锁代替持久化唯一索引（Cache-Only Deduplication）**
  - *表现*：仅在 Redis 里设置 `SETNX order_id 1`，如果 Redis 发生主从切换或缓存淘汰，锁直接失效。
  - *危害*：偶发性缓存抖动导致数千笔订单重复放款。
- **反模式 3：无返回快照导致假死（No Idempotent Response Snapshot）**
  - *表现*：第二次请求命中幂等时，直接抛异常报错，导致上游回调方认为请求失败并不断发起重试风暴。
  - *危害*：应返回与首次相同的成功状态（如 `{"code": 200, "status": "ALREADY_PROCESSED"}`），让上游停止重推。

---

## 四、 Do & Don't 对比

### 场景：第三方渠道结算回调处理

```python
# ❌ DON'T: 无唯一键保护，查表判定存在竞态，易产生重复结算
@app.route('/api/webhook/settlement-callback', methods=['POST'])
def settlement_callback():
    payload = request.json or {}
    biz_identifier = payload.get("biz_identifier")
    
    # 竞态漏洞：若第三方同时重推 2 个请求，此处将同时返回 None
    existing = db.query_one("SELECT id FROM biz_settlement WHERE biz_identifier = %s", (biz_identifier,))
    if existing:
        return {"code": 200, "msg": "已存在"}
        
    # 执行记账与扣划资金，极高概率出现重复记账
    create_settlement_record(payload)
    return {"code": 200, "msg": "处理成功"}

# ✅ DO: 利用数据库唯一索引 + 状态机实现绝对幂等
@app.route('/api/webhook/settlement-callback', methods=['POST'])
def settlement_callback():
    payload = request.json or {}
    biz_identifier = payload.get("biz_identifier")
    if not biz_identifier:
        return {"code": 400, "msg": "缺少 biz_identifier"}, 400

    try:
        with db_transaction() as tx:
            # 利用唯一键防止并发重复插入
            affected = tx.execute(
                """
                INSERT INTO biz_settlement_idempotency (biz_identifier, status, created_at)
                VALUES (%s, 'PROCESSING', NOW())
                ON DUPLICATE KEY UPDATE updated_at = NOW()
                """,
                (biz_identifier,)
            )
            # 查询当前幂等单据的终态
            record = tx.query_one(
                "SELECT status, response_json FROM biz_settlement_idempotency WHERE biz_identifier = %s FOR UPDATE",
                (biz_identifier,)
            )
            if record and record["status"] == "SUCCESS":
                # 已经成功执行过，直接返回先前生成的响应快照，确保上游感知幂等
                return json.loads(record["response_json"]), 200
            
            # 执行核心清算逻辑
            result_data = execute_settlement_logic(tx, payload)
            
            # 更新幂等状态为 SUCCESS 并保存快照
            tx.execute(
                "UPDATE biz_settlement_idempotency SET status = 'SUCCESS', response_json = %s WHERE biz_identifier = %s",
                (json.dumps(result_data), biz_identifier)
            )
            return result_data, 200

    except pymysql.err.IntegrityError:
        # 并发冲突被唯一索引天然拦截
        return {"code": 409, "msg": "该单据正在结算处理中，请勿重复提交"}, 409
```
