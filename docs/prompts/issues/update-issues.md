# Update Issues — Evidence Reconciliation Prompt

Use this entry point when the operator says **update issues**, **reconcile issues**, **sync tracking**, or an equivalent request during a Micrantha/Ryjen engineering task. This invocation explicitly authorizes **bounded issue-tracking mutations within the established task/project scope**, but does **not** authorize code changes, merges, releases, deployments, new credentials, or unrelated work.

Compose [Issue Grooming](issue-grooming.md), [Project Status Refresh](../project-review/status-refresh.md) where a baseline exists, [Implementation Completeness Review](../reviews/implementation-completeness.md) for purportedly delivered outcomes, and the [cross-project execution overlay](../overlays/cross-project-execution.md). Use the [Supervisor operating profile](../../engineering/chatgpt-supervisor-operating-profile.md) and shared [execution boundary](../README.md#shared-execution-boundary). For a raw unfiled idea, use [Classify and Route](../planning/classify-and-route.md) first.

## Compact invocation

> Update issues for the active project/workstream using current authoritative GitHub evidence. Reconcile existing issues against main, exact PR/CI/review state, delivered behavior, acceptance criteria, decisions, blockers, and dependencies; edit existing tracking in place, close only verifiably completed work, and create a new issue only for a distinct untracked outcome. Verify each mutation by read-back and report the changed issues and unresolved gaps. Do not change code or cross a merge/release/effect boundary.

## Execution contract

1. **Resolve the bounded project graph.** Start from the active issue/PR/workstream and its owning repository. Consult the canonical registry, related repositories, or portfolio inventory only as needed by dependency/ownership evidence. Do not enumerate or mutate the whole organization merely because the user used shorthand.
2. **Refresh evidence before writes.** Inspect current main, relevant open/closed issues, issue bodies/comments/labels/milestones, open/merged/closed PRs, exact PR heads/bases, reviews and unresolved threads, required CI/build/static-analysis results, accepted QART/RFC/ADR/specs, and actual delivered behavior. Distinguish observations from assumptions and stale history.
3. **Build an evidence-to-issue reconciliation map.** For each materially affected outcome classify it as **verified complete**, **partially delivered**, **in progress**, **blocked**, **superseded/duplicate**, **not started**, or **indeterminate**. Preserve the distinction between implementation merged, validation qualified, deployed/released, and accepted outcome delivered. Do not mark a work item complete merely because a PR was merged or CI turned green.
4. **Prefer existing tracking.** Search for duplicates, overlapping issues, parent/child relationships, and cross-project owner issues before creating anything. Update the owning issue's current status, remaining scope, evidence links/exact revisions, dependencies, blockers, non-goals, acceptance criteria, and verification gaps. Link coordination trackers without duplicating canonical requirements.
5. **Apply conservative state and priority changes.** Close only when all applicable outcome/acceptance criteria are evidenced; reopen if closure was premature and a material requirement remains. Supersede/mark duplicate only after preserving unique constraints and evidence. Apply repository-global P0–P3 rationale; keep severity, readiness, priority, and blocked status separate. Do not churn labels, titles, comments, or timestamps when nothing material changed.
6. **Use minimum sufficient mutations.** Preserve unique issue discussion/history and approved architecture decisions. Prefer one coherent body edit or concise evidence comment where appropriate. Create a new issue only if there is a separate, bounded, untracked result with clear ownership, rationale, dependencies, testable acceptance criteria, and non-goals. Avoid one issue per log line, test failure, or speculative follow-up.
7. **Handle uncertain writes safely.** After a timeout or disconnect, read back before retrying. Use current issue state when editing; do not overwrite another actor's newer material changes. Re-read affected issues after mutation to verify actual titles, bodies, labels, state, and relationships.
8. **Do not exceed authority.** An issue-update request is not permission to modify implementation, merge PRs, publish specs as accepted, deploy, or silently extend to unrelated repositories. If a required issue owner/acceptance decision is materially ambiguous, continue unambiguous updates and isolate only the blocked mutation.

## Output

Report succinctly:

- **Updated:** existing issue links and the substantive change to each.
- **Closed/reopened/superseded:** each issue with the evidence and disposition.
- **Created:** any genuinely new outcome and why no existing issue covered it.
- **Unchanged/blocked:** relevant issues requiring missing evidence or authority.
- **Next executable slice:** the highest-leverage authorized next work, if determined.

If reconciliation reveals no material changes, explicitly report **No issue mutations required** and the evidence checked. Do not equate a completed issue-update pass with completion of the underlying engineering task.
