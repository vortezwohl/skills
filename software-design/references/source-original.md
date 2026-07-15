Software Architecture / AI Coding / Design Patterns

# AI Coding 时代, 架构能力才是程序员的核心竞争力

如果说过去的软件开发难点在“把功能写出来”，那么今天更难的部分已经变成“让快速生成的大量代码仍然可演化、可协作、可验证”。 设计模式的价值，不再只是面试题或教科书知识，而是帮助人类在 AI 时代重新掌控结构、边界和变化。

这篇文章讲什么

从思想到实践，系统解释 10 大设计模式在 AI Coding 时代为什么更重要。

怎么讲

每个模式都讲变化点、结构意图、适用场景、反例、框架案例和 Python demo。

为什么要这样讲

因为今天最需要的不是会背定义，而是能在 AI 生成代码时做对结构判断。

## 一、为什么 AI Coding 时代反而更需要设计模式

很多人会误以为，既然 AI 已经可以大段生成代码，设计模式的重要性应该下降。现实恰好相反。AI 让“实现能力”变得廉价，结构失误却因此被成倍放大。 过去一个开发者亲手写几十个分支时，至少会在编码过程中逐渐感受到系统正在失控；今天模型可以在几十秒里生成上百行看似合理的代码，如果没有模式思维约束，系统会更快进入不可维护状态。

设计模式本质上不是“优雅类图”，而是工程世界对重复变化结构的压缩表达。它们关心的不是语言技巧，而是下面这些更根本的问题：哪里在变，谁该知道变化，变化该如何被隔离，系统该如何测试，以及多人协作时影响面如何被控制。

| AI Coding 中常见问题 | 典型表现 | 背后缺失的结构判断 | 模式能解决什么 |
| --- | --- | --- | --- |
| 功能越加越乱 | 每来一个需求就多一个分支 | 没有识别出算法或流程中的变化点 | `Strategy`、`Template Method` |
| 依赖横向扩散 | 到处直接创建具体对象 | 创建与使用没有分离 | `Factory Method`、`Abstract Factory` |
| 横切逻辑失控 | 日志、缓存、鉴权散在各处 | 没有把增强或控制逻辑收束到边界层 | `Decorator`、`Proxy`、`Facade` |

一个更尖锐的说法：

在 AI Coding 时代，设计模式的重要性不是体现在“让代码更漂亮”，而是体现在“防止模型把错误结构快速复制几十遍”。

## 二、理解设计模式，首先要理解“变化点”

大多数教材会从定义开始讲模式，但工程上更有效的顺序是反过来：先看变化点，再看结构。你真的理解一个设计模式，不是因为你记住了它的标准定义，而是因为你能回答五个问题。

1. 这个模式到底在隔离哪一种变化？是算法、创建过程、通知链路，还是访问控制？
2. 它额外引入了什么结构成本？接口、对象族、代理层还是继承层级？
3. 它和相邻模式的边界在哪里？例如 Decorator 与 Proxy，Factory Method 与 Abstract Factory。
4. 它在现代框架里通常如何出现？是显式类层级，还是配置、容器、回调、装饰器语法糖。
5. 如果不用它，系统通常会退化成什么坏味道？条件泥潭、重复编排、全局状态污染，还是耦合扩散。

本文的核心原则：

设计模式不是先验宗教，而是变化管理工具。真正的高水平不是“到处套模式”，而是“看见变化时知道该不该上模式，以及该上哪一种模式”。

## 三、10 大设计模式全景图

### 创建型模式

关注对象如何被创建，以及创建决策如何从使用方移走。

`Factory Method` / `Abstract Factory` / `Singleton`

### 结构型模式

关注对象如何被组织、包裹、兼容、增强和简化。

`Adapter` / `Decorator` / `Proxy` / `Facade`

### 行为型模式

关注职责如何流动，算法如何替换，事件如何传播，流程如何固定。

`Strategy` / `Observer` / `Template Method`

### AI 时代的附加含义

这些模式都是“给模型划边界”的方法，让生成代码时的自由度不会直接演化成结构灾难。

### Strategy：把变化算法从主流程里拔出来

关键词：算法家族、运行时替换、避免条件泥潭。

