# Complete GoF design-pattern catalog

## Coverage contract

This catalog teaches all 23 Gang of Four patterns: 5 creational, 7 structural, and 11 behavioral. “All design patterns” is not a finite category; treat GoF as the canonical complete catalog, and evaluate architectural styles/framework idioms separately. For every pattern: identify a proven variation, choose by intent rather than shape, state the cost, compare neighbors, and test the seam.

## Creational patterns

| Pattern | Intent and use | Cost, boundary, verification |
| --- | --- | --- |
| Abstract Factory | Create compatible product families when platform/theme/vendor families switch together. Client uses abstract factory/products. | More types; adding a product kind changes every factory. Factory Method creates one product, Builder assembles one complex product. Test every family combination and forbid mixed families. |
| Builder | Assemble a complex object through ordered/optional steps while preserving construction invariants. | Ceremony is wasteful for small values. Unlike Abstract Factory, it constructs one object step-by-step. Test incomplete/invalid sequences, defaults, and final immutability. |
| Factory Method | Defer one concrete product choice from users to a creator or injected creation seam. | Subclass/factory growth; a constructor function may be clearer. Unlike Abstract Factory, it does not select a family. Add a product without changing clients; test selection/lifecycle errors. |
| Prototype | Create a configured object by copying a prototype. | Deep/shallow copy, identity, resources, and mutable nested state are dangerous. Unlike Builder it copies rather than assembles. Mutate clone/original independently and test cycles/resources. |
| Singleton | Enforce a declared semantic uniqueness scope; prefer DI-container lifetime. | Hidden dependencies, test contamination, global mutation, concurrency ambiguity. Never use to avoid DI. Define scope and test isolation/reset/concurrency. |

## Structural patterns

| Pattern | Intent and use | Cost, boundary, verification |
| --- | --- | --- |
| Adapter | Translate an incompatible legacy/third-party interface into the target interface. | Can conceal a wrong model. Facade simplifies; Decorator enhances; Proxy controls. Contract-test data/error/version translation. |
| Bridge | Split two independent axes of variation to avoid a subclass cross-product. | Indirection is unjustified if axes do not vary independently. Strategy swaps one algorithm; Bridge is a durable abstraction/implementation split. Test axis combinations. |
| Composite | Treat leaf and part-whole tree uniformly through one component contract. | Shared contract may become dishonest. Decorator wraps one component; Composite holds many. Test empty/deep trees, cycles, and leaf restrictions. |
| Decorator | Stack optional responsibilities such as cache/retry/logging without subclass combinations. | Wrapper order, debugging, and identity matter. Proxy controls access; Adapter translates. Test individual/stacked/order-sensitive behavior and exceptions. |
| Facade | Give callers one high-level interface over repeated complex subsystem orchestration. | Can become a god object or hide transaction policy. Adapter translates while Facade simplifies. Test order, compensations, failures, and decoupled callers. |
| Flyweight | Share intrinsic immutable state when measured object-count pressure exists; provide extrinsic context on use. | Cache lifecycle/identity/thread safety; premature optimization is harmful. Prototype copies; Flyweight shares. Benchmark memory and test immutability/eviction. |
| Proxy | Preserve subject interface while controlling authorization, lazy load, remote access, cache, or transaction behavior. | Hidden latency/failures and policy bypass. Decorator enhances; Proxy controls. Test allowed/denied, cache invalidation, remote failure, and bypasses. |

## Behavioral patterns

| Pattern | Intent and use | Cost, boundary, verification |
| --- | --- | --- |
| Chain of Responsibility | Pass a request through ordered optional handlers until handled or exhausted. | Requests may vanish and ordering is policy. Observer broadcasts; Chain routes. Test no-handler, order, short-circuit, errors, and cycles. |
| Command | Represent an operation for queueing, audit, retry, scheduling, remote dispatch, or undo. | Many tiny types and idempotency ambiguity; a callable may suffice. Strategy selects algorithm; Command represents a request. Test serialization, retry, authorization, compensation. |
| Interpreter | Represent/evaluate a small stable DSL grammar through expression objects. | Grammar growth becomes class explosion; use parser engines for serious languages. Visitor adds operations to an AST; Interpreter defines semantics. Test invalid syntax, precedence, limits, diagnostics. |
| Iterator | Traverse an aggregate without exposing representation. | Mutation invalidation, resource lifetime, hidden I/O; language-native iteration may suffice. Test empty/deep/paginated/mutating/cancelled traversal. |
| Mediator | Centralize complex peer coordination so peers do not form a coupling mesh. | Mediator may become a god object. Facade simplifies client/subsystem; Mediator coordinates peers. Test rules, transitions, and prohibited direct coupling. |
| Memento | Capture/restore state without exposing internals for undo/checkpoints. | Memory, sensitive retention, versioning, shallow copies. Command may use Memento; it stores state not operation. Test restoration, branching, redaction, versions. |
| Observer | Broadcast a fact to independent subscribers without making publisher know consumers. | Ordering, handler failure, delivery, transaction, retries, idempotency, and consistency require separate design. Chain routes one request. Test lifecycle, duplicates, outbox/transaction policy. |
| State | Change context behavior according to explicit lifecycle state and transitions. | Too many classes for trivial conditionals; transitions can become hidden. Strategy is externally selected algorithm; State is lifecycle-selected behavior. Test transition table, illegal/concurrent/recovered states. |
| Strategy | Swap a family of algorithms serving one stable goal. | Unneeded for a few stable branches; selection policy can leak. Template Method fixes skeleton; State models lifecycle. Contract-test each algorithm and fallback/edge cases. |
| Template Method | Fix algorithm order/invariants and defer local steps to subclasses. | Fragile base class and inheritance hell; prefer composition for independently combinable changes. Test ordering, hooks, failure cleanup, subclass substitution. |
| Visitor | Add operations across a stable heterogeneous element structure through double dispatch. | New element types force every visitor change. Interpreter evaluates a grammar; Visitor adds operations. Test each visitor-element pair and missing operations. |

## Teaching checklist

For each candidate, explain: the changing thing; stable core; collaborators and dependency direction; lifecycle/ownership; direct alternative; nearest patterns rejected; failure semantics; and normal, boundary, failure, integration, concurrency, and performance tests where relevant.

## Non-negotiable distinctions

- Decorator / Proxy / Adapter = enhancement / control / translation.
- Factory Method / Abstract Factory / Builder / Prototype = one product choice / family choice / staged assembly / copying.
- Strategy / State / Template Method = chosen algorithm / lifecycle behavior / fixed skeleton.
- Observer / Chain / Command = broadcast fact / ordered propagation / represented operation.
- Facade / Mediator = simplify subsystem access / coordinate peers.
