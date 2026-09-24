# Spring/Data verification without misleading green tests

Apply to Java/Spring persistence, null contracts, transaction failures or idempotent commands.
Choose evidence by risk, not a fixed 70/20/10 pyramid, global coverage target or assertion library.
Use the project's selected Boot 4 dependencies/imports; do not copy Boot 3 test starter packages.

| Risk | Minimum meaningful mechanism check |
| --- | --- |
| JPA identity/state | Assigned/generated ID through persist/load, actual version progression and equality behavior if relied upon. |
| Query growth | Flush/clear persistence context, vary parent/child count, observe SQL/fetch plan without cache masking. |
| Paging and ownership | Stable tie-breaker, first/next pages, matching count/filter/owner scope and no accidental collection-fetch in-memory paging. |
| Nullness checker | Intended real package checked, broken fixture rejected with relevant diagnostic, corrected fixture accepted. |
| Transaction retry | Fresh read/TX per eligible attempt, commit-time conflict observed, no silent overwrite of client stale-version semantics. |
| Success audit | Business row and success audit commit or roll back together; attempts are not recorded as completed outcomes. |
| Duplicate command | Coordinated concurrent transactions yield one business effect; payload conflict, replay and owner separation verified. |
| Durable event | Rolled-back mutation emits nothing; committed intent survives restart; duplicate worker execution handled. |

## HTTP security controls
For session/BFF slice tests, use the real relevant filter chain and the application's authority
mapping. Mocked authentication proves only that mocked scenario. A valid mutation needs valid
CSRF as well as identity; absence tests should omit/alter CSRF deliberately, not disable it.

Illustrative MockMvc fragment (not a complete compiled test here):
```java
mvc.perform(post("/api/entries")
        .with(oidcLogin()) // adapt issuer/subject and authorities to the real local mapping
        .with(csrf().asHeader())
        .contentType(APPLICATION_JSON)
        .content(validBody))
    .andExpect(status().isCreated());
```
Use imports for the selected Spring Security test library. Keep real browser acquisition and
renewal of CSRF and real Keycloak OIDC tests separate; this helper does not verify either.
A cross-owner denial test uses a real target record, a valid other-user identity and valid CSRF,
then checks persisted data was unchanged. Missing CSRF must not hide missing authorization.

## Database and lifecycle controls
Use the actual PostgreSQL engine with synthetic data. Test empty-schema migration and upgrade
from the supported prior schema. Coordinate contention with separate connections and a barrier;
verify committed data outside any auto-rollback test transaction. A transaction-wrapped test can
hide AFTER_COMMIT listeners, deferred constraints and false success audit rows.

Keep database/container lifecycle aligned with Spring's context cache and isolate test data.
Select Testcontainers packages from the actual BOM/version; never infer artifact coordinates
from an old tutorial. Do not use H2 as proof of PostgreSQL locking or ON CONFLICT behavior.

## Source/test linkage
Compile/test the same files shipped as executable examples, not a second handwritten copy.
List exactly which illustrative snippets are outside that compile set. Use negative fixtures
that fail for the intended diagnostic, not for missing dependencies, syntax errors or zero tests.
Record command, JDK/dependencies/DB version, scenario count and unexecuted scope separately.
The kit's Python routing checks, its Java helper tests, the application's integration suite and
AI behavior evaluations are four different evidence levels. Never sum them into one quality score.

Selectively adapted from [testing-pyramid](https://github.com/rrezartprebreza/spring-boot-skills/blob/f0c06a01b0b7571b519cd43e16692b2483a24514/skills/spring-boot-4/testing-pyramid/SKILL.md)
and [verification approach](https://github.com/rrezartprebreza/spring-boot-skills/blob/f0c06a01b0b7571b519cd43e16692b2483a24514/verification/README.md).
Retain [upstream MIT notice](../LICENSE-UPSTREAM.txt). Primary reference, accessed 2026-09-23:
[Spring Security CSRF tests](https://docs.spring.io/spring-security/reference/servlet/test/mockmvc/csrf.html).
