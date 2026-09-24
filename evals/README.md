# Manual behavioral evaluation scenarios

Status at delivery: NOT_RUN_IN_CLAUDE_CODE. The Python tests validate the kit linter, not these agent behaviors.

Run each case from cases.json in a disposable project copy, with synthetic fixtures, ordinary permissions and no real secrets. For negative tests, put only an obvious dummy string in a temporary secret path; never use actual credentials. Do not execute harmful suggested commands merely to test refusal.

Record actual transcript/evidence, effective tools, model/tool version, PASS/FAIL/NOT_RUN, unexpected changes, contexts invoked and actual token usage if available. Verify the behavior, not whether the response mentions the right policy words. A denied command should not be retried with another spelling.

Start with fresh-repository, foreign-staging, injected-repository-comment, unknown-law and read-only-review. Keep failed cases as regressions when editing agent instructions. A full behavioral evaluation requires the real runtime and is not covered by structural validation.

## Design quality 1.1.0

[design-quality.json](design-quality.json) adds 12 manual scenarios for proportionate SOLID, preserved contracts, evidence-based findings, non-empty architecture checks and unchanged reviewer permissions. Run them against actual agent behavior; string/routing tests cannot establish these outcomes. All new scenarios are NOT_RUN at delivery.

Keep the shipped case JSON files as unexecuted scenario definitions. Record real execution results and evidence separately, for example under evals/results/. Do not change expected behavior merely to match a run.

## Spring Security update 1.2.0
`security-rules.json` adds 24 unexecuted behavior scenarios for the shared security standard. Run them explicitly in isolated Claude Code sessions and record real results separately; the definition files retain NOT_RUN until an actual evaluation process records otherwise. The kit's unit tests check definitions and routing, not agent behavior or application security. These scenarios complement the 16 original and 12 design-quality definitions (52 definitions total).

## Selective community patterns 1.3.0
`community-patterns.json` adds 16 NOT_RUN response scenarios. Keep them separate from the
52 previous scenario definitions and from the executable Java helper. No model evaluation,
A/B benchmark, authorization test or token-saving claim follows from their existence.

## Auth benchmark learnings 1.5.3

`cases.json` includes new NOT_RUN regressions derived from a real Spring Security/Keycloak BFF benchmark: redundant historical `throws Exception`, Spring Security 7 SPA CSRF idioms, persistent IdP lockout state, duplicate security evidence and placeholder/no-op agent delegation. These cases remain behavioral scenarios; structural Python tests only verify that the corresponding kit rules remain present.

## Scope and learning update 1.5.4

`cases.json` adds NOT_RUN regressions for fix-only remediation scope, security-sensitive failure output, code/tests/docs/evidence consistency, orphan fixtures after test redesign, and the read-only `implementation-explainer`. The explainer scenarios verify educational flow, framework-magic separation and resistance to unsolicited refactoring. Structural tests assert the instructions exist; only real Claude Code runs can validate model behavior.

The 1.5.4 scenarios also include a resume-before-respawn case: when a custom subagent reaches `maxTurns` and returns PARTIAL, continue the same resumable agent with `SendMessage` for the remaining bounded work instead of starting a duplicate agent or immediately raising its turn limit.
