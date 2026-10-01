# 04 - 测试覆盖与代码健康度标准 (Testing & Code Health)

## 一、 核心概念与审查准则

- **同包提交原则（Tests in the Same CL）**：
  - **任何修改或新增业务逻辑的变更，必须在同一个 CL/PR 中附带对应的单元测试或集成测试**（除极少数生产紧急救火外）。
  - 严禁“先上线功能，后续再补测试”的推脱承诺。
- **有效断言准则（Meaningful Assertions）**：
  - 测试不会自我校验；**当业务代码被破坏时，测试必须能够真实失败**。
  - 警惕“无断言测试”（只调用函数不报错就当测试通过）或“脆弱测试（Flaky Tests）”。
- **测试代码也是一等公民（Tests Are Code Too）**：
  - 绝不能因为“这只是测试代码”就容忍意大利面条式的混乱设计。
  - 测试必须保持简单、清晰、独立（F.I.R.S.T 原则：快速、独立、可重复、自足校验、及时）。
- **逐行审查法则（Review Every Line）**：
  - 审查者必须审阅被指派的所有代码行。**严禁因为代码是资深工程师写的，就粗略扫过并默认其正确**。
  - 若代码过于晦涩导致审查者无法看懂，应要求作者重构写清晰；如果你看不懂，未来的维护者大概率也看不懂。
- **上下文视野（Broader Context）**：
  - 不要只看 Diff 工具展示的那几行改动，必须结合整个类/文件的上下文来审视。
  - 例如：新增的 5 行代码可能本身没语法问题，但如果它是塞进了一个已经 100 行的遗留函数里，此时就必须要求重构拆分。

---

## 二、 测试与完整性审查决策树 (Decision Tree)

```text
审查 PR 中的测试代码
│
├── 1. 是否包含测试？
│   ├── 否，且新增/修改了分支逻辑 ──► 坚决驳回，要求同包补齐测试
│   └── 是 ──► 进入测试质量排查
│
├── 2. 断言有效性排查
│   ├── 测试是否有断言（assert）？ ──► 无断言或仅 assert True 视为虚假测试，立即拦截
│   ├── 断言是否只校验了响应码 200，未校验返回业务字段？ ──► 要求断言精确到核心业务状态与计算值
│   └── 是否覆盖了边界值与异常分支（如 400/500/None）？ ──► 要求补充负向测试用例
│
└── 3. 测试维护性排查
    ├── 测试之间是否存在共享可变全局状态或执行顺序依赖？ ──► 要求解耦，确保独立可重复执行
    └── 测试代码是否充斥大量重复的 Mock/Setup 逻辑？ ──► 建议提取标准的 Test Fixture / Builder
```

---

## 三、 测试与健康度反模式 (Anti-patterns)

- **反模式 1：虚假安全感（False Positive Tests / Trivial Asserts）**
  - *表现*：写了测试，但断言极其敷衍（如 `assert result is not None`），即便业务计算逻辑全算错，测试依然绿灯通过。
  - *危害*：制造了测试覆盖率虚高的假象，在重构时失去安全保护。
- **反模式 2：过度 Mock（Over-mocking / Mocking Internal Details）**
  - *表现*：把所有内部私有方法、中间变量都 Mock 掉，测试变成了对实现细节的死板镜像。
  - *危害*：业务代码稍微重构一下（即使对外行为完全一致），所有测试全部挂掉。
- **反模式 3：温水煮青蛙（Broken Window Syndrome）**
  - *表现*：看到原有文件已经很烂，于是在里面随便再加一个 if-else 补丁，导致文件越来越烂。
  - *危害*：小坏味道逐渐累加，最终使整个模块沦为无法维护的死代码。

---

## 四、 Do & Don't 对比

### 场景：测试用例断言设计

```python
# ❌ DON'T: 虚假测试，缺乏对业务结果的深度断言
def test_settle_order_discount():
    engine = FliggySettlementEngine()
    result = engine.verify({"amount": 100, "coupon": 20})
    # 只要没抛异常就过，完全无法验证扣减 20 元的逻辑是否生效
    assert result is not None

# ✅ DO: 覆盖输入、确切业务字段、计算精度与边界
def test_settle_order_should_deduct_coupon_accurately():
    engine = FliggySettlementEngine()
    order_payload = {
        "order_id": "FLIGGY_TEST_001",
        "gross_amount": Decimal("100.00"),
        "coupon_amount": Decimal("20.00")
    }
    
    result = engine.verify(order_payload)
    
    # 严格验证计算结果与业务状态
    assert result.is_valid is True
    assert result.settled_amount == Decimal("80.00")
    assert result.status == "READY_FOR_PAYMENT"
```
