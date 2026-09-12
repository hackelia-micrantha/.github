# Label mutation authority and rollback

This document defines the security and authority boundary that must exist before Micrantha label synchronization gains any write capability. It does **not** authorize or implement mutation.

Related: #27, #76, `label-synchronization.md`, and `SECURITY.md`.

## Decision

The first mutation pilot, if implemented, is restricted to `hackelia-micrantha/.github`, is **create-only**, and may create **one explicitly named canonical label per human dispatch**.

The workflow must run only from the default branch through explicit `workflow_dispatch`. For the same-repository pilot, prefer the ephemeral repository-scoped `GITHUB_TOKEN` and separate read from write authority across three jobs:

- **preflight** — `contents: read`, `issues: read`;
- **apply** — `contents: read`, `issues: write`; this is the only write-authorized job and is environment-gated;
- **receipt** — read-only, ungated, runs with `if: always()` after preflight/apply to preserve terminal evidence when GitHub schedules it after success, failure, approval rejection, or job cancellation.

No `contents: write`, `actions: write`, `workflows: write`, administration permission, organization permission, or inherited secret is required for repository label creation.

If synchronization later targets a different repository, the built-in token is no longer the intended authority boundary. Cross-repository mutation must use a short-lived GitHub App installation token with repository access limited to the reviewed target set and repository `Issues: write` only. A fine-grained personal access token is a fallback only when a GitHub App cannot provide the required capability; a classic PAT or broad personal credential is not acceptable.

### Rejected alternatives

- **Broad personal token** — rejected because authority, rotation, repository scope, and attribution are unnecessarily coupled to a human account.
- **Organization-admin token/App permissions** — rejected because repository label creation does not require organization administration.
- **Write-scoped token in preflight/report/receipt jobs** — rejected because evidence generation does not require mutation authority.
- **Write-scoped token on pull-request, push, schedule, or `pull_request_target` events** — rejected because unreviewed or ambient events must not create mutation authority.
- **Cross-repository use of the default `GITHUB_TOKEN`** — rejected as an architecture assumption; cross-repository authority must be separately scoped and explicit.
- **Multiple creates per dispatch** — rejected for the first pilot because one approval should authorize one bounded state transition and because a long multi-write sequence widens control-plane and label-state races.
- **Metadata update in the first pilot** — rejected because GitHub does not document conditional/CAS semantics for the label `PATCH` endpoint. A read immediately before `PATCH` cannot eliminate the remaining read/write race, so the first pilot avoids an operation that could overwrite concurrent metadata changes.
- **Rollback delete in the first pilot** — rejected because GitHub does not provide an atomic association-check-and-delete guard. A label could become used between a read and delete, so deletion remains unsupported even as rollback.

## Event and approval boundary

The initial mutation workflow must expose only `workflow_dispatch` and must require explicit inputs:

- `repository`;
- `label` — one canonical label selected by that repository's reviewed manifest entry;
- `expected_revision` — the exact `.github` control-plane revision;
- `plan_sha256` — the exact reviewed dry-run digest;
- `race_disposition_ref` — `none` only when the protected-environment reviewer confirms there is no unresolved prior mutation quarantine; otherwise a durable repository issue/ADR/evidence reference that disposes every outstanding quarantined run relevant to the target.

The first-pilot workflow must use a **fixed, hard-coded concurrency group** for `.github` mutation with `cancel-in-progress: false`. A second mutation workflow must not overlap a running or approval-waiting pilot. Broader rollout may key concurrency only from a reviewed allowlist; it must not let untrusted dispatch text choose an arbitrary concurrency boundary.

### Preflight job

The preflight job has read-only permissions and must:

