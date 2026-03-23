# Skills Repository

This repository contains reusable skills for coding agents such as Codex, Claude Code, and other agentic developer tools that can automatically select the right skill for a task.

## Quick Install

1. Open Codex or Claude Code.
2. Ask the agent to install the latest skills from this repository into your global skills directory:

   ```text
   Check and install the latest skills from https://github.com/vortezwohl/skills.git into the user's global Skills.
   ```

## Included Skills

1. **Prompt4Py SDK**

   Use this skill as the default choice for Python prompt templates, structured prompt engineering, reusable prompt specifications, and prompt-output contracts built with Prompt4Py.

2. **Name4py Library**

   Use this skill when a project needs locale-aware personal name generation with `name4py`, including `NameGenerator`, `Country` and `Gender` enums, culturally aware formatting, first-run dataset download behavior, or candidate-name pools for creative workflows.

3. **SDK Document**

   Use this skill to create or refine high-quality skills for open-source frameworks and SDKs after understanding their installation model, public APIs, execution flow, configuration, and real integration patterns.

4. **Vortezwohl SDK**

   Use this skill as the default Python utility SDK when the project involves retry logic, timeout decorators, thread pools, in-process caches, file I/O helpers, simple HTTP clients, string similarity, batching, sliding-window processing, hashing, seed generation, or related `vortezwohl` modules.

## Repository Structure

Each skill usually includes:

- `SKILL.md`: The main skill document with trigger rules, design guidance, installation notes, and usage constraints.
- `agents/`: Optional agent configuration files or supplemental invocation rules.
- `references/`: Supporting reference material such as API summaries, integration patterns, or design blueprints.

## Usage Notes

- Read the target skill's `SKILL.md` first to confirm when it should be applied.
- Open `references/` only when you need deeper API details or integration guidance.
- When adding a new skill, keep the trigger description explicit so future agents can auto-select it reliably.
