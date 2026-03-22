# Prompt4Py Integration Patterns

## Goal

Use Prompt4Py to formalize the prompt contract, then pair it with the project's existing LLM caller and response parser.

## Standard Flow

1. Build a `GeneralTemplate`.
2. Encode the reasoning and result protocol in `output_dtype`, `output_format`, and `output_example`.
3. Render the prompt with all required variables.
4. Send the rendered text to the LLM client.
5. Validate that required markers exist in the raw output.
6. Extract the tagged sections.
7. Parse the final payload into the expected datatype.

## COT Wrapper Pattern

A strong generic pattern is:

```text
[COT]
{reasoning content}
[RESULT]
{machine-readable or plain final output}
```

Why this works well:

- The reasoning block is clearly separated from the deliverable block.
- Parsers can split on stable tags.
- Prompt4Py can document the contract without knowing anything about the LLM transport.

## Recommended Template Shape

```python
template.output_dtype = "plaintext ([COT]) + json ([RESULT])"
template.output_format = """
[COT]
{structured reasoning}
[RESULT]
{
  "field_a": "...",
  "field_b": "..."
}
"""
template.output_example = """
[COT]
{reasoning summary}
[RESULT]
{
  "field_a": "demo",
  "field_b": "demo"
}
"""
template.constraint = [
    "(mandatory) Output exactly one [RESULT] block.",
    "(mandatory) The JSON object must be syntactically valid.",
    "(important) Do not include markdown fences.",
    "(recommended) Prefer stable wording for marker lines across retries."
]
```

## Parser Guidance

Keep parser logic separate from Prompt4Py and implement it with these rules:

- Fail fast if the declared result marker is missing.
- Trim wrapper braces or whitespace only when the protocol explicitly allows it.
- Parse only the final payload block into JSON or another structured type.
- Log or store the reasoning block separately when needed for debugging.

## Constraint Design

Use `constraint` as a list to declare protocol-critical guarantees. Keep priority tags in `constraint`, for example:

- `(mandatory) Output exactly one [RESULT] block.`
- `(mandatory) Do not include markdown fences.`
- `(mandatory) The JSON object must be syntactically valid.`
- `(important) Keep [COT] concise but complete.`
- `(recommended) Prefer stable wording for marker lines across retries.`

Do not use thinking or memory tags in `constraint`.

## Common Mistakes

- Declaring a schema in prose but not in `output_format`.
- Asking for JSON but not providing an example.
- Mixing parser logic into prompt-rendering code.
- Using ambiguous markers that can appear naturally in the generated content.

Choose unique markers and keep them stable across prompt and parser code.
