# 24 种经典代码坏味道诊断与速查矩阵 (Code Smells Catalog)

> 基于 Martin Fowler & Kent Beck《重构》经典分类体系，提供坏味道病症识别与对应重构手法的映射决策。

---

## 1. 核心概念与定义

- **代码坏味道（Code Smells）**：  
  代码中暗示着潜在质量缺陷或设计不合理的**表象线索**。坏味道本身不一定是 Bug，但它们通常意味着系统可维护性衰退、修改成本高昂或隐藏并发/逻辑陷阱。
- **坏味道六大分类**：
  1. **膨胀剂（Bloaters）**：体积失控、责任失焦的代码实体（如过长函数、过大类）。
  2. **面向对象滥用（OO Abusers）**：未完全发挥或误用多态与封装原则（如重复 Switch、临时字段）。
  3. **变革阻碍者（Change Preventers）**：阻碍软件扩展与修改的结构缺陷（如发散式变化、散弹式修改）。
  4. **可有可无者（Dispensables）**：没有实质存在意义的代码冗余（如死代码、夸夸其谈的未来性、劣质注释）。
  5. **耦合破坏者（Couplers）**：模块间不当过度亲密（如依恋情结、中间人、内幕交易）。
  6. **状态与全局污染（State & Mutability）**：全局可变数据与受污染的状态副作用。

---

## 2. 坏味道诊断与重构速查矩阵 (Decision Matrix)

### 分类一：膨胀剂 (Bloaters)

| 坏味道名称 (Smell) | 典型症状 (Symptoms) | 根因与危害 | 推荐重构手法 (Refactorings) |
| :--- | :--- | :--- | :--- |
| **神秘命名 (Mysterious Name)** | 变量/函数命名晦涩、缩写严重、与业务语义脱节 | 增加理解负荷，维护者需要读完整段逻辑才能猜出变量含义 | • **改变函数声明 (Change Function Declaration)**<br/>• **变量重命名 (Rename Variable)**<br/>• **字段重命名 (Rename Field)** |
| **过长函数 (Long Function)** | 单函数超过 20~30 行，混杂多层缩进与不同抽象层次 | 难以复用，隐藏局部状态副作用，测试分支几何级数增长 | • **提炼函数 (Extract Function)**<br/>• **以查询取代临时变量 (Replace Temp with Query)**<br/>• **引入参数对象 (Introduce Parameter Object)** |
| **过长参数列表 (Long Parameter List)** | 函数入参超过 3~4 个，调用方极易传错顺序 | 接口脆弱，传参记忆成本高，暗示函数承担了过多逻辑 | • **引入参数对象 (Introduce Parameter Object)**<br/>• **保持对象完整 (Preserve Whole Object)**<br/>• **以查询取代参数 (Replace Parameter with Query)** |
| **数据泥团 (Data Clumps)** | 相同的 3~4 个字段总是成群结队出现在多个类或函数参数中（如 start/end 日期） | 缺失关键领域实体，导致概念碎片化在多处 | • **提炼类 (Extract Class)**<br/>• **引入参数对象 (Introduce Parameter Object)** |
| **基本类型偏执 (Primitive Obsession)** | 肆意用字符串或数字表示电话、货币、坐标、状态码，到处散落正则校验 | 领域校验逻辑散落各处，缺乏强类型保护与领域行为收敛 | • **以对象取代基本类型 (Replace Primitive with Object)**<br/>• **以子类/多态取代类型码 (Replace Type Code with Subclasses)** |
| **过大的类 (Large Class)** | 类包含几十个字段或上千行代码，承担多个不同职责 | 违反单一职责（SRP），极易产生并发读写冲突与合并冲突 | • **提炼类 (Extract Class)**<br/>• **提炼超类 (Extract Superclass)**<br/>• **以子类取代类型码** |

---

### 分类二：变革阻碍者 (Change Preventers)

| 坏味道名称 (Smell) | 典型症状 (Symptoms) | 根因与危害 | 推荐重构手法 (Refactorings) |
| :--- | :--- | :--- | :--- |
| **发散式变化 (Divergent Change)** | **一个类受多种不同维度的变化影响**。<br/>例：“新增数据库字段要改它，新增支付方式要改它，改报表格式也要改它”。 | 违背高内聚原则，不同变更理由交织在同一模块内 | • **拆分阶段 (Split Phase)**<br/>• **提炼类 (Extract Class)**<br/>• **搬移函数 (Move Function)** |
| **散弹式修改 (Shotgun Surgery)** | **每当做一次业务修改，必须在数十个不同的类或文件中各改一两行**。 | 职责未能按变化维度聚合，极易遗漏某一处的修改而引发 Bug | • **搬移函数 (Move Function)**<br/>• **搬移字段 (Move Field)**<br/>• **将函数内联到类中 (Inline Class)** |

---

### 分类三：耦合破坏者 (Couplers)

