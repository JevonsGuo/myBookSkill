---
name: google-code-review-guide
description: 基于 Google 官方工程审查实践（Google Engineering Practices: Code Review Guide）的专业代码评审与业务逻辑扫描指南。适用于前后端代码扫描、业务逻辑完整性验证、PR/CL评审、架构设计评估、过度工程识别、单元测试质量审查及代码审查沟通场景。当用户提及“代码审查”、“Code Review”、“代码扫描”、“审查业务逻辑”、“检查代码坏味道”、“PR审查”或“Google规范”时触发。
---

# Google 开发者代码审查指南 (Google Code Review Guide)

基于 Google 官方工程实践（Google Engineering Practices），本技能将世界级工业级代码评审标准转化为 Agent 行动指南，专注于**代码健康度持续提升、前后端业务逻辑闭环排查、复杂度控制与测试质量捍卫**。

---

## 1. 核心心智模型 (Mental Models)

- **最高仲裁准则（The Senior Principle）**：  
  **“Reviewers should favor approving a CL once it definitely improves the overall code health of the system, even if the CL isn't perfect.”**  
  代码审查的目的不是追求绝对完美，而是追求**持续改进（Continuous Improvement）**。只要本次变更明确净增了系统健康度，就不应因微小修饰阻碍前进。
- **事实胜于个人偏好（Facts Over Opinions）**：  
  技术事实、基准数据与官方规范高于主观审美。设计方案有同等依据时，尊重作者偏好；Style Guide 是编码风格的绝对权威。
- **功能性第一防线（Functionality First）**：  
  审查绝不只是看代码格式，核心在于追问：**代码是否真正达成了意图？对端到端用户是否有益？边缘与并发场景是否闭环？**
- **严拒“稍后清理”陷阱（No "Clean It Up Later"）**：  
  经验表明，“稍后清理” 95% 会变成“永远不清理”。凡是引入新复杂度和坏味道的代码，必须在当前 PR 修正。

---

## 2. 章节与参考路由 (Reference Routing)

当执行不同审查任务或扫描代码时，主动查阅 `references/` 目录下的相应模块：

- **面临设计分歧、评审沟通冲突或仲裁标准时**：  
  查阅 [01-standard-and-mindset.md](references/01-standard-and-mindset.md)  
  *涵盖：Code Health 净增原则、评审者责任、事实与偏好权衡决策树、对事不对人法则。*

- **扫描前后端业务代码、排查边界条件或并发竞态时**：  
  查阅 [02-functionality-and-design.md](references/02-functionality-and-design.md)  
  *涵盖：功能正确性决策树、快乐路径反模式、前后端校验脱节、状态机异常流闭环。*

- **识别过度设计、臃肿类、晦涩函数或命名注释问题时**：  
  查阅 [03-complexity-and-overengineering.md](references/03-complexity-and-overengineering.md)  
  *涵盖：YAGNI 原则、投机性抽象识别、注释解释 Why 而非 What、函数单一职责。*

- **审查测试用例质量、防范虚假覆盖或逐行审查代码时**：  
  查阅 [04-testing-and-code-health.md](references/04-testing-and-code-health.md)  
  *涵盖：生产代码同包测试底线、真实断言防伪、过度 Mock 坏味道、逐行与上下文审查。*

- **面对庞大变更、需要拆分 PR 或作者试图推脱重构时**：  
  查阅 [05-pr-hygiene-and-pushback.md](references/05-pr-hygiene-and-pushback.md)  
  *涵盖：小变更拆分网格（水平/垂直）、重构与业务解耦、评论标签分级（Nit/Blocker/FYI）、推脱拦截。*

---

## 3. 落地自查与评审清单 (Checklists)

- [Google 代码审查与业务验证打分清单](checklists/review-checklist.md)：用于日常 PR 合并前核对、业务代码深度扫描与 Code Review 打分评估。

---

## 4. 实战指令示例 (Usage Examples)

- **业务逻辑与健壮性扫描**：
  > “请以 `google-code-review-guide` 的标准，扫描当前这个支付回调接口代码，重点检查功能完整性、边界异常处理和状态机闭环。”
- **PR 综合代码评审**：
  > “依据 `google-code-review-guide` 对这几个文件的改动进行 Code Review，输出包含设计、复杂度、测试及改进意见（区分 Blocker 与 Nit）的评审报告。”
- **过度设计与复杂度检查**：
  > “帮我审视当前新增的策略类与工厂设计，是否存在 YAGNI 违背和投机性抽象。”