1. reject any ref other than `refs/heads/main`;
2. require `repository` to equal `hackelia-micrantha/.github` for the first pilot;
3. require `expected_revision` to equal the running `github.sha`;
4. require `label` to be in the repository's selected canonical label set;
5. fetch live label state and regenerate the complete canonical plan;
6. require plan schema version 2 or later with stable GitHub label IDs captured for every selected existing canonical/alias/case snapshot and `stableIdentityComplete: true`;
7. fail closed unless the regenerated plan digest exactly equals `plan_sha256`;
8. require the requested label's current action to be exactly `create` and its first-pilot candidate flag to be true;
9. preserve `race_disposition_ref` as immutable dispatch evidence but not treat it as self-authorizing clearance;
10. expose only bounded, non-secret evidence required by downstream jobs.

### Protected-environment quarantine clearance

The protected `label-mutation` environment is part of the mutation authority boundary, not merely a confirmation click.

Before approving the apply job, the accountable reviewer must inspect prior mutation runs for the `.github` pilot and verify that none of these remain unresolved:

- `applied-with-race` receipts;
- `indeterminate-mutation` receipts;
- a prior apply job that may have reached mutation but has no terminal receipt;
- any other run explicitly marked `requiresDisposition: true`.

If an unresolved run exists, the reviewer must reject the new apply unless `race_disposition_ref` points to durable, reviewed disposition evidence covering every outstanding quarantine item. The environment approval and immutable dispatch input together record the clearance decision.

A run with `race_disposition_ref: none` may be approved only when the reviewer has verified there is no unresolved quarantine. If the platform cannot support this accountable review/recording boundary, mutation remains blocked until a machine-checkable quarantine mechanism is designed.

An `applied-with-race` or `indeterminate-mutation` receipt sets `requiresDisposition: true`. A missing terminal receipt after an apply job may have started is treated equivalently. That quarantine remains in force until human-reviewed durable disposition exists and a later protected-environment approval explicitly clears it. Merely generating a fresh plan/revision does not clear quarantine.

### Apply job

The apply job is the only job with `issues: write` and must be gated by the protected `label-mutation` environment or an explicitly reviewed equivalent boundary satisfying the quarantine-clearance contract above. The write-authorized job must not start—and therefore must not receive its write-capable job token—until approval succeeds.

After approval, the apply job must:

1. depend on successful preflight;
2. repeat the repository, ref, revision, label, and allowlist checks rather than trusting only preflight outputs;
3. record the approved `race_disposition_ref` in bounded evidence;
4. query the **live** `refs/heads/main` tip and require it to equal both `expected_revision` and the dispatch `github.sha`;
5. re-fetch live labels and regenerate the complete plan;
6. require plan schema/stable-identity completeness, the regenerated digest to equal the approved `plan_sha256`, and the requested label row to remain exactly `create`;
7. immediately before the single `POST`, query the live `main` tip again and re-fetch the requested canonical name plus configured aliases/case-equivalent names;
8. require that immediate operation precondition to match the approved `create` state;
9. mark durable bounded evidence that the mutation request is about to be attempted when the platform mechanism can do so without adding write authority outside the apply job;
10. perform exactly one create request;
11. capture the create response's stable GitHub label ID as `createdLabelId` when the request succeeds;
12. treat any conflict/validation failure, including an already-existing label, as terminal; never retry by reinterpreting changed state;
13. immediately after the request, query live `main`, re-fetch live labels, and regenerate the **complete canonical plan**;
14. require the post-plan to match the deterministic expected post-state: the requested row is exactly `no-op` with canonical name/color/description matching the approved desired snapshot, its stable label ID equals `createdLabelId`, no alias/case collision exists, and every other selected row retains the same action/current/desired state **and stable existing-label IDs** it had in the approved pre-plan;
15. classify any post-request control-plane advance or expected-post-plan/identity divergence as an applied race condition rather than plain success;
16. produce bounded outputs for the ungated receipt job.

The workflow must contain no mutation path that can be triggered from a pull request, fork, push, schedule, issue comment, repository dispatch, or unvalidated dynamic input.

### Receipt/finalizer job

The receipt job must have no label-write permission and no protected mutation environment. It must depend on preflight and apply with `if: always()` semantics and perform an independent read-only reconciliation whenever the apply job started or its mutation outcome is not conclusively known.

The receipt must distinguish these states:

- **`not-applied`** — the apply job never started, or reliable evidence proves the create request was not attempted;
- **`applied`** — the one create is known to have succeeded, `createdLabelId` is captured, and the complete postcondition is clean;
- **`applied-with-race`** — the create is known to have succeeded but control-plane or label-state/identity postconditions diverged;
- **`indeterminate-mutation`** — the apply job started and available evidence cannot prove whether the create request was accepted/completed, including runner loss/cancellation after the request may have been sent;
- **`failed`** — a non-mutation failure with reliable evidence that the create request was not attempted.

For any run where mutation may have occurred, the read-only finalizer must re-read live `main` and complete selected label state. Observed state is evidence only: when the create response/ID is unavailable, the finalizer must not attribute an existing matching label to this run merely because it is present.

The receipt must:

- record whether the write-authorized job started and its terminal job result;
- record `mutationStarted`, `mutationCompleted`, and `mutationOutcomeKnown` separately from the job result;
- record the reviewed `race_disposition_ref` supplied for this dispatch;
- record post-request control-plane, label-state, and stable-ID evidence when a create may have occurred;
- record `uncertaintyKinds`, including `mutation-outcome` for indeterminate runs;
- set `requiresDisposition: true` for `applied-with-race` and `indeterminate-mutation`;
- never infer that environment rejection, cancellation, a failed runner, or a skipped job did or did not perform a mutation without supporting evidence;
- preserve the terminal receipt as durable workflow evidence using a reviewed, pinned mechanism when the finalizer runs.

A whole-workflow cancellation or platform failure can prevent the finalizer itself from running. Therefore **absence of a terminal receipt for a run whose apply job may have started is itself quarantine evidence** and must block later mutation approval until durable manual reconciliation/disposition exists.

If GitHub does not expose the reason or reviewer identity for an environment rejection to the downstream job, the receipt must say so and link/reference the platform run/environment audit evidence rather than inventing attribution.

## Plan identity and stale-plan protection

An approved dry-run is evidence for one exact repository label state under one exact `.github` control-plane revision; it is not open-ended authorization.

The planner emits plan schema version 2 or later and computes `plan_sha256` over deterministic JSON containing at least:

- plan schema version;
- target repository;
- expected `.github` control-plane revision;
- label manifest digest;
- ordered selected canonical labels;
- complete normalized current snapshots for every selected canonical label and considered alias/case conflict, including stable GitHub label IDs for every existing label;
- desired canonical snapshots;
- ordered action classifications and reasons;
- `stableIdentityComplete`.

Stable identity is part of the approved state. Deleting and recreating a label with identical name/color/description changes its GitHub label ID and therefore changes the plan digest/postcondition.

The mutation workflow must regenerate this plan in read-only preflight and again in the write-authorized apply job after approval. The apply job must compare the expected revision with the live default-branch tip both when it starts and immediately before the one create request. After the create, it must regenerate the complete plan again and compare it with the deterministic expected post-state, including stable IDs, rather than checking only names/metadata.

Unrelated out-of-scope repository labels are preserved and need not invalidate a plan unless their name creates a selected canonical/alias/case collision.

A timestamp alone is not a stale-plan control. A prior successful plan must never be applied without exact current-state and live-control-plane revalidation. Likewise, a fresh plan does not clear unresolved mutation quarantine.

### Residual cross-API race

GitHub does not provide a transaction that atomically couples reading `refs/heads/main`, reading repository labels, and creating a repository label. Therefore an infinitesimal race remains between the final reads and the create request.

The first pilot bounds rather than conceals that limitation:

- one create is the maximum label effect of one dispatch;
- create cannot overwrite existing label metadata;
- a competing same-name create is treated as a terminal conflict/validation failure;
- a concurrent alias/case-equivalent create, canonical metadata edit, canonical delete/recreate, or other selected-label change can occur after the final pre-read, so the **complete plan including stable IDs is regenerated after the request**;
- the requested canonical ID must equal the successful create response ID;
- the receipt records `raceKinds` containing `control-plane`, `label-state`, or both when known post-request state differs from the approved invariant;
- `label-state` includes canonical absence, canonical metadata divergence, canonical ID divergence, canonical/alias/case collision, or any unexpected change/identity replacement of another selected row during the final API window;
- any detected known race yields overall result `applied-with-race`, not plain `applied`, sets `requiresDisposition: true`, and enters mutation quarantine;
- any unresolved mutation outcome yields `indeterminate-mutation`, also sets `requiresDisposition: true`, and enters quarantine;
- a clean `applied` result is allowed only when the post-request `main` tip is unchanged, the create response ID is known, and the complete post-plan including stable IDs matches the deterministic expected post-state.

If a future operation requires stronger atomicity than the GitHub API exposes, it must use a separately designed coordination mechanism or remain unsupported.

## Operation classes

### Initial pilot: one create only

The first implementation may authorize only:

- `create` — create one explicitly requested selected canonical label that is absent and has no configured alias/case-equivalent collision.

The manifest and plan may contain many `create` rows, but one dispatch authorizes exactly one named row. A second label requires a new dry-run/review/dispatch against then-current state and, when applicable, explicit clearance of any outstanding mutation quarantine.

### Metadata update

`update` remains report-only in the first mutation implementation.

GitHub documents conditional requests primarily for safe reads and does not document a conditional compare-and-swap contract for the repository-label update endpoint. A later update capability therefore requires a separate reviewed decision that explicitly accepts or mitigates the remaining API-level read/write race, defines exact overwrite/rollback semantics, and demonstrates why the capability is needed. It must not be enabled merely because the planner can classify an `update` row.

### Migration and rename

`migration` remains report-only in the first mutation implementation. An alias match never grants rename authority.

A later migration design must be separately reviewed and must identify:

- exact source and destination names and stable IDs;
- all open and closed issues and pull requests currently carrying the source label, or a deterministic digest plus complete retrievable evidence of that set;
- collision checks at apply time;
- the expected behavior of GitHub's label rename operation for existing associations;
- rollback/remediation constraints if the source name must be restored;
- how concurrent association changes are detected or dispositioned.

Migration authority must be explicit per source/destination pair. It must not be inferred from `aliases` alone.

### Delete and rollback delete

Delete is unsupported in the first implementation, including as rollback. No synchronization or rollback run may delete a repository label merely because it was created by the pilot, is unselected, aliased, superseded, or absent from the organization catalog.

The GitHub label API does not expose an atomic guard that can prove both label identity/metadata and absence of issue/PR associations at the instant of deletion. A future delete/rollback-delete capability therefore requires a separately reviewed coordination/atomicity design. Until then, a create inverse record is **evidence for manual disposition only**, not executable delete authority.

## Evidence record

Every dispatched mutation workflow should produce a durable JSON receipt from the ungated receipt/finalizer job when the platform schedules it after preflight/apply resolution. The receipt should contain:

- receipt schema version;
- target repository and requested label;
- GitHub run ID and run attempt;
- triggering actor;
- workflow/ref/control-plane revision;
- live default-branch revision observed when apply starts, immediately before the create, and immediately after it when available;
- plan digest, manifest digest, plan schema version, and `stableIdentityComplete`;
- normalized requested-label precondition snapshots including stable IDs for any existing alias/case state;
- reviewed `race_disposition_ref` for this dispatch;
- whether the write-authorized job started;
- `mutationStarted`, `mutationCompleted`, and `mutationOutcomeKnown`;
- API outcome/status and `createdLabelId` when a response is available;
- independent finalizer re-read evidence when mutation may have occurred;
- normalized post-plan evidence, including canonical/alias/case state and all selected-row actions/current/desired snapshots with stable existing-label IDs;
- `raceKinds` as an empty array for clean known state or containing `control-plane`, `label-state`, or both;
- `uncertaintyKinds`, including `mutation-outcome` when applicable;
- `requiresDisposition` boolean;
- overall result such as `not-applied`, `rejected-stale`, `rejected-collision`, `applied`, `applied-with-race`, `indeterminate-mutation`, or `failed`;
- non-executable inverse/remediation evidence for the created label when a create is known to have occurred.

