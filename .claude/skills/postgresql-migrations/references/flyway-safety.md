# Flyway migration safety

Use for schema/data changes that must survive upgrades of an existing database. Treat migration history as an immutable deployment record.

## Versioned migrations
- Add a new versioned migration for a new change. Do not edit a versioned migration after it has reached a persistent downstream environment; Flyway tracks checksums.
- Run `validate` in the delivery path before migrate where the project tooling supports it.
- Use repeatable migrations only for objects/reference definitions that are intentionally re-applied when their checksum changes. Make them safe to execute repeatedly.
- Keep one source of truth and the same migration ordering across environments. Environment-specific business schema drift requires explicit design, not hidden local SQL.

## Expand / migrate / contract
For a breaking change across independently deployed app/database versions:
1. Expand: add compatible columns/tables/indexes first; avoid making old code fail.
2. Migrate: backfill in bounded batches with restart/reconciliation rules; dual-read/write only when truly needed and time-box it.
3. Switch: deploy code using the new shape and verify production-like behavior.
4. Contract: remove old structures only after no supported application version relies on them.

Do not combine a destructive drop/rename with the first application version that stops using the old shape unless the deployment model proves no overlap.

## Locks, indexes and large tables
- Estimate affected rows and lock behavior before production-oriented migrations.
- Do not assume a DDL statement is harmless because it is one line.
- Use PostgreSQL-specific online/concurrent index techniques only when their transaction restrictions and Flyway execution mode are understood and tested.
- For large backfills, separate schema change from data migration when that reduces lock/rollback risk.
- Keep migration transactions short enough for the environment; do not call external services from a database migration.

## Data integrity and recovery
- Add NOT NULL/UNIQUE/FK/CHECK constraints from verified business invariants, considering existing invalid rows first.
- A down script is not a backup. Destructive data loss needs backup/restore or another explicit recovery mechanism.
- Test both an empty schema and upgrade from the supported previous state with representative synthetic data.
- Verify application compatibility before and after migration, including rollback/roll-forward expectations.

## Evidence
Report exact migration files, source schema version, Flyway validate/migrate results, PostgreSQL version used, lock/backfill risks and whether restore was exercised. Missing real-PostgreSQL execution is NOT_RUN, not a pass.

References:
- Versioned migrations: https://documentation.red-gate.com/fd/versioned-migrations-273973333.html
- Repeatable migrations: https://documentation.red-gate.com/fd/repeatable-migrations-273973335.html
- Validate command: https://documentation.red-gate.com/flyway/reference/commands/validate
