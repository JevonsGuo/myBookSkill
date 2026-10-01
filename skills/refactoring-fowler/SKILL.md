---
name: refactoring-fowler
description: 基于 Martin Fowler《重构：改善既有代码的设计》（第2版）的专业代码重构与坏味道治理指南。适用于扫描既有代码坏味道（Code Smells）、小步安全重构、降低圈复杂度、长函数/臃肿类拆解、消除深层嵌套（卫语句）、以多态取代条件表达式、引入参数对象、两顶帽子法则防范、测试防护网审查及技术债清理场景。当用户提及“代码重构”、“重构既有代码”、“消除代码坏味道”、“Code Smells”、“提炼函数”、“降低圈复杂度”、“卫语句优化”、“消除重复代码”、“消除技术债”或“Martin Fowler”时触发。
---

# Martin Fowler 代码重构与坏味道治理指南 (Refactoring Guide)

基于 Martin Fowler 权威典籍《重构：改善既有代码的设计》（第 2 版），本技能将世界级重构工程学转化为 Agent 实战行动指南，专注于**代码坏味道精准诊断、可观察行为严格保全、小步快跑节奏控制与无破坏性演进**。

---

## 1. 核心心智模型 (Mental Models)

- **重构的第一铁律（The Golden Rule of Refactoring）**：  
  **“If it changes observable behavior, it is NOT refactoring.”**  
  重构是在不改变软件外部可观察行为的前提下改善内部结构。任何引入新功能、更改 API 字段定义或修改报错逻辑的行为，均严禁与重构混为一谈。
- **两顶帽子法则（Two Hats Discipline）**：  
  时刻明确当前戴哪顶帽子——戴“添加新功能”帽子时只增添特性与测试；戴“重构”帽子时只调整结构并保证测试全绿。**严禁在一次提交中同时戴两顶帽子**。
- **重构微节奏（The Micro-steps Rhythm）**：  
  小步快跑：修改一小步 → 跑测试验证绿灯 → 提交版本。每次修改应控制在极短时间内，若测试失败可在 10 秒内 `git reset` 回滚，绝不让系统处于不可编译或测试飘红状态。
- **测试防护网（Self-Testing Code Guard）**：  
  缺乏自动化测试覆盖的重构等同于裸奔与盲目制造 Bug。重构前必须确保测试网有效；若缺乏测试，先补齐核心端到端/单元测试，再动手重构。

---

## 2. 章节与参考路由 (Reference Routing)

当执行不同重构分析或代码改善任务时，主动查阅 `references/` 目录下的相应模块：

- **把握重构时机、控制提交粒度或权衡重构与重写时**：  
  查阅 [01-principles-and-rhythm.md](references/01-principles-and-rhythm.md)  
  *涵盖：两顶帽子隔离法则、重构 vs 重写决策树、四维重构时机（预备性/理解性/捡垃圾式重构）、测试防护网。*

- **审查既有代码、诊断代码缺陷或定位技术债根因时**：  
  查阅 [02-code-smells-catalog.md](references/02-code-smells-catalog.md)  
  *涵盖：24 种经典代码坏味道速查矩阵（膨胀剂、变革阻碍者、面向对象滥用、耦合破坏者等病症识别与对应手法）。*

- **动手拆分长函数、降解深层嵌套分支或消除重复 switch 时**：  
  查阅 [03-core-refactorings.md](references/03-core-refactorings.md)  
  *涵盖：提炼函数/变量、以卫语句取代嵌套、以管道取代循环、以多态取代条件分支、引入参数对象等核心手法标准机制。*

- **评估重构风险、审查外部 API 兼容性或警惕过度设计时**：  
  查阅 [04-refactoring-anti-patterns.md](references/04-refactoring-anti-patterns.md)  
  *涵盖：重构紧急叫停决策树、大爆炸重构防御、破坏公共契约防范、废弃委托（Deprecate & Delegate）过渡策略。*

---

## 3. 落地自查与评审清单 (Checklists)

- [代码坏味道扫描与安全重构落地清单](checklists/review-checklist.md)：用于重构前方案自检、PR 合并前质量门禁核对与代码异味体检打分。

---

## 4. 实战指令示例 (Usage Examples)

- **代码坏味道体检与诊断**：
  > “请基于 `refactoring-fowler` 技能，扫描以下代码文件中的代码坏味道（Code Smells），列出具体病症、根因分类及推荐的最小化重构步骤。”

- **长函数与深层嵌套安全重构**：
  > “请使用 `refactoring-fowler` 规范，重构这段有 5 层嵌套 if-else 的计算逻辑。采用卫语句平铺主干，并保持外部行为与方法签名完全兼容。”

- **重构 PR 质量门禁评审**：
  > “请按照 `refactoring-fowler` 的 `checklists/review-checklist.md`，对本次重构提交进行逐项核对并给出健康度打分与合规性判定。”
