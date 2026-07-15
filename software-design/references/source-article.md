# Source article: English fidelity guide

## Preservation contract

- The complete supplied webpage is archived without omission in `source-original.md`. Read it whenever exact wording, every original Python demo, rendered table, metadata, or bibliography detail is needed.
- This English guide is the agent-oriented translation index. It preserves every substantive claim, decision rule, pattern scope, applicability rule, risk, framework mapping, and conclusion; the raw source remains the authority for source-level fidelity.

## Article metadata and thesis

Title: *In the AI Coding era, learning and understanding design patterns becomes increasingly important.* Published May 22, 2026, under Software Architecture / AI Coding / Design Patterns, credited on the page to vortezwohl, Wu Zihao, and Codex.

Architecture—not merely feature implementation—is the core competitive advantage. AI makes large implementations cheap, but magnifies structural mistakes: code must remain evolvable, collaborative, and verifiable. Patterns are compressed engineering knowledge about repeated structures of change: where change occurs, who knows it, how it is isolated, how it is tested, and how collaboration limits impact. Their AI-era function is preventing a model from copying a wrong structure dozens of times.

| Failure | Manifestation | Missing judgment | Candidate patterns |
| --- | --- | --- | --- |
| Feature chaos | Each request adds a branch | Algorithm/process variation ignored | Strategy, Template Method |
| Dependency diffusion | Concrete objects created everywhere | Creation not separated from use | Factory Method, Abstract Factory |
| Cross-cutting sprawl | Logging/cache/auth scattered | Enhancement/control not collected at a boundary | Decorator, Proxy, Facade |

## Variation-first teaching rule

Before selecting a pattern, answer: (1) which variation is isolated—algorithm, creation, notification, or access; (2) which cost is added—interfaces, families, proxy, or inheritance; (3) which neighboring pattern boundary applies; (4) how the pattern appears in a framework—classes, configuration, container, callbacks, decorators; and (5) which smell occurs without it—conditional swamp, duplicated orchestration, global-state pollution, or coupling diffusion. Patterns are change-management tools, not a priori religion.

## The article’s ten patterns

### Creational

- **Strategy is behavioral, but is listed below.** The creational group is Factory Method, Abstract Factory, and Singleton: move object-creation decisions out of users.
- **Factory Method:** defer concrete creation; callers that need reports, parsers, or clients should not choose JSON/HTML or local/remote. It fits exporters, parsers, storage backends, and clients; framework examples are Flask application factories and Spring Bean creation. Its demonstration creates JSON and HTML reports through distinct creators.
- **Abstract Factory:** create a compatible family rather than a single object. It fits themes, cross-platform components, and multi-vendor SDKs; use it when a whole consistent set changes. Distinguish it from Factory Method: the latter creates one object, the former a family. The demo supplies dark/light factories that create matching buttons and dialogs.
- **Singleton:** represent semantic global uniqueness for process configuration, registries, or resource facades—not reluctance to pass dependencies. Prefer DI-container-managed singleton scope; hand-written forms risk test pollution, residual state, and unclear concurrency. It does not fit ordinary business dependencies or mutable objects. The demo caches an `AppConfig` instance in `__new__`.

### Structural

- **Adapter:** translate incompatible old/new interfaces instead of rewriting legacy systems. It fits legacy integration, unified third-party SDKs, and payment/SMS gateways; examples include Spring MVC HandlerAdapter and Requests HTTPAdapter. The demo adapts `LegacySmsService.send_sms` to `send`. AI often generates ideal interfaces while real repositories carry history; Adapter is the buffer.
- **Decorator:** stack responsibility enhancements—logging, caching, authorization, retry, rate limiting, instrumentation, compression—without subclass combinations. Python `@cache`, `@retry`, and `@trace` express the same idea. Its intent is enhancement, not access control; the demo wraps a sender with a timestamp.
- **Proxy:** preserve an interface but control access, including authorization, lazy load, cache hit, remote invocation, and transaction wrapping. Its intent differs from Decorator even when the shape is similar. It fits authorization, transactions, remote services, and cache fronting; Spring AOP and ORM lazy loading are examples. The demo blocks unallowed file paths before delegating.
- **Facade:** expose one clear entry to a complex subsystem; do not eliminate complexity, place it correctly. It centralizes repeated orchestration such as inventory reservation, charging, and shipping, and fits ordering, payment, transcoding, aggregate search, and export. Its benefit is that callers do not bear low-level coordination. The demo’s `OrderFacade` coordinates inventory, payment, and shipping.

