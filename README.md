# Claude Code Fullstack Kit

Reusable Claude Code agents, skills and engineering guardrails for secure, maintainable full-stack development.

The kit is designed to support real software delivery rather than prompt-only code generation. It separates implementation, independent review, testing, security and platform concerns while keeping project-specific decisions outside the reusable core.

## What is included

### Agents

- `implementer` — implements bounded changes and relevant tests.
- `code-reviewer` — read-only evidence-based correctness and maintainability review.
- `security-reviewer` — read-only application-security review.
- `test-engineer` — independent test design and authorized verification.
- `frontend-reviewer` — read-only React/TypeScript review.
- `platform-reviewer` — read-only database, Docker and operational review.

### Skills

Core reusable skills:

- `change-planning`
- `spring-backend`
- `react-typescript`
- `postgresql-migrations`
- `application-security`
- `test-verification`
- `evidence-review`
- `delivery-operations`

Optional domain skill:

- `financial-calculations` — deterministic, versioned financial-rule implementation and verification.

## Usage guide

For practical guidance on when to use each agent and skill, recommended LIGHT / STANDARD / HIGH-RISK workflows, example prompts and token-efficient usage, see [docs/how-to-use.md](docs/how-to-use.md).

## Engineering principles

- Prefer the smallest complete solution.
- Preserve correct existing architecture unless evidence justifies change.
- Keep security controls enabled; do not weaken them to make tests pass.
- Separate server state, form state and local UI state on the frontend.
- Treat database constraints, transactions, concurrency and migrations as correctness concerns.
- Use framework-supported authentication/session mechanisms before custom infrastructure.
- Keep reviewers independent and read-only.
- Use real evidence for database, browser/OIDC and integration claims.
- Avoid speculative abstractions and unnecessary services.
- Do not automatically commit, push, deploy or run destructive Git operations.

## Risk-based workflow

### LIGHT

```text
implementer
-> relevant checks
```

### STANDARD

```text
implementer
-> code-reviewer
```

### HIGH-RISK

For security, migrations, concurrency or financial logic:

```text
test-engineer DESIGN
-> implementer
-> code-reviewer
-> security-reviewer / platform-reviewer when relevant
-> test-engineer VERIFY when useful
```

Only one agent should modify production code at a time.

## Installation

Copy the complete shared Claude Code configuration into your project:

```text
.claude/
├── agents/
├── skills/
├── policies/
└── settings.json
```

Then create project-specific instructions from the templates:

```text
templates/CLAUDE.md         -> CLAUDE.md
templates/project-profile.md -> docs/project-profile.md
```

Review `.claude/settings.json` before adopting it. Local overrides belong in `.claude/settings.local.json`, which should not be committed.

Project-specific decisions should stay outside the reusable agents and skills, for example:

- architecture and module boundaries
- selected Java/Spring/React versions
- authentication model
- session lifetimes
- deployment environment
- domain rules
- acceptance criteria

## Example task prompt

```text
Read CLAUDE.md and only the relevant skills.

Use the implementer agent to implement this bounded task.

After implementation:
- run relevant tests,
- request independent code review,
- request security or platform review only if the change touches those boundaries.

Do not commit, push or deploy.
```

## Validation

The repository ships structural regression tests and a static validator.

Run:

```bash
python scripts/validate_kit.py
python -m unittest discover -s tests -p "test_*.py"
python .claude/skills/spring-backend/scripts/verify_java_examples.py
```

The GitHub Actions workflow runs these checks on pushes and pull requests.

These checks validate repository structure and selected invariants. They do **not** prove Claude Code behavior, application security, production readiness or model quality.

Behavioral evaluation scenarios live under `evals/` and remain separate from structural validation.

## Technology coverage

The kit includes guidance for:

- Java / Spring Boot
- Spring Security
- Keycloak / OAuth2 / OIDC / BFF
- React / TypeScript / Vite
- Axios / TanStack Query
- React Hook Form / Zod
- PostgreSQL / JPA / Flyway
- Docker / Docker Compose
- Prometheus / Grafana / Loki / Tempo / OpenTelemetry
- testing, concurrency, idempotency and null-safety

The guidance is intentionally project-agnostic. A project is free to use only the relevant parts.

## Repository structure

```text
.
├── .claude/
│   ├── agents/
│   ├── skills/
│   ├── policies/
│   └── settings.json
├── .github/workflows/
├── evals/
├── scripts/
├── templates/
├── tests/
├── verification/
├── kit-manifest.json
├── LICENSE
├── README.md
└── THIRD_PARTY_NOTICES.md
```

## Third-party material

Some Spring-related guidance was selectively adapted from `rrezartprebreza/spring-boot-skills` under the MIT License. Required attribution is retained in `THIRD_PARTY_NOTICES.md` and the corresponding `LICENSE-UPSTREAM.txt` files.

## License

This repository is licensed under the MIT License. See `LICENSE`.