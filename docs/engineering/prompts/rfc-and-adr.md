# Prompt: derive RFC and ADR artifacts

```text
Use the supplied context and QART analysis to determine whether an RFC is warranted and which accepted decisions require ADRs.

## RFC threshold

Recommend an RFC when the proposal materially:
- crosses component, repository, team, or trust boundaries;
- changes a public or shared contract;
- changes a security, governance, data, or authorization model;
- requires migration or compatibility coordination;
- is costly or difficult to reverse;
- combines several architectural decisions that need coherent review.

Avoid an RFC for a narrow, local, low-risk, easily reversible implementation choice.

## RFC output

When warranted, draft:

1. Metadata and status
2. Summary
3. Motivation
4. Goals and non-goals
5. Background and current state
6. Proposal
7. Architecture, data flow, control flow, and trust boundaries
8. QART decision summary
9. Components and responsibilities
10. Interfaces and contracts
11. State and failure models
12. Security, privacy, and governance
13. Operational design and ownership
14. Compatibility, migration, rollout, and rollback
15. Alternatives considered
16. Delivery phases
17. Validation strategy
18. Success measures
19. Risks and mitigations
20. Unresolved questions that materially affect approval
21. Decision and disposition section

Clearly distinguish normative requirements, recommendations, assumptions, and unresolved questions.

## ADR output

For every accepted durable decision, draft a separate ADR containing:

1. Title
2. Status
3. Date and decision owners
4. Related RFC and QART slice
5. Context
6. Decision, stated clearly and normatively
7. Alternatives considered
8. Rationale
9. Positive consequences
10. Negative and accepted consequences
11. Security and governance consequences
12. Compatibility and migration consequences
13. Implementation constraints imposed by the decision
14. Validation conditions
15. Revisit triggers

Rules:

- Never convert a recommendation into an accepted ADR without explicit evidence that the decision was made.
- Mark undecided items as ADR candidates only.
- Do not copy the whole RFC into each ADR.
- Keep each ADR focused on one durable decision.
- Separate implementation details from architectural constraints.
- Preserve rejected alternatives and why they were rejected.
- Identify decisions that are too local or reversible to justify ADR ceremony.

## Final output

Provide:
- RFC required: Yes / No, with rationale
- RFC draft or recommended outline
- Accepted ADRs ready to record
- Undecided ADR candidates
- Decisions that should remain local implementation choices
- Missing approvals or evidence
- Traceability to plans, specifications, delivery issues, and validation

Context and QART analysis:
<PASTE CONTEXT AND QART SLICES HERE>
```
