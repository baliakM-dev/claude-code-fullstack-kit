# Verification levels in kit 1.3.0

## Shipped, executable Java example
From the kit root, after inspecting the files, run:
```sh
python .claude/skills/spring-backend/scripts/verify_java_examples.py
```
Requires Python 3.10+ and JDK 17+ (java and javac on PATH). No Maven/Gradle, downloaded JARs,
secrets, network, containers or database. Compiles the actual two shipped source files with
`--release 17 -Xlint:all -Werror` in a temporary directory and runs 20 explicit scenarios.
Missing prerequisites exit 2/NOT_RUN; failed compilation, missing scenario marker or assertion
exits 1. The root kit linter does not run this automatically.

The example verifies a deterministic, versioned, length-prefixed fingerprint and a typed scoped
key value. The independent known-vector test was calculated using Python hashlib/struct, not
by calling the Java implementation. It does NOT prove absence of cryptographic collisions,
authorization, database idempotency, CSRF, JPA, Spring transactions, NullAway or tax correctness.

The example contract is intentionally small: positive EUR amounts, 12 integral digits maximum,
exact cents with no rounding (precision and absolute scale each at most 64), a LocalDate and exact bounded Unicode text. Do not silently
substitute those sample constraints for a different application or financial-rule contract.

## PostgreSQL/Spring and nullness checks still required in the application
The SQL in `.claude/skills/spring-backend/assets/idempotency/request-results.sql` is a reference,
NOT a Flyway migration or completed idempotency endpoint. It is not run by the Java helper.
JPA/MockMvc/JSpecify snippets in Markdown are illustrative and not in the compile set.

During the relevant task, compile real application classes against its selected Boot BOM,
activate a compatible nullness checker with a positive and negative fixture, and run real
PostgreSQL concurrency/migration and Spring/BFF tests. See
[Spring/Data evidence](../.claude/skills/test-verification/references/spring-data-evidence.md).
Do not use H2, a Java map or a mock as proof of the PostgreSQL claim protocol.

## Model evaluations are separate
`evals/community-patterns.json` defines scenarios. It does not invoke a model. No A/B quality,
safety or token-saving benchmark is claimed. Preserve original inputs and independent criteria
and record actual isolated Claude Code runs separately if/when explicitly requested.
