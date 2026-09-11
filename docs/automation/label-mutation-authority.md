# Label mutation authority and rollback

This document defines the security and authority boundary that must exist before Micrantha label synchronization gains any write capability. It does **not** authorize or implement mutation.

Related: #27, #76, `label-synchronization.md`, and `SECURITY.md`.

## Decision

The first mutation pilot, if implemented, is restricted to `hackelia-micrantha/.github`, is **create-only**, and may create **one explicitly named canonical label per human dispatch**.

The workflow must run only from the default branch through explicit `workflow_dispatch`. For the same-repository pilot, prefer the ephemeral repository-scoped `GITHUB_TOKEN` and separate read from write authority across three jobs:

- **preflight** — `contents: read`, `issues: read`;
- **apply** — `contents: read`, `issues: write`; this is the only write-authorized job and is environment-gated;
- **receipt** — read-only, ungated, runs with `if: always()` after preflight/apply to preserve terminal evidence even when approval is rejected or cancelled.

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

## Event and approval boundary

The initial mutation workflow must expose only `workflow_dispatch` and must require explicit inputs:

- `repository`;
- `label` — one canonical label selected by that repository's reviewed manifest entry;
- `expected_revision` — the exact `.github` control-plane revision;
- `plan_sha256` — the exact reviewed dry-run digest.

### Preflight job

The preflight job has read-only permissions and must:

1. reject any ref other than `refs/heads/main`;
2. require `repository` to equal `hackelia-micrantha/.github` for the first pilot;
3. require `expected_revision` to equal the running `github.sha`;
4. require `label` to be in the repository's selected canonical label set;
5. fetch live label state and regenerate the complete canonical plan;
6. fail closed unless the regenerated plan digest exactly equals `plan_sha256`;
7. require the requested label's current action to be exactly `create` and its first-pilot candidate flag to be true;
8. expose only bounded, non-secret evidence required by downstream jobs.

### Apply job

The apply job is the only job with `issues: write` and must be gated by a protected `label-mutation` environment or an explicitly reviewed equivalent approval boundary. The write-authorized job must not start—and therefore must not receive its write-capable job token—until approval succeeds.

After approval, the apply job must:

1. depend on successful preflight;
2. repeat the repository, ref, revision, label, and allowlist checks rather than trusting only preflight outputs;
3. query the **live** `refs/heads/main` tip and require it to equal both `expected_revision` and the dispatch `github.sha`;
4. re-fetch live labels and regenerate the complete plan;
5. require the regenerated digest to equal the approved `plan_sha256` and the requested label row to remain exactly `create`;
6. immediately before the single `POST`, query the live `main` tip again and re-fetch the requested canonical name plus configured aliases/case-equivalent names;
7. require that immediate operation precondition to match the approved `create` state;
8. perform exactly one create request;
9. treat any conflict/validation failure, including an already-existing label, as terminal; never retry by reinterpreting changed state;
10. immediately after the request, re-read the live `main` tip **and the requested canonical name plus every configured alias/case-equivalent name**;
11. classify any post-request control-plane advance or newly introduced canonical/alias/case collision as an applied race condition rather than plain success;
12. produce bounded outputs for the ungated receipt job.

The workflow must contain no mutation path that can be triggered from a pull request, fork, push, schedule, issue comment, repository dispatch, or unvalidated dynamic input.

### Receipt/finalizer job

The receipt job must:

- have no label-write permission and no protected mutation environment;
- depend on preflight and apply with `if: always()` semantics so it can run after success, preflight failure, apply failure, cancellation, or environment rejection once GitHub resolves the gated job;
- record whether the write-authorized job started and its terminal job result;
- record `mutationStarted` and `mutationCompleted` separately from the job result;
- record post-request control-plane and label-state race evidence separately when a create occurred;
- never infer that environment rejection, cancellation, or a skipped job performed a mutation;
- preserve the terminal receipt as durable workflow evidence using a reviewed, pinned mechanism.

If GitHub does not expose the reason or reviewer identity for an environment rejection to the downstream job, the receipt must say so and link/reference the platform run/environment audit evidence rather than inventing attribution.

## Plan identity and stale-plan protection

An approved dry-run is evidence for one exact repository label state under one exact `.github` control-plane revision; it is not open-ended authorization.

The planner should emit a canonical machine-readable plan record and compute `plan_sha256` as SHA-256 over deterministic JSON containing at least:

- plan schema version;
- target repository;
- expected `.github` control-plane revision;
- label manifest digest;
- ordered selected canonical labels;
- complete normalized current snapshots for every selected canonical label and considered alias/case conflict;
- desired canonical snapshots;
- ordered action classifications and reasons.

The mutation workflow must regenerate this plan in read-only preflight and again in the write-authorized apply job after approval. The apply job must also compare the expected revision with the live default-branch tip both when it starts and immediately before the one create request.

Unrelated out-of-scope repository labels are preserved and need not invalidate a plan unless their name creates a selected canonical/alias/case collision.

A timestamp alone is not a stale-plan control. A prior successful plan must never be applied without exact current-state and live-control-plane revalidation.

### Residual cross-API race

GitHub does not provide a transaction that atomically couples reading `refs/heads/main`, reading repository labels, and creating a repository label. Therefore an infinitesimal race remains between the final reads and the create request.

The first pilot bounds rather than conceals that limitation:

- one create is the maximum effect of one dispatch;
- create cannot overwrite existing label metadata;
- a competing same-name create is treated as a terminal conflict/validation failure;
- a competing alias/case-equivalent create may coexist with the canonical create, so the canonical name, all configured aliases/case equivalents, and live `main` tip must be re-read immediately after the request;
- the receipt records `raceKinds` containing `control-plane`, `label-state`, or both when the post-request state differs from the approved invariant;
- any detected race yields overall result `applied-with-race`, not plain `applied`, and requires manual disposition before any further mutation;
- a clean `applied` result is allowed only when the post-request `main` tip and canonical/alias/case state still satisfy the approved invariant.

