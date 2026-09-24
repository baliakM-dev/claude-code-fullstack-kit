# React architecture and routing

Use this reference for feature structure, routing, component boundaries and performance decisions.

## Feature structure
Prefer feature/domain-oriented code for growing applications, for example:

```text
src/
  app/
  features/
    auth/
      api/
      components/
      hooks/
      types/
    profile/
    incomes/
  shared/
```

Do not force this exact tree into an established project. Preserve coherent existing conventions. Shared folders should contain genuinely cross-feature code, not become a dumping ground.

## Components and hooks
- Keep components focused on rendering/interaction. Move reusable data access or workflow logic to feature hooks/services only when it improves clarity.
- Avoid giant page components, but do not split every ten lines into a new component.
- Prefer composition and explicit props. Context is appropriate for stable cross-tree concerns, not as default state storage.
- Custom hooks must represent reusable React behavior; do not create wrappers that simply rename `useState` or one API call without value.

## Routing
Use the project's React Router mode deliberately. Declarative mode is enough for ordinary client routing; Data/Framework mode adds loaders/actions/pending APIs but also changes ownership of data fetching. Do not mix router loaders and TanStack Query for the same resource without a defined integration strategy.
- Route protection in React is UX/navigation only. Backend authorization remains mandatory.
- Handle deep links, refresh, not-found and unauthenticated redirects without loops.
- Lazy-load meaningful route/feature boundaries when bundle size justifies it; do not fragment tiny modules for theoretical performance.

## Performance
- Measure first. Do not add `useMemo`, `useCallback` or `React.memo` everywhere.
- Fix unnecessary network requests, unstable query keys, oversized payloads/lists and expensive rendering before blanket memoization.
- Paginate or virtualize large lists based on measured need.
- Preserve TanStack Query structural sharing unless there is evidence it is a problem.
- Do not introduce a global cache/store merely to avoid prop passing in a small tree.

## Accessibility
Use semantic HTML, associated labels, keyboard access, visible focus, correct button/link semantics and accessible error/status announcements. Do not replace semantic elements with clickable `div`s.

Primary sources:
- https://react.dev/learn/thinking-in-react
- https://react.dev/reference/react/useMemo
- https://reactrouter.com/start/modes
