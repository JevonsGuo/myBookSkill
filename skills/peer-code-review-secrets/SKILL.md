---
name: peer-code-review-secrets
description: 基于 SmartBear 工业级经典实证研究《同行代码审查的秘密》（Best Kept Secrets of Peer Code Review）的高效同行评审指南。专注于200-400行黄金审查规模控制、60分钟防疲劳断崖、作者导读机制、人机分工律（机器查语法/人类审逻辑）、高发缺陷清单挖掘（空指针/资源泄漏/N+1）及修复验证闭环。当用户提及“同行审查”、“Peer Review”、“审查规模”、“审查效率”、“代码走查规范”、“检查清单”、“SmartBear”时触发。
---

# 同行代码审查的秘密 (Best Kept Secrets of Peer Code Review)

基于 SmartBear 在思科系统（Cisco Systems）对 2500 次真实审查与 320 万行代码的实证研究，本技能将科学的同行代码审查规律转化为 Agent 行动准则，专注于**审查规模节奏控制、作者自我效应激发、人机分工分水岭、分类清单缺陷挖掘与修复验证闭环**。

---

## 1. 核心心智模型 (Mental Models)

- **200-400 行规模黄金律（The 200–400 LOC Rule）**：  
  单次审查代码量严格控制在 200~400 行以内，速度控制在 300~500 行/小时。**超 400 行或超 60 分钟，人类认知疲劳导致缺陷检出率断崖式暴跌**。
- **自我效应预期自净（The Ego Effect）**：  
  仅仅是“知道代码将被同行审阅”这一心理预期，就能促使作者在提交前自发排查并消除大量低级笔误。作者提交前必须先自行通读 Diff。
- **人机分工铁律（Automate Syntax, Review Logic）**：  
  机器负责格式、缩进、Linter 与基础语法；人类审查者绝不当“人肉编译器”，必须将 100% 脑力集中于**业务逻辑、边界时序、架构归属与异常防御**。
- **检查清单翻倍威力（Checklist Multiplier）**：  
  结构化分类清单能将缺陷检出率直接提升 100% 以上。团队线上复盘（RCA）必须直接反哺清单迭代。
- **修复验证与度量卫生（Verify Fixes & Metrics Hygiene）**：  
  15%~20% 的补丁会带来次生 Bug，必须复核修复 Diff；审查指标仅用于流程优化，**严禁用缺陷数量考核个人绩效（防范古德哈特定律）**。

---

## 2. 章节与参考路由 (Reference Routing)

当面临审查流程组织、规模把控或清单排查时，主动查阅 `references/` 目录下的相应模块：

- **评估 PR 规模合理性、控制单次审查速度与防范疲劳时**：  
  查阅 [01-empirical-limits-and-pacing.md](references/01-empirical-limits-and-pacing.md)  
  *涵盖：Cisco 实证数据、200-400 行规模界限、300-500 LOC/h 速度上限、60 分钟疲劳断崖。*

- **指导作者提交前自查、编写导读与建设无责正向文化时**：  
  查阅 [02-ego-effect-and-review-culture.md](references/02-ego-effect-and-review-culture.md)  
  *涵盖：自我效应心理学、作者主动导读（Guided Tour）批注、心理安全感与去个人化。*

- **划分自动化流水线边界、选择轻量级审查工具与形态时**：  
  查阅 [03-lightweight-methods-and-automation.md](references/03-lightweight-methods-and-automation.md)  
  *涵盖：5 大同行审查形态选型决策树、人肉 Linter 坏味道拦截、自动化 CI 门禁前置。*

- **利用分类清单挖掘空指针、资源泄漏与 N+1 陷阱时**：  
  查阅 [04-checklist-power-and-defect-mining.md](references/04-checklist-power-and-defect-mining.md)  
  *涵盖：清单翻倍效应、高发缺陷 6 大黄金分类、动态演进与 Living Checklist 机制。*

- **复核修复补丁、防范次生 Bug 与建立健康度量指标时**：  
  查阅 [05-defect-closure-and-metrics-hygiene.md](references/05-defect-closure-and-metrics-hygiene.md)  
  *涵盖：修复验证闭环铁律、古德哈特定律红线防范、RCA 根本原因分析与持续改进。*

---

## 3. 落地自查与评审清单 (Checklists)

- [SmartBear 轻量级同行审查落地打分自查表](checklists/peer-review-checklist.md)：用于日常同行代码走查、审查节奏把控与高发逻辑缺陷系统化排查。

---

## 4. 实战指令示例 (Usage Examples)

- **PR 审查节奏与规模体检**：
  > “依据 `peer-code-review-secrets` 的规模与节奏准则，评估当前 PR 是否超过了 400 行认知负荷极限，如果过大请给出科学拆分建议。”
- **基于分类清单的代码缺陷挖掘**：
  > “请使用 `peer-code-review-secrets` 的高发缺陷检查清单，对当前模块进行深度审查，重点排查空指针防御、资源泄漏（DB/句柄）以及 N+1 循环调用陷阱。”
- **修复补丁与次生缺陷复核**：
  > “对照 SmartBear 修复验证法则，复核作者最新提交的 Fix Commit，确认原缺陷是否根除，并检查是否引入了次生回归隐患。”
