---
name: Epic or plan
about: Coordinate a larger outcome across decisions, repositories, workstreams, or delivery slices
title: "[epic]: "
labels: []
assignees: []
---

## Outcome

Describe the larger observable result and why it matters.

## Status

Draft / Needs discovery / Needs decisions / Ready / In progress / Blocked / Complete / Superseded

## Priority

P0 / P1 / P2 / P3 — give a one-sentence repository-global rationale. Record blocking separately under **Dependencies**.

> An epic coordinates work. Its priority does not make the umbrella issue itself executable; identify the next bounded slice.

## Problem or opportunity

State the underlying problem, risk, gap, or opportunity. Distinguish verified facts from suspected causes and recommendations.

## Goals

- Outcome or system property that must become true

## Non-goals

- Adjacent or future work intentionally excluded

## Success measures and exit criteria

The epic is complete when the outcome is achieved, not merely when known child issues are closed.

- [ ] Observable result or threshold
- [ ] Required security, reliability, compatibility, or operational property
- [ ] Required adoption, migration, release, or deprecation outcome

## Current and desired state

Summarize the relevant architecture, workflows, constraints, trust boundaries, dependencies, and the durable target state.

## Decisions and design artifacts

| Decision or question | Artifact | Status | Owner | Blocks execution? |
| --- | --- | --- | --- | --- |
| Bounded question | QART / RFC / ADR / specification | Status or link | Owner | Yes / No |

Do not treat unresolved decisions as implementation requirements.

## Workstreams

### Workstream: Name

- **Outcome:**
- **Scope:**
- **Dependencies:**
- **Validation:**
- **Child issues:**

Repeat only for independently meaningful workstreams.

## Sequencing and milestones

1. Blocking evidence or decisions
2. Foundational contract or enabling slice
3. Core implementation and integration
4. Validation, migration, release, documentation, and cleanup

Identify which work may proceed in parallel and the exit criteria for each phase.

## Dependencies

- **Ready:**
- **Blocked by:**
- **Unlocks:**
- **External or cross-repository dependencies:**

## Security and operations

- Assets, trust boundaries, approvals, and residual risk:
- Deployment, configuration, observability, and support:
- Capacity, cost, backup, recovery, and incident posture:
- Compatibility, migration, rollout, rollback, and deprecation:

## Risks and mitigations

| Risk | Impact | Mitigation or contingency | Owner |
| --- | --- | --- | --- |
| Material risk | Low / Medium / High | Mitigation | Owner |

## Validation checkpoints

- [ ] Material decisions are resolved and recorded at the appropriate level.
- [ ] Public or cross-component contracts are specified.
- [ ] Foundational and integration behavior is demonstrated.
- [ ] Failure, security, migration, and rollback paths are validated where applicable.
- [ ] Success measures and exit criteria are verified.

## Next executable slice

- **Issue or proposed title:**
- **Observable outcome:**
- **Dependencies:**
- **Acceptance criteria:**

## Definition of done

- [ ] Epic exit criteria are met with evidence.
- [ ] Durable decisions and contracts are current.
- [ ] Child work is delivered in bounded, reviewable slices.
- [ ] Documentation, release state, and ownership match reality.
- [ ] Remaining work is explicitly deferred, superseded, or tracked separately.
