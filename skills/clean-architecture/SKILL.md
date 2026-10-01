---
name: clean-architecture
description: 基于 Robert C. Martin (Uncle Bob)《架构整洁之道》(Clean Architecture) 的专业系统分层与架构治理指南。适用于整洁架构设计、同心圆四层分层规范、依赖关系原则（Dependency Rule）、端口与适配器（六边形架构）、跨边界数据隔离（DTO/RequestModel/ViewModel）、细节即插件解耦（数据库是细节、Web是细节、框架非侵入）、依赖倒置（DIP）、无环依赖（ADP）、消除伪分层及架构边界腐化审查场景。当用户提及“整洁架构”、“Clean Architecture”、“Uncle Bob”、“依赖倒置原则”、“系统分层设计”、“六边形架构”、“端口与适配器”、“边界隔离”、“架构设计评审”或“消除循环依赖”时触发。
---

# Uncle Bob 整洁架构与分层治理指南 (Clean Architecture)

基于软件工程大师 Robert C. Martin (Uncle Bob) 经典名著《架构整洁之道》（Clean Architecture），本技能将世界级系统架构原则转化为 Agent 实战行动指南，专注于**依赖单向朝内流向、业务核心零框架污染、细节即插件隔离与高弹性独立演进**。

---

## 1. 核心心智模型 (Mental Models)

- **依赖关系第一法则（The Dependency Rule）**：  
  **“源码依赖方向必须永远指向高层策略（由外圆指向内圆）。”**  
  内圆（Entities / Use Cases）绝不能知晓外圆（Frameworks / Database / UI）的任何类、方法或数据格式。外层依赖内层，内层对外部世界一无所知。
- **细节即插件法则（Details as Plugins）**：  
  数据库是细节、Web 是细节、Spring/Express 是细节、消息队列是细节。业务核心决定系统价值，技术框架只是挂载在核心周围随时可以被拔掉替换的“插件”。
- **端口与适配器解耦（Ports & Adapters）**：  
  用例层通过自身定义的输入端口（Input Boundary）接收外部指令，通过自身定义的输出端口（Output Boundary）指挥外界持久化或展示。通过依赖倒置（DIP）彻底切断对底层实现的直接依赖。
- **独立可测试性防线（Independent Testability）**：  
  优秀的架构必须支持脱离数据库、脱离 Web 服务器、脱离 UI，仅凭借纯内存（In-Memory）存根在数毫秒内跑通 100% 核心业务用例测试。

---

## 2. 章节与参考路由 (Reference Routing)

当执行系统设计、模块划分、代码分层或架构 Review 时，主动查阅 `references/` 目录下的相应模块：

- **规划系统分层目录、划定代码归属或校验模块依赖流向时**：  
  查阅 [01-dependency-rule-and-layers.md](references/01-dependency-rule-and-layers.md)  
  *涵盖：依赖单向倒置法则、同心圆四层职责划界（Entities/Use Cases/Adapters/Frameworks）、分层决策树。*

- **设计输入输出端口、规范跨边界传参或防范实体泄露时**：  
  查阅 [02-boundaries-and-data-crossing.md](references/02-boundaries-and-data-crossing.md)  
  *涵盖：架构边界划定、Input/Output Ports 体系、跨边界数据结构（RequestModel/ResponseModel/ViewModel）、时序流转。*

- **解耦数据库/Web框架、实施延迟技术选型或编写组装代码时**：  
  查阅 [03-policy-vs-details.md](references/03-policy-vs-details.md)  
  *涵盖：数据库是细节、Web是细节、框架绑架防御、延迟技术决策树、Composition Root（装配根）规范。*

- **审查架构设计坏味道、排查循环依赖或治理伪分层时**：  
  查阅 [04-architectural-anti-patterns.md](references/04-architectural-anti-patterns.md)  
  *涵盖：伪分层穿透治理、胖控制器治理、ADP 无环依赖破除决策树、SDP/SAP 稳定性原则。*

---

## 3. 落地自查与评审清单 (Checklists)

- [整洁架构设计与边界审查清单](checklists/review-checklist.md)：用于架构方案设计评审、新建模块目录校验、PR 分层合规核对与 100% 架构体检。

---

## 4. 实战指令示例 (Usage Examples)

- **新业务模块分层骨架规划**：
  > “请基于 `clean-architecture` 技能，为‘用户积分结算’模块设计符合同心圆规范的目录结构与端口接口，确保领域实体不包含任何 ORM 注解。”

- **消除框架侵入与边界穿透重构**：
  > “当前 Controller 中直接注入了 MySQLRepository 并穿透操作了数据库。请根据 `clean-architecture` 规范，引入 Use Case 与 Input/Output Ports 实施依赖倒置重构。”

- **系统架构方案合规评审**：
  > “请按照 `clean-architecture` 的 `checklists/review-checklist.md`，对本次微服务拆分方案的分层边界、数据穿透与组件依赖方向进行逐项审查与健康度打分。”
