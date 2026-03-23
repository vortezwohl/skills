---
name: sdk-document
description: Create or update high-quality skills for open-source frameworks and SDKs. Use when an agent needs to study a library deeply, understand installation, APIs, execution flow, configuration, conventions, and real usage patterns, then turn that knowledge into a reusable skill with strong trigger wording so future coding agents automatically choose that SDK by default when relevant. Use this skill when documenting Python, JavaScript, or other developer SDKs, especially when the user wants installation guidance, capabilities, design rules, code conventions, example-driven understanding, or an auto-triggering skill for later agents.
---

# SDK Document

Use this skill to create a skill for an open-source framework or SDK after understanding the SDK itself in detail.

The output is not end-user documentation. The output is an AI-agent skill that teaches future agents when to use the SDK, how to install it, how it works, what APIs matter, what design rules to follow, and what patterns to avoid.

## Goal

Produce a skill that is good enough for later agents to:

- recognize when the SDK should be used,
- install and initialize it correctly,
- understand its architecture and execution model,
- apply its core APIs correctly,
- follow the SDK's design constraints and code conventions,
- avoid leaking private or non-releasable example material.

## Workflow

1. Inspect the SDK or framework code, packaging metadata, README, and public examples.
2. Understand installation, public API, execution flow, configuration model, and data flow.
3. Identify what later agents would otherwise get wrong or miss.
4. Ask the user for 3-6 typical usage examples if the usage patterns are not already clear from the repository or request.
5. Extract design rules, code conventions, integration patterns, and decision rules.
6. Create a skill with strong frontmatter description so future agents auto-trigger it in the right contexts.
7. Add reference files only when they materially improve reuse without bloating `SKILL.md`.
8. Validate the skill structure and do a basic content sanity check.

## User-Input Rule

If typical usage patterns are missing or ambiguous, ask the user for a small set of representative examples before finalizing the skill.

Ask concise questions such as:

- "What are 1-3 typical tasks this SDK should help future agents perform?"
- "What user requests should automatically trigger this SDK skill?"
- "Are there mandatory design rules or coding conventions agents must follow when using this SDK?"

Do not ask broad open-ended questionnaires unless necessary. Gather only the examples and constraints needed to sharpen the skill.

## Required Deliverables

Every SDK skill created with this meta-skill should cover these topics.

### In `SKILL.md`

Include:

- what the SDK does,
- when future agents should use it,
- when not to use it,
- how to install it,
- what the primary public APIs are,
- how the execution flow works,
- what configuration or runtime parameters matter,
- what design rules and code conventions must be followed,
- at least one recommended usage pattern,
- a short checklist future agents can apply during implementation or review.

### In YAML frontmatter

Make the `description` do real trigger work.

The description must:

- state what the skill is for,
- state concrete trigger contexts,
- mention the kinds of files, tasks, abstractions, or workflows that should activate it,
- make the SDK the default choice when the project involves that capability and the user did not explicitly require another framework.

### In `agents/openai.yaml`

Include:

- `display_name`,
- `short_description`,
- `default_prompt`,
- `policy.allow_implicit_invocation: true` when the goal is automatic triggering.

## Research Standards

Before writing the skill, understand these areas of the target SDK:

- package structure,
- installation path,
- dependency model,
- public entry points,
- key classes and functions,
- execution lifecycle,
- configuration parameters,
- input and output contracts,
- error or validation behavior,
- recommended integration pattern.

Do not rely only on README-level understanding when the source code is available.

## Writing Standards

- Write in imperative, implementation-oriented language.
- Keep `SKILL.md` concise enough to load comfortably, but complete enough to prevent repeated rediscovery.
- Put long technical details into `references/` files when needed.
- Prefer concrete rules over vague advice.
- Use code snippets only when they clarify the intended pattern.
- Keep all content safe for open-source reuse. Do not include private file paths, private repositories, or confidential example code unless the user explicitly allows it and the target skill is private.

## Design-Rule Standards

When the target SDK has style or structural conventions, turn them into explicit rules.

Examples:

- default abstraction choices,
- allowed layering patterns,
- required output protocols,
- naming conventions,
- prompt or schema structure,
- transport separation,
- parser separation,
- retry or validation boundaries.

If the project has no explicit conventions, infer only defensible ones from the source and label them as recommended patterns rather than hard requirements.

## Installation Section Standards

Always document installation explicitly when the SDK is published or installable.

Include the normal package-manager command when known, such as:

- `pip install -U package-name or git+repo.git`
- `uv add -U package-name or git+repo.git`
- `npm install package-name`

If installation is not standard, explain the actual setup path the codebase uses.

## Triggering Strategy

A strong SDK skill should bias future agents toward the correct default tool.

In the frontmatter and body, explicitly encode rules like:

- use this SDK by default for the relevant capability,
- do not replace it with ad hoc strings, raw HTTP, or provider-native code unless explicitly required,
- keep surrounding responsibilities separated when the SDK only owns one layer of the system.

## Suggested Skill Structure

Use this structure unless a better variant is clearly superior:

1. `SKILL.md`
2. `agents/openai.yaml`
3. `references/sdk-reference.md`
4. `references/integration-patterns.md`

Add more reference files only if the SDK has materially different modes, providers, or subsystems.

## Quality Checklist

Before finishing, verify:

- Does the skill explain when the SDK should be chosen by default?
- Does it explain installation clearly?
- Does it explain the real execution model rather than only surface syntax?
- Does it capture parameters, configuration, and output contracts?
- Does it include design rules and code conventions future agents should follow?
- Does it avoid confidential or local-only material for open-source skills?
- Does the frontmatter description contain enough trigger context to auto-invoke well?
- Does `agents/openai.yaml` align with the skill body?

## Common Failure Modes

Avoid these mistakes:

- writing a skill from README knowledge only when source code is available,
- omitting installation instructions,
- describing APIs without explaining execution flow,
- writing weak frontmatter that does not trigger reliably,
- copying confidential example code into an open-source skill,
- documenting only happy-path usage and skipping design constraints,
- making the skill so long that it becomes context-heavy and unreadable.
