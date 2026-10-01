# Branching and integration standard

Micrantha uses a **golden `main` trunk with short-lived topic branches**, plus temporary integration branches when several dependent changes must converge before the combined candidate is safe to admit to `main`.

This is trunk-based development with bounded branch composition. It is not classic GitFlow: a permanent organization-wide `develop` branch is not part of the default model.

## Core model

```text
feature/a ───────────────┐
fix/b ───────────────────┼──────────────► main
docs/c ──────────────────┘                 │
                                           ├── release tag
feature/d ─┐                                └── optional milestone tag
feature/e ─┼──► integration/<initiative> ──► main
fix/f ─────┘
```

Branches are mutable work or composition surfaces. `main` is the authoritative integrated source line. Tags are immutable named checkpoints.

## Golden `main`

The organization default branch is `main`.

`main` is **golden** in the following sense:

- it is the canonical authoritative integration line;
- a source state is golden only when an explicit admission event records that state as accepted and the repository's applicable merge gates were satisfied for the admitted candidate/result;
- Git ancestry, reachability, first-parent membership, branch naming, or presence on `main` is evidence about history but does **not** by itself prove that an intermediate commit was independently admitted;
- commits carried into `main` as topic/integration ancestry may remain historical implementation evidence without becoming separate golden states;
- release identity normally traces to a recorded admitted state, with review/validation evidence tied to the corresponding admission record;
- temporary integration branches, feature branches, environment branches, or generated branches do not become alternate sources of truth merely because they exist.

Golden does **not** mean every commit is automatically a public/stable release, deployed to production, or supported indefinitely. Release and deployment authority remain separate decisions governed by the release and deployment standards.

### Admission records

An admission record may be a provider-native pull-request/merge-queue/merge record or another repository-owned durable record, but it must identify enough immutable evidence to distinguish the state that was actually accepted.

Where applicable, bind:

- destination branch and repository;
- admitted candidate identity;
- resulting accepted commit/tree identity when the merge method synthesizes a different revision;
- admission/merge method;
- required review evidence;
- required validation/CI evidence;
- any governed equivalence proof used to transfer validation evidence across a mechanically bounded transformation.

A fast-forward, rebase, or merge operation can make multiple commits reachable from `main`; that topology does not retroactively create separate admission events for every ancestor.

A project-local override to another default/canonical branch requires an explicit documented decision and migration/compatibility rationale.

## Topic branches

Normal work should use short-lived topic branches such as:

- `feature/<scope>`;
- `fix/<scope>`;
- `refactor/<scope>`;
- `docs/<scope>`;
- `chore/<scope>`;
- issue- or initiative-derived names.

Branch prefixes are navigation conventions, not authority, security classifications, release channels, or proof of the work's actual contents.

Topic branches should:

- contain a bounded coherent change;
- remain short-lived where practical;
- inspect drift from current `main` closely enough to control stale-state and integration risk;
- enter `main` through normal review and validation for non-trivial changes;
- be deleted after merge when no continuing purpose remains.

Being behind `main` in commit ancestry is **not by itself** a synchronization defect, conflict, or reason to merge/rebase/update a topic branch. Preserve the existing candidate when intervening `main` changes are unrelated to the candidate's touched behavior, contracts, dependencies, generated/build inputs, validation assumptions, or admission policy.

Update the branch from `main` when evidence shows the intervening changes can materially affect the candidate or its verification, when Git reports an actual merge conflict, or when repository policy/merge-queue admission requires validation of a composed candidate against the current base. Prefer diff/compare and dependency/contract evidence over unconditional ancestry synchronization.

Long-running work should normally be decomposed into independently integrable slices. Feature flags, configuration, compatibility shims, or dormant code may be used when they let safe increments reach `main` without exposing incomplete behavior.

## Temporary integration branches

Temporary integration branches are appropriate when the **composed result** of several changes requires validation before the capability is safe to merge to `main`.

Typical cases include:

- several dependent feature branches implementing one initiative;
- coordinated refactors whose slices are individually reviewable but composition-sensitive;
- cross-surface changes that need an integrated candidate;
- parallel human/agent workstreams that must converge before acceptance;
- migrations where compatibility must be evaluated across several coordinated changes.

Prefer a scoped name such as:

