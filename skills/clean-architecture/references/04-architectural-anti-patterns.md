# 经典架构反模式与边界腐化 (Architectural Anti-Patterns)

> 识别在整洁架构落地中最容易发生的边界击穿、伪分层、循环依赖与架构腐化现象，并给出标准修复对策。

---

## 1. 核心概念与定义

- **架构腐化（Architectural Rot）**：  
  团队最初规划了清晰的分层架构，但由于赶工、偷懒或缺乏审查约束，内层开始随意引用外层代码、边界被无情穿透，最终系统迅速退化为彼此纠缠的大泥球（Big Ball of Mud）。
- **组件耦合三大原则（Uncle Bob's Coupling Principles）**：
  1. **无环依赖原则（ADP - Acyclic Dependencies Principle）**：组件的依赖图结构中绝不能出现环路。
  2. **稳定依赖原则（SDP - Stable Dependencies Principle）**：依赖方向必须朝着更稳定的方向行进（不稳定的组件应当依赖稳定的组件，而非反过来）。
  3. **稳定抽象原则（SAP - Stable Abstractions Principle）**：组件的抽象程度应当与其稳定程度一致（越稳定的核心模块，越应该高度抽象化）。

---

## 2. 经典架构反模式诊断与修复矩阵 (Diagnostic Matrix)

| 反模式名称 | 典型表象 (Symptoms) | 根本危害 | 标准修复对策 (Remedies) |
| :--- | :--- | :--- | :--- |
| **伪分层架构 (Pseudo-Layering)** | 建立了 Controller/Service/DAO 目录，但 Service 仅有 1 行透传代码，真正业务逻辑全在 Controller 或 SQL 中 | 徒增空转样板代码，分层失去防护意义，业务核心依然严重与交付机制耦合 | **将业务逻辑抽回 Use Cases 与 Entities**；Controller 仅负责参数提取与响应分发 |
| **胖控制器 (Fat Controllers)** | 单个 Controller 动辄 800~1000 行，里面混杂了参数提取、权限鉴权、价格计算、数据库事务提交与邮件发送 | 违背单一职责；无法独立测试业务逻辑；其他端（如小程序、CLI）无法复用该能力 | **将流程编排迁移到 Use Cases**，控制器仅保留调度与 HTTP 状态码映射 |
| **循环依赖 (Cyclic Dependencies - 违背 ADP)** | 模块 A 引用了 模块 B，模块 B 在内部又 `import` 了模块 A（直接或间接闭环） | 模块无法独立编译和打包；修改 A 会波及 B，改 B 又波及 A；极易引发运行时死锁或初始化异常 | • **应用依赖倒置（DIP）**，让 A 定义接口，B 实现接口；<br/>• **提炼共同抽象**，将循环依赖的共同概念下沉至新独立组件 |
| **万能工具类黑洞 (God Utils Black Hole)** | 创建了 `CommonUtils` 或 `BaseHelper`，里面包含数十个静态方法，全系统各层任意互相调用 | 成为全系统依赖的交叉汇聚点，任何一次修改都会导致全量重新编译；破坏分层边界 | **按领域细分并归位**：日期相关的做成 `DateRange` 值对象；加密相关的做成接口注入 |
| **稳定逆向依赖 (Violating SDP)** | 稳定核心的账户扣款模块，直接依赖了一个频繁改动的第三方外部 UI 样式库或非核心短信发送包 | 外部无关组件的频繁迭代，迫使核心稳定模块不断触发回归测试与重新部署 | **在核心模块定义 Output Port 接口**，将外部不稳定包封装在最外层适配器后方 |

---

## 3. 依赖闭环破除决策树 (ADP Breaker Decision Tree)

```mermaid
graph TD
    A[检测到模块 A 与 模块 B 产生循环依赖: A <--> B] --> B1{A 与 B 之间是否有一个应当处于更高层策略?}
    B1 -- 是, A 属于核心业务, B 属于辅助机制 --> C[解法 1: 依赖倒置 (DIP)<br/>在 A 中定义接口 Port, 由 B 实现该接口<br/>依赖方向从 B -> A, 破除环路]
    B1 -- 否, A 与 B 属于平级组件 --> D{循环依赖源于两者共同使用了一组公共数据结构吗?}
    D -- 是 --> E[解法 2: 创建新组件下沉<br/>新建独立小模块 C, 将被两者共同依赖的部分抽离至 C<br/>A -> C 且 B -> C, 依赖图变为有向无环 (DAG)]
    D -- 否 --> F[解法 3: 检查是否本就应为同一模块<br/>若职责严重交织, 考虑将 A 与 B 合并]
```

