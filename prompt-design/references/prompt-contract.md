# Canonical Prompt Contract

## Normative Status

Use this document as the language-independent specification for prompt fields, their meaning, and their serialized order. It is compatible with Prompt4Py `GeneralTemplate`, but it does not require Prompt4Py or Python.

The methodology uses a seven-layer **semantic design order**:

`ROLE -> OBJECTIVE -> INSTRUCTION -> CONSTRAINT -> CONTEXT -> INPUT -> OUTPUT`

The final prompt uses a different **serialized rendering order**. Never confuse the two.

## Canonical Serialized Order

Render fields in this exact relative order:

1. `ROLE`
2. `OBJECTIVE`
3. `INSTRUCTION`
4. `CAPABILITY` (optional)
5. `CONTEXT`
6. `INPUT`
7. `OUTPUT_LANGUAGE` (optional)
8. `OUTPUT_DATATYPE`
9. `OUTPUT_FORMAT`
10. `OUTPUT_EXAMPLE`
11. `CONSTRAINT`

Do not move `CONSTRAINT` earlier in the final rendered prompt merely because it is fourth in the semantic design model. The final order follows Prompt4Py's `GeneralTemplate` rendering sequence.

### `_TIMESTAMP` Compatibility Rule

`_TIMESTAMP` is not part of the generic prompt-design contract. Do not require or manually insert it in non-Prompt4Py implementations. When Prompt4Py renders it automatically, it appears before the canonical fields and is permitted only as a framework feature.

## Field Semantics

| Field | Required | Meaning and rules |
| --- | --- | --- |
| `ROLE` | Yes | A natural-language identity that gives the model a stable cognitive perspective. Never use internal topology as the role. |
| `OBJECTIVE` | Yes | Exactly one primary result for this invocation. Keep workflow sequencing out of it. |
| `INSTRUCTION` | Yes | A bullet list of atomic actions. One item expresses one action. |
| `CAPABILITY` | No | The capability boundary the model is expected to apply. Use only if it clarifies the work type. |
| `CONTEXT` | Yes | Read-only evidence, retrieved material, definitions, memory summaries, and deliberately placed few-shot examples. |
| `INPUT` | Yes | The immediate question, document, or parameters for this run. |
| `OUTPUT_LANGUAGE` | No | The response language when it matters. |
| `OUTPUT_DATATYPE` | Yes | The declared result type, such as `json`, `yaml`, `markdown`, or tagged plaintext. |
| `OUTPUT_FORMAT` | Yes | Exact schema, markers, key set, ordering rule, or grammar the parser expects. |
| `OUTPUT_EXAMPLE` | Yes | The shortest legal output that demonstrates the declared protocol. |
| `CONSTRAINT` | Yes | A bullet list of hard limits, forbidden behavior, required protocol rules, and formatting boundaries. |

## Canonical Markdown Form

Use this heading form for a language-neutral rendered prompt:

```markdown
# ROLE
You are a natural-language description of the required reasoning perspective.

# OBJECTIVE
Produce one clearly defined result for this invocation.

# INSTRUCTION
- Perform one atomic action.
- Perform the next atomic action.

# CAPABILITY
Optional capability boundary.

# CONTEXT
Read-only background, evidence, definitions, and intentionally positioned examples.

# INPUT
The current invocation payload.

# OUTPUT_LANGUAGE
English

# OUTPUT_DATATYPE
json

# OUTPUT_FORMAT
{
  "answer": "string",
  "evidence": ["string"],
  "risk_flags": ["string"]
}

# OUTPUT_EXAMPLE
{"answer":"...","evidence":["source fact"],"risk_flags":[]}

# CONSTRAINT
- Do not use unsupported claims.
- Return only the declared JSON object.
```

Omit only optional headings with no useful information. Preserve the order of all remaining headings.

## Variable Contract

- Use explicit placeholders such as `{{context_text}}` and `{{task_input}}`.
- Keep placeholder names flat and portable. Prefer letters, digits, and underscores.
- Document the owner of every variable: caller, retrieval layer, state store, or harness.
- Verify that every placeholder is supplied before provider invocation.
- Never use a placeholder as a substitute for an undocumented instruction or hidden business rule.

## Output Contract Rules

For any program-consumed answer:

1. Declare a datatype.
2. Declare the exact structure or markers.
3. Provide one legal example.
4. Define the parser or checker that decides acceptance.
5. Reject extra keys, missing keys, malformed markers, or invalid types according to the stated contract.

If the expected answer is human-readable prose, still state its format, required sections, language, and forbidden additions.

## Prompt4Py Mapping

| Generic contract | Prompt4Py attribute | Notes |
| --- | --- | --- |
| `ROLE` | `template.role` | Natural identity |
| `OBJECTIVE` | `template.objective` | One main goal |
| `INSTRUCTION` | `template.instruction` | Use a list of atomic directives |
| `CAPABILITY` | `template.capability` | Optional |
| `CONTEXT` | `template.context` | Read-only background |
| `INPUT` | `template.input` | Current payload |
| `OUTPUT_LANGUAGE` | `template.output_language` | Optional |
| `OUTPUT_DATATYPE` | `template.output_dtype` | Type declaration |
| `OUTPUT_FORMAT` | `template.output_format` | Parse-critical structure |
| `OUTPUT_EXAMPLE` | `template.output_example` | Legal protocol sample |
| `CONSTRAINT` | `template.constraint` | Use a list of hard rules |

Use `template.render(markdown=True, **variables)` before provider invocation. Prompt4Py ends at rendering; keep provider calls and workflow control outside it.

## Python Adoption Rule

Recommend Prompt4Py for reusable Python prompt templates. Do not install it without the user's explicit agreement. If the user agrees, install only through the project's virtual-environment interpreter, not the global interpreter by default.

Example Windows command after agreement:

```powershell
.\.venv\Scripts\python -m pip install prompt4py
```

If the project does not have a virtual environment, ask whether to create or use one before installation. Do not silently alter the user's environment.
