---
name: ci-workflow-review
description: Review CI/CD workflow architecture for performance, redundancy, evidence quality, runner efficiency, security, and maintainability without optimizing away required validation or authority boundaries.
---

# CI/CD workflow review

## Trigger

Use for requests such as `review CI workflows`, `optimize GitHub Actions`, `find redundant CI`, `review pipeline performance`, `why is CI slow`, or a periodic architecture review of CI/CD design.

Use this skill when the concern is the **shape and efficiency of the pipeline**, not primarily one failing run. For a concrete failing workflow, use `docs/prompts/ci/ci-failure-triage.md` first.

## Inputs

- repository or bounded repository set;
- CI/CD provider and workflow/pipeline definitions;
- current delivery model and required checks/gates;
- runner/executor topology and trust boundaries;
- current default-branch build/test/release commands;
- recent run/timing/queue/cache/cost evidence when accessible;
- project-local CI/CD rules and exceptions;
- mutation authorization if workflow edits are requested.

## Workflow

1. **Establish pipeline purpose and authority.** Identify pull-request, merge-queue, protected-branch, release, deployment, schedule, and manual responsibilities. Resolve which checks/evidence are actually required before suggesting consolidation.
2. **Build the execution graph.** Map triggers, jobs/stages, dependencies, matrices, runners, artifacts, caches, and publication/deployment effects.
3. **Measure when possible.** Inspect recent runtime, queue time, retries/flakes, cancellations, cache behavior, artifact transfer, and cost where the provider exposes it. Keep static hypotheses distinct from measured bottlenecks.
4. **Run the architecture review.** Apply `docs/prompts/ci/ci-workflow-review.md` across trigger overlap, critical path, repeated setup, matrices, caching, artifacts/rebuilds, concurrency, reuse, change-aware execution, reliability, security/authority, and observability.
5. **Classify duplication.** Distinguish `REDUNDANT-COMPUTE`, `INDEPENDENT-EVIDENCE`, `SHARED-SETUP-OPPORTUNITY`, `TRIGGER-OVERLAP`, `MEASURE-FIRST`, and `AMBIGUOUS`.
6. **Prioritize.** Prefer low-risk reductions in wasted computation/waiting first, then structural changes whose benefit is evidenced. Do not add abstraction whose operational/debugging cost exceeds the duplication it removes.
7. **Apply bounded fixes when authorized.** Preserve required-check semantics, exact-revision evidence, trust boundaries, release identity, and deployment authority.
8. **Validate.** Check provider syntax, representative exact-head runs, required-check names, artifact flow, permissions, runner selection, and before/after performance where practical.
9. **Re-review.** Confirm the change did not trade duplicated compute for hidden serialization, cache poisoning risk, false-green skips, or a larger shared failure domain.
10. **Track project-owned follow-up.** Route material repository-specific changes to the owning project. Promote a shared workflow/component only when repeated cross-project evidence shows the abstraction is genuinely reusable.

## Evidence invariants

- Similar commands do not prove redundant evidence.
- A green aggregate status is not proof that the intended revision/boundary ran.
- Queue time and runner startup are part of feedback latency even when job runtime is small.
- Parallelism is not automatically faster overall when runners are scarce or artifact transfer dominates.
- Caches and shared artifacts are optimization mechanisms with integrity/trust boundaries, not free storage.
- Release/deployment pipelines must preserve exact artifact/revision identity; do not rebuild materially different bytes merely to simplify workflow composition.
- Optimization must not grant broader permissions, expose self-hosted runners to untrusted code, or weaken independent platform/security/release checks.

## Human decisions

Use the shared ambiguity contract. Human disposition is required before changing a material optimization boundary when evidence cannot determine, for example:

- whether a check is intentionally required or independently evidentiary;
- whether a release is required to rebuild or should promote validated artifacts;
- supported platform/toolchain matrix scope;
- whether a runner label/group encodes a trust/hardware boundary;
- whether change-aware skipping is acceptable for a costly job.

Group such questions rather than interrupting for each YAML detail. Continue unaffected read-only review while decisions are pending.

## Mutation boundary

Read-only by default. Workflow edits, required-check changes, runner-label changes, cache/permission changes, deployment/release changes, and shared workflow publication require explicit mutation authority.

Never remove, rename, bypass, or make non-blocking a required validation merely to improve performance unless that semantic change is explicitly authorized and independently justified.

## Completion

Complete when:

- the relevant execution graph and evidence responsibilities are explicit;
- material duplication/performance findings are classified;
- measured evidence is separated from hypotheses;
- security/trust/release implications are reviewed;
- proposed changes have benefit/risk/validation criteria;
- any authorized edits have representative exact-head evidence;
- unresolved material decisions are explicit rather than guessed.

## References

- `docs/prompts/ci/ci-workflow-review.md`
- `docs/prompts/ci/ci-failure-triage.md`
- `docs/standards/ci-cd.md`
- `docs/standards/testing.md`
- `skills/test-strategy/SKILL.md`
- `skills/security-review/SKILL.md`
- `skills/release-integration/SKILL.md`
