# Google Code Review Developer Guide 提炼大纲与切片规划

## 一、 原书/官方文档结构映射
- `review/reviewer/standard.md` -> 核心标准与心智模型（持续提升 Code Health，事实胜于偏好）
- `review/reviewer/looking-for.md` -> 审查核心维度（Design, Functionality, Complexity, Tests, Naming, Comments, Style, Consistency, Documentation, Every Line）
- `review/reviewer/navigate.md` -> 审查流程与高效导航（抓主文件、先大后小）
- `review/reviewer/speed.md` -> 审查速度与响应规范（阻止上下文切换损耗）
- `review/reviewer/comments.md` -> 评论艺术与分级（Nit/Optional/FYI，对事不对人，讲清 Why）
- `review/reviewer/pushback.md` -> 推脱与异议处理（抵制“以后再改”、数据胜于雄辩）
- `review/developer/small-cls.md` -> 小 CL 拆分策略（横向分层、纵向切片、重构与业务解耦）
- `review/developer/cl-descriptions.md` -> 变更说明规范

## 二、 80/20 实战价值切片规划（拟生成 5 个切片 + 1 个自查清单）
- **Slug**: `google-code-review-guide`
- **切片 1: `references/01-standard-and-mindset.md`**：核心审查标准与心智模型（Code Health 净增原则、持续改进 vs 完美主义、事实与规范胜于个人偏好、拒绝与回退准则）
- **切片 2: `references/02-functionality-and-design.md`**：功能性与架构审查决策树（意图达成度、边界条件、并发竞态、架构归属、前后端协同与时序风险）
- **切片 3: `references/03-complexity-and-overengineering.md`**：复杂度与过度设计拦截（阅读者理解阈值、YAGNI 严格践行、命名与注释法则：注释解释 Why 而非 What）
- **切片 4: `references/04-testing-and-code-health.md`**：测试与代码健康度标准（同包提交测试、测试有效性与断言防伪、逐行审查原则与盲区）
- **切片 5: `references/05-pr-hygiene-and-pushback.md`**：小变更拆分与推脱拦截（小 CL 拆分范式、重构与功能解耦、评论标签分级 Nit/Optional、识破“以后再改”陷阱）
- **清单: `checklists/review-checklist.md`**：Google 级代码审查与业务逻辑验证落地打分表
