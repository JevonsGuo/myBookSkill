# 《测试用例生成 Skill》提炼大纲与架构拆解

- **来源**: 微信公众号「雏实」实战教程《测试用例生成Skill，附完整代码+md，直接照抄！》
- **核心定位**: 将资深测试工程师的“测试脑”、历史缺陷库、高频检查清单与交付自检标准系统化转化为 Agent Skill。
- **解决痛点**: 告别普通 Prompt 输出的浅层 Happy Path，杜绝漏测频控、边界值、Token失效、弱网并发与历史重复踩坑。

## 模块架构拆解 (8 大模块 -> 标准 Skill 布局)

1. **技能入口与心智模型 (`SKILL.md`)**:
   - 触发条件：测试用例、用例设计、测试分析、写测试用例、Test Case Generation
   - 心智模型：非 Happy Path 强制覆盖、生产线分步输出、缺陷记忆、自检评分闭环

2. **核心规范 (`references/`)**:
   - `01-system-core-principles.md`: 高级测试工程师角色与测试原则（6大覆盖维度、风险等级划分 P0/P1/P2）
   - `02-workflows-10steps.md`: 10 步强制链路（需求拆解 -> 风险点 -> 模板匹配 -> 边界值 -> 异常行为 -> Bug关联 -> 表格生成 -> 自评打分 -> 回归建议）
   - `03-scoring-and-self-review.md`: 100 分制质量评分标准（扣分规则、≥85分交付判定）
   - `04-outputs-specification.md`: 固定表格格式（用例编号、模块、场景、前置、步骤、预期、风险、回归、历史Bug）

3. **场景检查清单 (`templates/`)**:
   - `login-checklist.md`: 登录认证场景 Checklist
   - `payment-checklist.md`: 支付交易与结算 Checklist
   - `order-checklist.md`: 订单状态与交易流程 Checklist
   - `api-interface-checklist.md`: 接口通用技术与健壮性 Checklist

4. **真实缺陷库 (`cases/`)**:
   - `case-01-sms-rate-limit-bypass.md`: 验证码频控与过期失效
   - `case-02-token-expiration-leak.md`: Token失效后接口未拦截
   - `case-03-concurrent-double-spend.md`: 并发网络重试导致重复扣款

5. **规则与资产库 (`assets/`)**:
   - `boundary-value-rules.md`: 边界值与等价类判定规则
   - `user-abnormal-behaviors.md`: 用户异常行为库（弱网、连点、多端、刷新、超时）

6. **质量评审清单 (`checklists/`)**:
   - `test-case-quality-checklist.md`: 用例交付与走查落地清单
