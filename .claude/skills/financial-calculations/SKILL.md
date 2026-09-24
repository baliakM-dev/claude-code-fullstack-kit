---
name: "financial-calculations"
description: "Design, implement and test deterministic financial calculations with versioned rules and explainable results. Use for taxes, insurance contributions, reserves, cash-flow projections, rounding, effective dates and correcting historical results. Do not invent country-specific law or calculate authoritative amounts with a language model."
---

# Deterministic financial calculations

Read the supported population, jurisdiction, period, input contract and approved rules. Treat absent legislative authority or ambiguous rounding as a correctness blocker for that calculation, not an invitation to infer a convenient value.

## Model
1. Separate decimal parameters, algorithms, applicability and effective dates. A new rule may change the algorithm, not just a rate in a database.
2. Keep effective period, source publication date, adoption/verification date and the financial period being calculated distinct. Handle explicit transition rules; never silently carry a historical rule into an unknown future year.
3. Resolve a validated immutable rule snapshot in the application service, then pass it and validated inputs to a deterministic calculator. The calculator need not query the database merely because constants live there.
4. Define decimal precision, scale, operation order and the rounding step/mode from the actual rule. Use BigDecimal or exact suitable representations; never binary floating point for authoritative amounts.
5. Distinguish cash received, invoice issued, due obligation, payment already made, reserve and forecast. Prevent double counting. Determine cash availability from a real/reconciled opening balance, not revenue alone.
6. Missing inputs are not zero. Return supported results plus explicit blockers/uncertainty; never label a partial profile a complete tax return.

## Evidence and change management
Store the input snapshot, rule-set ID/version, calculator version, period, run time, intermediates, assumptions and warnings. Make a historical result reproducible. Publish rules through draft/review/approved lifecycle with independent reference cases and a human/domain approval; an agent cannot self-certify legal correctness.

When a rule or bug is corrected, identify affected runs, preserve earlier versions, compute a traceable revision and decide whether users must be notified. Avoid silently overwriting history.

Test independent examples, threshold/date boundaries, rounding, negative/zero cases only where legally meaningful, unsupported situations and correction behavior. Distinguish verified results from illustrative fixtures.

For forecasts begin with transparent scenarios and assumptions. Display estimates separately from confirmed data/official obligations. Evaluate more complex models against a baseline on held-out historical periods; do not invent confidence or accuracy.

Use [rule-record.md](references/rule-record.md) for a new rule. It defines a schema, not a valid rule. Real country-specific sources remain in project domain documentation.

Primary source for decimal semantics: https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/math/BigDecimal.html
