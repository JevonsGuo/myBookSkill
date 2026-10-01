# 05 - 金融级计算与安全失败准则 (Financial Rules & Fail-Safe Defaults)

## 一、 核心概念与审查标准

- **绝对禁用二进制浮点数记账（No Float for Currency）**：
  - 计算机的 IEEE 754 浮点数（Python `float`, JS `Number`, Java `double`）在二进制表示时存在天然的精度丢失（如 `0.1 + 0.2 != 0.3`）。
  - **任何涉及金额、税率、扣款率、分摊结算的计算，必须严格使用定点高精度类型**：
    - Python: `decimal.Decimal`
    - Java: `java.math.BigDecimal`
    - 数据库存储: `DECIMAL(18, 2)` 或以“分/厘”为单位的 `BIGINT`。
- **舍入截断模式明确性（Explicit Rounding Mode）**：
  - 金额四舍五入必须明确指定舍入规则（如 `ROUND_HALF_UP` 向上舍入，或 `ROUND_DOWN` 截断）。
  - 杜绝隐式系统默认舍入，防范“香肠术”（Salami Slicing）微小截断金额累计套利。
- **默认安全失败原则（Fail-Safe Defaults / Fail-Closed）**：
  - 当核对逻辑或第三方通信发生未捕获异常、超时或无法判定真伪时，**系统必须默认拒绝操作（Fail-Closed），绝不允许“发生异常时默认放行或认为对账平齐”**。
- **事务原子性（Atomic Transactions）**：
  - 资金扣除、账单生成与状态变更必须在同一个强一致性数据库事务中完成，禁止裸跑单条操作留下孤儿记录。

---

## 二、 资金与异常处置决策树 (Decision Tree)

```text
进行资金结算或对账规则核对
│
├── 1. 数据类型审查
│   ├── 代码中出现 float(amount) 或直接对浮点数进行加减乘除？
│   │   ├── 是 ──► 坚决拦截！强制重构成 Decimal(str(amount))
│   │   └── 否 ──► 进入舍入规则检查
│
├── 2. 舍入与差额平衡
│   ├── 多项费用分摊相加是否严格等于总额？
│   │   ├── 存在每笔独立四舍五入后求和 ──► 存在分角差额风险！
│   │   │   └── 必须增加平账逻辑：将差额（差 1 分钱）归入最后一笔费用或杂费（Incidental）
│   │   └── 已由尾项平账 ──► 通过
│
└── 3. 异常处理与事务边界
    ├── 发生网络超时或未知 Exception：
    │   ├── 吞掉异常并返回 200/成功？ ──► 严厉驳回！违背 Fail-Safe 原则
    │   └── 回滚事务（Rollback），记录告警日志，抛出或返回明确 500/重试 ──► 安全放行
```

---

## 三、 典型资金与异常反模式 (Anti-patterns)

- **反模式 1：浮点精度引发的幽灵差错（Float Rounding Phantom Discrepancy）**
  - *表现*：使用 Python `float` 运算：`100.0 - 99.9`，结果为 `0.09999999999999432`。对账系统将其与 `0.1` 比较，判定为“核对不一致，产生差错”。
  - *危害*：导致每天产生大量虚假差错报警，人工核对成本激增。
- **反模式 2：空异常捕获导致隐蔽成功（Swallowing Exceptions as Success）**
  - *表现*：
    ```python
    try:
        verify_settlement_rules()
    except Exception:
        pass  # 假装没问题，继续往下执行发放款
    ```
  - *危害*：在数据库宕机或断网时，直接把未经核对的单据放行。
- **反模式 3：分摊累加误差（Split Allocation Leakage）**
  - *表现*：100 元总额分摊给 3 个商家，每人 `100 / 3 = 33.33` 元。三个 33.33 相加得 99.99，导致 0.01 元资金凭空蒸发或账面不平。
  - *危害*：长期累积导致财务审计审计不通过。

---

## 四、 Do & Don't 对比

### 场景：订单金额分摊与平账计算

```python
# ❌ DON'T: 浮点数计算 + 独立四舍五入，无法保证总额平账
def calculate_split_bad(total_amount, ratio1, ratio2):
    # 浮点运算精度丢失
    part1 = round(total_amount * ratio1, 2)
    part2 = round(total_amount * ratio2, 2)
    # 剩余费用，可能出现 0.009999999 或与总额不一致
    part3 = total_amount - part1 - part2
    return part1, part2, part3

# ✅ DO: 使用高精度 Decimal + 尾项自动平账（零差额保真）
from decimal import Decimal, ROUND_HALF_UP

def calculate_split_safe(total_amount_str: str, ratio1_str: str, ratio2_str: str):
    total = Decimal(str(total_amount_str))
    r1 = Decimal(str(ratio1_str))
    r2 = Decimal(str(ratio2_str))
    
    # 显式指定 ROUND_HALF_UP 向上舍入
    two_places = Decimal('0.01')
    part1 = (total * r1).quantize(two_places, rounding=ROUND_HALF_UP)
    part2 = (total * r2).quantize(two_places, rounding=ROUND_HALF_UP)
    
    # 尾项平账法则：最后一项等于总额减去前面各项之和，确保相加严格等于 total
    part3 = total - part1 - part2
    
    assert (part1 + part2 + part3) == total, "总账金额必须严格守恒"
    return part1, part2, part3
```
