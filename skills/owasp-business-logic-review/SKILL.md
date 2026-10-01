---
name: owasp-business-logic-review
description: 基于 OWASP 业务逻辑安全标准（OWASP WSTG-BUSL & Code Review Guide）的深度业务逻辑审查与接口防漏洞指南。专注于前后端数据流校验、防数据篡改、状态机防跳步与防逆向扭转、并发竞态（TOCTOU）防御、幂等性与防重放攻击、金融级高精度金额计算（Decimal）及安全失败（Fail-Closed）准则。当用户提及“业务逻辑审查”、“业务漏洞扫描”、“检查状态机”、“并发双花”、“接口幂等性”、“金额精度”、“防篡改”或“OWASP”时触发。
---

# OWASP 业务逻辑安全与代码审查指南 (OWASP Business Logic Review)

基于 OWASP Web Security Testing Guide (WSTG-BUSL) 与 OWASP Code Review Guide，本技能将顶尖安全机构关于**业务逻辑缺陷（Business Logic Flaws）、状态机跳步、并发时差与金融资金安全**的审查法则转化为可直接执行的 Agent 行动指南。

---

## 1. 核心心智模型 (Mental Models)

- **零信任客户端（Zero-Trust Client）**：  
  前端的表单验证、禁用状态、隐藏字段仅用于交互体验；**服务端必须假设所有入参均可被篡改、重放和伪造**。严禁直接信任客户端传入的计算金额、折扣和状态。
- **状态机不可越步（Strict State Machine Guards）**：  
  业务实体必须拥有封闭的状态转移矩阵。**任何变更必须先断言当前持久化状态属于合法源状态**，坚决拦截跳步执行与终态逆向篡改。
- **消除 TOCTOU 时差（Zero-Window Concurrency）**：  
  严禁“内存中检查余量，然后再单发 UPDATE”。资产扣减与状态更新必须通过原子 SQL、行级锁（`FOR UPDATE`）或分布式锁闭环，杜绝并发双花与超卖。
- **物理唯一键保障绝对幂等（Physical Unique Key Idempotency）**：  
  应用层 `SELECT` 判定无法阻挡高并发重试。所有关键结算、对账与支付回调必须依赖数据库物理唯一索引（如 `biz_identifier`）防重。
- **金融高精度与默认安全失败（Decimal & Fail-Closed）**：  
  金额计算严禁使用二进制浮点数（`float`）；异常时严格回滚事务并默认拒绝放行（Fail-Closed）。

---

## 2. 章节与参考路由 (Reference Routing)

当执行不同审查任务或扫描业务代码时，主动查阅 `references/` 目录下的相应模块：

- **审查接口入参、防范数值篡改与越权访问时**：  
  查阅 [01-data-validation-and-integrity.md](references/01-data-validation-and-integrity.md)  
  *涵盖：零信任客户端法则、负数反向套现拦截、服务端强制重算定价、BOLA 越权防范。*

- **审查审批流、订单/结算流程是否可被跳步绕过时**：  
  查阅 [02-workflow-and-state-machine-bypass.md](references/02-workflow-and-state-machine-bypass.md)  
  *涵盖：状态机转移白名单矩阵、跨步骤向导独立校验、终态不可逆与不可篡改。*

- **排查高并发重复扣款、超卖或 TOCTOU 时差漏洞时**：  
  查阅 [03-concurrency-and-race-conditions.md](references/03-concurrency-and-race-conditions.md)  
  *涵盖：TOCTOU 漏洞剖析、并发防御四层阶梯（原子单条更新/乐观锁/行级锁/分布式锁）。*

- **设计支付/对账回调、防范用户双击或网络重放攻击时**：  
  查阅 [04-idempotency-and-replay-defense.md](references/04-idempotency-and-replay-defense.md)  
  *涵盖：唯一幂等键设计、数据库物理唯一索引防重、幂等响应快照返回机制。*

- **核对金额分摊、浮点数舍入计算与异常事务回滚时**：  
  查阅 [05-financial-rules-and-fail-safe.md](references/05-financial-rules-and-fail-safe.md)  
  *涵盖：Decimal 精度保真、ROUND_HALF_UP 显式舍入、尾项平账法则、Fail-Closed 安全失败。*

---

## 3. 落地自查与评审清单 (Checklists)

- [OWASP 业务逻辑安全审查落地清单](checklists/business-logic-checklist.md)：涵盖输入数据、状态机、并发原子性、幂等防重与资金安全的 15 条刚性核对项。

---

## 4. 实战指令示例 (Usage Examples)

- **接口防篡改与金额安全扫描**：
  > “请以 `owasp-business-logic-review` 技能标准，扫描当前结算接口的入参处理与定价逻辑，检查是否存在负数金额套现或信任客户端计算的隐患。”
- **状态机与工作流完整性审查**：
  > “依据 `owasp-business-logic-review` 的状态机法则，审查当前退款/结算流转代码，确认是否有跳步可能或终态单据被非法覆写的风险。”
- **并发扣款与幂等性审查**：
  > “分析当前对账/回调接口的并发处理逻辑，排查是否存在 TOCTOU 竞态条件，并检查物理唯一键幂等设计是否完备。”
