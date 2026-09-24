# Idempotent commands: explicit contract, not a global filter

Use when a task requires safe retries, duplicate-submit handling, imports or duplicate messages.
Do not add an idempotency framework to every endpoint or bootstrap. Distinguish protecting a
business uniqueness invariant from replaying one client's repeated command.

## Define the contract first
- Resolve authenticated owner/tenant server-side. Scope a key by that identity AND operation
  (including its contract version). Bound key/payload/response sizes and retention. A client key
  or fingerprint is not an authorization credential; authorize before execution AND replay.
- Specify missing key, same key/same payload, same key/different payload, in-progress work,
  expiry and changed permissions. Decide which outcomes are retained and their response codes.
- Canonicalize validated business fields, not raw JSON order. Decide numeric, whitespace,
  Unicode, date/time and omitted/null semantics explicitly. Include all fields affecting the
  operation and its version. Never hash a floating-point conversion of a financial amount.
- Reusing a key with changed intent must conflict, not return a misleading successful result.
  Fingerprints are equality checks, not encryption; low-entropy fields can still be sensitive.

## Database-local protocol
Use the [PostgreSQL reference](../assets/idempotency/request-results.sql) only after adapting
identity types and constraints; it is NOT an applied application migration.
1. Start an authorized, bounded transaction using the SAME DB/transaction manager as the write.
2. Claim `(owner, operation, key)` with INSERT ON CONFLICT DO NOTHING RETURNING. Enforce the
   uniqueness in PostgreSQL, not a check-then-insert or a JVM/Redis cache alone.
3. If claimed, apply the business mutation and persist a bounded immutable response snapshot
   before commit. Roll back the claim with the mutation on failure. Do not commit an unfinished
   claim in this single-transaction design.
4. If not claimed, in READ COMMITTED read the scoped row with a subsequent statement, compare
   the fingerprint and replay the stored result only when authorized and matching. A competing
   insert may block; bound lock/statement/transaction time and define a retryable timeout outcome.
5. Never catch a uniqueness exception and continue in an aborted transaction. Under stronger
   isolation retry the whole transaction where appropriate, not one statement in a stale snapshot.
6. Keep retention cleanup from racing active claims/replays. A missing row after conflict is not
   permission to guess success; retry the whole bounded protocol or return the agreed conflict.

For a workflow that intentionally commits IN_PROGRESS separately, design leases, ownership,
recovery and fencing; the simpler single-transaction protocol above does NOT provide those.
Only store allowlisted response fields/headers. Never retain Set-Cookie, tokens, authorization
headers, stack traces or current session material. Revalidate access to the referenced resource
before replay if the authorization policy can change. Idempotency is not a bypass around CSRF.

## External effects and expiration
Use durable intent plus an independently retryable worker for required external effects.
Use provider idempotency and reconciliation for uncertain outcomes. Define consumer/event
uniqueness and acknowledgment-after-commit for message handling. No exactly-once promise.
Deleting an expired key permits another execution: retain separate business uniqueness rules
where necessary and align retention with actual retry promises and data protection requirements.

## Concrete bounded example
[CommandFingerprint.java](../assets/idempotency/CommandFingerprint.java) demonstrates ONLY a
versioned, deterministic fingerprint for an example EUR received-amount command and a typed
owner/operation/key value. It does not persist claims, authenticate callers, implement CSRF,
store results, or coordinate concurrency. Its stated validation is an EXAMPLE API contract,
not tax logic or a replacement for the application's chosen amount/description rules.
[Its tests](../assets/idempotency/CommandFingerprintTest.java) run using
[verify-java-examples](../scripts/verify_java_examples.py), with a JDK and no downloaded libraries.
Do not mistake passing those tests for verified PostgreSQL or Spring behavior.

## Required integration evidence
For an implemented idempotent endpoint run simultaneous identical commands, changed-payload
conflict, owner and operation separation, rollback after claim, lost-response replay, bounded
wait and retention scenarios against real PostgreSQL. Assert one committed business effect,
not merely two matching HTTP statuses. With session authentication give both authorized requests
valid CSRF tokens. Test denied replay with changed authorization without exposing the snapshot.

Adapted from [upstream idempotency-patterns](https://github.com/rrezartprebreza/spring-boot-skills/blob/f0c06a01b0b7571b519cd43e16692b2483a24514/skills/spring-boot-4/idempotency-patterns/SKILL.md)
and its SQL example. Retain [upstream MIT notice](../LICENSE-UPSTREAM.txt).
Primary references, accessed 2026-09-23:
[INSERT](https://www.postgresql.org/docs/current/sql-insert.html),
[Isolation](https://www.postgresql.org/docs/current/transaction-iso.html).
