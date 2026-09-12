# Label synchronization

Organization-standard labels are reconciled conservatively. The current implementation is **report-only**: it can inventory a reviewed repository and describe what would change, but it cannot create, update, rename, or delete labels.

## Sources of truth

- `docs/standards/labels.md` defines the human-readable taxonomy and semantics.
- `metadata/labels.json` is the machine-readable synchronization manifest.
- `metadata/repositories.json` remains the repository registry. Every label-sync target must already exist there.
- `tools/label_sync.py` validates the manifest and produces deterministic plans.
- `docs/automation/label-mutation-authority.md` defines the separate security/authority contract that must be satisfied before any mutation implementation exists.

The validator requires the managed `priority:`, `status:`, `type:`, `area:`, and `maturity:` label names in `metadata/labels.json` to match the labels documented in `docs/standards/labels.md`. A manifest entry cannot silently introduce a new organization-standard label.

Compatibility aliases are intentionally conservative. An alias is recorded only when the legacy meaning is unambiguous for the canonical dimension. Generic names that could map to multiple dimensions are preserved for explicit review rather than guessed.

## Explicit adoption

The catalog is organization-wide; synchronization is not.

`metadata/labels.json` contains an explicit repository allowlist. Each allowlisted repository selects only the canonical labels it intends to adopt. Every existing label outside that selected synchronization surface—including an organization-standard label that the repository has not selected—is reported as preserved.

The initial pilot allowlists only `hackelia-micrantha/.github` in `report-only` mode.

## Plan outcomes and identity

The planner reports one of these outcomes for every selected canonical label:

- `no-op` — canonical name, color, and description already match;
- `create` — the canonical label is absent;
- `update` — the canonical label exists but its color or description differs;
- `migration` — the canonical label is absent and one documented compatibility alias exists;
- `collision` — applying a canonical label would be ambiguous because aliases or case-conflicting labels coexist.

Every action records the exact current label metadata involved and the exact desired canonical color and description. Plan schema version 2 also records GitHub's stable numeric label ID for every selected existing canonical/alias/case snapshot. Those IDs are part of `planSha256`, so delete/recreate with identical visible metadata changes the plan identity. `stableIdentityComplete` reports whether every selected existing snapshot carried a stable ID.

An action classification is evidence, not mutation authority. A collision is always visible and never silently overwritten. Out-of-scope repository labels are listed separately as preserved evidence and do not affect the mutation-relevant plan digest unless they enter a selected canonical/alias/case namespace.

## Report workflow

`.github/workflows/label-sync-report.yml` runs the planner for the `.github` pilot on relevant pull requests, pushes to `main`, and manual dispatches.

The workflow:

- runs only on GitHub-hosted infrastructure;
- uses read-only `contents` and `issues` permissions;
- validates the manifest before querying labels;
- emits the exact before/desired plan, stable selected-label identity status, and plan digest to the GitHub Actions step summary;
- has a bounded 10-minute runtime;
- contains no mutation step and no write-scoped credential.

## Mutation boundary

There is intentionally no `apply` command.

Issue #76 and [label mutation authority and rollback](label-mutation-authority.md) define the next gate. The initial mutation implementation, if separately reviewed and added later, must remain narrower than the report planner:

- `.github` is the only first pilot target;
- mutation is explicit human dispatch on the default branch only;
- one dispatch names and authorizes at most one selected canonical `create` row;
- read-only preflight, environment-gated write-authorized apply, and an ungated read-only receipt/finalizer are separate jobs;
- a fixed non-cancelling concurrency group serializes first-pilot mutation runs;
- the approved plan is bound to an exact control-plane revision, plan schema, stable label identities, and SHA-256 plan digest;
- mutation preflight/apply require `stableIdentityComplete: true` for selected existing state;
- after approval and immediately before the single create request, apply must verify that the **live** `main` tip still equals the approved revision;
- live label state is re-read and the complete plan is regenerated before mutation;
- the requested canonical/alias/case-equivalent precondition is re-read immediately before creation;
- a successful create must capture GitHub's returned stable label ID;
- after the request, the complete plan is regenerated and the requested canonical ID must equal the create response ID while every other selected existing label retains its approved stable ID;
- stale-plan, identity, or collision differences fail closed;
- metadata `update`, `migration`/rename, and delete remain report-only/unsupported until separately reviewed;
- **delete remains unsupported even as rollback**; inverse create evidence is remediation evidence only;
- the receipt/finalizer distinguishes known clean apply, known race, known non-apply, and an indeterminate mutation outcome.

For the same-repository `.github` pilot, the narrow credential is the ephemeral repository-scoped `GITHUB_TOKEN`; only the apply job receives `contents: read` and `issues: write`. Cross-repository rollout requires a short-lived GitHub App installation token scoped to the exact reviewed repositories with repository `Issues: write` only.

The protected environment is also the first-pilot quarantine boundary. Before approving another apply, its reviewer must verify that no prior `applied-with-race`, `indeterminate-mutation`, `requiresDisposition: true`, or missing-terminal-receipt state remains unresolved. If quarantine exists, the immutable dispatch must reference durable reviewed disposition evidence through `race_disposition_ref`; a fresh plan/revision alone does not clear quarantine.

If the apply runner is lost/cancelled after a create request may have been sent but before a reliable response/ID is recorded, the finalizer must re-read live state without claiming attribution and record `indeterminate-mutation` with `requiresDisposition: true`. If a whole-workflow cancellation prevents the finalizer from producing a terminal receipt after apply may have started, the missing receipt itself is quarantine evidence.

The create-only boundary deliberately avoids the repository-label `PATCH` race: GitHub does not document conditional compare-and-swap semantics for that unsafe update operation. A later metadata-update capability therefore requires its own reviewed need, concurrency semantics, and rollback design.

GitHub also does not make the final branch-ref/label reads and label-create request transactional. The first pilot bounds that residual race to one non-overwriting create per dispatch and regenerates the **complete canonical plan including stable IDs** after the request. Clean `applied` requires unchanged `main`, a known create response ID, the requested row at exact approved `no-op` state with that same ID and no alias/case collision, and every other selected row unchanged in visible state and stable identity. Known divergence yields `applied-with-race`; unknown mutation outcome yields `indeterminate-mutation`. Both quarantine further mutation pending durable disposition.

Organization-wide mutation must never be inferred from the existence of the catalog, from a successful report-only plan, from an `update`/`migration` classification, or from an alias match.
