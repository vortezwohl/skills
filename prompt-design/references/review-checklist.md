# Prompt Design Review and Delivery Gate

Use this checklist after reading the methodology and before presenting a prompt as complete. A passing checklist is evidence of interface quality, not evidence that an unexecuted model will behave perfectly.

## A. Scope and Objective

- [ ] The invocation has one primary objective.
- [ ] Explicit non-goals prevent hidden multi-stage work.
- [ ] The prompt is only responsible for one local reasoning operation.
- [ ] Any required sequencing, persistence, branching, retry, or acceptance is assigned to a harness.

## B. Field Separation

- [ ] `ROLE` is a natural-language cognitive identity, not an internal component name.
- [ ] `OBJECTIVE` contains no unrelated process steps.
- [ ] Every `INSTRUCTION` item is one observable action.
- [ ] `CONSTRAINT` contains hard boundaries and protocol rules only.
- [ ] `CONTEXT` is read-only background.
- [ ] `INPUT` contains only this invocation's payload.
- [ ] Unavoidable internal terminology is explained plainly in `CONTEXT`.
- [ ] Few-shot examples are managed as Context and intentionally positioned.

## C. Canonical Rendering Order

- [ ] The prompt uses the canonical relative order: `ROLE`, `OBJECTIVE`, `INSTRUCTION`, optional `CAPABILITY`, `CONTEXT`, `INPUT`, optional `OUTPUT_LANGUAGE`, `OUTPUT_DATATYPE`, `OUTPUT_FORMAT`, `OUTPUT_EXAMPLE`, `CONSTRAINT`.
- [ ] Optional fields are omitted only when they add no information.
- [ ] `_TIMESTAMP` appears only when a selected framework generates it; it is not a generic requirement.

## D. Output and Parsing

- [ ] `OUTPUT_DATATYPE` is explicit.
- [ ] `OUTPUT_FORMAT` specifies every required key, marker, section, or grammar rule.
- [ ] `OUTPUT_EXAMPLE` is valid under the declared format.
- [ ] A parser or checker can distinguish success from failure.
- [ ] The prompt says what to do with unsupported evidence or missing information.
- [ ] The declared output prohibits unneeded prose, markdown fences, or extra keys when they would break consumers.

## E. Variables and Runtime Data

- [ ] Every `{{placeholder}}` has a declared owner and a supplied value.
- [ ] Placeholders use portable flat names.
- [ ] Sensitive or untrusted data is isolated in Context or Input rather than converted into instructions.
- [ ] Missing variables fail before the provider call.

## F. Validation

- [ ] Run `validate_prompt_structure.py` for canonical prompt documents.
- [ ] Test at least one normal input.
- [ ] Test empty or missing input where the interface permits it.
- [ ] Test invalid or incomplete input.
- [ ] Test an output that violates the format and confirm that the checker rejects it.
- [ ] Test a missing-variable path if templates are rendered dynamically.
- [ ] Record any validation that could not be performed and the risk it leaves.

## G. Python and Prompt4Py

- [ ] In Python reusable-template work, Prompt4Py was recommended unless the user selected another abstraction.
- [ ] Prompt4Py installation was explicitly approved by the user.
- [ ] Installation, if any, targets only the project virtual environment.
- [ ] Provider calls, sandboxes, validation, retries, and state transitions remain outside Prompt4Py.

## Delivery Record

Include this short record in the handoff:

```markdown
Objective:
- ...

Prompt fields and rendering order:
- ...

Runtime variables:
- ...

Output acceptance rule:
- ...

Harness responsibilities:
- ...

Validation performed:
- ...

Unverified assumptions or remaining risks:
- ...
```
