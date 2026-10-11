---
name: project-review
description: Reconcile a Micrantha project against implementation, architecture, security, testing, backlog, documentation, maturity, and current evidence.
---

# Project review

## Trigger

Use for requests such as `review the project`, `review this repo`, `assess current state`, or when a repository needs a trustworthy baseline before planning or mutation.

## Inputs

- repository/project identity and accessible evidence;
- current branch/default branch and relevant open issues/PRs;
- project-local architecture, requirements, ADRs/RFCs, tests, CI, release and security evidence;
- explicit mutation authority if the operator wants findings applied.

## Workflow

1. Establish project purpose, maturity, supported contracts, repository role, and authoritative sources.
2. Reconcile implementation against issues, PRs, docs, decisions, CI, tests, releases, and public claims.
3. Inspect architecture, boundaries, duplication, complexity, modernization, performance, security, operability, UX where applicable, and maintainability.
4. Assess validation using the organization testing and CI/CD standards; distinguish exact evidence from assumptions or stale green checks.
5. Identify completed work, incomplete work, gaps, contradictions, overlap, stale artifacts, and opportunities.
6. Classify findings by impact and confidence; do not create one action per observation.
7. If writes are authorized, route material findings through `project-triage` and apply only bounded reconciliations.

## Evidence

Report verified facts separately from inference. Record evidence that could not be inspected. Prefer current default-branch/project-local evidence over copied summaries.

## Completion

Complete when the project has an evidence-backed current-state model, material discrepancies are explicit, and the next decision or executable work can be selected without repeating the broad review.

## References

- `docs/prompts/project-review/comprehensive-status-review.md`
- `docs/prompts/project-review/status-refresh.md`
- `docs/prompts/reviews/engineering-artifact-review.md`
- `docs/standards/testing.md`
- `docs/standards/ci-cd.md`
