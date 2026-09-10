# Label mutation authority and rollback

This document defines the security and authority boundary that must exist before Micrantha label synchronization gains any write capability. It does **not** authorize or implement mutation.

Related: #27, #76, `label-synchronization.md`, and `SECURITY.md`.

## Decision

The first mutation pilot, if implemented, is restricted to `hackelia-micrantha/.github` and must run only through an explicit human-triggered workflow on the default branch.

For that same-repository pilot, prefer the ephemeral repository-scoped `GITHUB_TOKEN`. Read-only preflight and write-authorized apply must be separate jobs:

- preflight: `contents: read`, `issues: read`;
- apply: `contents: read`, `issues: write`.

No `contents: write`, `actions: write`, `workflows: write`, administration permission, organization permission, or inherited secret is required for repository label creation.

If synchronization later targets a different repository, the built-in token is no longer the intended authority boundary. Cross-repository mutation must use a short-lived GitHub App installation token with repository access limited to the reviewed target set and repository `Issues: write` only. A fine-grained personal access token is a fallback only when a GitHub App cannot provide the required capability; a classic PAT or broad personal credential is not acceptable.

### Rejected alternatives

- **Broad personal token** — rejected because authority, rotation, repository scope, and attribution are unnecessarily coupled to a human account.
- **Organization-admin token/App permissions** — rejected because repository label management does not require organization administration.
- **Write-scoped token in the preflight/report job** — rejected because generating evidence does not require mutation authority.
- **Write-scoped token on pull-request, push, schedule, or `pull_request_target` events** — rejected because unreviewed or ambient events must not create mutation authority.
- **Cross-repository use of the default `GITHUB_TOKEN`** — rejected as an architecture assumption; cross-repository authority must be separately scoped and explicit.
- **Metadata update in the first pilot** — rejected because GitHub does not document conditional/CAS semantics for the label `PATCH` endpoint. A read immediately before `PATCH` cannot eliminate the remaining read/write race, so the first pilot avoids an operation that could overwrite concurrent metadata changes.

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
3. after any environment approval, query the live `refs/heads/main` tip and require it to equal both `expected_revision` and the dispatch `github.sha`; an advanced default branch makes the approved control plane stale and aborts the run;
4. re-fetch live labels after the apply job starts and regenerate the complete plan again;
5. compare the regenerated digest to the same approved `plan_sha256` before any write;
6. abort before mutation on any drift, collision, changed operation class, changed manifest, or changed control-plane revision;
7. execute only operation classes separately authorized for the pilot;
8. immediately before **each** create, re-fetch that canonical name plus its configured aliases/case-equivalent names and require the exact approved create precondition to remain true;
9. stop on the first API conflict/failure rather than retrying a changed state as though it were still approved;
10. emit the mutation receipt even on rejection or partial failure.

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

The mutation workflow must regenerate this plan twice: once in read-only preflight and again in the write-authorized apply job after approval and before mutation. It must also compare the expected revision with the **live** default-branch tip at apply time. Any difference in relevant label name, color, description, alias/collision state, selected-label set, manifest digest, control-plane revision, or action classification changes the authorization condition and must abort the run.

Unrelated out-of-scope repository labels are preserved and need not invalidate a plan unless their new name creates a selected canonical/alias/case collision.

A timestamp alone is not a stale-plan control. A prior successful plan must never be applied without exact current-state and live-control-plane revalidation.

## Operation classes

### Initial pilot: create only

The first implementation may authorize only:

- `create` — create a selected canonical label that is absent and has no configured alias/case-equivalent collision.

A create requires exact preconditions from the approved plan and an immediate per-operation read immediately before the `POST`. If another actor creates or changes a conflicting label between that read and the API request, the request must be treated as a conflict/failure and the run must stop; it must not reinterpret the new state or continue under broadened authority.

Operation order must be deterministic and recorded in the plan. The runner stops on the first failed write and does not automatically attempt rollback.

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

Every attempted apply run must emit a durable JSON receipt, even when it aborts before mutation. The receipt should contain:

- receipt schema version;
- target repository;
- GitHub run ID and run attempt;
- triggering actor;
- workflow/ref/control-plane revision;
- live default-branch revision observed after approval;
- plan digest and manifest digest;
- normalized pre-mutation label snapshots;
- ordered requested operations;
- per-operation immediate precondition snapshot, outcome, and API status;
- normalized post-mutation snapshots;
- overall result: `applied`, `no-op`, `rejected-stale`, `rejected-collision`, `failed`, or `partially-applied`;
- rollback record derived from the captured pre-mutation state.

Secrets, token material, private-key material, and unrelated repository contents must never appear in the receipt.

## Rollback contract

Rollback data is generated from captured state, not reconstructed later.

For a `create`, the inverse record identifies the created label and its exact post-state. Automatic deletion remains unsupported in the first implementation. A reviewed rollback may remove that label only if it still exactly matches the recorded post-state and has no issue or pull-request associations introduced after creation; otherwise it requires manual disposition.

Because metadata `update` is not authorized in the first pilot, update rollback is also outside the first implementation. A future update design must define its inverse and stale-post-state check before update authority exists.

A partially applied run must stop on the first failed operation, emit evidence for every completed and unattempted operation, and never guess at rollback. Rollback is a separate reviewed action, not an automatic failure handler.

## Idempotence and pilot evidence

The current `.github` report includes legacy alias migrations that are deliberately outside the first mutation authority. Therefore pilot idempotence is measured over the **mutation-authorized create surface**, not over update/migration rows that remain report-only.

The first mutation pilot is complete only when all of the following evidence exists for `hackelia-micrantha/.github`:

1. a reviewed dry-run from the exact merged control-plane revision with exact before/desired state and `plan_sha256`;
2. the plan explicitly identifies which rows are mutation-authorized (`create`) and which rows remain non-mutating (`update`, `migration`, `collision`, `no-op`);
3. explicit dispatch against that same reviewed revision and plan digest;
4. after approval, the live `main` tip still equals the expected revision;
5. successful writes for authorized create rows only, each with an immediate precondition check;
6. a post-run live inventory matching the desired state for the authorized create surface;
7. a fresh planner run returning `no-op` for every row that the pilot was authorized to create;
8. any remaining update/migration/collision rows are unchanged and explicitly dispositioned as deferred, blocked, or separately proposed work;
9. a receipt containing deterministic rollback data;
10. independent review of the run evidence before any second repository is allowlisted.

A pilot must not broaden its authority merely to make the whole report green. Deferred update/migration rows are valid evidence of a deliberately narrower capability boundary.

## Broader rollout gate

Do not expand beyond `.github` until the first pilot's authorized create surface is idempotent and reviewed, and every remaining update/migration/collision row has an explicit disposition. Any cross-repository rollout additionally requires:

- a GitHub App installation token scoped to the exact reviewed repositories and `Issues: write`;
- token minting only in the approved apply job, after read-only preflight;
- explicit repository opt-in in the manifest;
- the same live-default-branch, stale-plan, per-operation precondition, and collision controls;
- protected handling of App credentials/private keys;
- repository-by-repository evidence and rollback records.

Organization-wide wildcard mutation is not an accepted operating mode.
