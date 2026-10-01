# 10 步标准化用例生成流水线 (Stepwise Production Line)

为了防止 AI“一步到位”产生内容空洞与遗漏，Agent 必须按顺序输出每一步的**中间推导结果**，严禁跳步。

```text
Step 1: 需求解析 ──> Step 2: 拆解功能 ──> Step 3: 识别风险 ──> Step 4: 匹配 Checklist ──> Step 5: 边界分析
                                                                                             │
Step 10: 回归建议 <── Step 9: 质量自检 <── Step 8: 表格生成 <── Step 7: 历史关联 <── Step 6: 异常行为注入
```

---

## 步骤详解

### 步骤 1：输入与理解需求 (Requirement Ingestion)
- **动作**：阅读并复述用户的输入需求文本，梳理出前置条件、输入参数、预期业务产出与涉及的角色权限。

### 步骤 2：拆解功能模块 (Functional Decomposition)
- **动作**：将大需求拆解为独立的子模块或操作节点。
- **产出示例**：`[模块A: 验证码获取]`, `[模块B: 登录凭证核验]`, `[模块C: 会话Token签发与维持]`。

### 步骤 3：识别业务链路与高风险点 (Risk Identification)
- **动作**：从资损、安全、性能与数据一致性角度挖掘高危场景。
- **思考重点**：
  - 是否涉及资金/扣费/对账？
  - 是否存在并发双击可能？
  - 依赖的外部第三方接口如果超时或挂了怎么办？

### 步骤 4：匹配业务场景 Checklist (Template Matching)
- **动作**：在 `templates/` 目录中匹配对应的高频场景清单（如登录、支付、订单、接口）。
- **执行**：输出该 Checklist 的逐项勾选框，确保标准项不被遗漏。

### 步骤 5：补充边界值分析 (Boundary Value Analysis)
- **动作**：参考 `assets/boundary-value-rules.md`，对每一个输入参数提取其临界值：
  - 最小值、最小值-1、最大值、最大值+1、0、空值、非法字符。

### 步骤 6：注入用户异常行为与网络异常 (Abnormal Behavior Injection)
- **动作**：参考 `assets/user-abnormal-behaviors.md`，至少注入以下 2 项：
  - 按钮极速连点（防重复提交测试）；
  - 弱网高延迟（3秒响应）或断网离线状态；
  - 页面长时间挂起超时后提交；
  - 多端同一账号并发登录冲突。

### 步骤 7：关联历史真实缺陷 (Historical Bug Association)
- **动作**：检索 `cases/` 目录，找出本领域曾经踩过的坑（如频控失效、金额精度舍入误差、状态跳步），为每个历史缺陷生成 1~2 条防御性验证用例。

### 步骤 8：生成标准化测试用例表 (Generate Standard Table)
- **动作**：严格按照 `references/04-outputs-specification.md` 的表格列名与编号格式输出完整用例。

### 步骤 9：执行 100 分制质量打分自检 (Quality Scoring Gate)
- **动作**：按照 `references/03-scoring-and-self-review.md` 规则进行自我评审打分。
- **准入标准**：**总分必须 ≥85 分**。若低于 85 分，说明漏掉了边界值或异常流，必须当场补充修正。

### 步骤 10：输出重点回归建议与发布门禁 (Regression Guidance)
- **动作**：提炼出本次需求中最核心的 P0 冒烟测试路径，列出发布必须验证的 Checklist。