### Behavioral

- **Strategy:** extract a family of changing algorithms from the main flow. Pricing, routing, sorting, recall, risk control, scheduling, recommendation, rule matching, and review fit; two stable branches with almost no extension do not. AI tends to add one more conditional instead of recognizing interchangeable algorithms. The demo uses a pricing interface, percentage discount, and checkout context.
- **Observer:** separate “what happened” from “who responds.” Publishers should not know every consumer: payment may trigger inventory, points, notification, audit, and risk control. It fits notifications, extension points, plugins, and domain events; Spring ApplicationEventPublisher and Django Signals are cases. It is not a consistency silver bullet—transaction semantics must be designed separately. The demo event bus stores subscribers and publishes payloads.
- **Template Method:** fix a stable process skeleton and vary local steps, as in ETL or acquire/execute/cleanup database work. It fits ETL, database access, and fixed business pipelines; Spring JdbcTemplate is the example. Process order is guaranteed while subclasses supply variation; excessive inheritance risks inheritance hell. The demo’s data pipeline runs extract, transform, then load.

## Article selection table

| Real question | Prefer | Decision sentence |
| --- | --- | --- |
| Same goal, multiple algorithms | Strategy | The algorithm changes, not the main process. |
| Object creation changes | Factory Method | Users should not know how concrete implementation is created. |
| Switch a compatible component set | Abstract Factory | Need a consistent system, not one object. |
| One event notifies many responders | Observer | Publisher should not know every consumer. |
| Old/new interfaces conflict | Adapter | Add translation; do not dismantle legacy system. |
| Cross-cutting capability stacks | Decorator | Enhance responsibility rather than copy subclasses. |
| Access needs prior control | Proxy | Interface stays; access behavior changes. |
| Skeleton stable, steps vary | Template Method | Fix skeleton, open steps. |
| Subsystem needs a single entry | Facade | Caller should not carry orchestration complexity. |
| Global uniqueness is real | Singleton | First ask whether container management is correct. |

## Misuse, framework, and conclusion

Do not abstract when one implementation is stable; do not turn DI laziness into Singleton global state; do not treat Observer as an asynchronous silver bullet; do not confuse Decorator/Proxy/Adapter by shape; do not let Template Method become inheritance hell. The best use is precise introduction only when real change appears.

Spring repeatedly needs extracted creation for IoC, proxies for AOP, and template access for JDBC; Django signals embody Observer; Flask factories delay app creation; Requests transport adapters unify transports. Without this structural understanding, AI may generate code that runs yet violates the framework’s philosophy and becomes hard to maintain.

The article closes: what matters is not writing the first version but surviving the fifth iteration. Under AI speed, value is recognizing how code will decay and cutting off that path early. Preserve boundaries, substitution, evolution, testing, and collaboration. Code is not scarce; structure is.

## Source bibliography

Refactoring.Guru Design Patterns Catalog; Fowler, *Inversion of Control Containers and the Dependency Injection Pattern*; Spring references for Bean Scopes, ApplicationEventPublisher, Proxying Mechanisms, JDBC Core/JdbcTemplate; Django Signals; Flask Application Factories; Requests Transport Adapters; Python `abc` and `contextlib`; Ampatzoglou et al. (2015) on GoF patterns and stability; Ampatzoglou et al. (2016) systematic mapping study.
