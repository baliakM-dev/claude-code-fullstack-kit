# How to use the agents and skills

For copy-ready task examples, see [Prompt examples](prompt-examples.md).

This guide explains how to use the kit effectively in Claude Code without turning every task into a large multi-agent workflow.

The main principle is simple:

> Use the smallest workflow that gives enough evidence for the risk of the change.

The main Claude Code conversation should coordinate the work. Specialist agents should receive bounded tasks and return results to the main conversation. Avoid nested agent delegation and avoid running every reviewer for every change.

## Agents vs skills

Agents define **who performs a task**.

Examples:

- `implementer` writes a bounded change.
- `code-reviewer` independently reviews correctness.
- `security-reviewer` reviews security boundaries.
- `test-engineer` designs or executes behavioral tests.
- `frontend-reviewer` reviews React/TypeScript changes.
- `platform-reviewer` reviews database, Docker and operational changes.

Skills define **how that work should be done**.

Examples:

- `spring-backend` contains Spring/JVM engineering guidance.
- `react-typescript` contains frontend guidance.
- `application-security` contains security rules.
- `postgresql-migrations` contains PostgreSQL/Flyway guidance.
- `test-verification` contains testing methodology.
- `evidence-review` defines evidence-based code review.

Agents load only the skills relevant to the task. Do not preload the entire skill set for every change.

## Recommended workflow by risk

### LIGHT

Use for small, low-risk changes such as:

- copy or text changes
- simple UI adjustments
- local refactors with no contract change
- trivial configuration updates

Recommended flow:

```text
implementer
-> relevant checks
```

Example prompt:

```text
Read CLAUDE.md and only the relevant skills.

Use the implementer agent to make this small bounded change.
Run the relevant tests or checks.
Do not commit, push or deploy.
```

Do not add independent reviewers unless the change actually crosses an important boundary.

### STANDARD

Use for normal application features and bug fixes.

Examples:

- new REST endpoint
- new React feature
- ordinary persistence changes
- business logic changes without high financial/security risk

Recommended flow:

```text
implementer
-> code-reviewer
```

Example prompt:

```text
Read CLAUDE.md, the project profile and the exact task.

Use the implementer agent to implement the requested change with relevant tests.

After implementation, use the code-reviewer for an independent read-only review.
Fix only confirmed findings.
Do not commit, push or deploy.
```

### HIGH-RISK

Use when mistakes can create security, data-integrity, financial or operational impact.

Examples:

- authentication or authorization
- Keycloak/OIDC/session changes
- object ownership rules
- Flyway migrations
- concurrency or idempotency
- financial calculations
- destructive or large data changes
- production Docker/runtime changes

Recommended flow:

```text
test-engineer DESIGN
-> implementer
-> code-reviewer
-> security-reviewer and/or platform-reviewer when relevant
-> test-engineer VERIFY when dynamic evidence is useful
```

Use only the reviewers that match the actual risk.

## Using the implementer

Use `implementer` when production code, configuration or infrastructure must change.

Good task:

```text
Use the implementer agent.

Goal:
Add GET /api/profile for the authenticated user.

Acceptance criteria:
- returns the current user's profile
- derives identity from the authenticated principal
- does not accept ownerId from the browser
- returns 404 if no profile exists
- includes integration tests

Do not commit, push or deploy.
```

Avoid vague tasks such as:

```text
Improve the backend.
```

Bounded tasks produce better architecture, smaller diffs and more useful reviews.

## Using the code-reviewer

Use `code-reviewer` after meaningful implementation work.

It is intentionally read-only.

Ask it to review requirements and actual behavior, not just formatting:

```text
Use code-reviewer to independently review the completed change.

Check:
- acceptance criteria
- null and error paths
- contracts
- transaction boundaries
- ownership/authorization where relevant
- concurrency and persistence behavior
- whether tests prove the important behavior

Do not edit code.
Return only evidence-based findings.
```

A good reviewer is allowed to return `NO_BLOCKING_FINDINGS`. Do not require it to invent changes.

## Using the security-reviewer

Use `security-reviewer` when a change affects a security boundary.

Typical triggers:

- login/logout
- sessions or cookies
- OAuth2/OIDC
- Keycloak
- CSRF/CORS
- authorization
- owner/tenant checks
- secrets
- uploads
- proxy trust
- abuse protection
- sensitive-data exposure

Example:

```text
Use security-reviewer for an independent read-only review of this authentication change.

Verify:
- tokens remain server-side
- CSRF remains enforced
- cookies are configured safely
- authorization is default-deny
- proxy trust is explicit
- negative cases are covered

Do not edit files and do not claim dynamic tests were run.
```

Do not run the security reviewer for a CSS-only change.

## Using the test-engineer

The test engineer has two modes.

### DESIGN

Use before implementation for high-risk changes.

Its job is to derive independent expected behavior from requirements before seeing implementation details where practical.

Example:

```text
Use test-engineer in DESIGN mode.

From the acceptance criteria, define:
- positive scenarios
- negative scenarios
- forbidden side effects
- concurrency/security edge cases where relevant

Do not edit files or run commands.
```

This reduces the risk of writing tests that merely mirror the implementation.

### VERIFY

Use after implementation when dynamic evidence is valuable.

Example:

