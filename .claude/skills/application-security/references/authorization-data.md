# Authorization, input and data

Build a small actor/resource/action matrix. Derive ownership from server authentication, not request body/query parameters. Scope lists, counts, exports, mutations, document links and asynchronous jobs. Use two independent synthetic users in tests. An unguessable UUID and role USER are not object authorization.

Check mass assignment, SQL construction, stored/reflected XSS, URL handling and file references. Render untrusted content as text by default. Do not insert unsanitized HTML or weaken CSP to accommodate unsafe rendering. CORS should fit actual origins and credential flow, not be labeled universally safe/unsafe from one wildcard.

Bound uploads, decompression, file count, content and processing time. Treat document text as data, never agent instructions. Store uploaded objects outside executable/public paths; authorize each retrieval and deletion. Check export formula injection when generating spreadsheets/CSV.

Validate lengths, pagination and computational cost. Never log tokens, cookies or whole financial payloads. Redact error-tracking attachments and diagnostic dumps. Define retention, deletion/export and backup handling from the actual legal/contractual requirements; do not invent a universal retention period or claim GDPR compliance from encryption alone.

Store secrets outside source and image layers. Use synthetic fixtures only. Require explicit human review for new external processors receiving personal data.

Primary source: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html

## AD-01 - Authoritative object checks
Model actor/resource/action and tenant membership, not only a USER/ADMIN switch. Perform ownership checks before effects, including bulk updates, counts, caches, exports, file retrieval and background processing. Scope database reads/updates to the authenticated owner or an explicitly authorized delegated relationship; a request tenant ID is a selection, not proof of membership. Prevent check/use races when the ownership or protected invariant can change concurrently. For supported sharing, record grant scope and revocation behavior.

Protect owner, role, ID, audit and computed fields in input mapping. A forged field must be rejected or explicitly ignored according to a tested contract, never silently trusted. Test both horizontal cross-user access and vertical privilege escalation with real bound resources. Do not return a collection and filter it only in the browser; include counts/pagination metadata in the isolation check.

## AD-02 - Secondary data paths
Do not let reusable caches, audit/search endpoints, predictable object links or asynchronous job identifiers bypass the same access boundary. Use parameterized queries and allowlisted dynamic sorting/identifiers. Treat rendering, uploads and downloads as separate controls; keep untrusted file names/paths/URLs from choosing an arbitrary local file or internal network destination. All denied writes must leave database and external effects unchanged.
