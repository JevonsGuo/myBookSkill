# 01 - 输入逻辑校验与数据完整性 (Data Validation & Integrity)

## 一、 核心概念与审查基准

- **零信任客户端原则（Zero-Trust Client Principle）**：
  - **来自客户端的任何数据（包括 JSON Body、Query 参数、Headers、Cookie、甚至前端生成的隐藏字段）必须视作不可信与敌对的**。
  - 前端 UI 的表单验证、灰色不可选（disabled）按钮仅用于优化正常用户的交互体验，**绝不能作为后端的安全与业务防线**。
- **禁止信任客户端计算结果（Never Trust Client Calculations）**：
  - 核心商业属性（商品单价、折扣后实付、佣金比例、结算总额）必须且只能在**服务端权威数据库和领域逻辑中独立计算**。
  - 客户端只能传递“商品 ID、数量、选中的优惠券 ID”，绝不允许直接接收客户端算好的 `actual_amount`。
- **数值与边界强约束（Numeric Boundaries & Types）**：
  - 校验数值不仅要判空，必须强制校验业务合法区间（如金额 $> 0$、退款金额 $\le$ 订单剩余可退金额）。
  - 防范负数金额攻击（传入负数抵扣，反向套现增加余额）。

---

## 二、 输入数据逻辑审查决策树 (Decision Tree)

```text
接收到包含商业数据的前端请求
│
├── 1. 来源与字段审查
│   ├── 请求中包含由前端算出的单价/折后总额/佣金？ ──► 坚决剔除！改为服务端重算
│   └── 包含数据库主键或权限相关 ID？ ──► 必须校验当前登录身份是否拥有该资源的访问权（防 BOLA/越权）
│
├── 2. 数值与范围约束
│   ├── 金额字段是否允许负数？ ──► 严禁负数（除非特定红字对冲接口且有严格审批流）
│   ├── 数量/天数是否小于 1 或超出上限？ ──► 设定严苛业务上限，拦截越界
│   └── 字符串长度/特殊字符是否有约束？ ──► 防止长文本内存溢出与注入风险
│
└── 3. 终态判定
    └── 基础业务校验完全闭环 ──► 进入状态机与时序校验
```

---

## 三、 典型业务反模式 (Anti-patterns)

- **反模式 1：负数反向套现（Negative Price Manipulation）**
  - *表现*：订单结算接口接收 `{"amount": -500}`，系统未校验 `amount > 0`，扣款逻辑执行 `balance = balance - amount`，导致账户余额凭空增加 500 元。
  - *危害*：导致严重的资金与账目灾难。
- **反模式 2：前端传参定价格（Client-Supplied Price）**
  - *表现*：接口定义 `{"item_id": "123", "price": 0.01}`，后端直接用 `price` 生成结算单。
  - *危害*：攻击者拦截 HTTP 请求将 1000 元商品改为 0.01 元结算。
- **反模式 3：浮点数弱类型比对（Loose Type Matching）**
  - *表现*：在 Python 或 JS 中直接拿 `0.1 + 0.2` 与 `0.3` 做 `==` 比对。
  - *危害*：精度偏差导致本该通过的结算对账逻辑永久报错，或者出现微量金额差额悬挂。

---

## 四、 Do & Don't 对比

### 场景：订单结算接口入参校验

```python
# ❌ DON'T: 直接接收客户端计算的折后金额与数量，无正向边界校验
@app.route('/api/order/settle', methods=['POST'])
def settle_order():
    data = request.json
    order_id = data.get("order_id")
    # 致命漏洞：直接信任客户端传入的实付金额，若为负数或0.01将导致重大资金流失
    settled_amount = Decimal(str(data.get("settled_amount", 0)))
    
    execute_payment(order_id, settled_amount)
    return {"ok": True}

# ✅ DO: 服务端强制重算、严格验证正数与订单状态
@app.route('/api/order/settle', methods=['POST'])
def settle_order():
    data = request.json or {}
    order_id = data.get("order_id")
    coupon_id = data.get("coupon_id")
    
    if not order_id:
        return {"ok": False, "error": "MISSING_ORDER_ID"}, 400
        
    order = order_repo.get_by_id(order_id)
    if not order:
        return {"ok": False, "error": "ORDER_NOT_FOUND"}, 404
        
    # 服务端根据权威定价与优惠规则，独立计算应付/结算金额
    expected_amount = pricing_service.calculate_settlement(order, coupon_id)
    if expected_amount <= Decimal("0.00"):
        return {"ok": False, "error": "INVALID_CALCULATED_AMOUNT"}, 400
        
    execute_payment(order.id, expected_amount)
    return {"ok": True, "settled_amount": float(expected_amount)}
```
