---
name: test-case-generation
description: 基于工业级“测试脑”架构的专业测试用例生成与评审体系。拒绝只输出浅层 Happy Path，严格遵循 10 步强制执行工作流（需求拆解、风险识别、高频清单匹配、边界值计算、异常行为注入、历史Bug关联、标准表格输出、100分制自评打分与重点回归建议）。覆盖正常流、异常流、边界值、网络竞态、多端并发、资损风控与状态机防越权。当用户提及“生成测试用例”、“写测试用例”、“用例设计”、“测试方案”、“编写用例”、“功能测试用例”或“Test Case Generation”时触发。
---

# 工业级测试用例生成与评审指南 (Test Case Generation Skill)

本技能将资深测试工程师的**“测试脑”（风险驱动意识、边界值嗅觉、真实踩坑记忆与交付验收标准）**固化为标准化的 Agent 技能体系。旨在根除 AI 仅生成浅层“正常流”的通病，确保每份测试用例均具备严密性、实战深度与可执行性。

---

## 1. 核心心智模型 (Mental Models)

- **拒绝 Happy Path 偏见（Beyond the Happy Path）**：  
  正常流程仅占测试总量的 20%~30%；**70% 以上的缺陷潜藏在边界值、并发时差、超时重试、状态跳步与异常输入中**。严禁仅输出表面用例。
- **强制流水线分步生产（Enforced Stepwise Pipeline）**：  
  测试用例生成是严谨的推导过程，而非一次性文本输出。必须按 10 步工作流顺序输出中间分析结果，严禁跳步。
- **历史缺陷记忆驱动（Bug-Memory-Driven Testing）**：  
  没有“踩坑记忆”的用例苍白无力。生成用例时必须对照历史生产事故与高频缺陷库，强制生成对应防御性回归用例。
- **严格质量自检门禁（Scoring & Self-Review Gate）**：  
  用例生成后执行 100 分制打分自检。若缺少边界值、缺少异常流或缺少历史缺陷映射，触发硬性扣分；**评分 ≥85 分方可交付**。

---

## 2. 章节与参考路由 (Reference Routing)

在执行不同阶段的用例设计任务时，按需查阅 `references/` 目录中的对应规范：

- **了解角色底色、6 大覆盖维度与风险等级定义（P0/P1/P2）**：  
  查阅 [01-system-core-principles.md](references/01-system-core-principles.md)  
  *涵盖：高级测试工程师基准原则、风险驱动准则、P0/P1/P2 判定标准。*

- **执行 10 步标准化用例生成流水线（核心工作流）**：  
  查阅 [02-workflows-10steps.md](references/02-workflows-10steps.md)  
  *涵盖：需求拆解、风险识别、清单匹配、边界值、异常行为、历史Bug关联、表格生成、自检打分。*

- **执行 100 分制质量打分与扣分复查**：  
  查阅 [03-scoring-and-self-review.md](references/03-scoring-and-self-review.md)  
  *涵盖：5 大评分维度、硬性扣分红线、交付达标判定（≥85分）。*

- **输出统一 Markdown 表格（直接对接用例管理平台）**：  
  查阅 [04-outputs-specification.md](references/04-outputs-specification.md)  
  *涵盖：固定表格列名、TC-模块-序号编号规则、字段标准定义。*

---

## 3. 业务场景检查清单 (Templates & Checklists)

生成具体业务领域的用例时，主动加载 `templates/` 下对应的场景清单进行逐项核对：

- **账号与认证体系**：[templates/login-checklist.md](templates/login-checklist.md)（频控、Token过期、异地踢下线、弱网重试）
- **资金与支付对账**：[templates/payment-checklist.md](templates/payment-checklist.md)（并发扣款、时差、幂等性、金额精度）
- **交易与订单管理**：[templates/order-checklist.md](templates/order-checklist.md)（状态机闭环、取消退款、超时关单）
- **技术接口与网络**：[templates/api-interface-checklist.md](templates/api-interface-checklist.md)（参数篡改、超时重发、熔断降级）
- **全流程交付验收**：[checklists/test-case-quality-checklist.md](checklists/test-case-quality-checklist.md)（质量评审走查表）

---

## 4. 真实缺陷与长效资产库 (Cases & Assets)

- **典型历史缺陷库**：查阅 [cases/](cases/) 目录，汲取真实踩坑教训；
- **边界值判定规则库**：查阅 [assets/boundary-value-rules.md](assets/boundary-value-rules.md)（数值/字符/集合/时间越界）；
- **用户异常行为库**：查阅 [assets/user-abnormal-behaviors.md](assets/user-abnormal-behaviors.md)（连击、断网、刷新、并发双开）。

---

## 5. 实战执行指令示例 (Usage Examples)

### 指令：为新需求设计测试用例
> “请作为 `test-case-generation` 专家，根据以下需求设计测试用例。严格遵循 10 步工作流，匹配对应的场景 Checklist，输出标准表格并在末尾附上质量自评分数：
> 需求：[在此粘贴 PRD / 接口契约 / 功能描述]”
