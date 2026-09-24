# Prompt examples

These examples are starting points. Adapt acceptance criteria and project-specific decisions to the actual application.

The goal is to give Claude Code enough context to make a bounded, reviewable change without loading every agent and skill.

## New Spring Boot endpoint

Use for a normal backend feature with moderate risk.

```text
Read CLAUDE.md, docs/project-profile.md and only the relevant skills.

Use the implementer agent.

Goal:
Add GET /api/profile for the authenticated user.

Acceptance criteria:
- return the current user's profile
- derive identity from the authenticated principal
- do not accept ownerId/userId from the browser
- return 404 when no profile exists
- use the existing DTO and error-handling conventions
- add relevant integration tests

Technical constraints:
- preserve current Spring Boot architecture
- do not introduce a new service abstraction unless needed
- do not change unrelated code

After implementation:
- run relevant backend tests
- use code-reviewer for an independent read-only review
- use security-reviewer only if the change affects authorization or data exposure

Do not commit, push or deploy.
```

## New endpoint with database write

Use when creating or modifying persisted data.

```text
Read CLAUDE.md, docs/project-profile.md and relevant skills.

Use the implementer agent.

Goal:
Add POST /api/projects.

Acceptance criteria:
- authenticated users can create only their own project records
- owner identity comes from the authenticated principal, never from the request body
- validate required fields and field-length constraints
- persist through the existing repository pattern
- return the existing API error format
- add integration tests for success, validation failure and cross-user ownership attempts

Use:
- spring-backend
- postgresql-migrations only if the schema changes
- application-security because ownership is affected

After implementation:
- run relevant tests
- use code-reviewer
- use security-reviewer because object ownership is part of the change

Do not commit, push or deploy.
```

## React feature

```text
Read CLAUDE.md, docs/project-profile.md and the react-typescript skill.

Use the implementer agent.

Goal:
Add a Project List page.

Acceptance criteria:
- fetch data through the existing API client
- use TanStack Query for server state
- handle loading, empty, error and success states
- do not store server data in global client state
- keep access/refresh tokens out of React
- follow existing routing and component conventions
- add tests for user-visible behavior

Do not introduce new state-management libraries.

After implementation:
- run frontend tests
- use frontend-reviewer for an independent read-only review
- use code-reviewer if API or business contracts changed

Do not commit, push or deploy.
```

## Authentication / Keycloak / BFF change

Use HIGH-RISK workflow.

```text
Read CLAUDE.md, docs/project-profile.md and only the relevant security/backend skills.

This is a HIGH-RISK authentication change.

First use test-engineer in DESIGN mode.

Goal:
Implement server-side OAuth2/OIDC login through Spring Boot BFF and Keycloak.

Required behavior:
- Spring Boot is the confidential OAuth2 client
- use Authorization Code flow with PKCE where supported by the selected configuration
- React/browser must never receive access or refresh tokens
- browser receives only the application session cookie
- CSRF protection remains enabled for cookie-authenticated state-changing requests
- identity is based on verified issuer + subject
- logout invalidates the local application session
- no custom refresh endpoint or token scheduler unless a real downstream user-token requirement exists

Ask test-engineer to design:
- successful login
- unauthenticated access
- CSRF failure
- logout
- invalid/expired session behavior
- relevant real OIDC/browser checks

Then use implementer.

After implementation:
- run relevant tests
- use code-reviewer
- use security-reviewer
- use test-engineer in VERIFY mode for real protocol/browser evidence when practical

Do not commit, push or deploy.
```

## Authorization / ownership change

```text
Use HIGH-RISK workflow.

Goal:
Allow users to update their own document records only.

Acceptance criteria:
- ownership is derived server-side
- user A cannot read or modify user B's record
- authorization applies to direct lookups and list queries
- a valid session plus valid CSRF token must still not bypass ownership
- denied operations must not modify data
- tests must include cross-user negative scenarios

Use:
- application-security
- spring-backend
- postgresql-migrations if query/schema behavior changes

Run:
test-engineer DESIGN
-> implementer
-> code-reviewer
-> security-reviewer
-> test-engineer VERIFY where useful

Do not commit, push or deploy.
```

## Flyway migration

```text
Read CLAUDE.md, docs/project-profile.md and the postgresql-migrations skill.

Use the implementer agent.

Goal:
Add a new required column to an existing production table.

Before implementation:
- inspect current migrations and schema usage
- determine whether an expand/migrate/contract rollout is required
- identify locking and backfill risks

Rules:
- never edit an already-applied versioned migration
- preserve backward compatibility during rollout when required
- add constraints only when existing data can satisfy them
- add indexes only for real query patterns

After implementation:
- run migration tests against real PostgreSQL when engine semantics matter
- use code-reviewer
- use platform-reviewer
- use test-engineer VERIFY if the migration has meaningful data/locking risk

Do not run production migrations.
Do not commit, push or deploy.
```