```text
Use test-engineer in VERIFY mode.

Implement or run only the delegated test paths.
Do not modify production code.
Separate mock evidence from real PostgreSQL or real browser/OIDC evidence.
Report actual commands and results.
```

## Using the frontend-reviewer

Use `frontend-reviewer` for non-trivial React/TypeScript changes.

It checks areas such as:

- server state vs local state
- TanStack Query usage
- Axios/API boundaries
- forms and validation
- routing
- accessibility
- error handling
- unnecessary effects or memoization
- frontend security
- test quality

Example:

```text
Use frontend-reviewer for a read-only review of this React feature.

Focus on:
- state ownership
- API/cache behavior
- form validation
- accessibility
- error states
- unnecessary abstractions
- test coverage of user-visible behavior
```

## Using the platform-reviewer

Use `platform-reviewer` when the change affects:

- PostgreSQL schema/migrations
- Flyway rollout
- Docker/Compose
- persistence and volumes
- networking
- health/readiness
- backups/restore
- Prometheus/Grafana/Loki/Tempo/OpenTelemetry
- production runtime configuration

Example:

```text
Use platform-reviewer for an independent read-only review.

Check:
- migration safety
- rollout/backfill risk
- container runtime security
- persistence
- health checks
- observability cardinality
- backup/restore implications
```

## Skills and when they matter

### `change-planning`

Use before a non-trivial feature, bug fix or architecture change when the task needs clear acceptance criteria and risk classification.

Do not use it for every tiny edit.

### `spring-backend`

Use for Java/Kotlin Spring Boot work:

- controllers and APIs
- services and transactions
- DTOs and validation
- JPA
- null safety
- idempotency
- transaction failures
- external clients
- architecture decisions

### `react-typescript`

Use for React/TypeScript work:

- components
- API clients
- TanStack Query
- React Hook Form/Zod
- routing
- accessibility
- frontend testing

### `postgresql-migrations`

Use for:

- schema design
- normalization
- indexes
- JPA modeling
- Flyway migrations
- backfills
- concurrency/data ownership

### `application-security`

Use whenever the change touches authentication, authorization, browser credentials, sessions, CSRF/CORS, secrets, uploads or exposure.

### `test-verification`

Use when designing or executing meaningful behavioral verification.

### `evidence-review`

Used by independent code review to separate confirmed defects from hypotheses and preferences.

### `delivery-operations`

Use for Docker, Compose, CI/CD, logs, health checks, observability, backups and deployment preparation.

### `financial-calculations`

Optional domain skill. Use only for deterministic financial-rule logic such as tax, insurance, reserves, cash-flow calculations, rounding and effective dates.

Do not use it for ordinary CRUD or unrelated applications.

## Example workflows

### Spring CRUD feature

```text
implementer
  -> spring-backend
  -> postgresql-migrations if schema changes
code-reviewer
```

### React feature

```text
implementer
  -> react-typescript
frontend-reviewer for non-trivial UI/state changes
code-reviewer when business/API contracts changed
```

### Authentication / Keycloak BFF

```text
test-engineer DESIGN
implementer
  -> spring-backend
  -> application-security
code-reviewer
security-reviewer
test-engineer VERIFY for real protocol/browser evidence when required
```

### Flyway migration

```text
test-engineer DESIGN when migration is risky
implementer
  -> postgresql-migrations
  -> delivery-operations when rollout is affected
code-reviewer
platform-reviewer
test-engineer VERIFY against real PostgreSQL when engine semantics matter
```

### Financial calculation

```text
test-engineer DESIGN
implementer
  -> financial-calculations
  -> spring-backend if implemented in Spring
code-reviewer
test-engineer VERIFY
```

The expected result must come from an approved rule or independent fixture, not from the implementation itself.

## Token and context efficiency

The kit is intentionally designed to avoid unnecessary agent chains.

For better results and lower context usage:

1. Give each agent a bounded task.
2. Send acceptance criteria instead of the entire conversation.
3. Load only relevant skills and references.
4. Do not ask every reviewer to inspect every change.
5. Do not run DESIGN + VERIFY for low-risk work.
6. Do not ask multiple agents to write production code in parallel.
7. Do not repeatedly rescan the whole repository.
8. Treat reviewer findings as evidence to validate, not mandatory refactoring requests.
9. Stop blind retry loops after repeated failure and gather new evidence.
10. Keep project-specific decisions in `CLAUDE.md` and the project profile, not in reusable agents.

## Project-specific defaults

The reusable kit intentionally does not decide values such as:

- session lifetime
- login lockout thresholds
- production domain names
- deployment topology
- business rules
- tax or legal constants

Put those decisions in the project's `CLAUDE.md`, project profile or task specification.

This prevents reusable skills from silently inventing product policy.

## A good default prompt

For most normal tasks:

```text
Read CLAUDE.md, the project profile and only the relevant skills.

Classify the task risk as LIGHT, STANDARD or HIGH-RISK.

Use the smallest appropriate workflow:
- LIGHT: implementer + checks
- STANDARD: implementer + code-reviewer
- HIGH-RISK: independent test design first, then implementation and only the relevant specialist reviews

Do not run unrelated agents.
Do not commit, push or deploy.
Report actual checks and unresolved risks.
```

This is usually a better starting point than explicitly invoking every agent in the repository.