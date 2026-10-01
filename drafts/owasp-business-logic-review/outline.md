# OWASP 业务逻辑安全与代码审查指南 (Curation & Outline)

## 一、 知识源映射 (OWASP WSTG-BUSL & Code Review Guide)
- WSTG-BUSL-01: Test Business Logic Data Validation（数据逻辑校验与数值边界）
- WSTG-BUSL-02 & 03: Test Ability to Forge Requests & Integrity Checks（请求伪造、隐藏字段篡改与不可信客户端）
- WSTG-BUSL-04: Test for Process Timing / Race Conditions（并发竞态、TOCTOU、双花与时序穿透）
- WSTG-BUSL-05: Test Function Use Limits & Idempotency（频次限制、重放攻击与幂等性）
- WSTG-BUSL-06: Testing for Circumvention of Workflows（工作流跳步、状态机绕过与逆向流）
- WSTG-BUSL-07: Test Defenses Against Misuse & Financial Calculations（防滥用、异常事务回滚与财务舍入防护）

## 二、 5 大高密度切片规划 (References)
- **Slug**: `owasp-business-logic-review`
- **切片 1: `references/01-data-validation-and-integrity.md`**：输入数据逻辑校验与完整性（零信任客户端原则、负数/极值/精度、前端参数穿透、禁止依赖客户端计算）
- **切片 2: `references/02-workflow-and-state-machine-bypass.md`**：工作流跳步与状态机防绕过（严格状态转移矩阵、前置条件断言、逆向反向流拦截、不可越步结算）
- **切片 3: `references/03-concurrency-and-race-conditions.md`**：并发竞态与时序漏洞（TOCTOU 检查与使用时差、并发扣款、分布式锁/乐观锁、行级悲观锁应用）
- **切片 4: `references/04-idempotency-and-replay-defense.md`**：幂等性机制与防重复结算（幂等键设计、防并发重放、重试风暴阻断、令牌生命周期）
- **切片 5: `references/05-financial-rules-and-fail-safe.md`**：财务结算与安全失败准则（Decimal 浮点精度保护、舍入截断套利防范、异常事务原子回滚、Fail-Safe 默认安全）
- **落地清单: `checklists/business-logic-checklist.md`**：业务逻辑与接口安全审查 15 项自查表
