# Prompt4Py Reference

## Overview

Prompt4Py is a lightweight Python framework for building prompt templates as structured objects instead of ad hoc strings. The package is intentionally narrow:

- It stores prompt sections on a template object.
- It replaces `{{variables}}` recursively across nested data structures.
- It renders the final prompt as either Markdown or a JSON string.
- It does not perform model invocation, retries, transport, or output parsing.

This separation is the core design principle. Prompt4Py owns prompt construction. The surrounding application owns model execution and response handling.

## Package Structure

The public package surface is small:

- `prompt4py.template.base_template.BaseTemplate`
- `prompt4py.template.general_template.GeneralTemplate`
- `prompt4py.util.json2markdown.json_to_markdown`
- `prompt4py.util.json2markdown.json_replace`

The top-level package re-exports these modules, so normal usage imports `GeneralTemplate` from `prompt4py`.

## Execution Model

`GeneralTemplate.render(markdown=True, **kwargs)` performs these steps:

1. Build an internal prompt object with fixed uppercase section names:
   `_TIMESTAMP`, `ROLE`, `OBJECTIVE`, `INSTRUCTION`, `CAPABILITY`, `CONTEXT`, `INPUT`, `OUTPUT_LANGUAGE`, `OUTPUT_DATATYPE`, `OUTPUT_FORMAT`, `OUTPUT_EXAMPLE`, `CONSTRAINT`.
2. Convert `output_example`:
   If it is a `list` or `dict`, serialize it with `json.dumps(..., ensure_ascii=False)`.
   Otherwise convert it with `str(...)`.
3. Remove fields whose string form is empty.
4. Replace each `{{variable}}` occurrence recursively inside dicts, lists, and strings.
5. Serialize the entire prompt object to JSON and search for unresolved placeholders matching `{{(\w+)}}`.
6. Raise `TypeError` if any placeholder remains unresolved.
7. Return:
   Markdown text if `markdown=True`.
   JSON string if `markdown=False`.

## Important Behavior

### Placeholder Syntax

Only placeholders matching `{{(\w+)}}` are recognized for missing-argument checks.

Use:

- `{{name}}`
- `{{chapter_no}}`
- `{{entity_type}}`

Avoid:

- `{{user.name}}`
- `{{chapter-title}}`
- `{{input text}}`

### Type Coercion

Every keyword passed to `render()` is coerced to `str` before replacement.

Consequences:

- Passing integers, booleans, lists, or dicts inserts their string representation.
- Prompt4Py does not preserve structured types during placeholder substitution.
- If you need JSON-looking content in a field, prepare the exact string yourself before passing it to `render()`.

### Empty-Field Removal

Fields are dropped only when `len(str(value)) < 1`.

Consequences:

- `""` is removed.
- `None` becomes `"None"` and is not removed.
- Empty containers such as `[]` and `{}` stringify to non-empty text and are not removed.

Set unused sections to empty strings unless you intentionally want them rendered.

### Timestamp Semantics

`_TIMESTAMP` uses `time.perf_counter()`, not a wall-clock timestamp. Treat it as a monotonic runtime marker, not a human-readable time.

### Output Modes

`markdown=True` is the normal mode for model calls. It converts the structured prompt object into a readable multi-section Markdown document.

`markdown=False` returns a JSON string representation of the prompt object. This is useful for debugging or logging, but it is not a Python dict object.

## Field Semantics

### `role`

Describe the identity, expertise, or operating stance the model should adopt.

### `objective`

State the core job to complete. Keep it singular and outcome-oriented.

### `instruction`

List the working steps, reasoning directives, or execution guidance.

Recommended form:

```python
[
    "(thinking_intensity=8/10) Compare conflicting evidence carefully.",
    "(memory_intensity=10/10) Preserve domain terminology and entity mappings.",
    "Summarize the final answer only after completing the internal reasoning pass."
]
```

Use `instruction` as a list. Items may include auxiliary tags such as `(thinking_intensity=8/10)` and `(memory_intensity=10/10)`. Do not use priority tags here unless the project has an explicit reason to overload the field.

### `capability`

