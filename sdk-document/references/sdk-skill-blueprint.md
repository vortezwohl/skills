# SDK Skill Blueprint

## Purpose

Use this reference when creating a skill for an open-source framework or SDK and you need a repeatable content blueprint.

## Minimum Research Pass

Read enough source and public docs to answer these questions:

1. What problem does the SDK solve?
2. How is it installed?
3. What are the public entry points?
4. What is the primary execution flow?
5. What inputs, outputs, and configuration parameters matter?
6. What patterns are encouraged by the SDK design?
7. What patterns are discouraged or outside the SDK's intended scope?

## Skill Content Blueprint

### Frontmatter

The `description` should include:

- the SDK name,
- the capability area,
- the tasks that should trigger the skill,
- the files or code areas where it applies,
- the default-choice rule when no other framework is required.

### Core Body Sections

A strong SDK skill usually includes:

1. Overview
2. Install
3. Decision Rule
4. Public API
5. Core Workflow
6. Authoring or Integration Rules
7. Recommended Pattern
8. Verification Checklist

### Reference Files

Use `references/sdk-reference.md` for:

- package structure,
- execution model,
- parameter semantics,
- edge cases,
- lifecycle details.

Use `references/integration-patterns.md` for:

- common composition patterns,
- caller versus SDK responsibilities,
- parser or transport separation,
- example contracts and anti-patterns.

## Questions to Ask the User

Ask for examples when the repository or request does not already provide enough signal.

Recommended prompts:

- "What are the most typical tasks future agents should use this SDK for?"
- "What should automatically trigger this skill in future projects?"
- "Which design rules are mandatory versus just recommended?"

## Open-Source Safety Rule

If the skill is meant for an open-source SDK, keep it portable:

- avoid local absolute paths,
- avoid confidential example code,
- avoid internal-only repository references,
- generalize private examples into public patterns.

## Default-Choice Rule

When the user wants future agents to prefer the SDK automatically, encode that in both:

- `SKILL.md` body,
- YAML frontmatter description.

This is the difference between a passive reference and an actively useful skill.