```text
integration/<initiative>
integration/<epic-or-issue>
```

A temporary `develop` branch is allowed when established project tooling or workflow makes that name materially useful. It is still temporary and must not silently become a permanent second trunk.

### Required lifecycle

A temporary integration branch must have:

- a defined initiative or feature scope;
- an accountable owner;
- explicit entry and exit criteria;
- a bounded expected lifetime;
- a declared composition/integration validation plan;
- a strategy for synchronizing with current `main`;
- a final reviewed candidate path into `main`;
- deletion after convergence unless a different continuing branch purpose is explicitly authorized.

Example:

```text
feature/a ──┐
feature/b ──┼──► integration/operator-gateway ──► validation ──► main
fix/c ──────┘                                             │
                                                         └── delete integration branch
```

### Evidence rules

Evidence from component branches does not automatically prove the integrated candidate.

Composition-sensitive tests, build checks, migrations, contracts, security checks, or end-to-end validation must run against the actual integrated revision when those boundaries are affected.

Before the final merge to `main`, validate the exact candidate required by repository policy. If `main` changes in a way that can invalidate the evidence, rebase/merge/update or use a merge queue and revalidate as appropriate.

Temporary integration branches are candidate-composition surfaces, not release authority. Stable publication from one requires an explicit project-specific exception.

## Merge methods

Repositories may choose the merge method that preserves the most useful history, but the merge method must remain compatible with **all** applicable admission evidence requirements. For ordinary non-privileged topic branches, the default preference is **squash merge only when the repository's admission policy permits the synthesized result to inherit the required evidence**.

Use:

- **squash merge** for ordinary iterative topic branches when the PR is the useful unit of history and synthesizing a new commit does not invalidate required review or validation evidence;
- **rebase/fast-forward-style history** when individual commits are intentionally curated and useful as first-class history, while remembering that reachability/first-parent membership does not itself prove admission of intermediate commits;
- **merge commits** when preserving topology is materially useful, especially for temporary integration branches or coordinated multi-branch convergence.

### Independent-review evidence

The [independent-review contract](../governance/independent-review.md) is authoritative for review equivalence and exceptions.

A synthesized merge/squash revision is **not** automatically covered by independent review of a different pre-merge head. When exact-head review applies, use a merge/admission method that preserves the reviewed revision or obtain review of the final accepted revision unless the independent-review contract itself explicitly permits the bounded transformation.

This branching standard does not create an additional review-equivalence bypass.

### Validation/CI evidence

A synthesized accepted revision is also **not** automatically covered by CI/validation run against a different revision.

When repository policy requires exact-revision validation, use one of:

- an admission mechanism that exposes and validates the exact candidate before acceptance, such as an applicable merge-queue/test-merge mechanism;
- a merge method that preserves the already validated candidate identity; or
- a repository-governed validation-equivalence contract that is mechanically verifiable and explicitly scoped to the affected evidence class.

A validation-equivalence contract must bind the relevant candidate/base/result identities and prove that the transformation cannot alter the behavior the reused validation was intended to establish. At minimum consider tree identity, parent/base identity, workflow/configuration inputs, generated artifacts, and any metadata that can affect build/test/release behavior. Record the proof in the admission evidence.

Validation equivalence does **not** satisfy independent-review requirements unless the independent-review contract separately says so.

If neither exact validation nor an applicable governed validation-equivalence proof exists, the synthesized revision is ineligible for golden admission.

Do not choose a merge method solely to make history visually linear if doing so obscures material integration provenance.

## Tags as immutable checkpoints

Tags identify exact source states. They do not replace branches for active development and do not create authority by themselves.

### Release tags

Release tags are the primary normative use of tags.

Examples include:

- `v1.4.0`;
- `v2.0.0-rc.1`;
- another repository-documented release identity.

Published release tags must not be moved or overwritten. Use annotated or signed tags when repository risk or authenticity requirements justify them.

A release tag identifies the source revision for a release; the release record, validation, provenance, artifacts, and accountable release authority are still required.

### Feature and milestone tags

Feature or milestone tags are optional immutable markers for a **material integrated checkpoint** whose exact state has durable value.

Examples may include:

- a major protocol/format transition point;
- completion of a large multi-branch initiative;
- a compatibility boundary useful for downstream testing;
- a historically useful architecture milestone.

