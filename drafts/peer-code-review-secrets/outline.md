# 《同行代码审查的秘密》（Best Kept Secrets of Peer Code Review - SmartBear）提炼大纲

## 一、 知识源背景与核心数据（思科 2500 次代码审查实证研究）
- 作者：Jason Cohen（SmartBear 创始人）等
- 实证样本：思科系统（Cisco Systems）50 名工程师、2500 次审查、320 万行代码真实生产数据
- 核心发现：
  1. 单次审查超 400 行代码，缺陷检出率断崖式下跌；
  2. 审查速度超 500 行/小时，几乎无法发现深层逻辑缺陷；
  3. 单次连续审查超 60 分钟，疲劳导致有效性崩溃；
  4. 检查清单（Checklists）使常见缺陷检出率提升 100% 以上；
  5. 自动化工具抓语法格式，人类专注逻辑与架构；
  6. 修复验证（Verify Fixes）是防范次生 Bug 的必经环节。

## 二、 5 大高密度实战切片规划 (References)
- **Slug**: `peer-code-review-secrets`
- **切片 1: `references/01-empirical-limits-and-pacing.md`**：审查节奏与认知极限黄金律（200-400 LOC 限制、300-500 LOC/h 审查速度、60 分钟疲劳断崖、缺陷密度曲线）
- **切片 2: `references/02-ego-effect-and-review-culture.md`**：自我效应心理学与作者导读（Ego Effect 心理预期自净、作者提交前自查导读 Guided Tour、无责文化建设）
- **切片 3: `references/03-lightweight-methods-and-automation.md`**：轻量级审查形态与人机分工律（5 大审查形态选型决策树、自动化抓语法风格，人类专攻业务逻辑与并发设计）
- **切片 4: `references/04-checklist-power-and-defect-mining.md`**：检查清单威力与缺陷挖掘（分类错误清单 Checklist、排查高发缺陷模式、防范遗漏）
- **切片 5: `references/05-defect-closure-and-metrics-hygiene.md`**：缺陷闭环验证与度量卫生（必须验证修复有效性、防次生 Bug、度量指标不作绩效考评防范古德哈特定律、RCA 持续改进）
- **落地清单: `checklists/peer-review-checklist.md`**：SmartBear 轻量级同行审查落地打分自查表
