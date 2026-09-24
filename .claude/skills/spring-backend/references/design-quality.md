# Design quality: SOLID with evidence, not ceremony

Use this as the single Spring/JVM design standard for implementation and independent review. Apply it to the affected scope, not as permission for a whole-project rewrite. Preserve verified project decisions and the shared safety policy. Resolve conflicts explicitly; never bypass security, correctness or required verification to satisfy a style preference.

## Goal and proportionality
Aim for correct, secure, readable, changeable and testable code with justified complexity. Do not claim senior-level quality from a checklist alone. Before a nontrivial change identify the behavior, invariants, ownership, failure modes and boundaries that actually matter. Reuse the task plan; do not generate another architecture document for routine work.

Use domain names and coherent modules. Create API/application/domain/infrastructure subdivisions only where they separate real responsibilities; retain a suitable existing layout. Do not force Clean Architecture, DDD, CQRS, microservices or a generic framework into every feature. Record consequential tradeoffs in the project's existing decision format, briefly.

## SOLID as concrete decisions
| Principle | Apply to the changed code | Avoid |
| --- | --- | --- |
| S - Single Responsibility | Group behavior that changes for the same business/technical reason. Separate HTTP handling, business decisions, external integration and persistence when they change independently. A cohesive class may have multiple methods. | A controller calculating, persisting, exporting and emailing; one class per tiny step; arbitrary method/line quotas. |
| O - Open/Closed | Isolate a demonstrated axis of variation behind a stable contract when it reduces repeated changes. Adding a supported variant should preserve existing behavior and tests. A bug fix can still modify existing code. | An engine/plugin/strategy for one case; a new calculator class for every year when only validated parameters differ; freezing a wrong abstraction. |
| L - Liskov Substitution | Define accepted inputs, outputs, errors and side effects of a shared contract. Implementations must preserve those guarantees: no stronger hidden preconditions or weaker postconditions. Test substitutability when multiple implementations exist. | Successful zero/default results for unsupported cases; surprise side effects; client type checks to repair an inconsistent contract. |
| I - Interface Segregation | Expose operations that the consuming use case actually needs. Split an interface when unrelated consumers or capabilities create real coupling. | A universal service exposing unrelated admin/export/payment operations; marker interfaces or one interface per method without a boundary. |
| D - Dependency Inversion | Keep core policy independent of transport and vendor-specific details at meaningful boundaries. Supply dependencies explicitly. One implementation may justify an interface for an external boundary or module contract. | An interface and Impl for every class; hiding SQL/HTTP details inside supposedly domain-facing contracts; a service locator; circular dependencies masked by indirection. |

When proposing an abstraction, name the current boundary, independent reason for change or concrete variant it protects. Use a plain class or function when it is enough. Do not create an interface merely to mock a simple implementation. Dependency injection does not by itself establish dependency inversion or authorization.

## Simplicity, duplication and readability
- KISS: choose the least complex complete solution, including its failure handling and tests. Prefer straightforward control flow over clever streams, reflection or generic dispatch that obscure behavior.
- YAGNI: implement the requested capability, not imagined providers, services or extension points. Do not omit current security, integrity or required error handling under the label of simplicity.
- DRY: centralize the same rule or contract when it has one owner. Similar-looking formulas with different legal/business meaning may remain separate. Do not merge them just because their current expressions match.
- Use names that explain domain intent, accepted units and time semantics. Keep public APIs narrow. Explain non-obvious constraints and why a decision exists, not every visible line of code.
- Prefer cohesive methods and explicit dependencies; treat excessive branching or dependencies as investigation signals, not universal numeric failure thresholds.
- Preserve correct code. For a refactor state the concrete problem, smaller alternative and regression evidence. Do not rewrite unaffected code or suppress a rule to produce a cleaner-looking diff.