Secrets, token material, private-key material, and unrelated repository contents must never appear in the receipt.

## Rollback and quarantine contract

Rollback/remediation data is generated from captured state, not reconstructed later.

For a known successful `create`, the inverse record identifies `createdLabelId` and its exact observed post-state. It **does not authorize deletion**. Any removal of that label requires a future separately reviewed delete/rollback design with a coordination mechanism strong enough to address concurrent association changes.

Because metadata `update`, migration/rename, and delete are not authorized in the first pilot, their rollback operations are also outside the first implementation.

The first pilot has no intended multi-write partial-apply state because one dispatch authorizes one create. A failed or indeterminate request does not authorize a retry under changed state. Remediation is a separate reviewed action, not an automatic failure handler.

An `applied-with-race` or `indeterminate-mutation` result is distinct from rollback: the create may have succeeded, but the authority/evidence invariant was not cleanly preserved. Both enter mutation quarantine. A missing terminal receipt after apply may have started enters the same quarantine. The next environment reviewer must require durable disposition evidence before approving another write.

## Idempotence and pilot evidence

The current `.github` report includes legacy alias migrations that are deliberately outside the first mutation authority. Pilot idempotence is measured over each explicitly authorized create, not over update/migration rows that remain report-only.

The first mutation pilot is complete only when all of the following evidence exists for `hackelia-micrantha/.github`:

1. a reviewed dry-run from the exact merged control-plane revision with plan schema version 2+, stable selected-label IDs, `stableIdentityComplete: true`, exact before/desired state, and `plan_sha256`;
2. one canonical `create` row is explicitly chosen for the first dispatch;
3. explicit dispatch names that repository, label, revision, digest, and quarantine-disposition reference;
4. preflight succeeds read-only;
5. environment approval gates the only write-authorized job and verifies there is no unresolved mutation quarantine or missing terminal receipt;
6. after approval, live `main`, full plan, stable IDs, and digest still match the approved evidence;
7. immediately before the create, live `main` and label/alias/case preconditions still match;
8. exactly one create request occurs;
9. the successful create response's stable label ID is captured;
10. immediately after the request, live `main` and the complete canonical plan including stable IDs are re-read;
11. the requested row is exact `no-op` at approved metadata, its ID equals the create response ID, no alias/case collision exists, and every other selected row retains approved pre-plan state and stable IDs;
12. a clean pilot requires overall result `applied`, empty `raceKinds`, empty `uncertaintyKinds`, `mutationOutcomeKnown: true`, and `requiresDisposition: false`;
13. `applied-with-race`, `indeterminate-mutation`, or a missing terminal receipt halts the pilot in mutation quarantine until durable manual disposition;
14. a fresh planner run later still returns `no-op` for the created row with the same stable ID and no introduced alias/case collision;
15. remaining create/update/migration/collision rows are unchanged and require separate dispatches or disposition;
16. the receipt contains non-executable inverse/remediation evidence for the created label;
17. independent review of the run evidence occurs before any second repository is allowlisted.

A pilot must not broaden its authority merely to make the whole report green. Deferred create/update/migration rows are valid evidence of a deliberately narrower capability boundary.

## Broader rollout gate

Do not expand beyond `.github` until the first pilot is reviewed and the one-create-per-dispatch contract has proven repeatable. Any cross-repository rollout additionally requires:

- a GitHub App installation token scoped to the exact reviewed repositories and `Issues: write`;
- token minting only in the approved apply job, after read-only preflight;
- explicit repository opt-in in the manifest;
- a reviewed per-repository serialization/quarantine mechanism; human environment review alone should be reconsidered before scale;
- the same live-default-branch, stable-ID, stale-plan, single-operation precondition, complete post-plan verification, indeterminate-outcome quarantine, and collision controls;
- protected handling of App credentials/private keys;
- repository-by-repository evidence and non-executable remediation records.

Organization-wide wildcard mutation is not an accepted operating mode.
