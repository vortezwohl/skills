# Binding design and refactoring protocol

## Language neutrality

Write this skill's maintainer-facing instructions and canonical templates in English. This does not constrain user-facing output. Render every user-facing question, architecture proposal, approval request, and final report in the user's current interaction language unless the user explicitly requests a different language.

The numbered templates below prescribe decision semantics, not a required output language. Translate or adapt their wording while preserving the same 1 and 2 meanings. Accept a numeric reply or free-form feedback in any language, and treat explicit user language preferences as authoritative.

## Gate 0: Compatibility intent before design

Apply this gate before repository inspection, architectural analysis, pattern selection, or implementation planning when the request may affect behavior, contracts, data, configuration, integrations, or extension points.

Classify the request only far enough to determine whether this gate applies. Do not infer lifecycle, deployment status, external consumers, or compatibility requirements from the repository or task wording. A repository may be unfinished, actively developed, deployed, or consumed by unknown users.

Ask exactly one primary compatibility question:

```text
Before I analyze the architecture, please choose the compatibility intent:

1. Preserve backward compatibility - keep existing agreed behavior for the affected contracts.
2. Allow intentional breaking changes - prioritize a cleaner long-term design over legacy behavior.

You can also describe a custom compatibility boundary instead of choosing 1 or 2.
```

Treat a free-form answer as authoritative and restate it as a concise compatibility intent. Do not silently choose an option for the user.

Do not treat a missing reply in the same interaction as consent. Silence is actionable only when the user has explicitly established a default policy. After the user has seen a proposal, an unambiguous instruction such as "proceed", "implement this", or an equivalent request to continue is valid implicit approval only when it does not contradict the recorded compatibility contract.

## Gate 1: Compatibility contract

After the user provides the compatibility intent, identify the compatibility surface that actually applies. Consider public APIs, request and response schemas, CLI arguments, configuration keys and environment variables, persisted data and migrations, database schemas, events and message contracts, plugins and extension points, URLs, permissions, operational procedures, documented behavior, and internal consumers that the user explicitly includes.

When compatibility is required:

1. Name the preserved behavior, contract, consumer, and verification method.
2. Identify the smallest bounded mechanism that preserves it.
3. Give every adapter, dual-read, dual-write path, flag, versioned contract, or deprecated path an owner, retirement condition, and rollback boundary.
4. Reject permanent legacy layers that have no named consumer or removal condition.
5. Prefer a limited compatibility mechanism over broad duplication or speculative versioning.

When breaking changes are allowed:

1. Name the intended breakage and the invariants that remain protected.
2. Describe migration, cutover, communication, rollback limits, and irreversible changes when relevant.
3. Remove obsolete contracts instead of retaining undocumented legacy paths.
4. Prefer the clearest durable design over preserving legacy behavior by default.

Record unresolved consumers, ambiguous contracts, and unavailable migration evidence as risks. Ask a follow-up question when they materially change the compatibility decision.

## Diagnose before abstraction

Before selecting a pattern, record: objective and non-goals; observed facts versus assumptions; affected callers; stable core; independently changing parts; current smells; the approved compatibility contract; ownership and lifecycle; transactions; concurrency; performance and security constraints; framework extension points; and the smallest direct solution.

A pattern may be introduced only when all applicable claims are true: (1) a concrete variation is named and evidenced; (2) the pattern isolates it more directly than alternatives; (3) every added type, wrapper, event, or global has an owner and lifecycle; (4) public API and dependency direction improve or do not worsen; (5) failure behavior is testable; (6) adjacent patterns were rejected or deliberately combined by intent; and (7) the new structure costs less than continued branching, duplication, coupling, or inconsistency. Otherwise retain the direct design and state the extraction trigger.

## Gate 2: Architecture consent before implementation

After diagnosis and alternatives are complete, present a bounded architecture proposal. Include the compatibility contract, the smallest direct alternative, the recommended design, rejected alternatives, affected contracts and consumers, migration or cutover impact, rollback plan, validation plan, and remaining risks.

