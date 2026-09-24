-- REFERENCE ONLY: not a Flyway migration and not executed by the kit runner.
-- Adapted from rrezartprebreza/spring-boot-skills, commit f0c06a01b0b7571b519cd43e16692b2483a24514
-- skills/spring-boot-4/idempotency-patterns/examples/good-idempotency.sql
-- Copyright (c) 2026 Rrezart Prebreza. MIT notice: ../../LICENSE-UPSTREAM.txt
-- Changes: owner scope, hash/key bounds and response-pair consistency.
-- Identity is resolved server-side. Add the appropriate owner FK for the real schema.
-- Claim, business write and completed result MUST share one transaction and database.
CREATE TABLE request_results (
    owner_id UUID NOT NULL,
    operation VARCHAR(100) NOT NULL CHECK (length(operation) > 0),
    idempotency_key VARCHAR(128) NOT NULL CHECK (length(idempotency_key) > 0),
    request_hash VARCHAR(64) NOT NULL CHECK (request_hash ~ '^[0-9a-f]{64}$'),
    response_status INTEGER,
    response_body TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (owner_id, operation, idempotency_key),
    CHECK ((response_status IS NULL AND response_body IS NULL)
        OR (response_status IS NOT NULL AND response_status BETWEEN 200 AND 599 AND response_body IS NOT NULL))
);

-- Named-parameter JDBC statement; NOT executable migration SQL:
-- INSERT INTO request_results (owner_id, operation, idempotency_key, request_hash)
-- VALUES (:owner, :operation, :key, :hash)
-- ON CONFLICT (owner_id, operation, idempotency_key) DO NOTHING
-- RETURNING idempotency_key;
-- If claimed, do the local business mutation and fill response status/body BEFORE commit.
-- If not claimed, SELECT by the SAME owner/operation/key in a NEW statement under READ COMMITTED.
-- Re-authorize, compare hash and replay only a complete matching stored response.
-- Set deployment-specific lock/statement/transaction limits through authorized configuration.
-- Rollback must remove the claim and mutation together; never continue in an aborted TX.
-- This schema permits an unfinished row inside a TX; it DOES NOT itself prevent committing it.
-- The transaction/service contract and an integration regression must enforce completion.
-- Bound response size in the application; store only allowed safe fields, never credentials.
-- Do not deploy retention cleanup without defining races, expiry and the retry contract.
