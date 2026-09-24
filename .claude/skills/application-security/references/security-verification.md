# Security evidence and acceptance

Use these kit-specific case IDs for traceability, not as ASVS IDs. Select tests from the original contract and the actual credential/deployment model before copying implementation behavior. Mandatory means mandatory for the affected applicable boundary, not run every case on every task.

## Required test design
For each selected case record actor/initial state, exact operation, expected response, forbidden disclosure/effect and the enforcing control. Include positive controls: the known route and authorized user must work. Observe database/outbound effects where relevant, not only status codes. An unknown route returning 404 or a CSRF rejection hiding a missing ownership check is insufficient.

| ID | Activate when | Required observable behavior |
| --- | --- | --- |
| SEC-01 | New/changed Spring routes or chains | Known authorized operation works; anonymous/wrong-role access is denied; otherwise unmatched routes and alternate methods cannot escape the intended chains. |
| SEC-02 | Ownership/tenant data paths | User B cannot read/update/delete user A's actual object; lists/counts/exports/bulk/jobs disclose no A data. Correct user can operate. |
| SEC-03 | Browser unsafe operation | Missing/wrong CSRF token is rejected; valid session+token works. Isolate this from role/ownership tests; denied writes cause no mutation. |
| SEC-04 | SPA login/logout/CSRF | Real browser obtains a matching token; first mutation after login and after a new login following logout works. Old context cannot authorize operations. |
| SEC-05 | OIDC flow | Real synthetic-provider login/callback succeeds; wrong/missing transaction binding, replay and invalid redirect do not establish an authenticated session. Verify PKCE without persisting secrets. |
| SEC-06 | Session management | Session fixation protection, idle/absolute expiry, invalid/old-session reuse and declared restart behavior match the contract. |
| SEC-07 | Logout/account/role lifecycle | Local cookie/context/credential cleanup and chosen SSO/back-channel semantics work; disabled-account or role-revocation behavior meets documented latency. IdP outage is reported honestly. |
| SEC-08 | Downstream OAuth use | Access expiry refresh, renewed credential persistence, revoked refresh, transient failures and coordinated parallel use are tested. No blind duplicate write/retry. |
| SEC-09 | Actual bearer API | Invalid signature/issuer/audience/time/token type or absent scopes is denied; valid token with wrong owner still cannot access data. Key rotation/outage follows policy. |
| SEC-10 | Cross-origin browser access | Allowed origin preflight and actual request behave correctly; disallowed origin cannot read credentialed data; non-browser requests still face authorization. |
| SEC-11 | Proxy/ingress/management | HTTPS/host/cookie/redirect remain correct at public ingress; spoofed forwarded headers or direct backend access cannot bypass trust. Management exposure matches the intended audience. |
| SEC-12 | Login abuse/session limits | Failed attempts around N-1/N/N+1, reset, waits/recovery and concurrent-session policy follow the selected version. Cover shared NAT and account-denial risks. |
| SEC-13 | Logging/errors/browser storage | Sanitized synthetic checks detect no access/refresh tokens, secrets or personal payloads in logs/errors/telemetry/exports/browser state. Selected logout protocol exceptions are documented. |
| SEC-14 | Input/upload/export/integration | Payload/processing limits, SQL/mass-assignment protection, safe rendering, authorized file access and restricted outbound targets work for the affected surface. |

## Separate levels of evidence
- Unit/mocked principal tests: useful policy/handler evidence only. oidcLogin/jwt mocks do not validate a real provider, token signature or decoder configuration.
- HTTP integration: run the actual security chain with positive/negative controls. Do not use addFilters=false or substitute permissive test security to claim production security evidence. A test-only probe route may demonstrate catch-all coverage but is not a substitute for the real operation.
- Database: verify ownership, atomic denied writes, constraints and counts against relevant real PostgreSQL when that behavior depends on SQL. Use synthetic fixtures and actual ownership predicates.
- Browser/IdP/proxy: exercise actual cookie/header/token lifecycle, protocol flow and public-ingress behavior in an explicitly authorized isolated setup. Redact captures; never attach raw HAR files with credentials.
- Static/dependency/image scans: map actionable findings to the exact dependency/runtime, track justified exceptions with owner/revisit point, and record tool/database version. Scans cannot certify the absence of vulnerabilities.

## Completion and reviewer handoff
Implementation and test-engineer execution remain within their granted tools/paths. Static security reviewers cannot execute tests or probes. Main session supplies a sanitized manifest/evidence packet, while reviewers independently inspect the actual code.

For each selected case report PASS / FAIL / NOT_RUN / NOT_APPLICABLE with actual evidence, checked revision or new-file hashes, command/directory/exit status when run, and residual risk. NOT_APPLICABLE needs reason and activation condition (for example, no downstream bearer calls). A missing runtime is NOT_RUN, not NOT_APPLICABLE. Link applicable project decisions; unchosen production timeouts/limits are not a tested configuration.

Use evidence-review's CONFIRMED / NEEDS_VERIFICATION / OPTIONAL findings. Never silently suppress a finding or weaken controls to obtain green tests. Fix confirmed blockers and repeat affected checks. Production acceptance requires relevant real-flow evidence and separate review; a bootstrap with explicit gaps may be PARTIALLY_VERIFIED but is not production-ready.

Sources checked 2026-09-23:
- https://docs.spring.io/spring-security/reference/servlet/test/mockmvc/csrf.html
- https://docs.spring.io/spring-security/reference/servlet/test/mockmvc/oauth2.html
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