Ask exactly one approval question:

```text
Please confirm the proposed architecture:
1. Approve this architecture - I will implement the stated design and compatibility contract.
2. Request changes - tell me what you want changed before implementation.
You can also provide a different direction instead of choosing 1 or 2.
```

Treat free-form feedback as authoritative. If feedback changes constraints, return to the affected gate, revise the proposal, and request consent again. Do not implement while approval is unresolved.

## Selection rules

| Evidence | First candidate | Reject when |
| --- | --- | --- |
| Multiple algorithms, one goal | Strategy | Conditions are small, stable, or data/functions suffice. |
| Stable sequence, variable steps | Template Method | Variations combine independently or inheritance is brittle. |
| Explicit lifecycle behavior | State | No transition model exists. |
| Ordered optional handling | Chain | Every handler must run. |
| Independent event reactions | Observer | Transaction, delivery, order, or retry semantics are unspecified. |
| Queue, retry, audit, or undo operation | Command | A direct call is enough. |
| One product creation varies | Factory Method | A constructor or injected function is clearer. |
| Product family switches together | Abstract Factory | Only one product varies. |
| Complex staged construction | Builder | Value construction is simple. |
| Copy prepared configuration | Prototype | Copy semantics are unclear. |
| True scoped uniqueness | Singleton scope | It hides dependency passing. |
| Incompatible interfaces | Adapter | The actual issue is complexity, enhancement, or access. |
| Independent abstraction and implementation axes | Bridge | The axes are not independent. |
| Part-whole tree | Composite | The contract would be dishonest. |
| Stackable responsibility | Decorator | The actual intent is control or translation. |
| Repeated subsystem orchestration | Facade | It becomes a god object. |
| Measured shared-object pressure | Flyweight | There are no measurements or sharing is unsafe. |
| Controlled access, lazy loading, remote access, or transactions | Proxy | It only enhances or translates. |
| Small stable DSL | Interpreter | A real parser or engine is needed. |
| Hidden traversal | Iterator | Native iteration is enough. |
| Peer coupling mesh | Mediator | The mediator becomes a god object. |
| Exact internal rollback | Memento | State is too sensitive, too large, or history itself is needed. |
| Stable elements, many operations | Visitor | Elements change frequently. |

## Mandatory neighbor check

Explain these distinctions whenever relevant: Decorator, Proxy, and Adapter (enhance, control, translate); Facade and Mediator (simplify clients, coordinate peers); Factory Method, Abstract Factory, Builder, and Prototype (one product, family, staged assembly, copy); Strategy, State, and Template Method (algorithm, lifecycle, skeleton); Observer, Chain, and Command (broadcast, propagate, operation); Composite and Decorator (tree, wrapper).

## Approved refactoring and review execution gate

After architecture consent:

1. Characterize current behavior with existing tests or a focused reproduction.
2. Map callers, concrete dependencies, side effects, mutation, and failure paths within the approved compatibility scope.
3. Extract one smallest seam; do not mix cleanup with unrelated redesign.
4. Preserve or intentionally break behavior only as recorded in the compatibility contract.
5. Contract-test each new seam and run affected tests.
6. Check lifecycle, dependency direction, transaction and async semantics, error propagation, observability, resource cleanup, framework conventions, migration behavior, and rollback boundaries.
7. Stop when the approved objective is met.

Reject AI-generated structure that creates interfaces, factories, proxies, or events around one stable implementation; repeats orchestration; constructs infrastructure everywhere; hides dependencies globally; calls events an async solution without delivery design; combines optional behavior through inheritance; names wrappers by shape rather than intent; fights framework lifecycle; retains compatibility layers without named consumers and retirement conditions; or claims cleanliness without measurable boundary or test improvement.

## Required final report

State the compatibility intent, preserved and intentionally changed contracts, evidence, direct alternative, selected or rejected patterns and reasons, API and dependency impact, migration or rollback status, tests for normal, boundary, failure, integration, concurrency, and performance paths, validation actually run, and remaining risk. Never mark unrun verification as passed.
