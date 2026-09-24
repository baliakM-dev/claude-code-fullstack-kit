# Repository name

`claude-code-fullstack-kit`

## GitHub About

Reusable Claude Code agents and skills for secure full-stack development with Java/Spring Boot, React/TypeScript, PostgreSQL, Keycloak, Docker and modern DevOps practices.

## Short description

A reusable Claude Code development kit with universal agents, skills and workflows for implementation, testing, code review, security, frontend, database, Docker and observability.

## Suggested topics

`claude-code` `ai-agents` `developer-tools` `spring-boot` `java` `react` `typescript` `postgresql` `keycloak` `docker` `devops` `code-review` `testing` `security` `observability`

# README

## Claude Code Fullstack Kit

A reusable Claude Code development kit for building and reviewing secure, maintainable full-stack applications.

The repository contains reusable Claude Code agents, skills, engineering rules and validation workflows designed to support real software development rather than only code generation.

The goal is to use AI as an engineering assistant while keeping architecture decisions, security, testing and human review explicit.

## Main principles

* Keep agents reusable across projects.
* Prefer simple, correct solutions over unnecessary abstraction.
* Apply security by default without disabling controls to make development easier.
* Review code based on evidence instead of stylistic preference.
* Separate implementation, testing and independent review.
* Use framework-supported mechanisms before building custom infrastructure.
* Preserve existing correct code.
* Avoid introducing technologies without a concrete use case.
* Distinguish verified behaviour from assumptions.
* Keep production and development concerns separate.

## Agents

### `implementer`

Implements bounded changes using the relevant project instructions and skills.

Responsibilities include:

* minimal complete implementation
* preserving existing architecture
* running appropriate checks
* avoiding unrelated refactoring
* respecting Git safety rules
* reporting unresolved risks and required reviews

### `code-reviewer`

Performs independent evidence-based code review.

Reviews:

* functional correctness
* null handling
* contracts
* transactions
* concurrency
* persistence
* maintainability
* ownership boundaries
* regression risk

The reviewer does not change code and does not invent findings simply to produce a review.

### `security-reviewer`

Reviews authentication, authorization and application security boundaries.

Typical areas:

* Spring Security
* Keycloak / OIDC / OAuth2
* BFF architecture
* sessions and cookies
* CSRF / CORS
* object-level authorization
* secret handling
* proxy trust
* abuse protection
* security regression scenarios

### `test-engineer`

Designs behavioural tests independently from implementation and verifies changes with real evidence.

Supports:

* unit tests
* integration tests
* database tests
* HTTP/security tests
* Testcontainers
* frontend tests
* browser flows
* concurrency scenarios
* regression testing

### `frontend-reviewer`

Read-only reviewer for React and TypeScript changes.

Reviews:

* component architecture
* server state vs local state
* TanStack Query
* Axios/API clients
* React Hook Form
* Zod
* accessibility
* error handling
* performance
* frontend security
* test quality

### `platform-reviewer`

Read-only reviewer for infrastructure and operational changes.

Reviews:

* Docker
* Docker Compose
* runtime security
* networking
* persistence
* health checks
* Flyway rollout
* backup/restore
* Grafana
* Prometheus
* Loki
* Tempo
* OpenTelemetry

## Skills

The kit currently contains reusable skills for:

* change planning
* Spring backend development
* React/TypeScript
* PostgreSQL and Flyway migrations
* application security
* behavioural test verification
* evidence-based code review
* delivery and operations
* deterministic financial calculations

Skills are loaded only when relevant to reduce unnecessary context consumption.

## Backend engineering

The Spring skill covers topics such as:

* Spring Boot architecture
* REST APIs
* DTO boundaries
* validation
* transaction management
* JPA
* null safety
* idempotency
* optimistic locking
* transaction failures
* external integrations
* version compatibility
* maintainable SOLID design

The kit intentionally avoids patterns such as creating `ServiceInterface + ServiceImpl` for every service when no abstraction is required.

## Database and Flyway

Database guidance includes:

* PostgreSQL schema design
* functional dependencies
* 1NF / 2NF / 3NF / BCNF
* candidate keys
* foreign keys and constraints
* indexing
* query-driven optimisation
* JPA modelling
* concurrency
* Flyway migration safety
* expand/migrate/switch/contract migrations
* large-table backfills
* rollback/recovery planning

Normalization is not treated as a dogma. Intentional denormalization is acceptable when its purpose, consistency model and operational consequences are documented.

