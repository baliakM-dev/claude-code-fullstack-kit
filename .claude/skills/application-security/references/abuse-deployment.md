# Abuse prevention and runtime boundaries

If Keycloak validates passwords, configure brute-force protection there; a BFF failed-login counter cannot see every failure at the IdP. Define actual failure threshold, window, increasing waits, reset, maximum block and recovery. Values must reflect the deployment and risk, not a universal magic number. Distinguish failed-login limits from simultaneous-session limits.

Test N-1/N/N+1 according to the selected Keycloak version, reset/unblock, account-denial abuse, distributed sources and shared NAT. Avoid permanent lockout by default without a recovery design. Combine account/source/endpoint controls and useful sanitized alerts.

Trust forwarded headers only from known proxies which replace untrusted values. Validate external HTTPS scheme/host/redirect behavior. Do not use arbitrary X-Forwarded-For as a rate-limit identity. Protect admin and management interfaces. Separate Keycloak admin credentials, application database credentials and migrations.

Set practical request size, connection/time, authentication and expensive-endpoint limits. Application throttling is not volumetric DDoS protection. Describe what the hosting edge provides and what remains unprotected.

Do not expose databases, admin consoles or Docker sockets publicly. Minimize image/runtime privilege and filesystem access. Secure secrets and backups. Test restore and access boundaries, not merely configuration syntax.

Primary sources:
- https://www.keycloak.org/server/reverseproxy
- https://www.keycloak.org/docs/latest/server_admin/index.html#password-guess-brute-force-attacks

## AB-01 - Explicit identity-abuse configuration
Select and record parameters for the actual Keycloak version: failure threshold, counting/reset semantics, quick-login handling, wait progression/cap and recovery. Also record the separate simultaneous-session policy, admin MFA and password/account recovery flow. Do not call a number a universal best practice. Use testable development proposals; production needs a reviewed deployment-specific policy.

Keycloak controls password verification in this architecture. Keep registration, reset and public login responses resistant to account enumeration; apply bounded endpoint/source controls and test recovery without enabling an account-denial attack. A per-IP limit is incomplete against distributed traffic and can block shared-NAT users. New admin accounts need least roles and tested recovery; do not give the application realm-admin access as a convenience.

## AB-02 - Proxy and operational enforcement
Enforce the trusted ingress at the network boundary as well as in configuration. The proxy must overwrite untrusted forwarded host/scheme/client-address data; an attacker must not bypass it through a public backend port. Test canonical issuer, external HTTPS redirects and rate-limit identity. A config property accepting forwarded headers does not authenticate their sender.

Review application and separate management ports, Actuator exposure/authorization, API docs, Keycloak admin routes and health detail. Defining a custom application chain can require explicit management security; inspect effective behavior rather than relying on Boot defaults. Limit public diagnostics to intentional minimal signals.

Keep development relaxations out of production profiles. Use least runtime/database/migration permissions, encrypted transport, protected backup storage and a tested restore path. Document request/body/time/concurrency and expensive-calculation limits at the actual enforcing layer. DDoS protection at the hosting edge is separate from app throttling or circuit breakers.

Additional sources checked 2026-09-23:
- https://docs.spring.io/spring-boot/reference/actuator/endpoints.html
- https://www.keycloak.org/docs/latest/server_admin/index.html#password-guess-brute-force-attacks
- https://www.keycloak.org/server/reverseproxy