---

## 4. Do & Don't 对比

### 案例 1：破除循环依赖（DIP 应用）

- ❌ **Don't（业务模块与通知模块双向互相 import）**：
  ```typescript
  // order/OrderService.ts
  import { EmailNotifier } from '../notification/EmailNotifier'; // Order 依赖 Notification

  export class OrderService {
    cancelOrder(orderId: string) {
      // 业务逻辑...
      new EmailNotifier().sendCancellationEmail(orderId);
    }
  }

  // notification/EmailNotifier.ts
  import { OrderService } from '../order/OrderService'; // Notification 又反向依赖 Order!

  export class EmailNotifier {
    sendCancellationEmail(orderId: string) {
      const order = new OrderService().getOrder(orderId); // 形成环路！
      // 发送邮件...
    }
  }
  ```
- ✅ **Do（在用例层定义事件或输出端口，逆转依赖形成无环图）**：
  ```typescript
  // 1. 位于 order/use-cases/ports/OrderCancellationNotifier.ts
  export interface OrderCancellationNotifierPort {
    notifyOrderCancelled(orderId: string, customerEmail: string): Promise<void>;
  }

  // 2. 位于 order/use-cases/CancelOrderUseCase.ts
  export class CancelOrderUseCase {
    constructor(private readonly notifier: OrderCancellationNotifierPort) {}

    async execute(orderId: string): Promise<void> {
      // 核心业务状态扭转
      const order = await this.orderRepo.findById(orderId);
      order.cancel();
      await this.orderRepo.save(order);

      // 通过端口通知外界，Order 不依赖 EmailNotifier 的具体细节
      await this.notifier.notifyOrderCancelled(order.id, order.customerEmail);
    }
  }

  // 3. 位于 notification/adapters/EmailNotifierAdapter.ts
  // 依赖方向：Notification -> Order 端口 (单向依赖，ADP 闭环消除)
  import { OrderCancellationNotifierPort } from '../../order/use-cases/ports/OrderCancellationNotifier';

  export class EmailNotifierAdapter implements OrderCancellationNotifierPort {
    async notifyOrderCancelled(orderId: string, email: string): Promise<void> {
      // 执行真实的邮件发送
    }
  }
  ```

### 案例 2：伪分层 vs 真实高内聚用例

- ❌ **Don't（Controller 直接穿透 DAO，业务散落在路由里）**：
  ```typescript
  // Controller 做了全部事情，分层名存实亡
  app.post('/transfer', async (req, res) => {
    const { fromId, toId, amount } = req.body;
    const fromAcc = await db.query('SELECT * FROM accounts WHERE id = ?', [fromId]);
    if (fromAcc.balance < amount) return res.status(400).send('余额不足');
    await db.query('UPDATE accounts SET balance = balance - ? WHERE id = ?', [amount, fromId]);
    await db.query('UPDATE accounts SET balance = balance + ? WHERE id = ?', [amount, toId]);
    res.send({ status: 'ok' });
  });
  ```
- ✅ **Do（核心业务规则收敛在 Entity，事务协调在 Use Case，Controller 只负责调度）**：
  ```typescript
  // 核心业务校验在实体层
  class Account {
    withdraw(amount: Money) {
      if (this.balance.lessThan(amount)) throw new InsufficientFundsError();
      this.balance = this.balance.subtract(amount);
    }
    deposit(amount: Money) { this.balance = this.balance.add(amount); }
  }

  // 转账流程编排在用例层
  class TransferMoneyUseCase {
    async execute(req: TransferRequest): Promise<void> {
      const from = await this.accountRepo.findById(req.fromId);
      const to = await this.accountRepo.findById(req.toId);
      from.withdraw(req.amount);
      to.deposit(req.amount);
      await this.accountRepo.saveBothInTransaction(from, to);
    }
  }
  ```
