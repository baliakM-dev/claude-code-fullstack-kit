---
name: "test-verification"
description: "Design behavioral tests and verify changes with real evidence. Use for regression tests, acceptance scenarios, database and HTTP integration, browser/OIDC flows, concurrency and financial-rule checks. Distinguish test design, execution, independent review and unexecuted checks."
---

# Test design and evidence

Read the original requirements and independently approved expected behavior before mirroring implementation details. In a bug fix reproduce the failure first when practical. A test must be able to fail for the relevant defect.

## Select the evidence
- Domain behavior: deterministic unit tests including absent/invalid inputs and boundaries.
- API: status, payload, validation, unauthenticated/forbidden behavior, ownership and side effects.
- Persistence: real PostgreSQL when correctness depends on SQL, constraints, transaction isolation, migrations or concurrency. Align Testcontainers lifecycle with application context caching.
- Browser: important user interactions, loading/errors, session expiry and accessibility. Real OIDC/proxy integration is separate from mocked authentication.
  For React component/network evidence use [frontend testing](../react-typescript/references/testing-accessibility.md) when applicable.
- Financial: independent reference cases, period and rounding boundaries, missing data, invariant checks, reproducibility and corrections. Do not produce expected values by calling the same calculator under test.
- Concurrency: deliberately coordinated overlapping actions, not two sequential calls or arbitrary sleeps.
- Spring/JVM module boundaries or quality-tool setup: use [quality-verification.md](../spring-backend/references/quality-verification.md). Verify real class selection, positive/negative rule fixtures and actual test discovery; an empty selection is not a passing architecture guarantee.

- Security-relevant routes, sessions, identity, ownership or exposure: [security-verification](../application-security/references/security-verification.md). Select affected case IDs with positive controls; verify real denial side effects without disabling production security.

## Spring/Data details on demand
For JPA, nullness tools, commit/retry/audit behavior and duplicate commands, load
[spring-data-evidence.md](references/spring-data-evidence.md). To understand the corresponding
contracts load [JPA](../postgresql-migrations/references/jpa-modeling.md),
[null-safety](../spring-backend/references/null-safety.md),
[idempotency](../spring-backend/references/idempotent-commands.md) or
[transaction failure patterns](../spring-backend/references/transaction-failure-patterns.md)
only for the affected scenario. Do not treat reference examples as an already-tested application.

## Execute honestly
1. Inspect the command and invoked code before running. Use synthetic data in a permitted local/test environment. A test runner can execute arbitrary code and network requests.
2. Establish criteria and fixtures. Keep test data/time/order isolated. Integration tests that mutate external/provider state (for example IdP lockout counters, passwords, sessions, realm/client configuration or external resources) must use disposable state, a unique per-run resource, or explicit setup plus guaranteed cleanup/reset. A successful test must be immediately repeatable without manual repair of a shared development environment. Use explicit clocks and synchronization where needed; avoid arbitrary sleeps unless real elapsed time is itself part of an external system contract and no controllable alternative exists, and document that reason.
3. Run the smallest relevant checks, then any required wider regression. Prove one material behavior once at the lowest reliable layer; repeat it at another layer only when that layer proves a distinct mechanism (for example filter-chain behavior vs real server cookie/proxy behavior vs real OIDC protocol behavior). Capture exact command, directory, exit code and relevant sanitized output.
4. For a failed test distinguish product defect, test defect and environment failure using evidence. Do not delete it or relax assertions as a shortcut.
5. Report skipped checks as NOT_RUN with reason and residual risk. A zero exit status with zero relevant tests is not evidence for the scenario.
6. Coverage identifies gaps; no universal percentage proves correctness. Static analysis, dependency/image scans and selective mutation testing supplement behavior tests.

## Independent roles
An implementer still writes and executes relevant tests. Use an independent tester for high-risk case design or additional verification, not to excuse untested implementation. A tester does not fix application code without a new delegation.

Return [evidence-template.md](references/evidence-template.md) for nontrivial tasks. If no runtime is available return a usable scenario/command plan with NOT_RUN, not a fabricated success.

Primary source: https://docs.spring.io/spring-boot/reference/testing/testcontainers.html