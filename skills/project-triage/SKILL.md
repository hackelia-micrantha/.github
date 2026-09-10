---
name: project-triage
description: Convert a reviewed project state into a prioritized, dependency-aware, executable work queue and reconcile stale or overlapping work.
---

# Project triage

## Trigger

Use after `project-review`, for `triage issues`, `what is next?`, `update issues`, or when the backlog no longer represents the actual implementation state.

## Inputs

- a recent project review or equivalent trustworthy baseline;
- open issues, PRs, milestones/epics, accepted decisions, and blockers;
- current release/milestone goals and explicit mutation authority for backlog changes.

## Workflow

1. Reconcile open work against implementation and merged history.
2. Close or recommend closing work that is completed, duplicate, superseded, invalid, or no longer aligned.
3. Merge overlapping findings into the smallest coherent set of outcomes.
4. Preserve distinction among priority, severity, status, confidence, and size.
5. Identify dependency edges and blockers; prefer work that unlocks the current milestone or multiple downstream items.
6. Ensure P1 is a small next-up queue rather than a second backlog.
7. Route ambiguous work to the minimum responsible artifact: issue, spike, QART, RFC, ADR, security review, or epic.
8. Run `issue-grooming` on executable items and `implementation-plan` where sequencing is non-trivial.

## Evidence

Every priority or closure decision should cite current implementation, accepted decision, dependency, failure evidence, or milestone need rather than age or intuition alone.

## Completion

Complete when the backlog reflects reality, blockers and dependency edges are explicit, and at least one next executable slice can begin without additional broad triage.

## References

- `docs/prompts/planning/classify-and-route.md`
- `docs/prompts/planning/next-executable-slice.md`
- `docs/prompts/issues/issue-grooming.md`
- `docs/prompts/project-review/status-refresh.md`
- `CONTRIBUTING.md`
