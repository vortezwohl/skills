---
name: software-design
description: Teach and govern software design-pattern decisions for new features, architecture, refactoring, and optimization. Use when Codex must choose, justify, apply, reject, or review GoF design patterns; remove structural code smells; define extension boundaries; integrate frameworks or legacy APIs; or prevent AI-generated code from becoming over-abstracted, tightly coupled, or hard to evolve.
---

# Software Design

Design for the next verified change, not for a pattern name. Treat patterns as tools for managing observed or strongly evidenced variation—not as decorations.

## Mandatory operating protocol

1. Read `references/source-article.md` before the first design decision in every invocation. It is the agent-oriented fidelity guide; `references/source-original.md` is the complete unmodified source evidence.
2. Read `references/decision-protocol.md` before proposing a design or refactor. Follow every gate; do not skip a gate because the answer appears obvious.
3. Read the relevant entries in `references/gof-patterns.md` before choosing, rejecting, implementing, or reviewing a GoF pattern. Read all candidate entries when candidates are easily confused.
4. Inspect the repository before changing code. Identify callers, current tests, error paths, ownership, state, framework conventions, and existing abstractions.
5. Prefer the smallest design that isolates the proven change. A direct implementation is a valid and often preferred result.
6. Implement only after recording the decision evidence required by the protocol. Preserve or add tests before behavior-preserving refactors.
7. Re-run focused validation, then review cross-module compatibility, lifecycle, concurrency, observability, and rollback implications.

## Non-negotiable rules

- Do not start from “Which pattern should I use?” Start from “What changes independently, and what remains stable?”
- Do not introduce an interface, factory, wrapper, event, inheritance hierarchy, global object, or framework layer without naming the concrete variation it isolates and the cost it adds.
- Do not claim a pattern is appropriate because its class diagram resembles the code. Decide by intent, collaborators, lifecycle, and failure modes.
- Do not use a pattern merely because a framework uses it internally. Follow the framework’s extension mechanisms rather than reproducing its internal architecture.
- Do not convert uncertainty into speculative abstraction. If variation is not evidenced, retain the simpler design and state the trigger that would justify extraction later.
- Do not call an event an asynchronous solution. Define transaction boundaries, delivery guarantees, ordering, retries, idempotency, and consistency separately.
- Do not use Singleton to avoid dependency injection. Prefer explicit dependencies and container-managed lifetimes.
- Do not use inheritance when composition, a callback, or a direct function makes the variation clearer and safer.
- Do not present an unverified refactor as complete. Report the exact validation performed and the remaining risk.

## Required design record

For any non-trivial design, optimization, or refactor, include this record in the response or design artifact before implementation:

```md
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

- `references/source-article.md`: Agent-oriented fidelity guide for the original ten-pattern framing, examples, misuse warnings, framework examples, and bibliography.
- `references/source-original.md`: Complete unmodified source article, retained for exact source-level evidence and all original details.
- `references/gof-patterns.md`: Teaching catalog for all 23 Gang of Four patterns. Each entry explains intent, problem, structure, collaboration, trade-offs, neighboring patterns, misuse, and verification.
- `references/decision-protocol.md`: Binding diagnostic questions, selection matrix, refactoring sequence, review gates, and anti-pattern controls.

## Completion standard

Finish only when the selected design is justified against a simpler alternative, adjacent patterns are ruled in or out by intent, behavior is verified at the appropriate boundary, and no new abstraction lacks a named variation point.