| 坏味道名称 (Smell) | 典型症状 (Symptoms) | 根因与危害 | 推荐重构手法 (Refactorings) |
| :--- | :--- | :--- | :--- |
| **依恋情结 (Feature Envy)** | 一个类里的某个方法，总是频繁调用**另一个类**的 getter 和数据，远超过调用自身数据 | 数据与行为分离，面向对象退化为贫血的过程式代码 | • **搬移函数 (Move Function)**<br/>• **提炼函数后搬移 (Extract & Move Function)** |
| **过长消息链 (Message Chains)** | 代码中连续级联调用：`a.getB().getC().getD().getPayAmount()` | 严重违反迪米特法则（Law of Demeter），客户端与整个中间对象导航图强耦合 | • **隐藏委托关系 (Hide Delegate)**<br/>• **提炼函数并搬移到末端** |
| **中间人 (Middle Man)** | 某个类的一半方法都仅仅是把调用委托给内部字段，自身没有任何实际增值逻辑 | 过度封装与无意义的胶水透传，徒增间接层 | • **移除中间人 (Remove Middle Man)**<br/>• **内联函数 (Inline Function)** |
| **内幕交易 (Insider Trading)** | 两个模块在背地里互相访问对方私有或内部数据，私下暗通款曲 | 模块边界名存实亡，无法独立演进与测试 | • **搬移函数/字段 (Move Function/Field)**<br/>• **隐藏委托关系**<br/>• **以第三方抽象类隔离** |

---

### 分类四：面向对象滥用与可有可无者 (OO Abusers & Dispensables)

| 坏味道名称 (Smell) | 典型症状 (Symptoms) | 根因与危害 | 推荐重构手法 (Refactorings) |
| :--- | :--- | :--- | :--- |
| **重复的分支切换 (Repeated Switches)** | 在不同文件多处出现基于同一种 typeCode 的 `switch(type)` 或 `if-else` | 每次新增枚举类型，必须翻遍整个系统修改所有 switch 分支 | • **以多态取代条件表达式 (Replace Conditional with Polymorphism)** |
| **临时字段 (Temporary Field)** | 某个字段仅在特定复杂算法执行期间才有值，平时均为 null | 对象状态不自洽，阅读者极难理解该字段的生命周期 | • **提炼类 (Extract Class)**<br/>• **引入特例对象 (Introduce Special Case)** |
| **纯数据类 (Data Class)** | 只有 getter/setter 与公开属性，几乎没有任何操作自身的行为方法 | 沦为哑数据结构，导致其他调用方产生依恋情结（Feature Envy） | • **搬移函数 (Move Function)** 将操作这些数据的外部方法挪入该类 |
| **夸夸其谈未来性 (Speculative Generality)** | 设计了大量当前根本用不上的钩子、抽象基类、空委托和泛型包装 | “我们以后可能会用到”导致的过度设计（YAGNI），平白增加认知负担 | • **折叠继承体系 (Collapse Hierarchy)**<br/>• **内联函数/类 (Inline Class)**<br/>• **移除死代码 (Remove Dead Code)** |
| **劣质注释 (Comments)** | 充斥着解释“这段代码在做什么”的说明性注释 | 注释常用于粉饰恶臭代码（“注释越长，代码越臭”） | • **提炼函数 (让函数名自解释)**<br/>• **重命名符号 (以意图命名取代注释)** |

---

## 3. 反模式与坏味道 (Anti-patterns)

- **只看现象不除根（Symptom Masking）**：  
  *错误做法*：发现多处散弹式修改（Shotgun Surgery），没有将其聚合归一，而是在每个调用点写注释提醒“记得修改这里”。  
  *后果*：依赖人员自觉性的设计终究会在某次紧急发版时崩溃。
- **神化“消除一切重复”（Dogmatic DRY）**：  
  *错误做法*：两个处于完全不同业务领域、碰巧字段名长得一样的类，强行提炼出一个公用基类。  
  *后果*：引入了**偶然重复（Accidental Duplication）**的虚假耦合。当两个业务各自演进时，改动基类直接导致灾难性连锁故障。

---

## 4. Do & Don't 对比

### 案例 1：依恋情结 (Feature Envy) 重构

- ❌ **Don't（调用方比拥有者更懂对方的数据）**：
  ```javascript
  class OrderService {
    calculateTotal(order) {
      // OrderService 疯狂调用 order 的内部细节进行算术运算
      let total = 0;
      for (const item of order.items) {
        let discount = 1.0;
        if (item.quantity > 10) discount = 0.9;
        total += item.price * item.quantity * discount;
      }
      return total + order.shippingFee;
    }
  }
  ```
- ✅ **Do（搬移函数至数据拥有者身上，封装内部变化）**：
  ```javascript
  class OrderItem {
    get totalPrice() {
      const discount = this.quantity > 10 ? 0.9 : 1.0;
      return this.price * this.quantity * discount;
    }
  }

  class Order {
    get total() {
      const itemsTotal = this.items.reduce((sum, item) => sum + item.totalPrice, 0);
      return itemsTotal + this.shippingFee;
    }
  }

  // 外部调用干净清爽，内聚度极高
  class OrderService {
    calculateTotal(order) {
      return order.total;
    }
  }
  ```

### 案例 2：数据泥团 (Data Clumps) 重构

- ❌ **Don't（到处重复传递相同的散装字段）**：
  ```typescript
  function searchReservations(startDate: Date, endDate: Date, customerId: string) { ... }
  function calculateRoomRate(startDate: Date, endDate: Date, roomType: string) { ... }
  function isAvailable(startDate: Date, endDate: Date, roomId: string) { ... }
  ```
- ✅ **Do（引入值对象 DateRange，沉淀时间区间语义与校验）**：
  ```typescript
  class DateRange {
    constructor(readonly start: Date, readonly end: Date) {
      if (start > end) throw new Error("Start date cannot be after end date");
    }
    includes(date: Date): boolean { return date >= this.start && date <= this.end; }
  }

  function searchReservations(range: DateRange, customerId: string) { ... }
  function calculateRoomRate(range: DateRange, roomType: string) { ... }
  function isAvailable(range: DateRange, roomId: string) { ... }
  ```
