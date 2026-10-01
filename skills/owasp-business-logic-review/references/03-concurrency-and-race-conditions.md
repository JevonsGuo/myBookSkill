# 03 - 并发竞态与时序时差漏洞 (Concurrency & Race Conditions)

## 一、 核心概念与审查标准

- **TOCTOU 时差漏洞（Time-of-Check to Time-of-Use）**：
  - 代码先执行“检查（Check）”，然后再执行“使用/扣减（Use）”。**如果检查与扣减之间没有原子性锁保护，并发请求会在时差窗口期内全部通过检查**。
  - 典型后果：并发双花（Double Spending）、超额提现、库存超卖、优惠券被重复多次抵扣。
- **并发状态不一致（Lost Updates & Dirty Reads）**：
  - 多个并发线程同时读取了旧值（如余额 1000 元），分别在内存中各自扣除 100 元，然后先后写回数据库。后写者覆盖了先写者，导致其中一笔扣减凭空丢失。
- **原子性防护四层防御机制（Concurrency Defense Ladder）**：
  1. **层级 1：数据库原子单条更新（Atomic In-Place Update）**（最优先推荐，无锁高吞吐）；
  2. **层级 2：乐观锁机制（Optimistic Locking with Version）**（适合冲突率较低的读多写少场景）；
  3. **层级 3：行级悲观锁（Pessimistic Locking `FOR UPDATE`）**（适合强事务金钱结算）；
  4. **层级 4：分布式互斥锁（Distributed Lock，如 Redis RedLock）**（适合跨多个微服务、非单库事务的长流程）。

---

## 二、 并发模型选型决策树 (Decision Tree)

```text
需要更新关键业务资产（余额、库存、单据状态）
│
├── 1. 操作是否可以在单条 SQL 内原子完成？
│   ├── 是（如扣除固定金额且要求余额充足）
│   │   └── 选用原子单条更新：`UPDATE account SET balance = balance - %s WHERE id = %s AND balance >= %s`
│   └── 否（需要复杂业务计算、关联多张表）
│       └── 见下步
│
├── 2. 是否在单一数据库事务内？
│   ├── 是 ──► 评估冲突率：
│   │   ├── 冲突高、强一致性金钱业务 ──► 使用行级悲观锁：`SELECT ... FOR UPDATE`
│   │   └── 冲突低、大部分是独立修改 ──► 使用乐观锁：`WHERE id = %s AND version = %s`
│   │
│   └── 否（跨第三方支付接口、跨微服务调用）
│       └── 使用分布式锁（带自动续期与唯一请求标识），在最外层锁定业务唯一键（如 order_id / biz_identifier）
```

---

## 三、 典型并发反模式 (Anti-patterns)

- **反模式 1：应用层内存判断余量（In-Memory Balance Check）**
  - *表现*：先在 Python 中 `SELECT balance`，然后在 Python 代码里 `if balance >= amount:`，最后再发送 `UPDATE balance = %s`。
  - *危害*：10 个并发请求同时读取到同样的初始余额，导致账户被透支 10 倍。
- **反模式 2：非原子分布式锁释放（Non-atomic Lock Release）**
  - *表现*：使用 Redis 锁，释放时没有比对锁的持有者值（Value），或者在业务处理超时后误删了其他线程新获取的锁。
  - *危害*：导致锁机制失效，并发保护如同虚设。
- **反模式 3：跨外部调用的长事务（Long Transaction with External I/O）**
  - *表现*：在开启了 `FOR UPDATE` 的长事务中，发起耗时 5~10 秒的第三方银行或 OTA 网络请求。
  - *危害*：长期占用数据库连接与行锁，拖垮数据库连接池，造成全站雪崩。

---

## 四、 Do & Don't 对比

### 场景：扣减账户结算额度

```python
# ❌ DON'T: 内存中检查余额，典型的 TOCTOU 竞态漏洞
def deduct_balance(account_id, amount):
    # Step 1: 检查 (Check)
    account = db.query_one("SELECT balance FROM account WHERE id = %s", (account_id,))
    if account["balance"] < amount:
        return False, "余额不足"
    
    # 时差窗口（此时另一个并发请求完全可以读到尚未更新的 balance）
    
    # Step 2: 使用 (Use)
    new_balance = account["balance"] - amount
    db.execute("UPDATE account SET balance = %s WHERE id = %s", (new_balance, account_id))
    return True, "扣减成功"

# ✅ DO: 数据库原子行级锁与条件拦截，零时差窗口
def deduct_balance(account_id, amount):
    with db_transaction() as tx:
        # 单条 SQL 结合前置条件判断，原子执行
        affected_rows = tx.execute(
            "UPDATE account SET balance = balance - %s WHERE id = %s AND balance >= %s",
            (amount, account_id, amount)
        )
        if affected_rows == 0:
            return False, "余额不足或账户不存在"
        
        # 记录扣款流水（同事务）
        tx.execute(
            "INSERT INTO balance_journal (account_id, amount, created_at) VALUES (%s, %s, NOW())",
            (account_id, amount)
        )
    return True, "扣减成功"
```
