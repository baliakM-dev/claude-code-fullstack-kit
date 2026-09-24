# Spring Security implementation and review standard

These are kit policy IDs, not framework guarantees or ASVS requirements. Apply only the relevant sections; preserve compatible, proven decisions. Recheck APIs against the actual Spring Boot BOM and resolved Spring Security version.

## SS-01 - Framework and authentication model
Use SecurityFilterChain beans and the supported configuration DSL for the chosen servlet version; use the reactive equivalent only in a genuinely reactive app. Verify signatures against the actual resolved Spring Security version instead of copying historical examples. If the selected version's `HttpSecurity` chain and `build()` path do not throw a checked exception, do not keep `throws Exception` merely because older examples used it. Do not copy deprecated adapters or introduce a custom JWT/password filter when supported OAuth2 client/resource-server facilities fit. Keep the code modular but the effective policy easy to trace; SOLID does not require a filter, interface or chain per endpoint.

Distinguish browser session, bearer-only API and machine credentials. Disable unused authentication mechanisms deliberately; no fallback demo users, generated Basic-auth workflow, implicit grant or password grant in the BFF. When a different project actually owns passwords, use a supported adaptive PasswordEncoder and benchmark/tune its work factor. Never store reversible/plaintext passwords or duplicate Keycloak password authentication in the application.

## SS-02 - Complete chain coverage and explicit policy
Inventory each chain, order, matcher, provided protocol endpoints and credential model. securityMatcher selects a chain; authorization requestMatchers select rules within it. Ensure an intentional catch-all chain protects otherwise unmatched application paths; a request matching no chain receives no Spring Security protection. Prefer one coherent chain unless distinct credential models or constraints justify more.

Define public paths and methods narrowly, with deny-by-default handling for unspecified protected operations. Keep login start/callback, CSRF acquisition, logout and deliberately public assets/health reachable under their own policy. Never globally permit paths just to repair a redirect or failing test. Use permitAll rather than bypassing filters for paths needing headers and other protections. Review error/forward dispatch, path normalization, trailing slash and alternate methods with the actual routing configuration. Do not disable the firewall broadly to accept malformed paths.

## SS-03 - Authorities and service boundaries
Map only trusted issuer/client-specific roles or scopes; distinguish hasRole prefixes from hasAuthority values. Do not make every authenticated principal an admin, consume arbitrary realm roles, or accept roles/owner fields from a request. Document the mapping and test missing, wrong and changed authorities.

Enable method security explicitly if using its annotations. Verify calls pass through Spring proxies: annotations on unmanaged instances or same-object calls can be bypassed. Use an explicit authorized application boundary when jobs or alternate entry points need the same policy. Do not rely on post-authorization alone for a write: unauthorized work must not commit or cause external side effects. Avoid duplicate, divergent ownership checks; protect the invariant at the authoritative boundary and query.

## SS-04 - Denials and security context
Return the documented JSON 401/403 contract for APIs and redirect only at intended browser login entry points. A forbidden object may intentionally use a consistent 404 anti-enumeration policy. Missing CSRF on an unauthenticated mutation can be denied before authentication: test each control in isolation rather than forcing every failure to 401.

Use framework context/session lifecycle. Do not store Authentication in singleton mutable state or inherit a user's context into arbitrary thread pools. For authorized asynchronous work capture the intended actor/tenant and apply the documented authorization/revocation policy. A custom authentication integration must explicitly preserve/clear context according to the chosen version.

## SS-05 - Evidence, not appearance
Read the shared browser, BFF, resource-server and object-authorization references only where applicable. Preserve protections in the production chain during tests. Require a known protected operation to succeed for an authorized actor and fail for an unauthorized actor, without disclosure or mutation. A 404 on a nonexistent controller is not an authorization test.

Sources checked 2026-09-23; policy composition and review gates are kit design choices:
- https://docs.spring.io/spring-security/reference/servlet/configuration/java.html
- https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html
- https://docs.spring.io/spring-security/reference/servlet/authorization/method-security.html
- https://docs.spring.io/spring-security/reference/servlet/authentication/session-management.html
- https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html