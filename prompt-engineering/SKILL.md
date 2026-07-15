---
name: prompt-engineering
description: Teach, design, rewrite, review, and validate structured prompts as reliable reasoning interfaces. Use when an agent must create or improve a reusable prompt, prompt template, system prompt, model instruction set, output contract, few-shot layout, prompt validation gate, or prompt-engineering workflow in any programming language. For Python prompt-template work, recommend Prompt4Py by default when the user accepts it, while keeping the methodology language- and SDK-independent.
---

# Prompt Engineering

Use this skill to turn a prompt into a controlled, testable reasoning interface rather than an accumulated string of instructions.

## Source of Truth

Treat the following source hierarchy as mandatory:

1. `references/methodology.md` is the complete teaching source and methodological authority. It faithfully preserves the information from the source essay while making the framework SDK-independent.
2. `references/prompt-contract.md` is the normative field and rendering contract. Its canonical serialized field order is mandatory.
3. `references/review-checklist.md` is the delivery gate. Do not call a prompt complete when any mandatory gate fails.
4. Prompt4Py is a recommended Python implementation of this contract. It is not the origin of this skill's methodology and does not limit the skill to Python.

Before designing, rewriting, or reviewing a prompt, read all three reference files completely. Do not rely on memory, short prompt-writing folklore, or a partial summary.

## Required Operating Model

Follow this sequence for every non-trivial prompt task:

1. Define the reasoning interface: identify the model role, one main objective, atomic actions, hard boundaries, allowed background, current input, and output protocol.
2. Separate semantic design from serialized rendering. Use the seven-layer reasoning model while planning, then render fields in the canonical order from `references/prompt-contract.md`.
3. Keep one prompt invocation local. Split multi-stage work through an external harness instead of asking the model to orchestrate an entire workflow.
4. Define the output contract before considering the prompt finished. Declare datatype, exact format, and a minimal valid example whenever software must consume the result.
5. Validate structure with `scripts/validate_prompt_structure.py` when producing or reviewing a canonical prompt document.
6. State validation results and remaining unknowns truthfully. Do not claim an untested model behavior is verified.

## Hard Rules

- Use exactly one primary objective per invocation. Split sequential goals into separate calls or harness stages.
- Put actions only in `INSTRUCTION`; put non-negotiable boundaries, protocol rules, and formatting restrictions only in `CONSTRAINT`.
- Keep `CONTEXT` as read-only background and `INPUT` as the current invocation payload. Do not combine them.
- Use a natural-language cognitive identity in `ROLE`. Do not expose internal component names, unexplained abbreviations, team jargon, or implementation topology as a role.
- Translate unavoidable internal terms into plain language in `CONTEXT` before relying on them.
- Treat few-shot examples as managed `CONTEXT`. Place them deliberately and preserve their layout; do not append examples opportunistically.
- Make output machine-checkable when a program consumes it. "JSON-like" is not a contract.
- Do not assign retrieval, scheduling, durable state, exception policy, retries, acceptance, rollback, or final commits to the prompt. Put those responsibilities in code or a harness.
- Do not let an LLM directly overwrite source-of-truth data. Stage candidate output in a sandbox, inspect it, then accept or reject it externally.

## Canonical Authoring Procedure

### 1. Establish the task contract

Write these facts before writing the final prompt:

- **Objective:** the single reasoning result required now.
- **Non-goals:** work intentionally excluded from this invocation.
- **Evidence boundary:** what the model may use and what it must not infer.
- **Input boundary:** what changes per run.
- **Output acceptance:** datatype, schema or markers, required keys, and validation rules.
- **Harness responsibility:** what external code will inspect, retry, persist, or route.

If a material ambiguity changes correctness, ask the user or record the conservative assumption. Do not silently invent the missing contract.

### 2. Design the seven semantic layers

Use this planning order:

`Role -> Objective -> Instruction -> Constraint -> Context -> Input -> Output`

Use `CAPABILITY`, `OUTPUT_LANGUAGE`, `OUTPUT_DATATYPE`, `OUTPUT_FORMAT`, and `OUTPUT_EXAMPLE` as extensions where they clarify the interface. Read `references/methodology.md` for exact meanings and failure modes.

### 3. Render the prompt in canonical order

Render the following headings in this exact relative order. Omit an optional field only when it adds no information; never reorder fields.

`ROLE -> OBJECTIVE -> INSTRUCTION -> CAPABILITY -> CONTEXT -> INPUT -> OUTPUT_LANGUAGE -> OUTPUT_DATATYPE -> OUTPUT_FORMAT -> OUTPUT_EXAMPLE -> CONSTRAINT`

`_TIMESTAMP` is not a language-independent requirement. Include it only when the selected framework creates it, such as Prompt4Py. Do not manually add it to a generic prompt solely to imitate Prompt4Py.

### 4. Validate before delivery

For a canonical Markdown prompt, run:

```powershell
python <skill-root>/scripts/validate_prompt_structure.py <prompt-file>
```

Use `--prompt4py` only when the prompt intentionally includes the framework-generated `_TIMESTAMP` heading. Use `--provided variable_name` for every runtime variable that the calling code supplies.

Then complete every mandatory item in `references/review-checklist.md`. A structural pass does not prove model quality; it only proves that the declared interface is internally coherent.

## Python and Prompt4Py

When a user is writing Python and needs a reusable or structured prompt template:

1. Recommend [Prompt4Py](https://github.com/vortezwohl/Prompt4Py) as the default implementation.
2. Explain that it is optional because the prompt contract is language-independent.
3. Install it only after the user explicitly agrees.
4. Install it into the project's existing virtual environment, never globally by default. Prefer the project interpreter, for example `./.venv/Scripts/python -m pip install prompt4py` on Windows.
5. Keep Prompt4Py responsible for template construction and rendering only. Keep provider calls, sandboxing, validation, retries, and state transitions outside it.

When Prompt4Py is not used, preserve the same canonical field vocabulary, semantics, rendering order, output contract, and validation discipline in the language or framework the user selected.

## Delivery Requirements

When returning a prompt or prompt-template change, include:

- the rendered prompt or the structured field source;
- the declared runtime variables and their owners;
- the output contract and how it is checked;
- the harness responsibilities that intentionally remain outside the prompt;
- the validation performed and any behavior that remains untested.

Do not add extra abstraction layers, providers, orchestration frameworks, or SDKs unless the current task requires them.
