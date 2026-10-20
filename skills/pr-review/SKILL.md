---
name: pr-review
description: Review a pull request or bounded change set for correctness, architecture, security, scope, regressions, validation, and alignment with its authoritative work item.
---

# Pull request review

## Trigger

Use for `review PR`, `review this change`, or before a merge-readiness decision when the code/diff itself has not yet been critically reviewed.

## Inputs

- exact PR head/diff and current base;
- linked issue/spec/RFC/ADR and acceptance criteria;
- CI/test evidence, review threads, and relevant project-local standards.

## Workflow

1. Establish the intended outcome and review the actual diff, not only the PR description.
2. Check correctness, error handling, concurrency/state behavior, data handling, compatibility, and failure paths relevant to the change.
3. Review architecture and ownership boundaries; flag unnecessary coupling, duplication, or hidden policy decisions.
4. Review security: untrusted input, authorization, secrets, privilege, process/environment boundaries, supply-chain impact, and safe failure.
5. Verify tests and static analysis cover changed behavior at the smallest trustworthy layers; distinguish exact-head evidence from stale or unrelated runs.
6. Check migrations, docs, packaging, observability, operational impact, and rollback where applicable.
7. Reconcile unresolved review threads and identify scope that should be split rather than accepted as review debt.
8. Produce findings ordered by severity/merge impact with concrete evidence and remediation.

## External review publication

When preparing **substantive findings for a third-party repository**, follow the [canonical external-comment standard](../../docs/engineering/external-contribution-comments.md) before submitting inline comments or a review summary.

- Lead each independently actionable finding with a brief, accurate plain-language explanation of the failure mode; follow with exact code/contract evidence, impact, and a bounded fix or test.
- A grouped review summary may share one opening; avoid repetitive boilerplate across inline comments. Approvals with no findings and administrative replies need no ELI5 section.
- Keep private review notes and internal repository reviews in their existing format unless explicitly requested otherwise.
- Check the upstream project's review conventions and existing threads before commenting. Do not claim tests were executed without independent evidence.
- This is a **format/review preflight only**. Posting remains subject to the mutation boundary below; reading this skill never authorizes external publication.

## Mutation boundary

Read-only by default. Do not push fixes, resolve threads, modify labels, or merge unless explicitly authorized.

## Completion

Complete when all material findings are explicit and the change is ready to hand to `merge-readiness` for a merge/fix/block/close decision.

## References

- `docs/prompts/pull-requests/merge-gate-review.md`
- `docs/prompts/reviews/engineering-artifact-review.md`
- `docs/standards/testing.md`
- `docs/standards/ci-cd.md`
- `docs/standards/security.md`