## Security

The security model supports server-side BFF architectures using Spring Security and Keycloak.

Typical flow:

```text
Browser
   |
   | session cookie + CSRF
   v
Spring Boot BFF
   |
   | OAuth2/OIDC Authorization Code
   v
Keycloak
```

Principles include:

* no access tokens in React
* no refresh tokens in browser storage
* Authorization Code + PKCE
* server-side sessions
* CSRF protection for cookie-authenticated mutations
* issuer + subject identity
* default-deny authorization
* object-level ownership checks
* trusted reverse-proxy handling
* no custom authentication framework when Spring Security already provides the mechanism

## React and TypeScript

Frontend guidance supports:

* React
* TypeScript
* Vite
* Axios
* TanStack Query
* React Hook Form
* Zod
* React Router
* Vitest
* React Testing Library
* MSW
* Playwright
* accessibility testing

State is intentionally separated:

```text
Server state
→ TanStack Query

Form state
→ React Hook Form

Local UI state
→ useState / useReducer

Global client state
→ only when a real shared-state requirement exists
```

The kit avoids unnecessary `useEffect`, blanket memoization and speculative abstractions.

## Docker and observability

Operational guidance includes:

* multi-stage Docker builds
* non-root runtime users
* minimal images
* secret separation
* `.dockerignore`
* health/readiness checks
* persistent volumes
* Docker networking
* DEV/PROD separation
* resource management

Observability guidance supports:

```text
Spring Boot
   |
OpenTelemetry
   |
   +--> Prometheus --> Grafana
   +--> Loki -------> Grafana
   +--> Tempo ------> Grafana
```

It also includes rules for:

* metric cardinality
* structured logs
* trace/log correlation
* sensitive-data handling
* telemetry failure isolation

## Risk-based workflow

The kit intentionally avoids running every agent for every task.

### LIGHT

Small, low-risk changes:

```text
implementer
→ relevant tests
```

### STANDARD

Normal application changes:

```text
implementer
→ code-reviewer
```

### HIGH-RISK

Security, migrations, concurrency or financial logic:

```text
test-engineer DESIGN
→ implementer
→ code-reviewer
→ security-reviewer / platform-reviewer when relevant
→ test-engineer VERIFY when useful
```

Only one agent should modify production code at a time.

## Example workflow

A security-sensitive task might look like:

```text
Main Claude Code session
        |
        +--> test-engineer (DESIGN)
        |
        +--> implementer
        |
        +--> code-reviewer
        |
        +--> security-reviewer
```

Agents should not recursively delegate to additional agents unless the workflow explicitly requires it.

## Project-specific configuration

The agents and skills are intended to stay reusable.

Project-specific decisions should live outside them, for example:

```text
CLAUDE.md
docs/project-profile.md
docs/tasks/
```

Examples of project-specific decisions:

* chosen architecture
* supported Java/Spring versions
* authentication model
* session lifetime
* deployment environment
* domain rules
* application-specific acceptance criteria

This allows the same agents and skills to be reused across multiple projects.

## Installation

Copy the reusable Claude Code configuration into your project:

```text
.claude/
├── agents/
└── skills/
```

Then add project-specific instructions in:

```text
CLAUDE.md
```

Run Claude Code from the repository root so it can discover the project instructions and `.claude` configuration.

## Recommended usage

Instead of asking Claude to implement a large feature in one step, use bounded tasks with explicit acceptance criteria.

Example:

```text
Read CLAUDE.md and relevant skills.

Use the implementer agent to implement this task.

After implementation:
- run the relevant tests
- request independent code review
- request security review if the change modifies a security boundary

Do not commit, push or deploy.
```

## Validation philosophy

A passing test suite is evidence only for what was actually tested.

The kit distinguishes between:

* implemented
* statically reviewed
* dynamically verified
* integration tested
* production verified

It avoids claims such as "production-ready" or "secure" without appropriate evidence.

## Status

The kit is actively evolving based on real development tasks and benchmark scenarios.

Current focus areas include:

* Spring Boot / Keycloak BFF
* React frontend architecture
* PostgreSQL / Flyway
* Docker and observability
* application security
* testing and independent review
* context/token-efficient Claude Code workflows

## License

Choose a repository license appropriate for how you want others to reuse the kit.

For broad public reuse, MIT or Apache-2.0 are common options.

Before publishing, retain any required third-party attribution notices included in the repository.
