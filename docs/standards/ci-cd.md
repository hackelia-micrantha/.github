# CI/CD standard

CI/CD should provide trustworthy, least-privileged evidence about the exact revision being reviewed or released. A green aggregate status is insufficient when required work was skipped, ran against the wrong revision, or used an unsafe execution boundary.

## Baseline outcomes

Repositories beyond Experimental maturity should define automated checks appropriate to their stack and risk, normally including:

- formatting or style validation;
- linting and static analysis;
- unit or component tests;
- relevant contract and integration tests;
- build or package validation;
- dependency and supply-chain checks;
- documentation or link validation where documentation is a supported surface.

Native, platform, deployment, release, and end-to-end jobs should be added when those boundaries are part of the repository's declared outcome.

## Required-check design

- Use stable, meaningful job names suitable for branch protection.
- Keep required checks conservative: unexpected paths or classifier failures should run the safer validation path.
- A skipped required job must still produce an intentional, understandable result when GitHub branch rules depend on its name.
- Do not weaken, rename, or remove a gate solely to merge a change.
- Validate pull requests, pushes to protected branches, merge queues, and releases according to the repository's delivery model.
- Ensure checks and release jobs operate on the intended commit, tag, or merge-queue revision.

Change-aware gating is allowed when the classifier is tested, defaults safely, handles renames and generated files deliberately, and does not skip validation for unknown or shared-impact paths.

## Workflow permissions

Use least-privilege permissions at workflow and job scope. Default to read-only repository access and grant write capabilities only to the job that requires them.

Separate build and validation from publication. Untrusted code must not gain access to:

- repository or organization secrets;
- writable tokens;
- protected environments;
- signing identities;
- deployment credentials;
- persistent internal infrastructure.

Avoid `pull_request_target` for executing pull-request code. When it is required for metadata-only automation, do not check out or execute untrusted changes with privileged credentials.

## Source mutation and authoring boundary

**CI validates authoritative source; it does not author or repair it.**

Repository content should be classified by authority before automation is allowed to mutate it:

1. **Authoritative source** — human- or agent-authored code, configuration, documentation, product content, policy, tests, and other reviewed inputs whose repository history is the source of truth.
2. **Declared generated source** — deterministic, machine-owned paths produced from authoritative inputs by a documented generator contract.
3. **Derived state** — build artifacts, packages, release assets, deployment state, reports, caches, provenance bundles, and other outputs that are not authoritative source inputs.

The default rules are:

- authoritative source enters repository history through an explicit actor commit on a branch and normal review;
- pull-request validation must not rewrite, commit, push, or otherwise repair the branch it is validating;
- validation workflows should not require `contents: write`; a pull-request-triggered workflow that requests repository-content write authority requires an explicit documented exception and must not use that authority to mutate authoritative source on the reviewed branch;
- metadata-only pull-request automation should prefer scoped `pull-requests: write` or `issues: write` permissions and avoid repository-content write authority;
- release or deployment automation may write derived state when writing that state is the workflow's declared purpose and the authority is scoped to the minimum target;
- generated-source automation must declare the owned paths, generator, inputs, determinism/idempotency expectations, and accountable bot or actor identity;
- a generator may be invoked explicitly by an authoring actor, or by a dedicated bot that opens or updates its own clearly identified generated-source pull request; it should not opportunistically modify an existing human- or agent-authored pull request;
- CI should verify generated-source freshness by running the generator in a non-authoring mode and failing on an unexpected diff rather than silently committing the repair;
- retries and re-runs must not create additional source mutations or make review state depend on workflow timing.

Preferred mechanisms for substantial source transformations are, in order of fit:

- direct file changes committed to a feature branch;
- one atomic Git tree/commit for coordinated multi-file changes;
- a trusted local or agent checkout that runs the transformation, validation, and explicit commit;
- an explicit checked-in codemod or generator invoked by the authoring actor;
- a dedicated generated-source bot pull request when the repository intentionally treats specific paths as machine-owned.

