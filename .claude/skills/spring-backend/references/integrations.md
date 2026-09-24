# Outbound clients and logging

Use a supported HTTP client for the application's servlet/reactive model. Set connection and response timeouts, bound payloads, validate responses and sanitize errors. Allow only intended upstream hosts and redirects; never attach OAuth tokens to arbitrary user-supplied URLs.

Retry only failures for which retry is appropriate. Bound count, total duration and backoff. Protect non-idempotent requests with a contractually valid idempotency key or deduplication. A timeout is not proof that the upstream did nothing. Do not wrap a retry loop around every exception or expired credential.

A circuit breaker, inbound rate limiter and DDoS protection solve different problems. Add one only for a known failure mode. Cache only with ownership, freshness and invalidation defined.

Use structured application logs with request/trace correlation when available. No access/refresh tokens, session cookies, full personal records or credentials in logs. Error-reporting tools also receive data: redact and sample before shipping. Record operational failure without exposing sensitive values.

Primary source: https://docs.spring.io/spring-framework/reference/integration/rest-clients.html
