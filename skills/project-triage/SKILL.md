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

Establish the authoritative baseline first: resolve the project and its mapped repositories; refresh the milestone, open issues/PRs, relevant merged history, implementation and release evidence. For a large or cross-project backlog, use this order:

1. **Validate P0 evidence.** Check alleged active security, correctness, release, data-loss or required-validation failures against current evidence. Contain a verified interrupt before ordinary grooming; do not promote a title, security label, epic or future prerequisite to P0 by assumption.
2. **Reduce the P1 critical path.** Follow the current milestone's dependency graph and verified cost of delay. Keep a small executable **Now** queue (normally three to five per repository), distinguish blocked P1 dependencies and non-executable parent epics, and preserve their underlying priority rather than demoting them just to shrink the queue.
3. **Reconcile open PRs.** Inspect current heads, receiving branch, diffs, CI and review evidence where needed; map each PR to its governing issue and any stacked or merged work. Recommend merge, fix, block, deeper review, or supersede/close. Neither a low PR count nor a green historical check authorizes merge or deletion.
4. **Classify the remaining issues.** Use impact, urgency, dependency leverage, milestone fit and existing accepted decisions; distinguish priority from severity, readiness, blocked state, effort and confidence. Record missing/ambiguous priority as **unclassified**, not default P2. Do not mass-relabel from issue age, title or count alone.
5. **Consolidate the backlog.** Identify completed, duplicate, superseded, obsolete and overlapping work using implementation/acceptance evidence; recommend or perform only authorized issue updates and closures. Preserve unique requirements and security findings; do not create a new issue per observation or a parallel portfolio tracker.
6. **Select the next outcome.** Identify dependencies, required decisions and one independently verifiable executable slice. Route uncertainty to the smallest necessary issue, spike, QART, RFC, ADR, security review or epic; run `issue-grooming` on executable items and `implementation-plan` when sequencing is non-trivial.

For a focused single-issue request, perform only the applicable steps. Revisit the P1 **Now** queue if PR reconciliation or newly verified evidence changes readiness.

## Portfolio inventory and estimates

For a requested cross-project rollup, report per defined project (including mapped companion repositories without double-counting project identity):

- exact open **issue** and **PR** counts, their collection time, source/coverage, and whether pagination or permissions make any count incomplete;
- issues by **P0 / P1 / P2 / P3 / unclassified**; show high/normal/low summaries only as explicitly defined groupings, and distinguish observed priority metadata from a proposed triage reassignment;
- an order-of-magnitude **t-shirt size** (XS–XXL), indicative engineering effort/complexity, dominant uncertainty, blocker and next milestone slice. Separate implementation from evidence gathering, review, operator waits and release gates.

Avoid adding issue and PR estimates as independent tasks when PRs implement issues. Exclude parent-epic double-counting, distinguish research/disposition from delivery, and qualify low-evidence size estimates rather than presenting precise forecasts. Do not invent a grand total of person-days from overlapping project work.

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
