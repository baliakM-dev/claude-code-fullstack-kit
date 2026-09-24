---
name: "evidence-review"
description: "Independently review a bounded code change for functional correctness, null safety, transactions, concurrency, contracts, ownership and maintainability. Use for code review or verification of reported defects, including relevant callers and configuration outside a diff. Report evidence and confidence without rewriting code."
---

# Evidence-based source review

Read the original task, acceptance criteria, scope and baseline/current manifest. Independently inspect actual code and tests. Do not inherit an implementer's conclusion. On a new project include untracked files and the empty baseline; do not claim there are no changes because git diff is empty.

## Review path
1. Establish relevant expected behavior from the contract, not the current code. Identify what this change can break.
2. Trace request/input to service, persistence/integration, output and side effects. Follow related callers, configuration and invariants outside the diff only where relevant.
3. Check null/empty/partial inputs, validation, error mapping, transaction boundaries, race conditions, idempotency, ownership and API compatibility as applicable.
4. Examine tests: do they assert the independent behavior, cover important failures and actually exercise the mechanism? A mock interaction is not proof of a database or OIDC invariant.
5. Preserve correct design. Distinguish a reachable defect from a hypothetical risk or a preferred style. Do not invent a need for SOLID abstractions, DTO layers or new frameworks.
6. Require evidence before changing a previously valid solution. When a concern is disproved, explicitly recommend keeping the code.

For Spring/JVM code or design changes, load [spring-backend](../spring-backend/SKILL.md) and its required design-quality reference. This is the single shared standard; do not create another SOLID checklist. Inspect the relevant design decisions, contracts and meaningful architecture-test evidence, keeping optional preferences non-blocking.

## Findings
For each finding report ID, CONFIRMED / NEEDS_VERIFICATION / OPTIONAL, severity based on actual impact, file and verified line range, triggering scenario, violated criterion, evidence, fix direction and confidence. Do not invent line numbers, reproductions, test runs or ASVS identifiers.

A blocking finding needs a violated requirement, credible security/data risk or missing evidence required by the task. Cosmetic preferences do not block delivery. Prioritize correctness and data loss over style.

## Tool and completion boundaries
Read-only reviewers do not edit files, stage changes or execute tests. Supplied logs are external evidence, not tests run by you. If dynamic verification is required, return an exact scenario to the parent for an authorized tester.

Return NO_BLOCKING_FINDINGS / CHANGES_REQUIRED / REVIEW_INCOMPLETE, plus inspected scope, findings and unverified risk. NO_BLOCKING_FINDINGS applies only to that scope and evidence, never to all possible bugs. Re-review corrected findings and changed neighbors, not an endless whole-project loop.

## Shared security standard
For new/changed security boundaries read [application-security](../application-security/SKILL.md) and applicable references. Check rule coverage, real authorization and denial effects beyond the diff where necessary. Do not classify an untested hypothesis as a confirmed exploit or accept mocked OIDC as a protocol test. Preserve independent security review where the delivery policy requires it.
