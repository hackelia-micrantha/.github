# Label mutation authority and rollback

This document defines the security and authority boundary that must exist before Micrantha label synchronization gains any write capability. It does **not** authorize or implement mutation.

Related: #27, #76, `label-synchronization.md`, and `SECURITY.md`.

## Decision

The first mutation pilot, if implemented, is restricted to `hackelia-micrantha/.github` and must run only through an explicit human-triggered workflow on the default branch.

For that same-repository pilot, prefer the ephemeral repository-scoped `GITHUB_TOKEN`. Read-only preflight and write-authorized apply must be separate jobs:

- preflight: `contents: read`, `issues: read`;
- apply: `contents: read`, `issues: write`.

No `contents: write`, `actions: write`, `workflows: write`, administration permission, organization permission, or inherited secret is required for label create/update operations.

If synchronization later targets a different repository, the built-in token is no longer the intended authority boundary. Cross-repository mutation must use a short-lived GitHub App installation token with repository access limited to the reviewed target set and repository `Issues: write` only. A fine-grained personal access token is a fallback only when a GitHub App cannot provide the required capability; a classic PAT or broad personal credential is not acceptable.

### Rejected alternatives

- **Broad personal token** — rejected because authority, rotation, repository scope, and attribution are unnecessarily coupled to a human account.
- **Organization-admin token/App permissions** — rejected because repository label management does not require organization administration.
- **Write-scoped token in the preflight/report job** — rejected because generating evidence does not require mutation authority.
- **Write-scoped token on pull-request, push, schedule, or `pull_request_target` events** — rejected because unreviewed or ambient events must not create mutation authority.
- **Cross-repository use of the default `GITHUB_TOKEN`** — rejected as an architecture assumption; cross-repository authority must be separately scoped and explicit.

## Event and approval boundary

The initial mutation workflow must expose only `workflow_dispatch` and contain two jobs.

### Preflight job

The preflight job has read-only permissions and must:

1. reject any ref other than `refs/heads/main`;
2. require explicit inputs for `repository`, `expected_revision`, and `plan_sha256`;
3. require `repository` to equal `hackelia-micrantha/.github` for the first pilot;
4. require `expected_revision` to equal the running `github.sha`; this is the reviewed `.github` control-plane revision containing the workflow and manifest;
5. fetch live label state and regenerate the canonical plan;
6. fail closed unless the regenerated plan digest exactly equals `plan_sha256`;
7. expose only bounded, non-secret outputs required by the apply job.

### Apply job

The apply job is the only job with `issues: write`. It must:

1. depend on successful preflight;
2. repeat the repository/ref/revision allowlist checks rather than trusting only job outputs;
3. re-fetch live labels after the apply job starts and regenerate the plan again;
4. compare the regenerated digest to the same approved `plan_sha256` immediately before the first write;
5. abort before mutation on any drift, collision, changed operation class, or changed manifest/control-plane revision;
6. execute only operation classes separately authorized for the pilot;
7. emit the mutation receipt even on rejection or partial failure.

A protected environment named for label mutation should gate the apply job so approval occurs before the write-authorized job starts. If the repository cannot provide an equivalent approval gate, mutation remains blocked until an alternative is explicitly reviewed.

The workflow must contain no path that can be triggered from a pull request, fork, push, schedule, issue comment, repository dispatch, or unvalidated dynamic input.

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

The mutation workflow must regenerate this plan twice: once in read-only preflight and again in the write-authorized apply job immediately before mutation. Any difference in relevant label name, color, description, alias/collision state, selected-label set, manifest digest, control-plane revision, or action classification changes the digest and must abort the run.

Unrelated out-of-scope repository labels are preserved and need not invalidate a plan unless their new name creates a selected canonical/alias/case collision.

A timestamp alone is not a stale-plan control. A prior successful plan must never be applied without exact current-state revalidation.

## Operation classes

### Initial pilot: create and metadata update only

The first implementation may authorize only:

- `create` — create a selected canonical label that is still absent;
- `update` — change color and/or description of an existing selected canonical label whose name is unchanged.

Both operations require exact preconditions from the approved plan. A create must fail if any canonical, alias, or case-conflicting label appears after planning. An update must fail if the existing label snapshot differs from the approved snapshot.

Operation order must be deterministic and recorded in the plan. The runner stops on the first failed write and does not automatically attempt rollback.

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

Every attempted apply run must emit a durable JSON receipt, even when it aborts before mutation. The receipt should contain:

- receipt schema version;
- target repository;
- GitHub run ID and run attempt;
- triggering actor;
- workflow/ref/control-plane revision;
- plan digest and manifest digest;
- normalized pre-mutation label snapshots;
- ordered requested operations;
- per-operation outcome and API status;
- normalized post-mutation snapshots;
- overall result: `applied`, `no-op`, `rejected-stale`, `rejected-collision`, `failed`, or `partially-applied`;
- rollback record derived from the captured pre-mutation state.

Secrets, token material, private-key material, and unrelated repository contents must never appear in the receipt.

## Rollback contract

Rollback data is generated from captured state, not reconstructed later.

For an `update`, the inverse record restores the exact previous color and description, but only if the live label still matches the mutation run's recorded post-state. Otherwise rollback must stop as stale.

For a `create`, the inverse record identifies the created label and its exact post-state. Automatic deletion remains unsupported in the first implementation. A reviewed rollback may remove that label only if it still exactly matches the recorded post-state and has no issue or pull-request associations introduced after creation; otherwise it requires manual disposition.

A partially applied run must stop on the first failed operation, emit evidence for every completed and unattempted operation, and never guess at rollback. Rollback is a separate reviewed action, not an automatic failure handler.

## Idempotence and pilot evidence

The current `.github` report includes legacy alias migrations that are deliberately outside the first mutation authority. Therefore pilot idempotence is measured over the **mutation-authorized create/update surface**, not over migration rows that remain report-only.

The first mutation pilot is complete only when all of the following evidence exists for `hackelia-micrantha/.github`:

1. a reviewed dry-run from the exact merged control-plane revision with exact before/desired state and `plan_sha256`;
2. the plan explicitly identifies which rows are mutation-authorized (`create`/`update`) and which rows remain non-mutating (`migration`, `collision`, `no-op`);
3. explicit dispatch against that same reviewed revision and plan digest;
4. successful writes for authorized create/update rows only;
5. a post-run live inventory matching the desired state for the authorized create/update surface;
6. a fresh planner run returning `no-op` for every row that the pilot was authorized to create or update;
7. any remaining migration/collision rows are unchanged and explicitly dispositioned as deferred, blocked, or separately proposed work;
8. a receipt containing deterministic rollback data;
9. independent review of the run evidence before any second repository is allowlisted.

A pilot must not broaden its authority merely to make the whole report green. Deferred migration rows are valid evidence of a deliberately narrower capability boundary.

## Broader rollout gate

Do not expand beyond `.github` until the first pilot's authorized surface is idempotent and reviewed, and every remaining migration/collision row has an explicit disposition. Any cross-repository rollout additionally requires:

- a GitHub App installation token scoped to the exact reviewed repositories and `Issues: write`;
- token minting only in the approved apply job, after read-only preflight;
- explicit repository opt-in in the manifest;
- the same stale-plan and collision controls;
- protected handling of App credentials/private keys;
- repository-by-repository evidence and rollback records.

Organization-wide wildcard mutation is not an accepted operating mode.
