# Rule record schema (no legal rule supplied)

Required fields:
- stable rule ID, jurisdiction and supported subject/profile;
- source URL/document identity, exact provision/section and publication version;
- source verification date and verifier;
- applicability, effective_from/effective_to and transitional rules;
- required inputs and explicit exclusions;
- parameters with units, decimal scale and constraints;
- algorithm, order of operations and legally justified rounding points;
- independent examples and boundary expectations;
- status: DRAFT, REVIEW_REQUIRED or APPROVED;
- approval evidence (person/role/date) and associated calculator/tests version;
- superseded rule and correction/recalculation policy.

Never fill reviewer identity or approval by inventing a person. A timestamp or self-generated expected value does not prove approval. Unapproved fixtures must remain nonproduction.
