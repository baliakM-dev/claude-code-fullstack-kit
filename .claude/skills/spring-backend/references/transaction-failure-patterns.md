# Transaction failures, retries and durable outcomes

Use for changed multi-write invariants, optimistic conflicts, propagation, audit or commit-bound
side effects. Build on api-transactions.md; do not replace working repository transaction semantics.

## Verify actual transaction participation
- Identify the transaction manager, call path and participating resources. Separate logical
  REQUIRED scopes from the physical transaction. An inner failure caught by the caller can
  leave the transaction rollback-only; catching it does not repair it.
- A persistence conflict may surface at flush or commit. Keep success response generation and
  evidence consistent with actual commit, not merely a returned repository save call.
- For optimistic-lock/deadlock/serialization retries, first decide whether automatic retry
  preserves the API contract. A user's stale version/If-Match conflict may need a conflict
  response, not automatic replay that overwrites a newly edited value.
- When retry is correct, retry the complete unit in a fresh transaction with a fresh read,
  bounded attempts/backoff and an explicit exception policy. Keep the retry boundary outside
  any ambient transaction so REQUIRED does not rejoin the failed transaction. Cover commit
  failures too. Never use noRollbackFor to revive an aborted persistence transaction.
- Use supported retry facilities for the selected Framework version; retain existing compatible
  infrastructure outside the change scope. A shared annotation name is not proof of compatible
  imports/options. Do not add retry or concurrency-limiter dependencies without a real need.

## Success audit versus attempted work
Write a success audit and its local business mutation in the SAME transaction when they must
agree. Reserve independent commits for explicitly defined attempt/failure records. Do not make
an independent audit transaction reference a not-yet-committed parent or assert success that may
roll back. Review extra REQUIRES_NEW connections, lock waits and pool capacity.

Illustrative split, not a compiled application template:
```text
non-transactional retry coordinator (only for retryable contract)
  -> proxied transactional business operation
       -> freshly read owner-scoped data
       -> business mutation + success audit
       -> commit (failure must reach the coordinator)
  -> return success after the transaction completed
```

## Events and remote effects
AFTER_COMMIT can prevent a local listener from running on rollback; it does not make delivery
durable. @Async is not persistence. For required delivery use the existing durable mechanism or
write outbox intent atomically with the business mutation, dispatch outside that transaction and
handle redelivery. Do not introduce Kafka or an outbox for a disposable UI notification.

A remote timeout does not establish failure at the provider. Use provider-supported idempotency,
reconciliation and explicit states for irreversible operations. A DB transaction cannot roll back
an external payment/email. Do not save failure state then erase it by throwing from the same TX.

## Evidence
Test through Spring proxies. Observe committed data from another transaction, not only the
test's rollback scope. Cover conflicting edits, commit-time errors, success-audit rollback,
inner rollback-only propagation and missing delivery after a crash where durability is required.
Use barriers/latches and distinct connections; arbitrary sleep or mocked conflicts are insufficient.

Adapted from [upstream transactional-patterns](https://github.com/rrezartprebreza/spring-boot-skills/blob/f0c06a01b0b7571b519cd43e16692b2483a24514/skills/spring-boot-4/transactional-patterns/SKILL.md).
Retain [upstream MIT notice](../LICENSE-UPSTREAM.txt). Primary references, accessed 2026-09-23:
[Propagation](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/tx-propagation.html),
[Commit-bound listeners](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/event/TransactionalEventListener.html).
