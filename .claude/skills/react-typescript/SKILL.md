---
name: "react-typescript"
description: "Implement and review production-oriented React with TypeScript. Use for component architecture, Axios/API clients, TanStack Query server state, React Hook Form/Zod forms, React Router, BFF session/CSRF flows, accessibility, performance decisions and frontend tests. Preserve simple correct code and add libraries only when the problem justifies them."
---

# React and TypeScript

Inspect the app's package manager/lockfile, React and TypeScript versions, router mode, API contracts, existing state/form conventions and tests before changing architecture. Preserve coherent established choices unless there is a concrete defect or requirement.

## Workflow
1. Classify the change: rendering/local UI, server state/API, form/input, routing, auth/session, shared client state, accessibility/performance or testing.
2. Load only the matching reference below; do not load all frontend references by default.
3. Define observable states and failure behavior before implementation. Keep backend business rules, authorization and financial authority on the server.
4. Implement the smallest complete change using strict TypeScript and existing conventions.
5. Run the project's actual typecheck, lint, unit/component tests and build where applicable; add browser evidence for critical flows when available.
6. Report real checks and NOT_RUN items. Do not claim visual/accessibility/performance quality that was not measured.

## Reference routing
- HTTP/Axios, TanStack Query, query keys, mutations, caching, BFF requests: [server-state-api.md](references/server-state-api.md)
- React Hook Form/Zod, validation, local/global state, effects, money/date input: [forms-state.md](references/forms-state.md)
- Feature structure, components/hooks, React Router, performance, semantic UI: [architecture-routing.md](references/architecture-routing.md)
- RTL/MSW/Playwright/axe and frontend evidence: [testing-accessibility.md](references/testing-accessibility.md)
- Session cookies, CSRF, CORS, token storage or login/logout: [browser-csrf-cors](../application-security/references/browser-csrf-cors.md) and, for BFF identity flows, [bff-keycloak](../application-security/references/bff-keycloak.md)

## Core constraints
- Do not store or refresh OAuth access/refresh tokens in React for the BFF architecture. Auth comes from the backend session contract such as `/api/auth/me`.
- Do not use `useEffect + useState` as the default server-fetch pattern when TanStack Query already owns that concern.
- Do not put local UI state into TanStack Query or a global store without a cross-component ownership need.
- Axios is the project HTTP standard when selected, not a reason to create wrappers around every call or hide business behavior in interceptors.
- React Hook Form/Zod are for forms that benefit from them; do not add ceremony to trivial input.
- Client-side route guards/button hiding are UX only, never authorization.
- Avoid speculative abstractions, generic CRUD frameworks and blanket memoization.
- Preserve exact money/date semantics from the API. Do not calculate authoritative taxes in React.

## Completion
Return changed frontend areas; interaction/error states covered; actual type/lint/test/build commands and results; accessibility/browser checks actually run; and remaining risks. For auth/session changes require the corresponding security review; for ordinary frontend work use frontend review only when the risk/workflow calls for it.
