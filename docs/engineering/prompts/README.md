# AI prompts for engineering work

These prompts support Micrantha's decision-to-delivery workflow:

```text
Problem or opportunity
  -> QART slice
  -> RFC when broad review is required
  -> ADR after a durable decision
  -> Epic or plan
  -> Specification
  -> Delivery issue
  -> Validation and evidence
```

## Prompt catalogue

- [`classify-and-route.md`](classify-and-route.md) — classify raw notes and determine the minimum appropriate artifacts.
- [`groom-work-item.md`](groom-work-item.md) — turn an issue, plan, design, specification, or epic into an implementation-ready work item.
- [`qart-analysis.md`](qart-analysis.md) — decompose a design problem into independently decidable QART slices.
- [`rfc-and-adr.md`](rfc-and-adr.md) — draft an RFC and identify ADR candidates without recording undecided proposals as decisions.
- [`review-artifact.md`](review-artifact.md) — critically review an existing artifact for missing decisions, ambiguity, risk, and unnecessary ceremony.

## Usage rules

1. Supply repository context, existing decisions, constraints, and links when available.
2. Ask the model to distinguish facts, assumptions, recommendations, and unresolved decisions.
3. Require evidence for claims about implementation or current system behaviour.
4. Do not let the model invent requirements merely to make an artifact appear complete.
5. Prefer the smallest artifact set that preserves decision quality and traceability.
6. Treat generated content as a draft requiring accountable human review.
7. Do not place secrets, credentials, private customer data, or unredacted incident data in prompts.

## Expected AI posture

The model should:

- preserve known constraints and accepted decisions;
- expose uncertainty instead of concealing it;
- identify security, trust-boundary, compatibility, operability, migration, and rollback concerns when material;
- recommend QART before ADR when a decision is unresolved;
- recommend an RFC only when broader review or cross-boundary coordination is warranted;
- derive independently reviewable and mergeable delivery slices after decisions are sufficiently mature;
- avoid treating generated prose as evidence that a design is correct.

## Prompt input envelope

For more reliable results, prepend this context:

```text
Repository or system:
Current state:
Desired outcome:
Known constraints:
Accepted decisions:
Relevant links or evidence:
Audience and decision owners:
Source material:
```