Strategy 的本质，是承认“算法”本身就是变化点。折扣规则、路由策略、排序规则、召回策略、风控规则，这些业务场景都有一个共同点：目标一致，但实现规则经常变化。 如果主流程中不断累加 `if / elif / else`，代码很快就会变成条件泥潭。

在 AI Coding 场景里，Strategy 的价值尤其大。因为模型非常擅长为每个新需求多写一个分支，却不会主动把这些分支识别为“同一接口下的一组可替换算法”。 因此，是否能从一堆相似条件里抽出策略接口，往往决定系统是继续保持可扩展，还是在第三、第四次迭代后开始僵化。

- 适合：定价、排序、调度、推荐、规则匹配、审核。
- 不适合：只有两个稳定分支且几乎不扩展的简单逻辑。
- 典型框架感知：Spring 中大量面向接口的资源访问和策略替换思想都能映射到它。[[3]](#ref-3)

```
from abc import ABC, abstractmethod


class PricingStrategy(ABC):
    @abstractmethod
    def price(self, amount: float) -> float:
        raise NotImplementedError


class PercentageDiscount(PricingStrategy):
    def __init__(self, percent: float) -> None:
        self.percent = percent

    def price(self, amount: float) -> float:
        return round(amount * (1 - self.percent), 2)


class Checkout:
    def __init__(self, strategy: PricingStrategy) -> None:
        self.strategy = strategy

    def total(self, amount: float) -> float:
        return self.strategy.price(amount)
```

等待运行...

### Observer：把“发生了什么”与“谁来响应”拆开

关键词：事件驱动、发布订阅、认知解耦。

Observer 解决的问题不是“通知别人很麻烦”，而是“发布方不应该知道所有消费者是谁”。订单支付成功之后，库存、积分、通知、审计、风控都可能要做事。 如果支付主流程亲自调所有模块，每加一个消费者都要改主流程。

在 AI 生成代码时，这种问题很常见。模型会自然地把“顺手做的事”继续塞进主链路里。Observer 提供了一种更成熟的结构：主流程只发布事实，附加行为由订阅者自己接住。

- 适合：通知、事件扩展点、插件机制、领域事件。
- 风险：不能把它当成一致性银弹，事务语义仍需单独设计。
- 典型案例：Spring `ApplicationEventPublisher`、Django Signals。[[4]](#ref-4)[[7]](#ref-7)

```
class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list] = {}

    def subscribe(self, event: str, fn) -> None:
        self._subscribers.setdefault(event, []).append(fn)

    def publish(self, event: str, payload: dict) -> None:
        for fn in self._subscribers.get(event, []):
            fn(payload)
```

等待运行...

### Factory Method：把创建哪种对象的决定延迟出去

关键词：创建延迟、解耦具体类、集中扩展入口。

Factory Method 关注的是“创建过程”本身的变化。当调用方只关心“我要一个报表对象”“我要一个解析器”“我要一个客户端”时，它不应该同时承担“到底创建 Json 还是 Html，Local 还是 Remote”的决定。

这在框架中极其常见。对象创建往往伴随配置读取、依赖装配、生命周期管理，远不只是一个简单的构造函数。把具体实例化决策放到工厂体系中，可以让新类型接入时影响面更集中。

- 适合：导出器、解析器、存储后端、客户端实例。
- 典型案例：Flask Application Factory，Spring Bean 创建思想。[[8]](#ref-8)[[3]](#ref-3)

```
class JsonReport:
    def render(self) -> str:
        return '{"status": "ok"}'


class HtmlReport:
    def render(self) -> str:
        return "<p>ok</p>"


class JsonReportCreator:
    def create_report(self):
        return JsonReport()


class HtmlReportCreator:
    def create_report(self):
        return HtmlReport()
```

等待运行...

### Abstract Factory：创建的不是一个对象，而是一整套兼容对象

关键词：对象族、一致性、成套切换。

如果 Factory Method 关注“创建哪个对象”，那么 Abstract Factory 关注“创建哪一整套彼此兼容的对象族”。典型例子是主题系统、数据库方言、云厂商适配层。 你切换的不是一个按钮，而是一整套按钮、对话框、输入框、颜色系统。

这在 AI 生成前端或 SDK 集成代码时尤其有用。因为模型常常会在局部生成看似合理但整体风格不一致的组件，而 Abstract Factory 可以把“一致性”本身结构化。

- 适合：主题系统、多平台组件、多供应商 SDK。
- 边界辨析：Factory Method 面向单对象；Abstract Factory 面向对象家族。

```
class DarkThemeFactory:
    def create_button(self) -> str:
        return "dark-button"

    def create_dialog(self) -> str:
        return "dark-dialog"


class LightThemeFactory:
    def create_button(self) -> str:
        return "light-button"

    def create_dialog(self) -> str:
        return "light-dialog"
```

等待运行...

### Singleton：全局唯一很诱人，但必须克制

关键词：唯一实例、全局访问、状态污染风险。

Singleton 是最容易被误用的模式之一。它应该表达的是“语义上全局唯一”的资源，例如进程级配置、注册表、资源门面，而不是“我懒得传递依赖，所以做成全局变量”。

在现代工程里，更推荐让容器管理 singleton scope，而不是每个业务类都自己实现一遍单例。因为手写单例很容易带来测试污染、状态残留和并发语义不清。

- 适合：配置对象、全局资源注册表。
- 不适合：普通业务依赖、可变状态很多的对象。
- 现代实践：能交给 DI 容器，就尽量别手写。

```
class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.debug = False
        return cls._instance
```

等待运行...

### Adapter：旧系统不动，新系统照样接上

关键词：接口翻译、兼容层、遗留系统接入。

Adapter 适合处理“旧接口与新接口不兼容”的问题。真正的软件工程很少是从零起步，更多是在遗留系统、第三方 API、旧 SDK 和新模块之间搭桥。 Adapter 的价值在于：你不需要重写旧系统，只需要补一层翻译。

在 AI Coding 场景里，这一点非常现实。模型通常会根据“理想接口”生成新代码，而现实项目里往往是一堆历史包袱。Adapter 就是让理想结构与现实系统相遇时不至于撞碎的缓冲层。

- 适合：遗留系统整合、第三方 SDK 统一封装、支付短信网关接入。
- 典型案例：Spring MVC `HandlerAdapter`，Requests `HTTPAdapter`。[[5]](#ref-5)[[9]](#ref-9)

```
class LegacySmsService:
    def send_sms(self, mobile: str, content: str) -> str:
        return f"SMS to {mobile}: {content}"


class SmsAdapter:
    def __init__(self, legacy: LegacySmsService) -> None:
        self.legacy = legacy

    def send(self, user: str, message: str) -> str:
        return self.legacy.send_sms(user, message)
```

等待运行...

### Decorator：不改原类，也能一层层加能力

关键词：职责增强、组合叠加、横切能力。

Decorator 最适合日志、缓存、鉴权、重试、限流、埋点、压缩这类横切增强。它和继承相比更灵活，因为能力可以按需叠加，而不是预先派生出一大堆组合子类。

Python 里的装饰器语法，本质就是这种思想的广泛普及。一个 `@cache`、`@retry`、`@trace`，其实都在告诉你：增强职责，不一定非得改原函数。

- 适合：横切能力、按需叠加的增强行为。
- 边界辨析：Decorator 是增强职责，不是控制访问。

```
class BasicSender:
    def send(self, message: str) -> str:
        return f"send:{message}"


class TimestampDecorator:
    def __init__(self, wrapped) -> None:
        self.wrapped = wrapped

    def send(self, message: str) -> str:
        return self.wrapped.send(f"[2026-05-22] {message}")
```

等待运行...

### Proxy：接口相同，但访问行为不同

关键词：控制访问、懒加载、远程代理、权限边界。

Proxy 的结构往往和 Decorator 很像，但意图不同。Decorator 是在增强职责，Proxy 是在控制访问。 你看上去在访问真实对象，实际上先经过一个控制层，它可以负责权限校验、懒加载、缓存命中、远程调用、事务包裹。

现代框架里，Proxy 极其重要。Spring AOP 的很多能力都基于代理机制；ORM 的懒加载对象本身也是代理思想的工程化体现。[[5]](#ref-5)

- 适合：权限控制、事务代理、远程服务、本地缓存前置。
- 边界辨析：结构相似不等于模式相同，关键看意图。

```
class FileStore:
    def read(self, path: str) -> str:
        return f"content({path})"


class AccessProxy:
    def __init__(self, store: FileStore, allowed: set[str]) -> None:
        self.store = store
        self.allowed = allowed

    def read(self, path: str) -> str:
        if path not in self.allowed:
            raise PermissionError(path)
        return self.store.read(path)
```

等待运行...

### Template Method：先固定流程骨架，再留局部变化

关键词：算法骨架、步骤延迟、稳定流程。

Template Method 非常适合那种“主流程稳定，但局部步骤会换”的问题。 例如抽取、转换、加载，或者获取连接、执行核心逻辑、清理资源。你不希望调用方每次都自己拼整个流程，也不希望所有细节都被写死在同一个实现里。

它的魅力在于：流程顺序由模板保证，变化点则交给子类实现。Spring 的 `JdbcTemplate` 正是这种思想的经典工业案例。[[6]](#ref-6)

- 适合：ETL、数据库访问、固定业务管道。
- 风险：过度依赖继承会走向层级膨胀，应警惕变成继承地狱。

```
class DataPipeline:
    def run(self) -> str:
        raw = self.extract()
        clean = self.transform(raw)
        return self.load(clean)

    def extract(self) -> str:
        raise NotImplementedError

    def transform(self, raw: str) -> str:
        raise NotImplementedError

    def load(self, clean: str) -> str:
        raise NotImplementedError
```

等待运行...

### Facade：复杂子系统，对外只给一个清晰入口

关键词：统一入口、隐藏编排复杂度、降低调用方负担。

Facade 不是消灭复杂性，而是把复杂性留在该留的地方。下单、支付、物流、库存、通知，这些子系统可能都很复杂，但调用方没必要每次都重新写一遍编排逻辑。

在 AI 时代，这一点格外关键。模型很容易在多个地方各写一遍“预占库存 -> 扣款 -> 发货”的流程，这类重复编排一旦散开，后续维护会非常痛苦。Facade 的意义就是把高频协作流程集中起来。

- 适合：下单、支付、转码、聚合搜索、导出流程。
- 好处：调用方只面对一个高层接口，不承担底层协作细节。

```
class Inventory:
    def reserve(self, sku: str) -> str:
        return f"reserved:{sku}"


class Payment:
    def charge(self, user: str, amount: float) -> str:
        return f"charged:{user}:{amount}"


class Shipping:
    def create(self, sku: str) -> str:
        return f"ship:{sku}"


class OrderFacade:
    def place(self, user: str, sku: str, amount: float) -> list[str]:
        return [
            Inventory().reserve(sku),
            Payment().charge(user, amount),
            Shipping().create(sku),
        ]
```

等待运行...

## 四、10 个模式放在一起时，应该怎么选

| 真正的问题 | 优先考虑的模式 | 判断句 |
| --- | --- | --- |
| 同一个目标有多种算法 | Strategy | 变化的是算法，不是主流程 |
| 对象创建过程会变化 | Factory Method | 使用方不该知道具体实现如何被创建 |
| 要切换整套兼容组件 | Abstract Factory | 你需要的不是一个对象，而是一整套一致系统 |
| 一个事件要通知多个响应者 | Observer | 发布方不应认识所有消费者 |
| 旧接口和新接口不兼容 | Adapter | 补翻译层，而不是大拆旧系统 |
| 横切能力需要可叠加 | Decorator | 增强职责，而不是复制子类 |
| 访问前要做控制 | Proxy | 接口不变，访问行为改变 |
| 流程骨架稳定，步骤局部可变 | Template Method | 先定骨架，再开放步骤 |
| 子系统太复杂，对外要统一入口 | Facade | 调用方不该承担编排复杂度 |
| 确实需要全局唯一实例 | Singleton | 但先确认是否应该交给容器管理 |

## 五、AI Coding 时代最常见的模式误用

今天最危险的问题，不是“开发者不会设计模式”，而是“模型学会几个模式名字后开始到处套壳”。这会让系统表面上看起来很工程化，实际上只是多了一层层没有必要的结构噪音。

- 为了抽象而抽象：明明只有一个实现，也先造接口、工厂和代理。
- 用 Singleton 掩盖依赖传递：把依赖注入偷懒成全局状态。
- 把 Observer 误当异步银弹：任何事都发事件，最终一致性和时序全乱。
- 把 Decorator、Proxy、Adapter 混为一谈：只看结构，不看意图。
- 把 Template Method 用成继承地狱：层级越来越深，扩展点越来越碎。

一个务实结论：

最好的设计模式使用方式，不是“模式越多越高级”，而是“只有在真实变化出现时，才精确地引入恰当模式”。

## 六、为什么 Spring、Django、Flask、Requests 这些框架会反复使用这些模式

因为这些模式和框架面对的问题天然同构。Spring 需要 IOC，于是创建逻辑必须抽离；它需要 AOP，于是代理机制成为核心；它需要模板化数据库访问，于是 Template Method 变成基础骨架。 Django 需要信号系统，于是 Observer 思想自然出现；Flask 需要延迟创建应用对象，于是工厂思想很自然；Requests 需要对不同传输层做统一封装，于是 Adapter 结构非常合理。[[3]](#ref-3)[[5]](#ref-5)[[6]](#ref-6)[[7]](#ref-7)[[8]](#ref-8)[[9]](#ref-9)

这件事对 AI Coding 的意义非常直接：如果你不理解框架底层依赖的是哪类结构，模型就会为你生成“能跑，但不顺着框架哲学”的代码。短期可能能过，长期会非常难维护。

## 七、最后的判断：AI Coding 时代最值钱的不是写出第一版，而是第五次迭代后还站得住

设计模式在今天真正重要，不是因为它们属于经典，而是因为它们刚好提供了一套跨时代都稳定有效的结构判断工具。 当 AI 让代码生成变得极快时，人类最值钱的能力就不再是“我能敲出来”，而是“我知道这段代码之后会朝哪里腐化，以及该如何在一开始就把腐化路径切断”。

所以，理解设计模式，并不是为了把系统写得更像教科书；而是为了在 AI 带来的速度优势面前，仍然守住软件工程最本质的东西：边界、替换、演化、测试、协作。

一句收束全文的话：

AI Coding 时代，真正稀缺的不是代码，而是结构。设计模式正是结构思维最短、最稳、最经得起时间检验的训练路径之一。

---

## 参考文献

[[1]](https://refactoring.guru/design-patterns/catalog) Refactoring.Guru. *Design Patterns Catalog*.

[[2]](https://martinfowler.com/articles/injection.html) Fowler, M. *Inversion of Control Containers and the Dependency Injection Pattern*.

[[3]](https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html) Spring Framework Reference. *Bean Scopes*.

[[4]](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/ApplicationEventPublisher.html) Spring Framework Javadoc. *ApplicationEventPublisher*.

[[5]](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html) Spring Framework Reference. *Proxying Mechanisms*.

[[6]](https://docs.spring.io/spring-framework/reference/data-access/jdbc/core.html) Spring Framework Reference. *JDBC Core and JdbcTemplate*.

[[7]](https://docs.djangoproject.com/en/stable/topics/signals/) Django Documentation. *Signals*.

[[8]](https://flask.palletsprojects.com/en/stable/patterns/appfactories/) Flask Documentation. *Application Factories*.

[[9]](https://requests.readthedocs.io/en/latest/user/advanced/#transport-adapters) Requests Documentation. *Transport Adapters*.

[[10]](https://docs.python.org/3/library/abc.html) Python Documentation. *abc*.

[[11]](https://docs.python.org/3/library/contextlib.html) Python Documentation. *contextlib*.

[[12]](https://doi.org/10.1016/j.infsof.2015.05.006) Ampatzoglou, A., Chatzigeorgiou, A., Charalampidou, S., and Avgeriou, P. The effect of GoF design patterns on stability: A case study. *Information and Software Technology*, 2015.

[[13]](https://www.sciencedirect.com/science/article/pii/S0164121216302321) Ampatzoglou, A., et al. The state of the art on software engineering design patterns: A systematic mapping study. *Journal of Systems and Software*, 2016.
