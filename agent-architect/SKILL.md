---
name: agent-architect
description: "Provide architecture guardrails for non-trivial feature work, refactors, integrations, and structural changes. Use proactively before generating or reviewing code that may introduce boundaries, dependencies, state, lifecycles, abstractions, concurrency, or evolution costs. Resolve the user's backward-compatibility intent and obtain consent for the proposed architecture before implementation, then choose the smallest justified design and make validation and remaining risks explicit."
---

# Agent Architect

Design for the next verified change, not for a pattern name. Treat patterns as tools for managing observed or strongly evidenced variation - not as decorations.

## Mandatory operating protocol

1. Classify the request only far enough to determine whether this skill applies. Do not inspect the repository or begin architecture analysis during this classification.
2. Read `references/decision-protocol.md` before asking the user anything. At this point, use only Gate 0; do not inspect the repository or make a design decision.
3. Apply Gate 0 and receive the user's compatibility intent before repository inspection, architecture analysis, pattern selection, or implementation planning for any task that may affect behavior, contracts, data, configuration, integrations, or extension points.
4. After Gate 0 is resolved, follow every remaining applicable gate in `references/decision-protocol.md`; do not skip a gate because the answer appears obvious.
5. Read `references/source-article.md` before the first design decision. It is the complete English source article and primary reference for the skill.
6. Read the relevant entries in `references/gof-patterns.md` before choosing, rejecting, implementing, or reviewing a GoF pattern. Read all candidate entries when candidates are easily confused.
7. Inspect the repository only after the compatibility-intent gate is resolved. Identify callers, current tests, error paths, ownership, state, framework conventions, and existing abstractions.
8. Prefer the smallest design that isolates the proven change. A direct implementation is a valid and often preferred result.
9. Present the bounded architecture proposal and apply the architecture-consent gate before implementation.
10. Implement only after recording the decision evidence required by the protocol. Preserve or add tests before behavior-preserving refactors.
11. Re-run focused validation, then review cross-module compatibility, lifecycle, concurrency, observability, and rollback implications.

## Non-negotiable rules

- Do not begin by generating structure or choosing a pattern by resemblance. First identify what changes independently and what remains stable.
- Do not inspect the repository, select an architecture, or propose implementation details before resolving the user's compatibility intent when the task can affect an existing contract or behavior.
- Do not assume backward compatibility merely because a system may be in production, and do not assume a breaking redesign is acceptable merely because the repository appears unfinished.
- Treat compatibility as a scoped contract. Name the preserved and intentionally changed behaviors; do not merely state that a design is compatible.
- Do not impose English or any other fixed language on user-facing questions, proposals, or reports. Use the user's current interaction language unless the user explicitly requests a different language.
- Do not implement an architecture that the user has not approved, except when the user has explicitly authorized a default approval policy or has validly advanced the presented proposal to implementation.
- Do not introduce an interface, factory, wrapper, event, inheritance hierarchy, global object, or framework layer without naming the concrete variation it isolates and the cost it adds.
- Do not claim a pattern is appropriate because its class diagram resembles the code. Decide by intent, collaborators, lifecycle, and failure modes.
- Do not use a pattern merely because a framework uses it internally. Follow the framework's extension mechanisms rather than reproducing its internal architecture.
- Do not convert uncertainty into speculative abstraction. If variation is not evidenced, retain the simpler design and state the trigger that would justify extraction later.
- Do not call an event an asynchronous solution. Define transaction boundaries, delivery guarantees, ordering, retries, idempotency, and consistency separately.
- Do not use Singleton to avoid dependency injection. Prefer explicit dependencies and container-managed lifetimes.
- Do not use inheritance when composition, a callback, or a direct function makes the variation clearer and safer.
- Do not present an unverified refactor as complete. Report the exact validation performed and the remaining risk.

## Required design record

For any non-trivial design, optimization, or refactor, include this record in the response or design artifact before implementation:

```md
## Compatibility intent and consent
- User-selected compatibility intent and evidence:
- Preserved contracts and behavior:
- Explicitly breakable contracts and behavior:
- Compatibility mechanism, owner, retirement condition, and rollback boundary:
- Architecture approval status and user feedback:

## Design diagnosis
- Objective and non-goals:
- Observed evidence and affected callers:
- Stable core:
- Independent variation points:
- Current smells or failure modes:
- Constraints: compatibility, lifecycle, transactions, concurrency, performance, framework rules:

## Alternatives
- Smallest direct design:
- Candidate patterns and the variation each isolates:
- Adjacent patterns rejected, with reasons:
- Added structure and ongoing cost:

## Decision
- Chosen design (or justified decision to use no pattern):
- Public API and dependency-direction impact:
- Migration and rollback plan, if relevant:

## Verification
- Existing tests preserved:
- New normal, boundary, failure, and integration cases:
- Cross-module and operational checks:
- Remaining uncertainty or risk:
```

## Reference map

- `references/source-article.md`: Complete English source article for the ten-pattern framing, examples, misuse warnings, framework mappings, and bibliography.
- `references/gof-patterns.md`: Teaching catalog for all 23 Gang of Four patterns. Each entry explains intent, problem, structure, collaboration, trade-offs, neighboring patterns, misuse, and verification.
- `references/decision-protocol.md`: Binding compatibility-intent and architecture-consent gates, diagnostic questions, selection matrix, refactoring sequence, review gates, and anti-pattern controls.

## Completion standard

Finish only when the selected design is justified against a simpler alternative, the compatibility contract and architecture consent are recorded, adjacent patterns are ruled in or out by intent, behavior is verified at the appropriate boundary, and no new abstraction lacks a named variation point.