## JVM and Spring quality baseline
- Use constructor injection for mandatory application dependencies; keep those references final where appropriate. Do not look dependencies up through ApplicationContext or hide a design cycle with setter injection or @Lazy. Honor legitimate framework/third-party lifecycle constraints with a specific explanation.
- Prefer immutable input/result objects and locally controlled state. A record/data class does not make referenced collections deeply immutable. Do not blindly make JPA entities records/data classes or all classes final; respect persistence, serialization and proxy requirements of the chosen versions.
- Keep controllers focused on HTTP adaptation and application calls. Keep business calculations out of controllers, DTO mappers and entity listeners. Do not add empty pass-through layers to satisfy a diagram. Respect the documented module API; avoid cross-module writes through another module's internal repository.
- Define nullability, missing values and invalid states at boundaries. Use typed DTOs for known schemas, explicit optional results and domain invariants. Never replace a failed lookup with a valid-looking zero/empty value. Check annotation semantics: a range constraint alone need not reject null. Preserve the distinction between absent PATCH fields and explicit null.
- Keep mutation and authorization explicit. Do not bind owner, role, audit or computed fields from arbitrary request data. Reuse the security and database skills for their authoritative rules; mapping is not authorization.
- Test actual transaction participation, exception/rollback behavior and concurrent writes for the affected use case. Self-invocation in proxy mode must not be mistaken for an intercepted transaction. Do not swallow errors and commit a partial operation. Read api-transactions.md for the detailed checks.
- Use a deliberate money/decimal and time contract. Keep computation deterministic with explicit input/rule/time snapshots and no hidden database or network calls. Do not replace validated financial semantics with a design-pattern preference; use the financial skill for its domain-specific verification process.
- Bound external I/O, queries and result sizes. Verify a suspected N+1 or concurrency problem through the relevant code path/test rather than prescribing caches, eager loading, locks or reactive code by default. Read integrations.md and the database skill when affected.
- Reuse supported framework behavior for errors, security and configuration. Add a library or override only with a demonstrated purpose, compatibility check and relevant tests. Keep logs useful without leaking secrets or personal payloads.

## Verification and exceptions
Select concrete evidence for each material risk: behavior/contract tests, a real mechanism integration test, or a meaningful architecture check. Use quality-verification.md for tool selection and non-vacuous checks. Do not make all five SOLID letters into mandatory test classes or a numeric score.

If a requested design departs from an established boundary, explain the conflict and smaller alternatives. An intentional exception needs affected scope, reason, risk and supporting evidence. Record a review trigger for a long-lived exception. Do not invent an exception or silently relax a gate to hide a failure. Raise unresolved correctness/security/data risks to the parent; retain unrelated safe work.

## Implementation and review contract
- Implementer: load this reference for a Spring/JVM code or design change. Before writing, select the relevant decisions and evidence from the task. After writing, check the changed code and impacted neighbors; retain relevant tests and the existing report format.
- Independent reviewer: read the same reference, original criteria and actual code. Check cohesion, module direction, contracts/substitutability, complexity and failure paths in the affected neighborhood. Do not inherit an implementer's self-assessment.
- A finding must name the location, concrete violated contract/criterion or risk, triggering scenario, impact, evidence and minimum useful correction. Preserve CONFIRMED / NEEDS_VERIFICATION / OPTIONAL categories. A bare 'violates SOLID' or preference for a pattern is not a blocking finding.
- In the existing completion report add only material design decisions, intentional exceptions and missing design evidence; normally a few lines, not a second report. For routine changes with no material design tradeoff omit a SOLID essay.
- Keep review scope and tool permissions unchanged. Read-only reviewers do not execute architecture tests or edit the source. Ask the parent for sanitized execution evidence or an authorized tester. Missing required execution is NOT_RUN / PARTIALLY_VERIFIED, not a pass.

## Contrasting examples (reasoning guidance, not application code)
| Situation | Expected decision |
| --- | --- |
| One cohesive service supports a single CRUD use case; no independent abstraction boundary is present. | Keep the concrete service; do not add ServiceInterface/ServiceImpl automatically. |
| A vendor HTTP integration leaks transport DTOs and retry decisions into core business rules. | Consider a narrow domain-facing boundary and adapter even with one vendor; explain the actual coupling being removed. |
| Two tax regimes happen to use an identical arithmetic expression today. | Keep their independent semantics and rule ownership; share only genuinely identical primitives. |
| A reviewer prefers a new pattern but demonstrates no defect or breached project decision. | Keep working code or report an OPTIONAL suggestion; do not block delivery. |

## Primary references
These sources support definitions and framework mechanisms. The scope, exception handling, reporting and proportionality rules above are this kit's engineering policy, not a vendor certification. Recheck version-sensitive details against the selected project baseline. Sources accessed: 2026-09-23.

- [SOLID definitions](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html)
- [Spring dependency injection](https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html)
- [Spring transaction interception](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html)
- [Spring Boot project structure](https://docs.spring.io/spring-boot/reference/using/structuring-your-code.html)
