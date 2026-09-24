# Server state and API access

Use this reference for HTTP clients, TanStack Query, cache ownership, mutations and BFF-aware requests.

## Boundaries
- Treat remote/server data as server state. Prefer TanStack Query for reusable async server state that needs caching, deduplication, retries, invalidation or shared lifecycle.
- Do not move purely local UI state (open dialog, selected tab, draft toggle) into TanStack Query.
- Do not fetch ordinary server data with `useEffect + useState` when the project already uses TanStack Query and the data fits its model.
- Do not add TanStack Query for a one-off static value or trivial synchronous state merely to follow a pattern.

## Axios client
When the project standard is Axios, create one bounded API client rather than ad-hoc instances in components.
- Set base URL and credentials from the deployment contract; for the BFF, browser requests normally use the application session cookie rather than bearer tokens.
- Add a finite timeout appropriate to the operation. Cancellation should propagate through `AbortSignal` where supported.
- Keep interceptors limited to cross-cutting transport concerns such as safe error normalization or CSRF header wiring. Never hide business branching, navigation loops or token refresh logic in a global interceptor.
- Never read/store access or refresh tokens in browser storage or JavaScript state for this BFF architecture.
- Do not log raw request/response bodies when they can contain personal, financial, session or CSRF data.
- Normalize transport errors into a small typed application error shape while preserving status and safe problem details needed by callers.

## Query design
- Build stable hierarchical query keys that include every variable that changes the result. Prefer small key factories per feature over free-form string duplication.
- Use `useQuery`/`useInfiniteQuery` for reads and `useMutation` for server-changing commands.
- Choose `staleTime`, retry and refetch behavior from data volatility and failure semantics. Do not set a universal `Infinity`, disable refetch globally, or blindly accept retry defaults for every endpoint.
- Do not automatically retry authentication/authorization failures, validation failures, conflicts or non-idempotent commands. Query retries for transient reads may be reasonable; mutations require explicit semantics.
- After mutations, prefer precise invalidation or direct cache updates when the new state is known. Avoid invalidating the entire cache.
- Optimistic updates require a rollback path, a conflict strategy and server authority. Do not use them for sensitive financial actions merely for perceived speed.
- Clear or remove principal-scoped cached data on logout/account switch. A stale cached response from a previous principal is a security/data-leak risk.

## BFF session and CSRF
- Auth state comes from the backend contract such as `/api/auth/me`; do not infer auth from a JWT in the browser.
- Login starts the server OAuth2 route/redirect. Do not call the Keycloak token endpoint from React.
- Mutating requests must send the CSRF token/header required by the backend. A `403` caused by missing CSRF is not a reason to disable CSRF.
- Distinguish `401 unauthenticated`, `403 forbidden`, `409 conflict`, validation errors, timeout/network failures and `5xx` in application behavior.

## Evidence
For changes to API/cache behavior, test at least the relevant loading/success/error states, query-key separation, invalidation or cache update, logout cache clearing and cancellation/stale-response behavior. Use MSW or the project's equivalent for component/integration tests; a mocked hook alone does not prove the HTTP contract.

Primary sources:
- https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
- https://tanstack.com/query/latest/docs/framework/react/guides/query-keys
- https://axios-http.com/docs/req_config
- https://axios-http.com/docs/interceptors
