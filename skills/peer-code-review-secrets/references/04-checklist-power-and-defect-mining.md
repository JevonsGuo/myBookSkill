# 04 - 检查清单威力与高发缺陷挖掘 (Checklist Power & Defect Mining)

## 一、 核心概念与实证数据

- **检查清单翻倍效应（The Checklist Multiplier）**：
  - SmartBear 实证数据表明：**使用经过精心设计的分类检查清单（Checklist），能使同行审查的缺陷检出率直接提升 100% 以上**。
  - 人脑在非结构化自由阅读代码时，极易凭直觉跳过熟悉的代码块；**而清单强迫大脑从被动浏览转变为主动排查（Active Interrogation）**。
- **动态演进法则（Living Checklists / RCA Feedback Loop）**：
  - 清单不能是一成不变的死八股，而必须与团队的**线上故障复盘（RCA, Root Cause Analysis）**直接联动。
  - **“每出现一次严重线上 Bug，如果属于代码走查可防范的范畴，就在清单中追加一条一句话判定项”**。
- **高发缺陷六大通用黄金类别（Top 6 Defect Categories）**：
  1. **空值与未初始化（Null / None References）**：字典取值无默认值、未判空直接链式调用；
  2. **边界与偏移量（Boundary & Off-by-One）**：`<` vs `<=`, `0` vs `1`, 数组下标与分页越界；
  3. **资源泄漏（Resource Leaks）**：数据库连接、文件句柄、网络会话未在 `finally` 或 `with` 块中关闭；
  4. **异常吞噬（Exception Swallowing）**：空的 `except: pass` 抹除了关键错误栈；
  5. **并发与共享状态（Concurrency & Mutability）**：全局字典/列表在多线程/协程下被无锁篡改；
  6. **性能陷阱（Performance Traps）**：循环内执行 SQL 查询（N+1 问题）、大规模全表扫描。

---

## 二、 缺陷挖掘操作决策树 (Decision Tree)

```text
对照检查清单审阅代码块
│
├── 1. 外部入参与数据引用排查
│   ├── 是否存在裸取字典字段 (如 `row['field']`)？ ──► 要求改为 `.get('field')` 或显式 KeyError 保护
│   └── 对象方法调用前是否排查了 None？ ──► 补齐前置 Guard
│
├── 2. 外部资源生命周期排查
│   ├── 获取了 DB Connection / 文件句柄？
│   │   ├── 裸调用 `conn.close()` ──► 存在异常时泄漏风险！
│   │   │   └── 强制要求使用上下文管理器：`with _get_db_connection():`
│   │   └── 已由 with/try-finally 管理 ──► 安全放行
│
└── 3. 循环与集合操作排查
    ├── 循环体内部是否存在数据库 I/O 或 HTTP 请求？ ──► 识别出 N+1 坏味道，要求批量化处理
    └── 是否存在多线程并发写入非线程安全容器？ ──► 要求增加同步锁或改为线程私有隔离
```

---

## 三、 清单应用反模式 (Anti-patterns)

- **反模式 1：冗长到无法执行的百页圣经（The 100-Item Checklist Fatigue）**
  - *表现*：制定了 100 多项巨细靡遗的清单，审查者看到就头晕，最终无人使用。
  - *危害*：过犹不及，清单应聚焦在**最容易漏网的 10~15 条核心高危项**。
- **反模式 2：静止不动的僵尸清单（Static Obsolete Checklist）**
  - *表现*：三年前写的审查清单，团队技术栈已经演进，清单从未更新过。
  - *危害*：无法拦截新型架构和业务漏洞。
- **反模式 3：形式主义勾选（Mindless Box-Ticking）**
  - *表现*：审查者连代码都没看，机械式地把所有复选框全打钩提交。
  - *危害*：沦为官僚形式主义。

---

## 四、 Do & Don't 对比

### 场景：排查数据库连接与异常释放（如 routes.py 中）

```python
# ❌ DON'T: 裸建立连接，发生异常时 connection 无法关闭，导致连接池耗尽
def query_data(env):
    conn = pymysql.connect(...)
    cur = conn.cursor()
    cur.execute("SELECT ...")
    row = cur.fetchone()
    # 如果上面 fetch 或业务逻辑抛异常，下面的 close 永远无法执行！
    cur.close()
    conn.close()
    return row

# ✅ DO: 使用上下文管理器确保在任何崩溃/异常分支下 100% 自动释放
@contextmanager
def _get_db_connection(env):
    cfg, err = _get_db_config(env)
    if err:
        raise ValueError(err)
    conn = pymysql.connect(**cfg)
    try:
        yield conn
    finally:
        try:
            conn.close()
        except Exception:
            pass

def query_data(env):
    with _get_db_connection(env) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT ...")
            return cur.fetchone()
```
