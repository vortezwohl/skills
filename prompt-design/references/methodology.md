# Structured Prompt Design Methodology

## Purpose and Fidelity

This reference is the complete teaching layer for `prompt-design`. It preserves the source essay's engineering claims, tables, examples, implementation model, and anti-patterns in an SDK-independent form. The source essay presents Prompt4Py as its practical center; this skill keeps that historical and technical context while generalizing the method so agents can apply it in any language.

Source essay: [Structured Prompt Design Methodology: From Writing a Prompt to Building a Controlled Text System](https://vortezwohl.github.io/prompt-engineering/2026/05/23/%E7%BB%93%E6%9E%84%E5%8C%96%E6%8F%90%E7%A4%BA%E8%AF%8D%E8%AE%BE%E8%AE%A1%E6%96%B9%E6%B3%95%E8%AE%BA.html), published May 23, 2026.

## 1. Define a Reasoning Interface, Not a Clever Sentence

Prompt engineering fails when it is treated as a collection of text tricks. One-off prompts can survive that approach, but real tasks become unstable as objectives change, context grows, software consumes the output, and failures must be discovered and repaired.

A prompt is therefore closer to a **reasoning interface** than to a natural-language sentence. The interface declares:

- who the model is for this invocation;
- what this invocation must accomplish;
- what material the model may rely on;
- what output protocol the result must obey; and
- how the surrounding system handles failure after the invocation returns.

| Treat the prompt as | Typical practice | Short-term appearance | Long-term result |
| --- | --- | --- | --- |
| A string | Keep appending sentences, rules, and examples | Fast to change | Hard to maintain, vague boundaries, difficult reuse |
| A reasoning interface | Define structured fields, then render text | Slightly slower initially | Testable, composable, inspectable, evolvable |

The goal is not merely a polished output once. The goal is a controlled text system that remains dependable as task scope, scale, validation, and retries increase.

## 2. Preserve the Source Essay's Practical Center Without Coupling the Skill

The source essay argues that a stable implementation interface prevents methodology from collapsing into intuition. Prompt4Py demonstrates the key move: declare fields and render them instead of concatenating strings.

This skill preserves that engineering lesson:

- A prompt must answer role, objective, actions, boundaries, context, current input, and output contract before invocation.
- Structure must exist independently of a provider SDK.
- A concrete implementation can enforce the structure and make it reusable.

For Python, Prompt4Py is the preferred concrete implementation because its `GeneralTemplate` already exposes the relevant fields and a deterministic rendering order. For other languages, use an equivalent structured representation and preserve the same contract.

A representative structured template has a natural role, one objective, a list of actions, a separate list of boundaries, capability, background context, current input, response language, data type, exact output shape, and an optional minimal legal example. Rendering happens after variables are supplied.

## 3. Use the Seven-Layer Core Skeleton

The seven-layer model defines the prompt's core responsibility boundary. It is a core skeleton, not the complete property list of any one SDK.

| Layer | Question answered | Design requirement |
| --- | --- | --- |
| Role | Who is the model now? | Use only a natural cognitive identity. Do not use internal module names or implementation details. |
| Objective | What must this invocation accomplish? | State one goal. Do not mix process explanation or unrelated background into it. |
| Instruction | How should the model do the work? | Use atomic instructions; one action per item. |
| Constraint | What must never be violated? | Use only hard rules, protocols, and format boundaries. |
| Context | What background may the model rely on? | Put read-only knowledge, retrieval results, and memory summaries here; do not put the current task instructions here. |
| Input | What is the immediate payload for this run? | Put the current question, document, or parameters here; do not mix them with background. |
| Output | What must the result look like? | Define a datatype, a format skeleton, and a legal example together. |

Use this order for semantic reasoning and authoring. The serialized order is intentionally different and is governed by `prompt-contract.md`.

## 4. Use Extension Fields Deliberately

The seven layers are not the whole structured prompt. The following extension fields describe capability and response protocol.

| Field | Problem it solves | Use it explicitly when |
| --- | --- | --- |
| `CAPABILITY` | Declares the capability boundary expected from the model | The task needs to emphasize the type of work the model is performing |
| `OUTPUT_DATATYPE` | Declares the data type | Software consumes the result |
| `OUTPUT_FORMAT` | Declares schema, markers, or protocol | Output must be parsed strictly |
| `OUTPUT_EXAMPLE` | Shows the shortest legal sample | The protocol could be ambiguous |
| `OUTPUT_LANGUAGE` | Declares response language | The system is multilingual or language switching matters |

These fields are not decoration. They turn an intention into an inspectable interface.

## 5. Apply the Seven Operational Rules

1. **Write only a natural identity in Role.** Do not write internal system topology.
2. **Give Objective one primary goal.** Do not compress multiple workflow stages into a single sentence.
3. **Separate Instruction from Constraint.** Instructions are actions; constraints are boundaries.
4. **Separate Context from Input.** Background and the current invocation payload must not share one block.
5. **Declare datatype, format, and example for Output.** Treat all three as the minimum output protocol.
6. **Use the prompt only to define a reasoning interface.** Do not use it to orchestrate end-to-end business work.
7. **Do not force internal terms on the model.** If they are necessary, explain them in plain language inside Context.

## 6. Make Each Layer Operational

### Role: give an executable cognitive perspective

Role is not an architecture disclosure mechanism. A label such as "chapter-conflict-detector V3 submodule" supplies noise rather than a usable perspective. Prefer a natural identity such as "a structural editor focused on narrative contradictions."

Do not assume that an LLM shares a team's abbreviations, code names, or implicit implementation context. The prompt addresses the model's natural-language understanding, not a private team vocabulary.

### Objective: perform one reasoning task

Failures often begin when one goal combines reading materials, finding issues, proposing a plan, returning JSON, and conducting risk review. Restrict one call to one reasoning task. Let external workflow code schedule the other stages.

### Instruction and Constraint: distinguish actions from prohibitions

`INSTRUCTION` states what to do. `CONSTRAINT` states what must not happen or what protocol cannot be violated. If they are mixed, a retry mechanism cannot diagnose whether the model skipped an action or crossed a boundary.

### Context and Input: distinguish durable background from the current run

Context is the background the model may use to reason. Input is this run's immediate task object. Their separation enables caching, truncation, replacement, reuse, and local retries.

Treat few-shot demonstrations as Context. Their position is meaningful: do not insert examples arbitrarily because in-context demonstration placement has positional effects. Place and manage them deliberately.

If business terminology, abbreviations, or process code names must appear, translate each into a natural-language explanation in Context before expecting the model to reason from it.

### Output: make the protocol program-consumable

"Roughly JSON" has no engineering meaning. Explicitly declare the output datatype, required structure or markers, and a legal example. Only then can a checker or parser determine what counts as success or failure.

### Harness: keep the business loop outside the prompt

A prompt must not own retrieval, scheduling, state persistence, exception handling, or retry policy. It only defines one reasoning call. Task splitting, run order, text sandboxing, checkers, repair, acceptance, and rollback belong in system code or a harness.

## 7. Position the LLM as a Constrained Reasoning Module

An LLM is powerful but must not directly control an end-to-end task. Give it controlled input for a local cognitive operation, then let the system accept, repair, branch, or invoke another stage.

| Incorrect approach | Why it loses control | Better approach |
| --- | --- | --- |
| Give the entire task to the model | State, validation, recovery, and exceptions collapse into one generation | Split work into constrained reasoning steps |
| Let the model decide the next step | Flow becomes unpredictable, difficult to audit, and difficult to reproduce | Let the harness own scheduling and branches |
| Let the model modify the final result directly | Intermediate state contaminates the source of truth | Write to a text sandbox, inspect, then commit externally |

## 8. Build the Minimum Engineering Skeleton

The minimum architecture contains four distinct responsibilities:

1. **Structured prompt builder:** defines and renders the reasoning interface.
2. **Text sandbox:** holds source text, working notes, and staged candidate output separately.
3. **Inspector:** validates that candidate output obeys the declared contract.
4. **Harness:** decides retry, acceptance, rejection, state transition, and the next stage.

A language-neutral sandbox model is:

```text
TextSandbox
  source_text       immutable source of truth
  working_notes     isolated intermediate notes
  candidate_output  staged model result
```

The provider call remains outside the prompt builder. The important boundary is not the syntax of a template; it is the separation between prompt construction and provider invocation, sandbox management, validation, retries, and state transitions.

A minimum reasoning stage therefore works as follows:

1. Build a prompt from `task_input` and `context_text`.
2. Invoke the chosen provider outside the template library.
3. Store the response as `candidate_output` in the sandbox.
4. Parse and inspect required fields such as an answer, evidence list, and risk flags.
5. Let the harness decide whether to retry, accept, branch, or stop.

## 9. Reject the Common Anti-Patterns

| Anti-pattern | Root problem | Why it is dangerous |
| --- | --- | --- |
| Role is an internal module name | The role has no executable semantic meaning | The model receives noise instead of a cognitive perspective |
| One Objective contains many phases | Task boundary is distorted | Failures cannot be retried locally |
| Instruction and Constraint are mixed | Actions and boundaries are entangled | The system cannot tell what failed |
| Context and Input are mixed | Background and current parameters are entangled | Caching, trimming, replacement, and reuse become difficult |
| Internal terms or jargon are used directly | Private implicit context is mistaken for shared model context | The model may appear to comply while reasoning from the wrong meaning |
| The LLM controls the whole task | There is no external order layer | State, validation, and exception handling become uncontrolled |

## 10. Final Principle

Use three distinct responsibilities:

- **Structured prompt layer:** owns prompt structure and rendering.
- **Harness:** owns order, state, inspection, retries, acceptance, and recovery.
- **LLM:** performs local reasoning inside that order.

This is stricter than a long free-form prompt, but it is more stable as systems scale, tasks become complex, and validation and retries become necessary.

## Source References

1. [Prompt4Py](https://github.com/vortezwohl/Prompt4Py)
2. [Where to Show Demos in Your Prompt: A Positional Bias of In-Context Learning](https://arxiv.org/abs/2307.08257)
3. [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
4. [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
5. [Context Engineering for Coding Agents](https://www.youtube.com/watch?v=4w0a8oH0e9A)
6. [12 Factor Agents](https://github.com/humanlayer/12-factor-agents)
