# Book to Skill 知识库工程化建设指南与实战 SOP

本项目旨在将长篇技术书籍、领域手册与规范文档，系统化转化为符合标准规范、支持按需调用的 **Agent Skills（AI 智能体技能包）**。

当你（AI）在这个项目中接收到新书籍或转化任务时，请严格遵循本文档定义的目录架构、标准模板与执行 SOP 进行作业。

---

## 一、 核心设计哲学

1. **渐进式加载（Progressive Disclosure）**
   - 严禁将数万字的书籍全文或整章大段塞进单文件。
   - 平时仅由 `SKILL.md` 提供轻量级路由与元数据；只有当具体任务触发时，Agent 才按需深入读取 `references/` 对应章节，最大限度节省 Token 并避免注意力稀释（Lost in the Middle）。
2. **行动准则大于背景故事**
   - 滤除历史闲聊、环境搭建、故事铺垫等废话。
   - 提炼核心为：**思维模型（Mental Models）**、**决策树（Decision Rules: 何时用 A 何时用 B）**、**反模式（Anti-patterns: 严禁做什么）** 与 **自查清单（Checklists）**。
3. **高精准触发（Trigger Tuning）**
   - `SKILL.md` 的 YAML Frontmatter 中的 `description` 必须精准描述应用场景与核心关键词，确保未来存放 50+ 本书时不会产生技能误触发。

---

## 二、 推荐目录架构

```text
.
├── sources/                      # 原始书籍文件（PDF / EPUB / MOBI / Markdown 等）
│   └── .gitignore                # 建议忽略大文件和版权书籍，不提交进 Git
│
├── pipeline/                     # 转换流水线与复用模板
│   ├── prompts/                  # 提炼阶段专用 Prompt
│   │   ├── 01_extract_outline.md
│   │   ├── 02_extract_chapter.md
│   │   └── 03_generate_checklist.md
│   └── scripts/                  # 文本提取、格式转换或批处理脚本
│
├── drafts/                       # 中间过程稿（书籍目录草稿、各章提取笔记）
│   └── <book-slug>/
│
├── skills/                       # 【核心交付产物】生产就绪的 Agent 技能库
│   └── <book-slug>/              # 每本书一个独立标准 Skill 目录
│       ├── SKILL.md              # 技能入口、元数据与路由索引
│       ├── references/           # 模块化章节/专题（3 ~ 8 个关键切片）
│       │   ├── 01-core-principles.md
│       │   ├── 02-patterns.md
│       │   └── 03-anti-patterns.md
│       └── checklists/           # 落地自查与评审清单（最常被调用的实战资产）
│           └── review-checklist.md
│
└── BOOK_TO_SKILL_GUIDE.md        # 本规范文档
```

---

## 三、 标准模板规范

### 1. `SKILL.md` 模板规范（入口路由，控制在 100~200 行内）

每个 `<book-slug>/SKILL.md` 必须具备合法的 YAML Frontmatter 及结构化路由：

```markdown
---
name: <book-slug>
description: 简明扼要说明本书适用的核心场景、解决的问题、核心作者及触发关键词（如：DDD领域驱动设计、聚合根划分、防腐层设计指导）。
---

# <书名中文/英文标准全名> 指南

## 1. 核心心智模型（Mental Models）
- **核心法则 1**：一两句话总结全书最不可动摇的设计底线。
- **核心法则 2**：高内聚低耦合的具体衡量标准。

## 2. 章节与参考路由（Reference Routing）
当执行不同任务时，主动阅读 `references/` 目录下的相应文档：
- **涉及 [场景 A：例如分层架构/接口定义] 时**：查阅 [01-architecture-rules.md](references/01-architecture-rules.md)
- **涉及 [场景 B：例如异常处理/事务边界] 时**：查阅 [02-transaction-boundaries.md](references/02-transaction-boundaries.md)
- **发现坏味道或代码重构时**：查阅 [03-anti-patterns.md](references/03-anti-patterns.md)

## 3. 实战自查表（Checklists）
- [开发/评审阶段自查清单](checklists/review-checklist.md)：用于方案审查或 Code Review 打分。
```

### 2. `references/*.md` 编写规范（切片模块）

每个切片文件聚焦单一核心领域，建议包含以下小节：
* **核心概念与定义**（极简，用加粗与要点列表）
* **决策指南（Decision Tree）**：表格或流程化列出“遇到情况 X 时选方案 A；遇到情况 Y 时选方案 B”
* **反模式（Anti-patterns & Code Smells）**：明确列举经典错误做法与危害
* **Do & Don't 对比**：提供简明代码或设计正反例

### 3. `checklists/*.md` 编写规范（实战清单）

清单是 Agent 审查代码与辅助设计的最高频工具，应采用 Markdown 复选框形式：
* 包含 10 ~ 15 个直击痛点的核对项
* 每项后附一句话判定依据或惩罚代价

---

## 四、 转换单本书的 5 步标准 SOP

当你作为 AI 协助用户开始搞一本书时，请按顺序推进：

### Step 1. 目录审查与价值筛选（Curation）
1. 读取原书目录（Table of Contents），滤除前言、历史、基础工具搭建等无实战意义章节。
2. 挑选出全书贡献了 80% 实战价值的 3~6 个核心主题。
3. 与用户确认待提取的切片规划。

### Step 2. 核心骨架与心智模型提炼（Mental Models）
1. 提炼全书的底层推导逻辑和架构哲学。
2. 拟定技能的英文标识符（如 `clean-architecture`、`ddia-distributed-data`、`refactoring-fowler`）。

### Step 3. 逐个切片精细化提炼（References）
1. 对筛选出的核心主题，依次从文本中提炼“规则、决策条件、反模式、正反例”。
2. 存放到 `skills/<book-slug>/references/` 下。

### Step 4. 落地清单与入口组装（Checklist & SKILL.md）
1. 编写 1 份可直接用于项目 Review 的自查清单 `checklists/review-checklist.md`。
2. 组装 `SKILL.md`，重点打磨 YAML Frontmatter 中的 `description`，确保关键词清晰精确。

### Step 5. 挂载验证与发布
1. **全局可用**：软链接至用户的全局技能库：
   ```bash
   ln -s "$(pwd)/skills/<book-slug>" ~/.gemini/config/skills/<book-slug>
   # 或 ~/.claude/skills/<book-slug>
   ```
2. **项目专属**：软链接至特定工程根目录下的 `.agents/skills/<book-slug>`。

---

## 五、 给 AI Agent 的指令说明

在新的项目中，如果用户输入类似：“*我把《领域驱动设计》放进 `sources/` 了，帮我把它做成一个 Skill*”：
1. **主动发起 Step 1**：先扫描 `sources/` 下的书籍文件，提取目录并输出转化规划提案；
2. **切忌一次性生成不可维护的长文本**，严格按照目录结构将文件写入 `skills/<book-slug>/` 对应的子目录；
3. **保持自查与验证**：生成完毕后，检查各 markdown 文件的相对引用链接是否正确可用。
