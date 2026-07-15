# Binding design and refactoring protocol

## Diagnose before abstraction

Before selecting a pattern, record: objective/non-goals; observed facts versus assumptions; affected callers; stable core; independently changing parts; current smells; compatibility; ownership/lifecycle; transactions; concurrency; performance/security constraints; framework extension points; and the smallest direct solution.

A pattern may be introduced only when all applicable claims are true: (1) a concrete variation is named and evidenced; (2) the pattern isolates it more directly than alternatives; (3) every added type/wrapper/event/global has an owner and lifecycle; (4) public API/dependency direction improve or do not worsen; (5) failure behavior is testable; (6) adjacent patterns were rejected or deliberately combined by intent; and (7) the new structure costs less than continued branching, duplication, coupling, or inconsistency. Otherwise retain the direct design and state the extraction trigger.

## Selection rules

| Evidence | First candidate | Reject when |
| --- | --- | --- |
| Multiple algorithms, one goal | Strategy | Conditions are small/stable or data/functions suffice. |
| Stable sequence, variable steps | Template Method | Variations combine independently or inheritance is brittle. |
| Explicit lifecycle behavior | State | No transition model exists. |
| Ordered optional handling | Chain | Every handler must run. |
| Independent event reactions | Observer | Transaction/delivery/order/retry semantics are unspecified. |
| Queue/retry/audit/undo operation | Command | Direct call is enough. |
| One product creation varies | Factory Method | Constructor/injected function is clearer. |
| Product family switches together | Abstract Factory | Only one product varies. |
| Complex staged construction | Builder | Value construction is simple. |
| Copy prepared configuration | Prototype | Copy semantics are unclear. |
| True scoped uniqueness | Singleton scope | It hides dependency passing. |
| Incompatible interfaces | Adapter | Actual issue is complexity, enhancement, or access. |
| Independent abstraction/implementation axes | Bridge | Axes are not independent. |
| Part-whole tree | Composite | Contract would be dishonest. |
| Stackable responsibility | Decorator | Actual intent is control/translation. |
| Repeated subsystem orchestration | Facade | It becomes a god object. |
| Measured shared-object pressure | Flyweight | No measurements or unsafe sharing. |
| Controlled access/lazy/remote/transaction | Proxy | It only enhances or translates. |
| Small stable DSL | Interpreter | A real parser/engine is needed. |
| Hidden traversal | Iterator | Native iteration is enough. |
| Peer coupling mesh | Mediator | Mediator becomes a god object. |
| Exact internal rollback | Memento | State is too sensitive/large or history itself is needed. |
| Stable elements, many operations | Visitor | Elements change frequently. |

## Mandatory neighbor check

Explain these distinctions whenever relevant: Decorator/Proxy/Adapter (enhance/control/translate); Facade/Mediator (simplify clients/coordinate peers); Factory Method/Abstract Factory/Builder/Prototype (one product/family/staged assembly/copy); Strategy/State/Template Method (algorithm/lifecycle/skeleton); Observer/Chain/Command (broadcast/propagate/operation); Composite/Decorator (tree/wrapper).

## Refactoring and review gate

1. Characterize current behavior with existing tests or focused reproduction.
2. Map callers, concrete dependencies, side effects, mutation, and failure paths.
3. Extract one smallest seam; do not mix cleanup with unrelated redesign.
4. Preserve behavior unless change is explicitly requested.
5. Contract-test each new seam and run affected tests.
6. Check lifecycle, dependency direction, transaction/async semantics, error propagation, observability, resource cleanup, and framework conventions.
7. Stop when the objective is met.

Reject AI-generated structure that: creates interfaces/factories/proxies/events around one stable implementation; repeats orchestration; constructs infrastructure everywhere; hides dependencies globally; calls events an async solution without delivery design; combines optional behavior through inheritance; names wrappers by shape rather than intent; fights framework lifecycle; or claims cleanliness without measurable boundary/test improvement.

## Required final report

State the evidence, direct alternative, selected or rejected patterns and reasons, API/dependency impact, tests for normal/boundary/failure/integration/concurrency/performance paths, validation actually run, and remaining risk. Never mark unrun verification as passed.
