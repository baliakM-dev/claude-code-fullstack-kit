# Forms, validation and client state

Use this reference for forms, validation, state placement and user-input workflows.

## State ownership
Classify state before selecting a library:
- server state -> TanStack Query when caching/lifecycle is useful;
- form state -> React Hook Form (or the project's established form library) for nontrivial forms;
- local ephemeral UI state -> `useState`/`useReducer`;
- cross-feature client state -> Context or a dedicated store only when ownership truly spans features and prop composition is not clearer.

Do not introduce Zustand/Redux/Context for state that belongs to one component or one form. Do not mirror query data into local state unless the UI intentionally creates an editable draft with explicit synchronization semantics.

## Forms
For medium/large forms, prefer React Hook Form with schema validation such as Zod when the project has selected them. Small forms may stay simple; do not add a dependency for one checkbox.
- Define request DTO/schema at the boundary; avoid one mega-schema shared across unrelated screens.
- Keep server validation authoritative. Client validation improves UX but does not replace backend validation.
- Map field-level backend errors back to fields; show global errors separately.
- Preserve user input after recoverable failures.
- Prevent accidental duplicate submissions in the UI, but do not claim this replaces server idempotency for financial or externally visible effects.
- Disable/lock only the affected submit action while pending; retain accessible status feedback.

## TypeScript
- Keep `strict` enabled. Avoid `any`, double assertions and broad `as` casts as escape hatches.
- Treat external data as untrusted. Static TypeScript types do not validate runtime JSON; add runtime parsing where contract risk justifies it.
- Prefer discriminated unions for explicit UI states when they reduce impossible combinations.
- Do not create generic form/CRUD abstractions before repeated stable requirements exist.

## Derived state and effects
- Derive values during render when possible instead of synchronizing duplicated state with an effect.
- Use effects for synchronization with external systems, subscriptions or imperative APIs. Clean them up and handle stale/cancelled work.
- Do not use an effect merely to transform props/query data into another state variable.

## Money and dates
- Never use JavaScript floating-point arithmetic as the authority for tax/accounting results.
- Preserve decimal strings or exact minor units according to the API contract.
- Keep date-only business values distinct from timestamps/time zones. Do not silently convert a date-only value through local timezone serialization.

Primary sources:
- https://react.dev/learn/you-might-not-need-an-effect
- https://react-hook-form.com/get-started
- https://zod.dev/
