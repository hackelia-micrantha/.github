# Automation foundation

This directory documents the shared automation surfaces maintained by the Micrantha organization meta repository.

See [automation security boundaries](SECURITY.md) for the caller, input, secret, runner, and token trust model, [shared automation versioning](versioning.md) for immutable caller pins, compatibility, pilots, and rollback, and [label mutation authority](label-mutation-authority.md) for the separately reviewed write boundary that must exist before label synchronization can mutate repository state.

## Scope

The automation foundation provides:

- organization workflow starter templates under `workflow-templates/`;
- reusable, read-only CI workflows under `.github/workflows/`;
- a machine-readable repository registry under `metadata/`;
- registry validation and read-only repository-health reporting;
- report-only label synchronization planning;
- explicit adoption and trust-boundary guidance.

It does not automatically modify repository settings, labels, branch protections, secrets, environments, runners, releases, or repository files outside this repository. The current label synchronization implementation is report-only and contains no write path.

## Workflow starter templates

GitHub exposes files in `workflow-templates/` when organization repositories create a new Actions workflow. Each workflow file has a matching `.properties.json` metadata file.

The starter templates intentionally remain small:

- **Mise CI** runs a repository-defined `mise run ci` task through the shared reusable workflow.
- **Docs CI** runs a repository-defined `mise run docs-ci` task through the same shared workflow.
- **Nix flake CI** runs `nix flake check --print-build-logs` through the shared Nix workflow.

Repositories own the actual task definitions, test coverage, build graph, and required checks. A starter template is an adoption aid, not proof that the repository satisfies the organization standards.

GitHub replaces `$default-branch` when a starter template is installed. Repositories should review generated event triggers, runner selection, concurrency, permissions, task names, and the pinned shared-workflow revision before making the workflow required.

The starter templates are pinned to the reviewed automation-v1 candidate commit `c0016c206607f6f101b8e6b70340ad7d4ab52837`. They must not be changed back to `@main`; advancing the pin is a reviewed shared-automation version change.

## Reusable workflows

The initial reusable workflows are deliberately narrow:

- `.github/workflows/reusable-mise-ci.yml`
- `.github/workflows/reusable-nix-ci.yml`

They:

- use read-only `contents` permission;
- do not inherit or request caller secrets;
- use GitHub-hosted runners by default;
- expose bounded inputs for task, command, runner, working directory, and delegated-job timeout;
- pin external actions to reviewed commit SHAs;
- avoid deployment, release, mutation, or approval behavior.

Callers should pin reusable workflows to a reviewed immutable commit SHA or immutable release tag before treating them as required production gates. The execution identity is the commit SHA; a release tag is human-readable discovery metadata and must never move.

Permissions can only be maintained or reduced across a reusable workflow chain. A caller remains responsible for granting the minimum permissions required by its complete workflow.

## Repository registry

`metadata/repositories.json` is an advisory machine-readable projection of the canonical [repository responsibility catalogue](../architecture/repository-catalogue.md).

The registry records:

- repository location and visibility;
- default branch;
- classification and maturity;
- authoritative responsibility summary;
- whether health monitoring is enabled;
- the minimal files that the health report should verify.

The catalogue and repository-local evidence remain authoritative. Registry changes that alter ownership, maturity, or support claims require the same accountable review as the corresponding documentation changes.

`metadata/repositories.schema.json` supports editors and external validation. `tools/repository_health.py validate` performs dependency-free structural and semantic checks used by CI.

The registry is intentionally a **reviewed monitoring scope**, not an implicit list of every repository visible in the organization. [Repository registry coverage](repository-registry-coverage.md) records repositories intentionally excluded from health checks while ownership, lifecycle, or topology remains unresolved. Every organization repository should appear in exactly one of these two surfaces: the machine-readable registry or the reviewed exclusion record.

For repository creation, transfer, public/private split, supersession, or archival, update the registry or exclusion record in the same reviewed change. Do not infer authority from repository naming, visibility, age, or a `-community` suffix.

## Repository-health reporting

`.github/workflows/repository-health.yml` runs weekly and on reviewed registry/health changes to `main`, and remains manually dispatchable. It is read-only and produces Markdown and JSON reports.

The report checks registered repositories for:

- repository accessibility;
- visibility, archived state, and default-branch drift;
- configured required files;
- registry inconsistencies.

The built-in `GITHUB_TOKEN` can reliably inspect the current repository and public repositories. Routine health runs do not require a standing cross-repository credential solely to remove `unknown` results. Private repositories inaccessible to the workflow token remain `unknown`, not warning/error/deletion/lifecycle claims. If a complete private audit is needed, prefer a short-lived read-only GitHub App installation token scoped to the reviewed repository set.

The workflow never opens issues, changes labels, edits repositories, or alters settings. Health findings are evidence for human triage. A missing or inaccessible private repository is reported as unknown when the configured token cannot read it; it is not silently treated as deleted.

Before a repository is monitored, required-file expectations must be justified by that repository's actual contract. A health baseline remains non-blocking until false positives, inaccessible private repositories, and known topology differences are reconciled.

## Metadata validation

`.github/workflows/meta-validation.yml` validates:

- registry structure and semantics;
- workflow-template and `.properties.json` pairing;
- JSON metadata syntax;
- known reusable-workflow references from starter templates;
- label synchronization manifest semantics.

The workflow uses only read permissions and runs on pull requests and pushes to the default branch.

## Label synchronization

The current [label synchronization](label-synchronization.md) surface is deliberately report-only. It has a canonical machine-readable label catalog, explicit per-repository adoption, deterministic collision/migration planning, exact before/desired evidence, and no `apply` command.

Any future mutation must follow [label mutation authority and rollback](label-mutation-authority.md). In particular:

1. mutation remains separate from pull-request/push/scheduled reporting;
2. the first pilot is `.github` only, is **create-only**, and authorizes exactly **one explicitly named canonical label per human dispatch**;
3. read-only preflight, environment-gated write apply, and an ungated read-only receipt/finalizer remain separate jobs;
4. after approval and again immediately before the one create request, the live default-branch tip must still equal the approved control-plane revision;
5. stale-plan and collision checks fail closed and the requested label/alias/case precondition is re-read immediately before creation;
6. metadata update, migration/rename, and delete remain unsupported initially;
7. the receipt/finalizer records terminal evidence even when approval is rejected or the write job never starts;
8. cross-repository mutation requires a short-lived GitHub App installation token scoped to reviewed repositories and minimum label-management permission.

The create API does not make the branch-ref read and label write transactional. The pilot therefore bounds that residual race to one non-overwriting create and regenerates the **complete canonical plan** immediately after the request. Clean `applied` requires unchanged `main`, the requested row at exact `no-op` with approved metadata/no alias collision, and every other selected row unchanged. Any control-plane or expected-post-plan divergence is `applied-with-race` with explicit race kinds and blocks further mutation pending manual disposition.

## Adoption sequence

1. Confirm repository classification, maturity, and authority in the catalogue and registry.
2. Install the appropriate workflow starter template.
3. Define repository-owned `mise` tasks or Nix checks.
4. Review triggers, runners, permissions, fork behavior, and timeout expectations.
5. Run the workflow without making it required.
6. Reconcile failures and unsupported assumptions.
7. Keep the reusable workflow pinned to a reviewed immutable revision.
8. Make the stable check name required only after repeatable success.

## Change control

Changes to shared workflows can affect many repositories. Pull requests should identify:

- current callers and expected blast radius;
- compatibility and migration behavior;
- runner and action-runtime requirements;
- permission or secret changes;
- expected check-name changes;
- rollback or previous version;
- validation against at least one representative caller before release.
