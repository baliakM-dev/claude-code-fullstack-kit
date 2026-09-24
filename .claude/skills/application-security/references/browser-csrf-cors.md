# Browser security: CSRF, CORS, cookies and headers

## BR-01 - Credential-driven CSRF policy
Keep CSRF on browser-session unsafe methods, including local logout. REST, JSON and STATELESS are not proof of CSRF safety; automatically attached cookies or other browser credentials still matter. A genuinely bearer-only chain may exclude CSRF only after proving it cannot authenticate through ambient credentials; isolate it from the browser chain. A narrowly matched webhook needs its own independent signature/replay policy, not blanket exclusion of /api/**.

Do not use GET for business mutations or local logout. Protocol callbacks such as a validated OIDC return have a separate protocol-bound anti-forgery flow; do not reject that flow blindly or exclude every login-related path without analysis. An exception must have its own documented authentication and anti-replay evidence.

## BR-02 - Version-correct React/SPA integration
Choose one documented acquisition/transport mechanism and test it with the actual frontend client. A JavaScript-readable CSRF value is distinct from the HttpOnly authentication cookie. Returning a raw cookie token must match the request handler's expectations; preserve deferred loading and BREACH protections as appropriate to that mechanism.

Use the selected version's supported SPA configuration when available. For Spring Security 7+ session-authenticated SPAs, prefer the framework-native SPA configuration; when it is the only CSRF customization, `.csrf(CsrfConfigurer::spa)` is the concise canonical form, while `.csrf(csrf -> csrf.spa())` is equivalent and not a defect. Otherwise use that version's documented handler/repository integration. Do not paste a legacy custom handler over a newer supported facility without a reason. Renew/reacquire the token after login/logout and test a subsequent mutation. A successful csrf() MockMvc request does not prove real browser acquisition works. Do not blindly replay a write after a 403/network error; renew UI state without duplicating an uncertain operation.

## BR-03 - Session-cookie boundary
Use Secure and HttpOnly for production session cookies, narrow host/path scope and a SameSite value tested against the real OIDC response mode and deployment. Avoid a parent-domain cookie when not needed. Do not confuse site and origin or require Strict when it breaks the selected callback. SameSite=None requires a deliberate cross-site design and Secure; it is not the universal default. Local HTTP exceptions must be isolated to development and cannot silently carry into production.

Document cookie name and cleanup behavior; an optional __Host- prefix has requirements and can affect framework/logout integration. Verify custom names against back-channel logout/session-store support before adoption. Do not place sessions or access/refresh tokens in URLs, browser storage or frontend state. Clear user-specific UI/query/service-worker caches when the principal changes.

## BR-04 - CORS is browser sharing, not authorization
Prefer same-origin routing for this project's BFF, but preserve other projects' verified origins. Allow only required schemes/hosts/ports, methods and headers for credentialed cross-origin access. Reject arbitrary origin reflection and do not use a broad credentialed origin pattern. An intentionally public non-credentialed wildcard endpoint is not automatically a severe vulnerability.

Ensure preflight handling happens before authentication decisions for the configured CORS paths; preflight does not carry the login session. A permitted OPTIONS result never authorizes the subsequent write. Test allowed/disallowed actual origins and credentials. CORS does not stop non-browser clients and is not a substitute for CSRF or object authorization.

## BR-05 - Actual browser-delivered headers
Keep relevant security headers and sanitized error responses. Configure CSP on the actual HTML-serving layer, not merely the JSON API. Use framing, content-type, referrer and caching policies appropriate to the app. Do not globally disable headers or add unsafe inline/eval allowances to silence a frontend issue without review.

Serve production via HTTPS. Add HSTS only with the host/subdomain deployment consequences understood; do not enable preload blindly. Prevent shared caching of personalized responses, but allow intentional static-asset caching. Verify headers after the reverse proxy, not only in a controller unit test.

Sources checked 2026-09-23:
- https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html
- https://docs.spring.io/spring-security/reference/features/exploits/csrf.html
- https://docs.spring.io/spring-security/reference/servlet/integrations/cors.html
- https://docs.spring.io/spring-security/reference/servlet/exploits/headers.html
- https://docs.spring.io/spring-security/reference/servlet/oauth2/login/logout.html