# Spring BFF and Keycloak

## BF-01 - Protocol contract
Use Spring as a confidential OAuth2/OIDC client, Authorization Code, PKCE S256 and the selected client-authentication method. In this kit PKCE is a deliberate baseline for confidential clients, not a claim that every specification mandates it. Verify a transaction-specific challenge/verifier and library-bound state/nonce in the real flow without capturing secret values. Restrict redirect and post-logout URIs; reject arbitrary return URLs and token/authorization-code replay.

Resolve the canonical issuer consistently through development containers and production proxy. Never turn off issuer, TLS, nonce or state checks to fix hostnames. Use least scopes and exact intended registrations. Disable unused direct/implicit grants and service-account privileges for the browser client; avoid offline tokens by default. Link identity using verified issuer+subject, not mutable email or an untrusted request ID.

Keep access/refresh tokens and client secrets on the server, out of DTOs, browser storage, URLs and logs. The browser authenticates to this app with an opaque session; its CSRF value is separate. A standard RP logout may intentionally transport an id_token_hint to the configured IdP: explicitly document that exception, never use the ID token as an API credential, and redact protocol URLs. Do not write a custom BFF JWT scheme to avoid this distinction.

## BF-02 - Three separate lifecycles
Document application session, authorized-client storage and Keycloak SSO/client session separately. Configure fixation protection, idle and absolute lifetime, renewal, restart and reauthentication semantics. An idle timeout does not establish an absolute lifetime. A local session can outlive an access token or an IdP event unless the chosen design couples them.

Record disabled-account, role-change and logout/revocation propagation latency and mechanism. For material authorization changes use a policy appropriate to risk: bounded reauthentication, supported back-channel invalidation or another explicitly tested mechanism. Do not promise immediate revocation from an ordinary local session or locally validated JWT. For multiple replicas design persistence, encryption/access, registry/invalidation and concurrent updates; a JVM-local store/lock is not a distributed guarantee. Do not automatically add Redis for a single-node prototype.

## BF-03 - Refresh only when a token is actually used
First determine whether downstream calls need an access token. Local session-authenticated CRUD does not require a refresh scheduler. If no downstream token is used, mark refresh NOT_APPLICABLE with an activation condition, while still satisfying the session/revocation policy.

When needed, identify OAuth2AuthorizedClientRepository/Service, the appropriate OAuth2AuthorizedClientManager/provider, caller that invokes authorize and persistence of renewed credentials. Use framework-supported client integration for the request/background context. oauth2Login alone is not evidence of refresh. Test access expiry/tolerance, refresh rotation, revoked/expired refresh and concurrent use, including replicas where deployed.

Differentiate invalid_grant from a transient timeout; clean relevant credentials and follow reauthentication policy without infinite retry/login loops. Bound refresh coordination and failures. Do not replay an uncertain non-idempotent downstream write after 401/timeout without a valid deduplication contract. Constrain destinations and forwarded credentials so a BFF cannot proxy tokens to a user-chosen URL.

## BF-04 - Logout is more than deleting a cookie
Use supported local logout handlers for SecurityContext/session cleanup, authorized-client cleanup according to its storage and cookie deletion with matching attributes. Protect local logout with CSRF. Explicitly choose local-only versus RP-initiated SSO logout and the behavior if the IdP is unreachable; never claim global logout if only local invalidation succeeded.

If back-channel logout is required, use the framework's validated logout-token flow, trusted issuer/audience and session mapping. Match its endpoint and exemptions narrowly; test bad tokens and wrong sessions. Check the selected version's cookie-name and OidcSessionRegistry/session-store constraints, including Spring Session/custom names and replicas. Do not assume a default in-memory registry invalidates every node. Logout alone cannot erase independently accepted JWTs already issued elsewhere.

## BF-05 - Evidence
Use synthetic users and the actual provider/browser/proxy configuration. Cover callback rejection, session fixation, expiry, CSRF lifecycle, old-session reuse, chosen SSO behavior and IdP outage. Mock oidcLogin tests application handlers, not protocol validity. Read the shared security-verification matrix for affected cases; report non-executed integration as NOT_RUN.

Sources checked 2026-09-23:
- https://www.rfc-editor.org/rfc/rfc9700.html
- https://docs.spring.io/spring-security/reference/servlet/oauth2/client/authorized-clients.html
- https://docs.spring.io/spring-security/reference/servlet/oauth2/client/core.html
- https://docs.spring.io/spring-security/reference/servlet/authentication/session-management.html
- https://docs.spring.io/spring-security/reference/servlet/oauth2/login/logout.html
- https://openid.net/specs/openid-connect-rpinitiated-1_0.html
