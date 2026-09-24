# Relational normalization and schema quality

Use normalization as a design check, not as a score. Start from the domain, candidate keys and functional dependencies. Preserve a simpler correct schema rather than decomposing tables mechanically.

## Baseline
1. Identify the row's meaning and candidate keys before choosing a primary key. A surrogate key does not remove natural-key or uniqueness constraints.
2. Record material functional dependencies for business data that can drift when duplicated.
3. Check 1NF/2NF/3NF for transactional tables. For 3NF, non-key facts should describe the key, the whole key and not another non-key fact.
4. Check BCNF when overlapping candidate keys or unusual dependencies exist. A determinant that is not a superkey is a warning to inspect. Do not decompose blindly if it destroys an important dependency or creates an impractical write model.
5. Prefer lossless decomposition. Preserve dependencies in constraints when practical; where the database cannot express a cross-table invariant directly, define which application or process owns it and how it is tested.
6. Do not create one table per concept word. Cohesion, write consistency, query patterns and lifecycle matter.

## Common problems
- Store the same descriptive fact in multiple transactional rows when it has one authoritative owner.
- Store derived totals as authoritative facts without a documented recomputation/invalidation contract.
- Use comma-separated or JSON arrays to avoid a real relationship when individual values need constraints or joins.
- Put unrelated optional concepts into one sparse table merely to avoid joins.
- Use a surrogate primary key but omit a real business unique constraint.
- Model many-to-many business relationships with attributes without an explicit join entity/table.

## Deliberate denormalization
Denormalization is allowed for a measured read/performance need, analytics/read models, snapshots or immutable historical evidence. Before adding it, document:
- authoritative source;
- duplicated/derived fields;
- update or rebuild mechanism;
- stale-data tolerance;
- failure/reconciliation path;
- evidence that normalization or a normal index/query design is insufficient.

A read model, materialized view or immutable calculation snapshot can legitimately duplicate data. Do not call that a 3NF defect when duplication is the declared contract.

## Review evidence
For a changed schema, reviewer should be able to state:
- row meaning and candidate key(s);
- important functional dependencies;
- constraints enforcing identity/ownership/invariants;
- any 3NF/BCNF exception and its reason;
- migration path from existing data;
- affected query/index strategy.

Reject a finding that only says "not BCNF" without the concrete dependency, anomaly and correction tradeoff.

References:
- PostgreSQL constraints: https://www.postgresql.org/docs/current/ddl-constraints.html
- PostgreSQL generated columns: https://www.postgresql.org/docs/current/ddl-generated-columns.html
