# Prompt: classify and route engineering work

```text
Analyze the supplied engineering material and determine the minimum set of artifacts needed to move it responsibly from uncertainty to delivery.

Micrantha uses these artifact types:

- QART slice: explores one bounded decision through Questions, Alternatives, Recommendations, and Trade-offs.
- RFC: proposes a substantial cross-boundary or difficult-to-reverse change for review.
- ADR: records an accepted durable architectural decision.
- Epic: coordinates a larger outcome across workstreams.
- Plan: defines sequencing, dependencies, checkpoints, and contingencies.
- Design: explains system structure, responsibilities, boundaries, and behaviour.
- Specification: defines normative contracts and conformance behaviour.
- Investigation or spike: reduces uncertainty and produces evidence or a decision.
- Delivery issue: implements one bounded, independently verifiable outcome.

Tasks:

1. Summarize the underlying problem or opportunity.
2. Classify the primary and secondary work-item types.
3. Classify decision maturity for each material question:
   - unframed;
   - needs investigation;
   - ready for QART;
   - ready for RFC review;
   - ready for decision;
   - decided and ready for ADR;
   - superseded.
4. Identify independently decidable questions. Do not combine unrelated decisions into one QART slice.
5. Recommend the smallest justified artifact set.
6. Explain why each artifact is or is not required.
7. Identify missing evidence, hidden dependencies, contradictions, and scope risks.
8. Identify material security, governance, trust-boundary, compatibility, operability, migration, and rollback concerns.
9. Propose a traceability map from decisions to delivery and validation.
10. Do not draft an ADR for an unresolved decision.

Use this output structure:

## Assessment
- Problem or opportunity
- Primary type
- Secondary types
- Readiness
- Scope assessment
- Primary risks

## Decision inventory
For each decision:
- Question
- Maturity
- Decision drivers
- Evidence available
- Evidence missing
- Recommended next artifact

## Artifact map
Show the proposed relationship between QART slices, RFCs, ADRs, plans or epics, specifications, delivery issues, and validation.

## Recommended next actions
Order actions by dependency and decision value.

## Assumptions and unresolved questions
Distinguish assumptions from facts. Do not invent requirements.

Context and source material:
<PASTE CONTEXT, NOTES, ISSUE, OR DISCUSSION HERE>
```
