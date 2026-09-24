# Third-party notices

This kit selectively adapts documentation and a SQL example from
[rrezartprebreza/spring-boot-skills](https://github.com/rrezartprebreza/spring-boot-skills),
commit `f0c06a01b0b7571b519cd43e16692b2483a24514` (inspected 2026-09-23). Upstream author: Rrezart Prebreza. License: MIT.
This is an independent adaptation, not an upstream release or endorsement.

The exact inspected paths, upstream Git blob IDs and destination files are recorded in
[upstream-sources.json](docs/upstream-sources.json). The integration decisions and exclusions
are in [upstream-integration.md](docs/upstream-integration.md).

Preserve the complete upstream copyright and permission notice when redistributing the
adapted portions. A copy accompanies each affected skill so individual skill exports retain it:
[spring-backend](.claude/skills/spring-backend/LICENSE-UPSTREAM.txt),
[postgresql-migrations](.claude/skills/postgresql-migrations/LICENSE-UPSTREAM.txt),
[test-verification](.claude/skills/test-verification/LICENSE-UPSTREAM.txt).

The Java fingerprint example and its local test runner were newly written for this update;
they are not extracted upstream templates. No upstream installer, automatic agent orchestration,
MCP integration, custom JWT authentication code, or full verification application was imported.
This notice does not assign a new license to unrelated pre-existing project files.
