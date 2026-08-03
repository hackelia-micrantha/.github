---
name: Design proposal
about: Explore or propose a substantial architectural, security, governance, or cross-system change
title: "[design]: "
labels: ""
assignees: ""
---

## Summary

Describe the problem, proposed direction, and why a design decision is needed.

## Status

Draft / Needs evidence / Needs QART / In review / Ready for decision / Accepted / Rejected / Superseded

## Priority

P0 / P1 / P2 / P3 — give a one-sentence repository-global rationale. Record blocking separately under **Dependencies**.

## Motivation and current state

Explain the current limitation or opportunity, affected users or operators, existing architecture and contracts, material constraints, and supporting evidence.

## Goals

- Required outcome

## Non-goals

- Adjacent or future work intentionally excluded

## Decision inventory

Create one bounded question per material decision.

| Question | Alternatives | Current recommendation | Evidence needed | Status / artifact |
| --- | --- | --- | --- | --- |
| Neutral decision question | Credible options, including defer when viable | Recommendation or pending | Missing evidence | QART / RFC / ADR / local choice |

Use a separate QART analysis when alternatives or trade-offs require substantial treatment. Do not record an ADR until a durable decision is accepted.

## Proposed design

Describe applicable:

- components and responsibilities;
- interfaces, schemas, protocols, commands, or configuration;
- data and control flow;
- state ownership and consistency;
- deployment and integration points;
- trust, authorization, approval, and execution boundaries;
- failure handling and recovery;
- evidence, observability, and ownership.

## Alternatives and trade-offs

For each credible alternative include benefits, costs, security and operational impact, compatibility and migration impact, reversibility, and evidence.

## Security, privacy, and governance

- Assets and trust boundaries:
- Authentication, authorization, delegation, or approvals:
- Sensitive data and secret handling:
- Evidence, provenance, and retention:
- Failure posture and residual risk:

## Operations, compatibility, and rollout

- Deployment and configuration:
- Monitoring, diagnostics, and support:
- Capacity or cost:
- Compatibility and mixed-version behavior:
- Migration, staged rollout, rollback, and deprecation:

## Validation required for decision

- Prototype, spike, or benchmark:
- Contract or integration validation:
- Security or threat review:
- Failure, recovery, migration, or compatibility validation:
- Stakeholder or owner review:

## Dependencies

- **Ready:**
- **Blocked by:**
- **Unlocks:**
- **Related repositories or systems:**

## Decision and outputs

- **Disposition:** Pending / Accepted / Rejected / Withdrawn / Superseded
- **Decision owners:**
- **RFC required:** Yes / No / Pending
- **ADRs required:**
- **Specifications required:**
- **Parent epic or plan:**
- **Next executable slice:**
