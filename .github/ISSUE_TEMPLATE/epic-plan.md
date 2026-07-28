---
name: Epic or plan
description: Coordinate a larger outcome across decisions, specifications, repositories, or delivery slices
title: "Epic: "
labels: []
assignees: []
---

## Executive summary

Describe the larger outcome, why it matters, and what successful completion changes for users, operators, developers, or the system.

## Status

Draft / Needs discovery / Needs decisions / Ready / In progress / Blocked / Complete

## Problem or opportunity

State the underlying problem, risk, gap, or opportunity. Distinguish symptoms, suspected causes, and strategic value.

## Goals

- <Outcome that must become true>
- <Capability or system property required>

## Non-goals

- <Adjacent or future work intentionally excluded>

## Success measures and exit criteria

The epic is complete when the outcome is achieved, not merely when known child issues are closed.

- [ ] <Observable result or threshold>
- [ ] <Security, reliability, compatibility, or operational property>
- [ ] <Adoption, migration, or deprecation outcome>

## Stakeholders and actors

| Actor or stakeholder | Need, responsibility, or decision authority |
|---|---|
| <Actor> | <Need or role> |

## Current state

Describe the relevant architecture, workflows, constraints, trust boundaries, dependencies, operational limitations, and prior decisions.

## Desired state

Describe the durable target architecture or operating model and its externally observable properties.

## Decisions and design artifacts

| Decision or design question | Artifact | Status | Owner |
|---|---|---|---|
| <Question or proposal> | QART / RFC / ADR / Spec | <Status or link> | <Owner> |

Do not treat unresolved decisions as implementation requirements.

## Workstreams

### Workstream 1: <name>

- **Outcome:**
- **Scope:**
- **Dependencies:**
- **Validation:**
- **Child issues:**

### Workstream 2: <name>

<Repeat as needed.>

## Sequencing and milestones

1. <Decision, foundation, or contract milestone>
2. <Core implementation milestone>
3. <Integration, migration, or adoption milestone>
4. <Hardening, documentation, and cleanup milestone>

Identify which work may proceed in parallel and which milestones are gates.

## Dependencies

- **Blocked by:**
- **Blocks:**
- **External dependencies:**
- **Cross-repository dependencies:**

## Security and governance

- Assets and trust boundaries:
- Threats and abuse cases:
- Required controls and approvals:
- Evidence and provenance:
- Residual risk and acceptance owner:

## Operational and delivery considerations

- Deployment and configuration:
- Observability and support:
- Capacity and cost:
- Migration and compatibility:
- Rollout and rollback:
- Incident and recovery posture:

## Risks and mitigations

| Risk | Likelihood | Impact | Mitigation / contingency |
|---|---:|---:|---|
| <Risk> | Low / Medium / High | Low / Medium / High | <Mitigation> |

## Validation checkpoints

- [ ] Architecture and security decisions reviewed
- [ ] Public or cross-component contracts specified
- [ ] Foundation demonstrated independently
- [ ] Integration and failure paths validated
- [ ] Migration and rollback exercised
- [ ] Success measures verified

## Documentation outputs

- [ ] QART slices
- [ ] RFCs
- [ ] ADRs
- [ ] Specifications
- [ ] Architecture and threat-model documentation
- [ ] Operator or user documentation
- [ ] Migration and troubleshooting guides
- [ ] Demo or evidence pack

Remove outputs that do not apply.

## Open questions

Include only unresolved decisions that materially affect architecture, scope, safety, sequencing, or acceptance. Assign a decision owner and target point in the plan.

## Definition of done

- [ ] Epic exit criteria and success measures are met
- [ ] Material decisions are recorded in ADRs
- [ ] Required specifications and contracts are published
- [ ] Child work is delivered in reviewable slices
- [ ] Primary, failure, migration, and adversarial paths are validated
- [ ] Security and operational controls are effective
- [ ] Documentation and ownership are current
- [ ] Remaining work is explicitly deferred or captured separately
