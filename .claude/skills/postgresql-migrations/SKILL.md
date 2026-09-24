---
name: "postgresql-migrations"
description: "Design and review PostgreSQL schemas, queries, ownership boundaries and versioned migrations. Use for data-model changes, Flyway migrations, indexes, transaction conflicts, owner-scoped CRUD, JPA entity lifecycle/queries, backfills and database restore considerations."
---

# PostgreSQL and migrations

Read the existing schema, migrations, data ownership, affected queries and deployment sequence. A fresh database and an existing production database require different evidence.

## Select additional detail only when relevant
- Relational design, functional dependencies, 3NF/BCNF or deliberate denormalization: [normalization.md](references/normalization.md).
- Flyway rollout, checksums, repeatable migrations, expand/contract or destructive changes: [flyway-safety.md](references/flyway-safety.md).
- JPA entity lifecycle, assigned IDs, query plans, projections, pagination or batching: [jpa-modeling.md](references/jpa-modeling.md).
- Required duplicate command/replay protocol: [idempotent-commands.md](../spring-backend/references/idempotent-commands.md).
- Failure propagation, audit or transaction retries: [transaction-failure-patterns.md](../spring-backend/references/transaction-failure-patterns.md).
- For SQL/locking/framework tests, use [spring-data-evidence.md](../test-verification/references/spring-data-evidence.md).

## Schema and authorization
- For transactional relational tables, identify candidate keys and material functional dependencies before finalizing the shape. Check at least 3NF; inspect BCNF when determinants/candidate keys overlap. Do not normalize or denormalize mechanically; document deliberate exceptions and their consistency mechanism.
- Model amounts, currency, timestamps and business dates explicitly. Prefer NUMERIC with documented precision/scale for decimal rules; choose types from domain requirements.
- Enforce not-null, foreign-key, uniqueness and check constraints where they express real invariants. Cover ownership in queries for reads, updates, deletes, list counts, exports and jobs.
- Parameterize values. Allowlist dynamic sort/filter identifiers. Do not load a global object and assume a URL or UI supplied a trustworthy owner.
- Derive internal identity from the authenticated issuer/subject mapping; do not use mutable email as the ownership key.
- Treat PostgreSQL RLS as an additional design choice, not an automatic substitute for application authorization. Verify role bypass, table-owner behavior and pooled connection state before relying on it.

## Migration workflow
For any nontrivial Flyway change read [flyway-safety.md](references/flyway-safety.md).

1. Add a versioned migration. Do not edit an applied migration to change its checksum. A local disposable prototype reset needs explicit local-only approval.
2. Evaluate existing rows, defaults, backfill size, lock duration, indexes and compatibility with both old and new code during rollout.
3. Prefer expand/contract for breaking changes. Document destructive impact and a recovery plan; a down migration is not automatically data recovery.
4. Run from an empty schema and from the supported previous schema with representative synthetic data. Check constraints and new behavior, not just that SQL parses.
5. Test real PostgreSQL behavior for transactions, concurrent writes and SQL. H2 compatibility is not evidence for a PostgreSQL-specific invariant.
6. Keep runtime credentials less privileged than migration/admin identities where operationally feasible. Never expose database ports publicly or retrieve production records to make a test pass.

Inspect query plans and representative size when performance is at issue. Avoid adding indexes by intuition alone or claiming performance from tiny fixtures.

Return migration risk, actual checks, rollback/roll-forward implications and independent-review status.

Primary sources:
- https://www.postgresql.org/docs/current/ddl-constraints.html
- https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- https://www.postgresql.org/docs/current/mvcc.html
- https://docs.spring.io/spring-boot/reference/testing/testcontainers.html
