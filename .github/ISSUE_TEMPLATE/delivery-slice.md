---
name: Engineering delivery slice
description: Deliver a bounded cross-cutting implementation, integration, migration, infrastructure, or refactoring outcome
title: "[delivery]: "
labels: []
assignees: []
---

> Use the bug, feature, or security form when one of those describes the work directly. Use this form for a bounded engineering outcome that crosses concerns or implements an already-understood decision.

## Outcome

Describe what will be observably true when this slice is complete.

## Priority

P0 / P1 / P2 / P3 — give a one-sentence repository-global rationale. Record blocking separately under **Dependencies**.

## Context and evidence

Summarize the current state, relevant implementation evidence, constraints, and links to issues, QART analyses, RFCs, ADRs, specifications, or pull requests.

## Scope

### In scope

- Required behavior or deliverable

### Non-goals

- Adjacent or follow-up work intentionally excluded

## Requirements and constraints

- Functional behavior:
- Compatibility or migration:
- Security or trust boundaries:
- Reliability and recovery:
- Operability and observability:
- Performance or capacity:

Remove dimensions that do not materially apply.

## Acceptance criteria

- [ ] Primary outcome is demonstrably complete.
- [ ] Relevant failure and edge behavior is defined and verified.
- [ ] Required compatibility, migration, or rollback behavior is verified.
- [ ] Security and authorization boundaries are preserved or strengthened.
- [ ] Documentation and operational guidance are current.

Replace generic checks with concrete, observable criteria.

## Validation

- Unit or component tests:
- Contract or integration tests:
- End-to-end or manual demonstration:
- Security or negative-path tests:
- Migration, compatibility, or rollback evidence:
- CI or release evidence:

## Dependencies

- **Ready:**
- **Blocked by:**
- **Unlocks:**
- **Related:**

## Delivery notes

- Expected files or components:
- Rollout or deployment:
- Rollback or recovery:
- Remaining follow-up:

## Definition of done

- [ ] Acceptance criteria are satisfied with evidence.
- [ ] Required checks pass without weakening relevant gates.
- [ ] The outcome is integrated, documented, and usable where applicable.
- [ ] Remaining work is explicitly deferred or tracked separately.
