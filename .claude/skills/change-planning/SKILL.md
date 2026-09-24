---
name: "change-planning"
description: "Plan a bounded software change from requirements, existing code and constraints. Use before bootstrap, nontrivial features, bug fixes or architecture decisions. Produce acceptance criteria, risk classification, relevant skills and verification steps; do not implement merely because a plan was requested."
---

# Plan a change

Read existing project instructions, the project profile and the exact request. Distinguish planning from implementation authorization. On a new project explicitly record that application code, build commands and previous decisions may not exist.

## Workflow
1. Restate the outcome and non-goals. Reuse a valid plan rather than regenerating it in each agent.
2. Inspect the relevant system boundary: actors, ownership, inputs, outputs, persistence and failure behavior. For a bug seek a reproducer before a solution.
3. Write observable acceptance criteria. Include denied operations and missing-input behavior, not only the happy path.
4. Separate confirmed facts, reversible assumptions and blocked domain decisions. Do not invent legislation, a dependency version, an API or a benchmark. For current technical choices verify primary documentation and record the date.
5. Choose the smallest complete change and affected files/modules. Preserve existing architecture when appropriate. Justify migrations or new infrastructure with a requirement or evidence.
6. Assign a risk level using the highest relevant risk below. Name exact tests and independent reviews. Do not silently downgrade a change to avoid review.
7. Hand off requirements and expected behavior separately from implementation guesses. Do not prescribe a desired reviewer verdict.

## Risk routing (project defaults, not an industry standard)
- LIGHT: wording, isolated presentation or trivial nonbehavioral changes. One implementer and relevant checks. No synthetic test requirement for a plain text edit.
- STANDARD: normal behavior/API/UI work. Implementer with tests, deterministic checks, independent code-reviewer.
- HIGH-RISK: authentication, object authorization, migrations affecting existing data, concurrency, payments, financial rules or production exposure. Independent test design before implementation; targeted code review; security review where security is affected; platform review where migrations/runtime/observability/deployment are affected; human approval. Financial rule acceptance also requires an independent domain authority.
- If two risks overlap, combine their evidence requirements, not two full duplicate pipelines.

## Output
Return: goal; non-goals; criteria; supported/unsupported cases; assumptions/blockers; affected areas; risk and rationale; implementation sequence; checks; independent-review needs. Keep a routine plan to approximately one screen. For actual missing production-critical data, stop only the affected scope.

Use [handoff.md](references/handoff.md) when delegating or recording a larger task.
