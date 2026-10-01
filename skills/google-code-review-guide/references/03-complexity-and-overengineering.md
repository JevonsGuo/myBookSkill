# 03 - 复杂度控制与过度设计拦截 (Complexity & Over-engineering)

## 一、 核心概念与审查基准

- **复杂度的定义（Definition of "Too Complex"）**：
  - **无法被后续阅读代码的工程师快速理解**（High Cognitive Load）。
  - **其他工程师未来尝试调用或修改该代码时，极易不经意间引入新的 Bug**。
- **过度设计（Over-engineering / YAGNI 准则）**：
  - *核心原则*：**只解决当下明确需要解决的问题，严禁为“未来可能会发生的问题”编写投机性代码**。
  - 当未来的需求真正发生、呈现出具体业务形态时，再去重构演进。过早泛化往往预测错误，留下难以清除的僵尸抽象。
- **命名法则（Naming Standards）**：
  - 变量、函数与类名应具备自解释性（Self-documenting）。
  - 长度适中：足以准确传达职责与含义，同时不至于冗长晦涩。
- **注释法则（The Comment Rule）**：
  - **代码解释“What（在做什么）”，注释解释“Why（为什么这样做）”**。
  - 如果一段代码难以理解，**第一响应必须是简化代码结构，而不是写一段冗长的注释来解释这段复杂的代码**。
  - 例外情况：复杂算法、正则表达式、非显而易见的业务折中、兼容特定遗留系统 Bug 时，需要清晰的 Why 注释。

---

## 二、 复杂度与设计精简决策树 (Decision Tree)

| 场景 | 审查判定 | 审查决策与处置动作 |
| :--- | :--- | :--- |
| **出现了深层泛型/抽象工厂** | 当前系统仅有单一实现，作者称“为了以后扩展” | **坚决驳回**：要求移除多余的抽象层，直接采用简单的直接实现 |
| **代码逻辑难以理解** | 作者在方法上方写了 20 行注释解释执行流程 | **要求重构代码**：拆解大函数、提取具名子函数，将注释化为自解释的代码 |
| **代码使用了奇技淫巧（如复杂位运算或深层三元表达式）** | 既没有性能关键瓶颈证明，又极大降低了可读性 | **要求改写为直白清晰的常规语法**：可读性与可维护性优先于微小的非瓶颈性能 |
| **变量命名为 `temp`, `data`, `res` 等模糊词** | 变量在多处被引用，含义不明 | **要求改用具象业务名词**（如 `settlement_batch_context`） |

---

## 三、 典型坏味道与反模式 (Anti-patterns)

- **反模式 1：投机性抽象（Speculative Generality）**
  - *表现*：为了一个简单的两数计算，设计了 `CalculationStrategyFactory`, `AbstractFeeCalculatorProvider` 等 5 个接口与工厂。
  - *危害*：阅读者在十几个类之间反复跳转，维护成本暴增，而 99% 的扩展分支永远不会被实现。
- **反模式 2：掩耳盗铃式注释（Excuse Comments）**
  - *表现*：代码中充斥着“// 这里先粗暴循环，可能会 O(N^2)，注意性能”或“// 这段逻辑很乱，别动它”。
  - *危害*：用注释当作写出低质、复杂代码的免死金牌。
- **反模式 3：过长函数与上帝类（Long Method & God Class）**
  - *表现*：单个函数超过 80~100 行，内部交织了鉴权、数据解析、DB 读写、第三方调用、错误处理全部逻辑。
  - *危害*：无法做细粒度单元测试，变更时牵一发而动全身。

---

## 四、 Do & Don't 对比

### 场景：注释与函数自解释性

```python
# ❌ DON'T: 晦涩代码 + 用注释解释 What
# 遍历用户列表，如果状态是 1 且金额大于 1000 就将标记设置为 true
for u in u_list:
    if u[2] == 1 and u[5] > 1000:
        u[8] = True

# ✅ DO: 自解释命名 + 提炼函数，消除不必要的注释
VIP_THRESHOLD = Decimal('1000.00')

def should_upgrade_to_vip(user: User) -> bool:
    return user.status == UserStatus.ACTIVE and user.total_spend > VIP_THRESHOLD

for user in active_users:
    if should_upgrade_to_vip(user):
        user.mark_as_vip()
```

### 场景：过早泛化与当前实现

```python
# ❌ DON'T: 为只有一个实现的业务做全套抽象工厂与动态加载
class AbstractSettlementRuleEngineFactoryProvider:
    def create_instance_from_meta(self, meta_type: str) -> ISettlementRuleEngine:
        pass  # 实际目前全系统只有飞猪一种订单结算

# ✅ DO: 聚焦当前明确需求，保持直观扁平
class FliggySettlementEngine:
    """处理飞猪结算核对，未来若接入美团/携程且有真实通用逻辑时再抽象接口。"""
    def verify(self, order_data: dict) -> VerificationResult:
        ...
```