An ordinary merged feature does not need a tag. Its PR and commit history are normally sufficient.

When used, a feature/milestone tag should:

- point to an accepted integrated commit, normally on `main`;
- have a clear namespaced/documented purpose;
- be immutable once published;
- not imply a release, support promise, deployment, or maturity level unless separately declared;
- not become a substitute for versioned releases when consumers need a supported artifact identity.

Avoid creating a dense parallel taxonomy of tags for every issue or PR.

## Maintenance and release branches

Long-lived release/maintenance branches are exceptional. Create them only when supported source lines must genuinely diverge, for example:

- security or critical fixes must be backported to an older supported major version;
- an app/store or appliance release line must remain frozen while `main` advances;
- an enterprise/regulatory support commitment requires maintenance of an older release line.

Do not create `release/*` branches merely because a release is approaching.

A maintenance branch must document:

- which supported line it owns;
- support duration;
- allowed change classes;
- release/tag authority;
- backport/forward-port expectations;
- validation and security-update policy.

Hotfixes for an older supported line branch from that line or affected release revision, then reconcile forward into `main` when the fix also applies there.

## CI and merge queues

CI should distinguish:

- component/topic-branch evidence;
- temporary integration-branch composition evidence;
- final `main` admission evidence;
- release/deployment evidence.

A green component branch is not a substitute for integration validation when composition can change behavior.

Use merge queues where concurrent changes make pre-merge evidence stale. The merge-queue candidate is another exact candidate to validate; the queue does not become a second trunk.

Cancel superseded topic-branch CI when safe, but preserve integration, merge-queue, release, deployment, and evidence-producing runs when cancellation could leave ambiguous state.

## Protection and direct pushes

Repositories beyond Experimental maturity should normally protect `main` according to their risk and delivery model.

For non-trivial changes:

- prefer pull requests over direct pushes;
- require the applicable checks for the exact candidate;
- require independent review when the change crosses a policy-defined privileged boundary;
- do not weaken protection or required checks simply to admit a change.

Emergency/break-glass procedures may differ but must preserve accountability and post-event evidence.

Temporary integration branches may use appropriate protection when multiple contributors, automation, or high-risk composition makes accidental mutation material.

## Automation and agents

Human and automated contributors follow the same authority model.

- Authoring agents use explicit topic/integration branches and commits.
- Validation automation must not opportunistically repair the candidate it is validating.
- Generated-source bots use their own declared branches/PRs where repository-tracked generated source is justified.
- Automation must not infer release or merge authority from a branch prefix or tag name.
- Repository tools may report branch/tag posture, but observations do not grant authority.

## Anti-patterns

Avoid these organization defaults:

- a permanent `develop` branch that shadows `main`;
- feature branches kept alive as durable alternate product lines;
- release branches created for every ordinary release;
- stable releases cut from temporary integration branches without explicit authority;
- treating every commit reachable from `main` or present in its first-parent chain as independently admitted/golden without an admission record;
- squash-merging an exact-head-reviewed privileged change without review coverage permitted by the independent-review contract;
- reusing CI/validation from a pre-merge revision for a synthesized accepted revision without exact validation or a governed validation-equivalence proof;
- tags used as mutable pointers;
- feature tags for every PR or issue;
- treating branch names as environment/security authority;
- treating a green pre-merge topic branch as proof of a different merge candidate.

## Relationship to other standards

- [CI/CD](ci-cd.md) governs exact-revision validation, runner trust, workflow permissions, and evidence.
- [Releases and versioning](releases.md) governs release authority, supported identities, artifacts, provenance, and immutable stable tags.
- [Testing and validation](testing.md) governs the evidence required for affected behavior.
- [Independent review](../governance/independent-review.md) governs non-author review for privileged changes.
- Repository bootstrap uses `main` as the explicit organization default branch but does not create extra branches without an applicable project decision.

## Local overrides

A repository may use a different branching model when its delivery/support domain requires it.

The override should state:

- which organization default changes;
- why trunk + bounded integration branches is insufficient;
- which branches become authoritative for what purpose;
- merge, release, deployment, and support authority;
- synchronization and stale-state controls;
- cleanup/end-of-life policy;
- owner and review date.

An override must not create ambiguous release authority or silently redefine which revision passed required validation.
