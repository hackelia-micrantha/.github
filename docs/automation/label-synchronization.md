# Label synchronization

Organization-standard labels are reconciled conservatively. The first implementation is **report-only**: it can inventory a reviewed repository and describe what would change, but it cannot create, update, rename, or delete labels.

## Sources of truth

- `docs/standards/labels.md` defines the human-readable taxonomy and semantics.
- `metadata/labels.json` is the machine-readable synchronization manifest.
- `metadata/repositories.json` remains the repository registry. Every label-sync target must already exist there.
- `tools/label_sync.py` validates the manifest and produces deterministic plans.

The validator requires the managed `priority:`, `status:`, `type:`, `area:`, and `maturity:` label names in `metadata/labels.json` to match the labels documented in `docs/standards/labels.md`. A manifest entry cannot silently introduce a new organization-standard label.

## Explicit adoption

The catalog is organization-wide; synchronization is not.

`metadata/labels.json` contains an explicit repository allowlist. Each allowlisted repository selects only the canonical labels it intends to adopt. A repository-specific label that is not selected remains outside the synchronization surface and is preserved.

The initial pilot allowlists only `hackelia-micrantha/.github` in `report-only` mode.

## Plan outcomes

The planner reports one of these outcomes for every selected canonical label:

- `no-op` — canonical name, color, and description already match;
- `create` — the canonical label is absent;
- `update` — the canonical label exists but its color or description differs;
- `migration` — the canonical label is absent and one documented compatibility alias exists;
- `collision` — applying a canonical label would be ambiguous because aliases or case-conflicting labels coexist.

`update` and `migration` are observations, not authority to mutate. A collision is always visible and never silently overwritten.

Repository-specific labels are listed separately as preserved evidence.

## Report workflow

`.github/workflows/label-sync-report.yml` runs the planner for the `.github` pilot on relevant pull requests, pushes to `main`, and manual dispatches.

The workflow:

- runs only on GitHub-hosted infrastructure;
- uses read-only `contents` and `issues` permissions;
- validates the manifest before querying labels;
- emits the exact plan to the GitHub Actions step summary;
- has a bounded 10-minute runtime;
- contains no mutation step and no write-scoped credential.

## Mutation boundary

There is intentionally no `apply` command.

A later reviewed slice may add mutation only after issue #27 records an explicit target/label allowlist, reviewed dry-run evidence, a dedicated least-privilege credential or GitHub App, collision/migration handling, before/after evidence, rollback behavior, and an independently reviewed opt-in mutation boundary.

Rename and delete remain disabled unless a separate migration explicitly authorizes them. Organization-wide mutation must never be inferred from the existence of the catalog or from a report-only plan.
