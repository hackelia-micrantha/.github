# Automation foundation

This directory documents the shared automation surfaces maintained by the Micrantha organization meta repository.

See [automation security boundaries](SECURITY.md) for the caller, input, secret, runner, and token trust model.

## Scope

The automation foundation provides:

- organization workflow starter templates under `workflow-templates/`;
- reusable, read-only CI workflows under `.github/workflows/`;
- a machine-readable repository registry under `metadata/`;
- registry validation and read-only repository-health reporting;
- explicit adoption and trust-boundary guidance.

It does not automatically modify repository settings, labels, branch protections, secrets, environments, runners, releases, or repository files outside this repository.

## Workflow starter templates

GitHub exposes files in `workflow-templates/` when organization repositories create a new Actions workflow. Each workflow file has a matching `.properties.json` metadata file.

The starter templates intentionally remain small:

- **Mise CI** runs a repository-defined `mise run ci` task through the shared reusable workflow.
- **Docs CI** runs a repository-defined `mise run docs-ci` task through the same shared workflow.
- **Nix flake CI** runs `nix flake check --print-build-logs` through the shared Nix workflow.

Repositories own the actual task definitions, test coverage, build graph, and required checks. A starter template is an adoption aid, not proof that the repository satisfies the organization standards.

GitHub replaces `$default-branch` when a starter template is installed. Repositories should review generated event triggers, runner selection, concurrency, permissions, and task names before making the workflow required.

## Reusable workflows

The initial reusable workflows are deliberately narrow:

- `.github/workflows/reusable-mise-ci.yml`
- `.github/workflows/reusable-nix-ci.yml`

They:

- use read-only `contents` permission;
- do not inherit or request caller secrets;
- use GitHub-hosted runners by default;
- expose bounded inputs for task, command, runner, and working directory;
- pin external actions to reviewed commit SHAs;
- avoid deployment, release, mutation, or approval behavior.

Callers should pin reusable workflows to a reviewed release tag or commit SHA before treating them as required production gates. The starter templates use `@main` only as an initial adoption path until a versioned automation release is published.

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

## Repository-health reporting

`.github/workflows/repository-health.yml` runs weekly and on manual dispatch. It is read-only and produces Markdown and JSON reports.

The report checks registered repositories for:

- repository accessibility;
- visibility, archived state, and default-branch drift;
- configured required files;
- registry inconsistencies.

The built-in `GITHUB_TOKEN` can reliably inspect the current repository and public repositories. To include private organization repositories, configure an organization or repository secret named `ORG_REPOSITORY_READ_TOKEN` containing a fine-grained token or GitHub App token with read-only access to the registered repositories and repository contents.

The workflow never opens issues, changes labels, edits repositories, or alters settings. Health findings are evidence for human triage. A missing or inaccessible private repository is reported as unknown when the configured token cannot read it; it is not silently treated as deleted.

## Metadata validation

`.github/workflows/meta-validation.yml` validates:

- registry structure and semantics;
- workflow-template and `.properties.json` pairing;
- JSON metadata syntax;
- known reusable-workflow references from starter templates.

The workflow uses only read permissions and runs on pull requests and pushes to the default branch.

## Label synchronization

Organization-wide label synchronization is intentionally not included in this slice. Label mutation requires explicit credentials, collision handling, repository opt-in, dry-run evidence, and a rollback strategy.

A future label-sync workflow should:

1. read the shared taxonomy from `docs/standards/labels.md` or a derived machine-readable source;
2. default to dry-run;
3. require an explicit repository allowlist;
4. preserve repository-specific labels;
5. never delete or rename labels without a reviewed migration plan;
6. use a dedicated least-privilege GitHub App or fine-grained token;
7. emit a complete before-and-after report.

## Adoption sequence

1. Confirm repository classification, maturity, and authority in the catalogue and registry.
2. Install the appropriate workflow starter template.
3. Define repository-owned `mise` tasks or Nix checks.
4. Review triggers, runners, permissions, and fork behavior.
5. Run the workflow without making it required.
6. Reconcile failures and unsupported assumptions.
7. Pin the reusable workflow to a reviewed version.
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