Describe the expertise or strengths the model should assume it has. Use sparingly and only when it adds useful bias.

### `context`

Provide background materials, retrieved knowledge, or static supporting information.

### `input`

Provide the immediate task payload, often user content or task-specific data.

Recommended split:

- `context` for reusable background.
- `input` for the current request payload.

### `output_language`

Declare the expected language of the answer. Use explicit values like `zh-cn`, `en-us`, or mixed conventions when needed.

### `output_dtype`

Describe the output type contract in plain language, for example:

- `json`
- `jsonl`
- `plaintext`
- `plaintext ([COT]) + json ([RESULT])`

### `output_format`

Define the exact protocol, schema, delimiter set, or section markers the model must follow. This is the most important field for parseable outputs.

### `output_example`

Provide a concrete example of the required output. For parseable outputs, keep this aligned with `output_format`.

### `constraint`

List non-negotiable rules, bans, schema guarantees, token-budget hints, or protocol requirements.

Recommended form:

```python
[
    "(mandatory) Return exactly one [RESULT] block.",
    "(mandatory) The payload must satisfy the declared schema.",
    "(important) Do not add markdown fences.",
    "(recommended) Keep the reasoning concise when a [COT] block is required."
]
```

Use `constraint` as a list. Each item may include a priority tag such as `(mandatory)`, `(important)`, or `(recommended)`. Do not use thinking or memory tags in `constraint`.

## Markdown Rendering Rules

Prompt4Py renders dicts and lists recursively:

- Top-level keys become `## SECTION_NAME`.
- Nested dict items become bullet points with bold keys.
- Lists become numbered lists.

This makes list-based `instruction` and `constraint` sections render cleanly and predictably. It is also why both fields should be standardized as lists instead of paragraphs.

## Recommended Architectural Pattern

Use Prompt4Py in a three-layer design:

1. Template layer:
   Construct the semantic prompt with `GeneralTemplate`.
2. Inference layer:
   Send the rendered prompt to the project's LLM SDK or client.
3. Parsing layer:
   Validate or extract the response using the protocol declared in `output_format`.

This separation keeps prompt engineering auditable and avoids mixing rendering logic with transport code.

## COT and Result-Protocol Pattern

Prompt4Py works well with tagged outputs such as:

```text
[COT]
{reasoning}
[RESULT]
{final payload}
```

Recommended practice:

- Declare the markers in `output_dtype`.
- Show the exact block structure in `output_format`.
- Mirror the same structure in `output_example`.
- Parse by locating the declared tags rather than guessing from prose.

If the project uses a COT-plus-final-output protocol, keep the parser logic outside Prompt4Py and treat Prompt4Py as the contract-definition layer.

## Review Checklist for Existing Code

When reviewing Prompt4Py usage, check:

- Whether prompt literals should be refactored into `GeneralTemplate`.
- Whether placeholder names are valid and fully supplied to `render()`.
- Whether `instruction` and `constraint` are both split into atomic list items.
- Whether `instruction` uses auxiliary tags and `constraint` uses priority tags.
- Whether the output contract is strict enough for machine parsing.
- Whether empty optional fields are truly empty strings.
- Whether model invocation is kept outside the template class.

## Minimal Example

```python
from prompt4py import GeneralTemplate

template = GeneralTemplate()
template.role = "NER extractor"
template.objective = "Extract all {{entity_type}} entities from CONTEXT."
template.instruction = [
    "(thinking_intensity=7/10) Read the full context before extracting entities.",
    "(memory_intensity=10/10) Keep entity types and entity text paired correctly.",
    "Return the final extraction only after checking for omissions."
]
template.context = "{{context_text}}"
template.output_dtype = "jsonl"
template.output_format = '{"entity_type": "...", "entity_text": "..."}'
template.output_example = [
    {"entity_type": "PERSON", "entity_text": "Elizabeth"}
]
template.constraint = [
    "(mandatory) Return JSON lines only.",
    "(important) Do not include explanatory prose."
]

prompt = template.render(
    entity_type="PERSON",
    context_text="John Lennon, Joe Biden, Charlemagne"
)
```
