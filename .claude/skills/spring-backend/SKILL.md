---
name: "spring-backend"
description: "Design, implement and review Java or Kotlin Spring Boot backends. Use for bootstrap, API contracts, DTOs, validation, persistence boundaries, transactions, external clients, version compatibility, SOLID/design quality, JSpecify/null contracts, idempotency, transaction failures and production configuration. Respect the chosen JVM language and existing architecture; do not implement React here."
---

# Spring backend engineering

Read the project profile, build/wrapper, relevant configuration, API contract and tests. Use the language already selected; a task does not authorize conversion between Java and Kotlin. For an empty project choose a documented stable compatible stack before generating code.

## Load only the relevant reference
- Spring/JVM code or design implementation/review: [design-quality.md](references/design-quality.md). Apply to affected scope; do not turn it into a whole-project checklist.
- Quality-tool setup or a changed module/contract boundary: [quality-verification.md](references/quality-verification.md).
- New build, upgrade or dependency uncertainty: [versions.md](references/versions.md).
- Java API, service and transaction changes: [api-transactions.md](references/api-transactions.md).
- Java nullability, NPE fixes or checker setup: [null-safety.md](references/null-safety.md).
- Transaction failures, audit, eligible retries or commit events: [transaction-failure-patterns.md](references/transaction-failure-patterns.md).
- Required duplicate-submit, command replay or import retry semantics: [idempotent-commands.md](references/idempotent-commands.md).
- JPA/entity/query or database changes: [postgresql-migrations](../postgresql-migrations/SKILL.md), including its JPA reference only for JPA work.
- Kotlin-specific code or a language decision: [kotlin.md](references/kotlin.md).
- HTTP integration, timeouts, retries and observability: [integrations.md](references/integrations.md).

- New/changed Spring endpoint, authentication, authorization, session/token lifecycle or security configuration: [application-security](../application-security/SKILL.md). Load its shared Spring Security standard and only the additional references relevant to that credential model.

## Implementation
1. Derive the contract and failure modes before classes. Group code by a meaningful domain/module. Avoid empty layers or an interface per class.
2. Keep HTTP DTOs distinct from persistence entities. Validate untrusted fields and fail with stable, sanitized errors. Use constructor injection and explicit boundaries.
3. Resolve identity and owner/tenant scope server-side. Never trust a client-provided owner ID as authorization. Read the application-security and postgresql-migrations skills when those boundaries are touched.
4. Put a transaction around the atomic business operation, not around a remote call or view rendering. Verify proxy participation, rollback behavior and concurrent writes.
5. Keep domain computation deterministic where practical: pass rules, clock/time and inputs; load database data in the application boundary.
6. Avoid speculative microservices, reactive code, caching and generic frameworks. Justify abstractions by actual variants and ownership.
7. Implement relevant regression, API and persistence tests; verify compilation against the chosen dependency set. Read test-verification for the evidence contract. Apply design-quality to implementation and self-review; establish meaningful architecture checks when a protected boundary exists.

Report behavior and key mechanism, material design decisions/exceptions, actual checks, unverified assumptions and required independent review. Use the design-quality review contract; avoid generic SOLID compliance claims. Do not call a successful compilation full behavioral verification.
