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

## Plan outcomes

The planner reports one of these outcomes for every selected canonical label:

- `no-op` — canonical name, color, and description already match;
- `create` — the canonical label is absent;
- `update` — the canonical label exists but its color or description differs;
- `migration` — the canonical label is absent and one documented compatibility alias exists;
- `collision` — applying a canonical label would be ambiguous because aliases or case-conflicting labels coexist.

Every action records the exact current label metadata involved and the exact desired canonical color and description. `update` and `migration` are observations, not authority to mutate. A collision is always visible and never silently overwritten.

Out-of-scope repository labels are listed separately as preserved evidence.

## Report workflow

`.github/workflows/label-sync-report.yml` runs the planner for the `.github` pilot on relevant pull requests, pushes to `main`, and manual dispatches.

The workflow:

- runs only on GitHub-hosted infrastructure;
- uses read-only `contents` and `issues` permissions;
- validates the manifest before querying labels;
- emits the exact before/desired plan to the GitHub Actions step summary;
- has a bounded 10-minute runtime;
- contains no mutation step and no write-scoped credential.

## Mutation boundary

There is intentionally no `apply` command.

Issue #76 and [label mutation authority and rollback](label-mutation-authority.md) define the next gate. The initial mutation implementation, if separately reviewed and added later, must remain narrower than the report planner:

- `.github` is the only first pilot target;
- mutation is explicit human dispatch on the default branch only;
- the approved plan is bound to an exact workflow revision and SHA-256 plan digest;
- live label state is re-read and the plan is regenerated immediately before mutation;
- stale-plan or collision differences fail closed;
- only `create` and same-name metadata `update` may be authorized initially;
- `migration`/rename remains report-only until separately authorized;
- delete remains unsupported;
- every attempted mutation emits before/after evidence and rollback data.

For the same-repository `.github` pilot, the narrow credential is the ephemeral repository-scoped `GITHUB_TOKEN` with `contents: read` and `issues: write`. Cross-repository rollout requires a short-lived GitHub App installation token scoped to the exact reviewed repositories with repository `Issues: write` only.

Organization-wide mutation must never be inferred from the existence of the catalog, from a successful report-only plan, or from an alias match.
