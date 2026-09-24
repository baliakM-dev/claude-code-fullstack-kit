---
name: "delivery-operations"
description: "Build and review development and delivery infrastructure: Docker, Compose, CI/CD, version pinning, logs, health checks, migrations, backups and restore. Use for repository bootstrap, deployment preparation and operational changes; never interpret preparation as permission to publish or deploy."
---

# Delivery and operations

Read the target environment, build/lockfiles, exposure, data stores, secret strategy and current runbook. Separate a local developer stack from staging and production.

## Select additional detail only when relevant
- Dockerfile, Compose, image/runtime hardening, networks, mounts or container lifecycle: [docker-containers.md](references/docker-containers.md).
- Grafana, Prometheus, Loki, Tempo, OpenTelemetry/Alloy and telemetry exposure/cardinality: [observability-stack.md](references/observability-stack.md).
- Agent permissions and executable-environment boundaries: [agent-environment.md](references/agent-environment.md).

## Workflow
1. Keep one documented command path per operation. Use checked-in wrappers/lockfiles and compatible supported versions. Verify downloads and CI action references from official sources at setup; do not invent a SHA or use floating latest as a reproducibility claim.
2. Build minimal multi-stage images with suitable runtime identity and writable paths. Keep build credentials out of layers; use build-secret facilities where needed. Configure .dockerignore deliberately.
3. Bind development admin/database ports to loopback when they must be published. Keep private services on private networks. A dev Keycloak start-dev configuration is not a production template.
4. Use startup/readiness/health signals that test the intended dependency without leaking internals. Bound startup retries and shutdown. Avoid dependencies that only appear healthy because a process is running.
5. CI should compile/type-check, lint or analyze where configured, run relevant tests and scan dependencies/images/secrets. Use least permissions, protect merge gates and do not expose trusted secrets to untrusted pull requests. An AI approval is not a replacement for CI.
6. Document migrations before rollout, backward compatibility, recovery and a human approval gate. Never auto-push, publish or deploy because a build passed.
7. Start with useful structured logs, health, error reporting and external availability checks. Redact personal data before transport. Add a metrics/tracing stack only for a real operational requirement.
8. Define backup scope (application DB, identity DB, uploaded objects and required configuration), encryption, separate credentials, retention and off-site copy. Test restoring into an isolated environment and check data/functionality. Backups without restore evidence are unverified.

Return actual checks and the remaining deployment risks. Do not claim production readiness from Docker Compose syntax validation.

Primary source: https://docs.docker.com/build/building/best-practices/

## Shared runtime security
For ingress, TLS, forwarded headers, management exposure, runtime privileges or identity-service changes read [abuse-deployment](../application-security/references/abuse-deployment.md). Verify controls at the actual ingress and document missing runtime evidence; do not label a Compose syntax check a penetration test.
