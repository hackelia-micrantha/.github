---
name: merge-readiness
description: Decide whether a pull request is safe to merge using exact-head review, CI, test, dependency, and integration evidence.
---

# Merge readiness

## Trigger

Use for `review to fix or merge`, `is this green PR mergeable?`, or after `pr-review` has established the substantive findings.

## Inputs

- exact PR head SHA and current base branch state;
- review findings and unresolved threads;
- required checks/workflow runs for the exact head;
- linked acceptance criteria and dependency/blocker state.

## Workflow

1. Confirm the reviewed head SHA is still current and the base has not introduced a material conflict or semantic regression.
2. Confirm all merge-blocking review findings are resolved or explicitly dispositioned.
3. Verify required checks are present, completed, non-stale, correctly scoped, and tied to the exact head revision.
4. Treat skipped, cancelled, flaky, missing, neutralized, or unrelated checks as evidence gaps rather than success.
5. Verify applicable unit/component, contract, integration, end-to-end, security, migration, packaging, and static-analysis evidence according to risk.
6. Re-evaluate dependency edges and whether another pending change must land first.
7. Choose exactly one disposition: `merge`, `fix`, `block`, or `close`, and state the minimum evidence/change required for any non-merge disposition.
8. Merge only when mutation authority is explicit; use expected-head protection where supported.

## Completion

Complete when there is a concrete disposition grounded in the exact current head and no material ambiguity remains about why the PR can or cannot merge.

## References

- `docs/prompts/pull-requests/merge-gate-review.md`
- `docs/prompts/ci/ci-failure-triage.md`
- `docs/standards/testing.md`
- `docs/standards/ci-cd.md`
