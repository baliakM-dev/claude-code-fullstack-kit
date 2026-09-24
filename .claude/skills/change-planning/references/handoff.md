# Task handoff contract

- Task ID and original user outcome.
- Acceptance criteria and independent expected results.
- Allowed changes and explicit non-goals.
- Project-profile path and relevant decisions.
- Risk and required evidence.
- Baseline/head IDs, or initial-file manifest when there is no HEAD.
- Staged, unstaged and untracked paths; note unrelated work to preserve.
- Relevant files and targeted reference paths, not a repository dump.
- Actual commands known to exist; missing commands are NOT_CONFIGURED.
- Known findings without a suggested approval verdict.

A reviewer needs a reproducible change boundary. An empty diff is not proof of no changes: include newly created files. If files change after review, invalidate approval for the affected scope and review the changed evidence.

Acceptance example: given an authenticated owner and one received payment, the monthly list includes it; another user's list and direct ID requests never expose it. Do not constrain a solution to a specific class count.