## Bug fix

```text
Read CLAUDE.md and the relevant code only.

Use the implementer agent.

Bug:
<describe the observed behavior>

Expected:
<describe the correct behavior>

Steps:
1. reproduce the defect with a failing test when practical
2. identify the smallest root cause
3. implement the smallest fix
4. keep the regression test
5. avoid unrelated refactoring

After implementation:
- run the failing test and relevant nearby tests
- use code-reviewer for an independent review

Do not commit, push or deploy.
```

## External API integration

```text
Read CLAUDE.md, docs/project-profile.md and relevant backend/operations skills.

Use the implementer agent.

Goal:
Add an integration client for <external service>.

Acceptance criteria:
- use a dedicated typed client boundary
- configure base URL and credentials externally
- do not log secrets or full sensitive payloads
- define connect/read timeouts
- map transport errors into the application's error model
- do not add retries for non-idempotent operations unless the operation contract makes them safe
- add tests for success, timeout and upstream error mapping

Use delivery-operations if runtime/network configuration changes.

After implementation:
- run relevant tests
- use code-reviewer
- use security-reviewer if credentials, sensitive data or authentication are involved

Do not commit, push or deploy.
```

## Docker / Compose change

```text
Read CLAUDE.md, docs/project-profile.md and delivery-operations.

Use the implementer agent.

Goal:
Add a production-oriented Dockerfile for the backend.

Acceptance criteria:
- multi-stage build
- minimal runtime image
- non-root runtime user
- no secrets copied into the image
- correct signal handling
- health/readiness behavior documented
- build context minimized with .dockerignore
- keep development and production concerns separate

After implementation:
- build and run the image locally if authorized
- use platform-reviewer for an independent read-only review

Do not publish images or deploy.
```

## Code review only

```text
Use code-reviewer only.

Review this completed change against the original requirements.

Check:
- functional correctness
- null and error paths
- API contracts
- transactions
- persistence behavior
- concurrency where relevant
- ownership/authorization where relevant
- whether tests prove the important behavior
- unnecessary complexity

Do not edit code.
Do not invent findings.
Return NO_BLOCKING_FINDINGS if no blocking issue is supported by evidence.
```

## Security review only

```text
Use security-reviewer only.

Review the changed security boundary.

Check:
- authentication flow
- authorization enforcement
- object ownership
- session/cookie behavior
- CSRF/CORS
- token exposure
- secret handling
- proxy trust
- abuse controls where relevant
- negative tests and forbidden side effects

Do not edit code.
Separate CONFIRMED findings from NEEDS_VERIFICATION risks.
```

## Planning a new feature before coding

```text
Use the change-planning skill.

Feature:
<feature description>

Produce:
- acceptance criteria
- affected modules/files
- security/data risks
- schema/API impact
- relevant agents and skills
- verification plan
- LIGHT / STANDARD / HIGH-RISK classification

Do not implement anything yet.
```

## Default prompt for day-to-day development

```text
Read CLAUDE.md, the project profile and only the relevant skills.

Classify this task as LIGHT, STANDARD or HIGH-RISK.

Use the smallest appropriate workflow:
- LIGHT: implementer + relevant checks
- STANDARD: implementer + code-reviewer
- HIGH-RISK: test-engineer DESIGN -> implementer -> code-reviewer -> only the relevant specialist reviewers -> test-engineer VERIFY when useful

Do not run unrelated agents.
Do not introduce new technology without a concrete need.
Do not commit, push or deploy.
Report actual checks, skipped checks and unresolved risks.
```

## Optional domain example: financial calculation

Use only when the project actually contains authoritative financial-rule logic.

```text
Read CLAUDE.md, docs/project-profile.md and the financial-calculations skill.

This is a HIGH-RISK deterministic calculation change.

Goal:
Implement a versioned calculation rule from an approved specification.

Acceptance criteria:
- use the approved rule source and effective date
- keep calculation logic deterministic
- use exact decimal arithmetic and explicit rounding
- preserve the input and rule-version snapshot needed for reproducibility
- do not infer missing legal or regulatory values
- add independent reference cases and boundary tests

Run:
test-engineer DESIGN
-> implementer
-> code-reviewer
-> test-engineer VERIFY

Do not change expected values merely to match the implementation.
Do not commit, push or deploy.
```