A workflow whose purpose is validation must not become the mechanism that authors the change merely because direct source-edit tooling is inconvenient.

### Generated-source exception contract

When repository-tracked generated source is justified, document at minimum:

```markdown
## Generated-source contract

- Owned paths:
- Authoritative inputs:
- Generator and version:
- Invocation:
- Determinism/idempotency expectation:
- CI freshness check:
- Bot/actor identity allowed to write:
- Review boundary:
- Regeneration/recovery procedure:
```

The exception does not permit arbitrary source writes outside the declared paths and does not convert generated output into independent authority over its inputs.

## Self-hosted runners

Self-hosted runners are privileged infrastructure and require an explicit trust model.

- Do not execute untrusted fork pull-request code on persistent self-hosted runners.
- Prefer ephemeral, isolated runners for untrusted or high-risk workloads.
- Separate runner groups by trust, repository, environment, and credential scope.
- Minimize host mounts, device access, network reachability, and reusable state.
- Clear workspaces, caches, credentials, and temporary artifacts between jobs.
- Pin or attest runner images and bootstrap dependencies.
- Monitor runner availability, queueing, disk pressure, and compromise indicators.

Cost or speed does not justify exposing organization infrastructure to untrusted code.

## Dependencies and actions

- Pin third-party actions to immutable commit SHAs where practical, with a visible version comment.
- Review action permissions, maintainer reputation, transitive behavior, and update strategy.
- Use lockfiles and reproducible dependency installation.
- Cache only trusted, integrity-checked material and scope caches to avoid cross-trust poisoning.
- Record exceptions for floating action versions or network-fetched build inputs.

## Reproducibility and command interface

CI commands should be runnable locally or in an equivalent documented environment. Prefer a small, discoverable task interface over duplicated shell fragments.

Micrantha repositories may use `mise` tasks as the standard entry point for formatting, linting, tests, builds, and release validation. Do not introduce `make` solely as an organizational requirement. Repository-local tools remain acceptable when commands and prerequisites are documented.

Scripts should be bounded, tested where logic is material, and avoid becoming an undocumented second build system.

## Concurrency and performance

- Cancel superseded pull-request runs when safe.
- Do not cancel release, deployment, merge-queue, or evidence-producing work when cancellation could leave ambiguous state.
- Use caches and matrices deliberately; measure before adding complexity.
- Keep fast deterministic checks early, but do not hide slow required validation indefinitely.
- Split independent jobs while preserving clear required-gate semantics.

## Artifacts and evidence

Artifacts should have:

- clear names and producing revision;
- bounded retention appropriate to debugging, audit, or release needs;
- protection from secret or personal-data leakage;
- checksums or stronger integrity evidence when consumed downstream;
- provenance and SBOMs according to release and supply-chain risk.

Do not upload entire workspaces or verbose logs without reviewing their contents.

## Deployment and environments

- Use protected environments for sensitive publication or deployment.
- Separate build identity from deployment identity.
- Require explicit approval where the governance or risk model demands it.
- Make deployment idempotent or safely resumable.
- Define rollback, recovery, and partial-failure behavior.
- Preserve who approved, what revision was deployed, which artifacts were used, and the resulting environment state.

## Release pipelines

Release automation should validate version identity, source revision, changelog or release notes, artifacts, checksums, signatures or provenance where required, and publication targets. A release job must not rebuild materially different artifacts after approval without recording that distinction.

## Failure handling

When CI fails:

1. determine whether the product, test, workflow, runner, or external dependency failed;
2. preserve relevant logs and artifact evidence without exposing secrets;
3. repair the root cause rather than bypassing the gate;
4. re-run against the current revision;
5. identify flakiness or skipped coverage explicitly;
6. confirm all required checks exist and completed before merge or release.

## Local overrides

Repository-specific workflows may differ, but they should document required checks, runner trust, publication authority, release identity, source-mutation exceptions, and any reduced validation. A local override cannot silently redefine a green check as evidence for a boundary that did not run.