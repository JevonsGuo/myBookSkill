# myBookSkill: Agent Skills 知识库工程化体系

> 将长篇技术书籍、领域手册、安全标准与最佳工程实践，系统化转化为符合 Antigravity / Claude 标准规范、支持按需渐进加载的 **Agent Skills（智能体技能包）**。

---

## 📖 核心设计哲学 (Philosophy)

1. **渐进式加载（Progressive Disclosure）**
   - 彻底避免将数万字的书籍原文塞入 Context。通过精简的入口路由（`SKILL.md`）提供核心元数据，仅在具体任务触发时按需动态读取 `references/`，最大限度节省 Token 并避免注意力稀释（Lost in the Middle）。
2. **行动准则大于背景故事**
   - 剔除历史闲聊与故事铺垫，直接沉淀高浓度工程资产：**思维模型（Mental Models）**、**决策树（Decision Rules）**、**反模式（Anti-Patterns）**与**自查清单（Checklists）**。
3. **闭环质检门禁（Quality Gate）**
   - 技能输出均配备自检清单与打分机制，确保产出物（用例、代码审查意见、安全扫描结论）具备高严密性与实操性。

---

## 📦 已就绪的 Agent 技能包 (Skills Catalog)

| 技能名称 | 核心知识来源 | 核心能力与适用场景 |
| :--- | :--- | :--- |
| **`test-case-generation`** | 工业级“测试脑”架构 & 测试工程学 | 强制 10 步流水线，拒绝浅层 Happy Path，覆盖边界值、并发时差、网络异常、历史踩坑与 100 分自评门禁 |
| **`owasp-business-logic-review`** | OWASP WSTG & 业务逻辑审查指南 | 聚焦业务逻辑漏洞：防数据篡改、状态机防跳步/逆向扭转、并发竞态（TOCTOU）、接口幂等性与 Decimal 金额精度 |
| **`peer-code-review-secrets`** | SmartBear《同行代码审查的秘密》 | 200~400 行审查规模控制、60分钟防疲劳断崖、人机分工律、高发缺陷热点挖掘（资源泄漏、空指针、N+1查询） |
| **`google-code-review-guide`** | Google Engineering Practices Guide | Google 级工程实践：可维护性审查、过度设计防御（YAGNI）、单测有效性、小颗粒度变更规范 |
| **`show-me`** | 架构与可视化指南 | 自动生成 Mermaid 流程图、时序图、系统拓扑与高内聚前端可视化视图 |

---

## 📂 仓库目录架构

```text
.
├── pipeline/                     # 转换流水线与复用工具
│   ├── prompts/                  # 知识提炼专用 Prompt 模版
│   │   ├── 01_extract_outline.md
│   │   ├── 02_extract_chapter.md
│   │   └── 03_generate_checklist.md
│   └── scripts/
│       └── distribute.py         # 技能分发与部署工具
│
├── drafts/                       # 提炼草稿与书籍大纲笔记
│
├── skills/                       # 【核心交付产物】生产就绪的 Agent 技能库
│   ├── test-case-generation/
│   ├── owasp-business-logic-review/
│   ├── peer-code-review-secrets/
│   ├── google-code-review-guide/
│   └── show-me/
│
├── AGENTS.md                     # Book-to-Skill 工程化建设指南与实战 SOP
└── README.md                     # 项目全局说明文档
```

---

## 🚀 快速上手与技能分发

本项目内置了自动化分发脚本 [distribute.py](pipeline/scripts/distribute.py)，可轻松将技能安装到本地全局或具体项目中：

### 1. 查看可用技能列表
```bash
python3 pipeline/scripts/distribute.py --list
```

### 2. 安装技能到本地全局环境（~/.gemini/config/skills/）
```bash
python3 pipeline/scripts/distribute.py --skill test-case-generation --target global
```

### 3. 安装技能到指定业务项目（如业务项目的 .agents/skills/）
```bash
python3 pipeline/scripts/distribute.py --skill owasp-business-logic-review --target /path/to/your-project
```

---

## 🛠️ 如何提炼新书籍或领域规范？

详细请参阅 [AGENTS.md](AGENTS.md) 遵循标准的 5 步 SOP：
1. **目录审查与价值筛选 (Curation)**：筛选贡献 80% 实战价值的核心主题；
2. **核心骨架与心智模型提炼 (Mental Models)**：确定底层推导逻辑与技能命名；
3. **逐个切片精细化提炼 (References)**：提炼决策树、反模式与正反例；
4. **落地清单与入口组装 (Checklists & SKILL.md)**：编写可执行审查表并精修 YAML 触发词；
5. **分发验证与发布 (Deploy)**：挂载至目标环境测试调用。