If a future operation requires stronger atomicity than the GitHub API exposes, it must use a separately designed coordination mechanism or remain unsupported.

## Operation classes

### Initial pilot: one create only

The first implementation may authorize only:

- `create` — create one explicitly requested selected canonical label that is absent and has no configured alias/case-equivalent collision.

The manifest and plan may contain many `create` rows, but one dispatch authorizes exactly one named row. A second label requires a new dry-run/review/dispatch against then-current state.

### Metadata update

`update` remains report-only in the first mutation implementation.

GitHub documents conditional requests primarily for safe reads and does not document a conditional compare-and-swap contract for the repository-label update endpoint. A later update capability therefore requires a separate reviewed decision that explicitly accepts or mitigates the remaining API-level read/write race, defines exact overwrite/rollback semantics, and demonstrates why the capability is needed. It must not be enabled merely because the planner can classify an `update` row.

### Migration and rename

`migration` remains report-only in the first mutation implementation. An alias match never grants rename authority.

A later migration design must be separately reviewed and must identify:

- exact source and destination names;
- all open and closed issues and pull requests currently carrying the source label, or a deterministic digest plus complete retrievable evidence of that set;
- collision checks at apply time;
- the expected behavior of GitHub's label rename operation for existing associations;
- rollback preconditions if the source name must be restored;
- how concurrent association changes are detected or dispositioned.

Migration authority must be explicit per source/destination pair. It must not be inferred from `aliases` alone.

### Delete

Delete is unsupported in the first implementation. No synchronization run may delete a repository label merely because it is unselected, aliased, superseded, or absent from the organization catalog.

## Evidence record

Every dispatched mutation workflow must produce a durable JSON receipt from the ungated receipt/finalizer job after GitHub resolves preflight and apply. The receipt should contain:

- receipt schema version;
- target repository and requested label;
- GitHub run ID and run attempt;
- triggering actor;
- workflow/ref/control-plane revision;
- live default-branch revision observed when apply starts, immediately before the create, and immediately after it when available;
- plan digest and manifest digest;
- normalized requested-label precondition snapshots;
- whether the write-authorized job started;
- whether mutation started/completed;
- API outcome/status when a request occurred;
- normalized post-mutation snapshots for the requested canonical label and all configured aliases/case-equivalent names;
- `raceKinds` as an empty array for clean state or containing `control-plane`, `label-state`, or both;
- overall result such as `not-applied`, `rejected-stale`, `rejected-collision`, `applied`, `applied-with-race`, or `failed`;
- rollback record derived from captured state when a create occurred.

Secrets, token material, private-key material, and unrelated repository contents must never appear in the receipt.

## Rollback contract

Rollback data is generated from captured state, not reconstructed later.

For a `create`, the inverse record identifies the created label and its exact post-state. Automatic deletion remains unsupported in the first implementation. A reviewed rollback may remove that label only if it still exactly matches the recorded post-state and has no issue or pull-request associations introduced after creation; otherwise it requires manual disposition.

Because metadata `update` is not authorized in the first pilot, update rollback is also outside the first implementation. A future update design must define its inverse and stale-post-state check before update authority exists.

The first pilot has no multi-write partial-apply state because one dispatch authorizes one create. A failed request does not authorize a retry under changed state. Rollback is a separate reviewed action, not an automatic failure handler.

## Idempotence and pilot evidence

The current `.github` report includes legacy alias migrations that are deliberately outside the first mutation authority. Pilot idempotence is measured over each explicitly authorized create, not over update/migration rows that remain report-only.

The first mutation pilot is complete only when all of the following evidence exists for `hackelia-micrantha/.github`:

1. a reviewed dry-run from the exact merged control-plane revision with exact before/desired state and `plan_sha256`;
2. one canonical `create` row is explicitly chosen for the first dispatch;
3. explicit dispatch names that repository, label, revision, and digest;
4. preflight succeeds read-only;
5. environment approval gates the only write-authorized job;
6. after approval, the live `main` tip and full plan still match the approved evidence;
7. immediately before the create, live `main` and label/alias/case preconditions still match;
8. exactly one create request occurs;
9. immediately after the request, live `main` plus the canonical/alias/case-equivalent set are re-read and the receipt records any `raceKinds`;
10. a clean pilot requires overall result `applied` with empty `raceKinds`; `applied-with-race` halts the pilot for manual disposition before any further mutation;
11. a fresh planner run returns `no-op` for the created row with no newly introduced alias/case collision;
12. remaining create/update/migration/collision rows are unchanged and require separate dispatches or disposition;
13. the ungated receipt contains deterministic rollback data for the created label;
14. independent review of the run evidence occurs before any second repository is allowlisted.

A pilot must not broaden its authority merely to make the whole report green. Deferred create/update/migration rows are valid evidence of a deliberately narrower capability boundary.

## Broader rollout gate

Do not expand beyond `.github` until the first pilot is reviewed and the one-create-per-dispatch contract has proven repeatable. Any cross-repository rollout additionally requires:

- a GitHub App installation token scoped to the exact reviewed repositories and `Issues: write`;
- token minting only in the approved apply job, after read-only preflight;
- explicit repository opt-in in the manifest;
- the same live-default-branch, stale-plan, single-operation precondition, post-write canonical/alias/case verification, and collision controls;
- protected handling of App credentials/private keys;
- repository-by-repository evidence and rollback records.

Organization-wide wildcard mutation is not an accepted operating mode.
