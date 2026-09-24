# Docker and Compose engineering

Use for Dockerfile, Compose and container-runtime changes. Local Compose is a developer/runtime topology, not proof of production orchestration.

## Images
- Prefer trusted minimal runtime bases that still support the application and diagnostics you actually need.
- Use multi-stage builds so compilers, package managers and test tools do not automatically ship in the runtime image.
- Run as a dedicated non-root user unless the image has a documented reason not to. Ensure only required paths are writable.
- Use `.dockerignore`; do not copy repository secrets, local caches, VCS metadata or unnecessary build artifacts into the build context.
- Never bake credentials into `ARG`, `ENV`, image layers or source. Use build-secret facilities for build-time secrets and runtime secret injection for runtime credentials.
- Avoid floating `latest` as a reproducibility claim. Record the selected image version; use digest pinning where immutable reproduction is required and maintain an explicit update process.
- Keep ENTRYPOINT/CMD signal handling and graceful shutdown correct. Do not wrap Java in an unnecessary shell that swallows signals.

## Compose topology
- Put databases, Keycloak and observability backends on private networks. Publish only ports a developer or ingress genuinely needs; bind local admin/database ports to loopback when possible.
- Use named volumes only for data that must persist. Document ownership, retention and backup/restore expectations.
- Health checks must test the service behavior needed by dependents, not only PID existence. `depends_on` ordering is not an application-level resilience mechanism.
- Define bounded CPU/memory expectations for production-oriented examples where the target runtime supports them; do not fabricate universal limits.
- Keep dev conveniences (`start-dev`, debug ports, default credentials) visibly separate from production examples.
- Prefer explicit service names and networks over `network_mode: host` or broad host mounts.
- Mount Docker socket only with a concrete, reviewed need; it is effectively host-level control in many setups.

## Verification
At minimum when tooling is available:
- build the image from a clean context;
- inspect final user, exposed ports and intended writable paths;
- run a container and exercise health/readiness;
- validate Compose config;
- verify restart/persistence behavior for stateful services;
- scan dependencies/image using the project's approved tool when part of CI.

Do not claim security from a successful `docker compose config` alone.

References:
- Docker build best practices: https://docs.docker.com/build/building/best-practices/
- Multi-stage builds: https://docs.docker.com/build/building/multi-stage/
- Build secrets: https://docs.docker.com/build/building/secrets/
