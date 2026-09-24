# Frontend testing and accessibility evidence

Use this reference when implementing or reviewing significant frontend behavior.

## Test levels
- Unit: pure formatters, parsers and domain-free utilities.
- Component/integration: React Testing Library with MSW or equivalent at the network boundary. Test user-visible behavior rather than component internals.
- Browser/E2E: Playwright for critical flows such as BFF login handoff, session expiry, profile completion and protected navigation.
- Accessibility: semantic assertions plus axe where available; automated checks do not replace keyboard/focus/manual review for important screens.

## Required behavioral states
Select relevant states, not a universal checklist:
- initial/loading;
- empty;
- success;
- validation error;
- network/timeout/server error;
- unauthenticated/session expired;
- forbidden;
- conflict/stale update;
- mutation pending and duplicate-click prevention;
- retry/recovery;
- logout/account switch cache clearing.

For BFF auth, mocked `/api/auth/me` component tests are useful but do not prove real OIDC redirects, cookie attributes, CSRF lifecycle or Keycloak integration. Keep those as separate browser/integration evidence.

## Review traps
Reject tests that only assert implementation details such as hook call counts or CSS class names when user behavior is the contract. Avoid snapshot-only coverage for interactive flows. Ensure a negative fixture can fail when the relevant bug is introduced.

Primary sources:
- https://testing-library.com/docs/guiding-principles
- https://playwright.dev/docs/intro
