# Bearer APIs: conditional, not a replacement for BFF

## RS-01 - Activation and authentication separation
Read this only for an actual bearer-token API or machine integration. Preserve session BFF for the browser unless a new requirement explicitly changes it. Record issuer, intended audience, scopes, token type and consumers. Do not make one route accept session and bearer credentials accidentally or set the OIDC browser flow STATELESS without a complete design.

Use Spring Security OAuth2 Resource Server rather than a custom JWT parser/filter. Configure its own chain and coverage intentionally. Disable CSRF only after establishing no ambient browser credentials authenticate that chain; Basic auth being stateless is not by itself sufficient.

## RS-02 - Validation and authorities
For JWTs validate the signature, intended algorithms, issuer, required audience and validity period with bounded clock skew. Configure audience validation explicitly for the selected Boot/Security version; issuer validation alone is not audience validation. Reject missing required claims, wrong keys, wrong audience, expired/future-invalid tokens and ID tokens used as access tokens under the issuer's documented token profile. Do not fetch arbitrary token-provided key URLs or confuse successful decoding with validation.

Use trusted discovery/JWK sources with verified TLS and a deliberate key-rotation/outage policy. Test known and unknown keys without disabling checks. Define role/scope conversion, least privilege and object-level authorization; an otherwise valid JWT is not permission to access any record.

For opaque tokens use supported introspection, protected credentials and a bounded failure/cache policy; explicitly document how caching affects revocation. Never log raw tokens, authorization headers or introspection secrets.

## RS-03 - Delivery and revocation
Return appropriate bearer authentication/access-denial responses without leaking internal validation details. Keep tokens out of query parameters and unapproved downstream hosts. Service accounts use least client permissions and independently protected credentials; no user-password grant as a shortcut.

State token lifetime and revocation latency. Local JWT verification does not normally query the IdP on every request; do not claim instant token revocation or add a denial-list service without a requirement. Test invalid credentials separately from missing scopes and object ownership.

Sources checked 2026-09-23:
- https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html
- https://www.rfc-editor.org/rfc/rfc9700.html
- https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/opaque-token.html
