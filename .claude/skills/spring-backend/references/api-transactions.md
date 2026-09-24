# API and transaction review

Define request/response types, nullability, accepted ranges, field lengths and error semantics. Use stable error codes without stack traces or secrets. Bound page size and sorting choices. Do not bind arbitrary entity fields from a request. Prefer explicit mapping; add MapStruct only when it improves this codebase.

Review null inputs, optional database results, empty collections, partial external responses and serialization. Do not turn every absent value into an empty string or default number. Treat missing data according to the business contract.

Test the transaction boundary as it actually runs through Spring. A same-object invocation can bypass a proxy. A readOnly hint is not access control. Know rollback semantics for the actual exception and version. Do not swallow a failure and accidentally commit half an operation.

Enforce uniqueness and integrity in the database as well as the application. Check-then-insert alone is racy. Use optimistic/pessimistic concurrency or an atomic SQL operation only where the invariant needs it. Map conflicts predictably. Do not add a JVM lock and claim it protects multiple instances.

Avoid lazy loading through JSON serialization or uncontrolled N+1 queries. Select required fields and test meaningful query behavior; do not replace all lazy associations with eager loading. Keep external I/O out of long database transactions.

Use BigDecimal or an appropriate explicit money type for financial values. Do not construct a decimal from a binary floating-point calculation. Separate accounting dates from event timestamps.

Primary sources:
- https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html
- https://docs.spring.io/spring-data/jpa/reference/jpa/transactions.html
- https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/math/BigDecimal.html
