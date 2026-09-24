# JPA identity, lifecycle and query behavior

Apply to actual JPA changes, not plain JDBC or every backend edit. Inspect the exact
Boot-managed Hibernate/Jakarta/Spring Data versions and existing entity conventions first.
Keep API types, aggregate boundaries and ID contracts unless the task authorizes a change.

## Identity and state
- Model persistent entities as identity-bearing objects, not automatically as records or
  Kotlin data classes. Keep the no-arg constructor and proxy/instantiation model compatible
  with the actual provider; avoid broad Lombok `@Data`, public setters and mutable equality.
- Initialize collections. Add behavior methods where they protect invariants; do not create
  an elaborate domain model for a simple lookup record. Never invent financial constraints.
- Choose equality deliberately. A natural key must truly be immutable and constrained in
  the DB; mutable email is NOT a safe identity default. Otherwise preserve object identity
  or the established generated-ID pattern. Verify symmetry, proxy/detached behavior and hash
  collection membership before/after persistence. Never include mutable associations.
- For assigned IDs, verify Spring Data new-state detection. A nullable wrapper `@Version`
  is inspected before the ID; a primitive version does not supply this signal. Where a
  version is appropriate leave it provider-managed. Otherwise use a correctly implemented
  `Persistable` lifecycle or an explicit persist path. Do not add @Version merely as ceremony.
- After merge/save use the returned managed instance when needed; do not assume the supplied
  detached object became managed. `save`/`flush` is not evidence that commit succeeded.
- Use enums with an explicit stable mapping. String names also need migration planning when
  renamed. Avoid new ordinal mappings; preserve existing data through a deliberate migration.

## Relationships, page queries and batching
- Specify ownership, cascade and orphan removal from the child's real lifecycle. Do not
  cascade remove into independently owned shared data. Maintain both sides when bidirectional
  navigation is needed; avoid large graphs when an ID reference is enough.
- Select bounded data with an intentional fetch plan. Do not make all associations EAGER to
  fix lazy loading. Check to-one lazy behavior against the provider and mapping, not just annotations.
- Prefer DTO projections for list views where possible. Count queries, aggregates and exports
  must carry the same owner/tenant predicate as the data query. Never filter ownership in memory.
- Do not combine a collection fetch join/entity graph with pagination without demonstrating
  correct row limits, counts and bounded query behavior. Use a projection or page root IDs
  first and fetch bounded details second, then restore order and scope to the same owner.
- Use deterministic sorting with a tie-breaker. Normal offset paging is fine for bounded UI
  pages. Adopt keyset paging for a demonstrated need; bind the cursor to filter/owner scope,
  validate it, and document effects of concurrent inserts/updates. Test ties and page boundaries.
- Verify the number/shape of SQL queries with a clear persistence context and cache assumptions.
  A warm first-level cache or mock repository must not hide an N+1 regression.
- Match indexes to predicates and ordering; inspect plans using representative synthetic data.
  Do not invent an optimal index from column names alone.
- For required bulk throughput, verify whether the ID strategy allows actual JDBC batching.
  Do not migrate public IDs to UUID merely to copy an example. Configure measured batch sizes,
  deliberate flush/clear boundaries and database limits; `saveAll` is not proof of one SQL batch.
- Bulk JPQL/native writes bypass parts of entity lifecycle/version handling: reconcile the
  persistence context, authorization, audit and concurrency contract explicitly.

## Concrete query shape (illustrative, compile against the selected application)
```java
// Owner is resolved server-side; this query alone does not implement authentication.
Optional<Entry> findByIdAndOwnerId(UUID id, UUID ownerId);
Page<EntrySummary> findByOwnerIdAndBusinessDateGreaterThanEqualAndBusinessDateLessThan(
    UUID ownerId, LocalDate fromInclusive, LocalDate toExclusive, Pageable pageable);
```
`EntrySummary` must be a projection matching the real mapping. Bound page size and allowlist
sort fields. Choose the next month's first day as an exclusive date boundary for a monthly view.
Do not add an unscoped `findById` fallback when the owner-scoped lookup returns empty.

## Required evidence when affected
Verify persist/load/update/delete through the real provider and PostgreSQL; include DB constraints,
assigned-ID state, proxy/equality behavior where relied on, two competing edits for an optimistic
version policy, actual pagination/count scope, and query growth with multiple parent records.
Do not require tests for features that do not exist. Use NOT_APPLICABLE with an activation trigger.

Adapted selectively from [upstream spring-data-jpa](https://github.com/rrezartprebreza/spring-boot-skills/blob/f0c06a01b0b7571b519cd43e16692b2483a24514/skills/spring-boot-4/spring-data-jpa/SKILL.md).
Retain [upstream MIT notice](../LICENSE-UPSTREAM.txt). Primary source, accessed 2026-09-23:
[Spring Data entity state](https://docs.spring.io/spring-data/jpa/reference/jpa/entity-persistence.html).
