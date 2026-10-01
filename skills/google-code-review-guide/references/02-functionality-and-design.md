# 02 - 功能正确性与架构设计审查 (Functionality & Design)

## 一、 核心概念与审查维度

- **功能性黄金问答（The Functionality Question）**：
  1. **代码是否真正达成了开发者的意图？**
  2. **开发者的意图对代码的使用者（最终用户与后续维护的工程师）是否真正有益？**
- **双重用户心智（Dual Users）**：
  - *终端用户*：是否会导致交互卡顿、数据丢失、报错提示不知所云、业务状态卡死？
  - *开发者用户*：未来调用这段 API、继承这个类、扩展这个逻辑时，是否容易误用或引入新 Bug？
- **并发与竞态防御（Parallel Programming & Concurrency）**：
  - 并发问题（死锁、竞争条件、内存可见性、ABA 问题）很难通过常规单元测试复现。
  - **审查者必须在大脑中模拟并发执行**：是否存在未加保护的共享可变状态？锁的粒度是否对称？事务边界是否完整？
- **架构归属（Architectural Placement）**：
  - 这段逻辑属于业务层、领域层还是基础设施层？
  - 是否应该沉淀到公共库，还是仅在此模块内私有实现？是否破坏了既有的依赖方向？

---

## 二、 业务功能与设计决策树 (Decision Tree)

```text
遇到新增业务逻辑变更
│
├── 1. 架构定位审查
│   ├── 该功能本系统正准备弃用/下线？ ──► 立即礼貌拒绝该变更，指出替代路线
│   ├── 该逻辑在其他模块已有现成实现？ ──► 指引复用已有公共模块，避免重复造轮子
│   └── 依赖方向是否跨层（如底层依赖上层）？ ──► 驳回并要求依赖倒置（Dependency Inversion）
│
├── 2. 功能闭环与数据流审查
│   ├── 输入参数是否存在空值/负数/越界？ ──► 要求补充边界防御和前置校验（Preconditions）
│   ├── 异步/并发操作是否存在共享状态？ ──► 评估锁或无锁并发模型，严防竞态条件与死锁
│   └── 状态机扭转是否闭环（如退款、失败回调）？ ──► 重点排查异常流是否会造成状态挂死
│
└── 3. 终态判定
    └── 整体架构与功能无严重设计缺陷 ──► 进入细节与测试审查
```

---

## 三、 典型业务反模式与漏洞 (Anti-patterns)

- **反模式 1：快乐路径偏见（Happy Path Bias）**
  - *表现*：代码只处理了第三方接口返回 200 或数据格式完全合法的理想状态，缺少超时重试、状态不一致重试补偿。
  - *危害*：一旦网络抖动或上游返回空字段，系统直接抛出未捕获异常并崩溃。
- **反模式 2：盲目并发（Unjustified Concurrency）**
  - *表现*：为了“看起来更高级”，在一个简单的批处理逻辑中引入多线程/协程，却引入了数据竞争风险。
  - *危害*：排查死锁与数据不一致消耗数百倍维护成本，得不偿失。
- **反模式 3：前后端校验脱节（Frontend-Only Validation）**
  - *表现*：认为前端已经通过下拉框或表单校验了“金额必须大于 0”，后端的 API 路由就直接信任传入参数。
  - *危害*：攻击者或第三方脚本直接绕过前端调用接口，导致非法业务数据落地。

---

## 四、 Do & Don't 对比

### 场景：后端接口接收金额与订单状态时

```python
# ❌ DON'T: 假设前端传入的数据一定是可信的，缺乏防御性编程
@app.route('/api/settle', methods=['POST'])
def settle_order():
    data = request.json
    order_id = data['order_id']
    amount = data['amount']
    # 直接计算并执行扣款，若 amount 为负数或订单已被取消，业务将发生灾难
    execute_payment(order_id, amount)
    return {"status": "success"}

# ✅ DO: 前置断言、边界防范、状态机校验
@app.route('/api/settle', methods=['POST'])
def settle_order():
    data = request.json
    if not data or 'order_id' not in data or 'amount' not in data:
        return {"error": "INVALID_ARGUMENT", "message": "Missing required fields"}, 400
    
    amount = Decimal(str(data['amount']))
    if amount <= Decimal('0.00'):
        return {"error": "INVALID_AMOUNT", "message": "Amount must be strictly positive"}, 400
    
    order = order_repo.find_by_id_for_update(data['order_id'])
    if not order or not order.can_settle():
        return {"error": "ILLEGAL_STATE", "message": f"Order {order.id} cannot be settled in state {order.status}"}, 409
        
    order.execute_settlement(amount)
    return {"status": "success", "order_id": order.id}
```
