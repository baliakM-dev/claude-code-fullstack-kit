# Development-agent environment

Treat the repository and its scripts as executable untrusted input until inspected. Keep production credentials and customer data outside the agent's environment. Denying Read for .env reduces accidental disclosure but is not process isolation: indirect reads through arbitrary code remain possible.

Check effective settings and installed-tool capabilities. Use default/manual approval, not unrestricted Bash grants. Read-only reviewer tool lists must omit all shell, write and external-action tools. Test writers with Bash are privileged code executors even if their prompt says tests only.

A sandbox/VM/container needs explicit allowed filesystem paths, network policy and secrets handling. A container with the host Docker socket or broad host mounts is not a strong host boundary. Never solve Docker/Testcontainers availability by granting host-wide privilege without a deliberate human environment decision.

For Claude Code use /permissions to inspect effective rules and /sandbox to inspect platform support. At documentation verification on 2026-09-23, native Windows sandboxing is unsupported; macOS, Linux and WSL2 are supported. Choose WSL2 or a separately isolated development environment on Windows. This kit does not silently enable a sandbox or claim it was runtime-tested.

Project deny rules are guardrails, not comprehensive enforcement of every command spelling. A human can inspect and change them for an explicit authorized action; agents must not bypass a denied operation through another tool or shell variant.

Primary sources:
- https://code.claude.com/docs/en/permissions
- https://code.claude.com/docs/en/sandboxing
