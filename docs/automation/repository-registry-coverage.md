# Repository registry coverage

This document records the organization-wide repository census used to bound the Micrantha repository-health baseline.

The machine-readable registry in `metadata/repositories.json` remains the monitored set. Repositories listed here are **intentionally excluded from automated health checks until their ownership, lifecycle, topology, or repository-health contract is explicitly reconciled**. Exclusion is not a claim that a repository is obsolete, unsupported, outside the project portfolio, or safe to archive.

Canonical project identity and portfolio tier are owned separately by `hackelia-micrantha/hackelia-micrantha/registry/projects.yaml`. Repository-health inclusion/exclusion must not be used to infer portfolio membership.

## Census method

The census is derived from the repositories visible to the organization GitHub installation and records GitHub state directly rather than inferring it from names or old documentation.

For each unregistered repository this document records:

- current visibility;
- current default branch;
- current GitHub archive state;
- the reason it is not yet part of the monitored health baseline.

Repository-local evidence and the canonical responsibility catalogue remain authoritative for implementation ownership and maturity. The canonical project registry remains authoritative for project identity and portfolio tier.

## Current exclusions

### Historical or unclassified surfaces

These repositories predate the current responsibility catalogue or do not yet have a reviewed current project identity. They are excluded from health monitoring until a concrete owner/lifecycle decision is made.

| Repository | Visibility | Default branch | Archived | Baseline disposition |
| --- | --- | --- | --- | --- |
| `stimulus` | private | `main` | no | Unclassified historical testing/tooling surface; ownership review required. |
| `micra` | private | `master` | no | Historical project/build tool; ownership and supersession review required. |
| `garden` | private | `master` | no | Historical Garden project surface; explicitly outside portfolio scope; lifecycle/repository disposition remains separate work. |
| `garden-library` | private | `master` | no | Historical Garden shared library; outside portfolio scope with its project family. |
| `garden-sdk` | private | `master` | no | Historical Garden SDK; outside portfolio scope with its project family. |
| `garden-nursery` | private | `master` | no | Historical Garden frontend; outside portfolio scope with its project family. |
| `scouter` | private | `master` | no | Historical Scouter project surface; explicitly outside portfolio scope; lifecycle/repository disposition remains separate work. |
| `scouter-backend` | private | `master` | no | Historical Scouter backend; outside portfolio scope with its project family. |
| `scouter-frontend` | private | `master` | no | Historical Scouter frontend; outside portfolio scope with its project family. |
| `scouter-prototype` | private | `main` | no | Historical Android prototype; outside portfolio scope with its project family. |
| `sandbox` | private | `main` | no | Unclassified development-environment experiment; reconcile against Sandcastle/Dubnium before assigning authority. |
| `codemux` | private | `main` | no | Unclassified live-coding tool; ownership review required. |
| `lab-service` | private | `main` | no | Unclassified lab support service; ownership review required. |
| `kredux` | private | `main` | no | Unclassified Kotlin library; ownership/support review required. |
| `pura` | private | `main` | no | Unclassified application repository; lifecycle decision required. |
| `yard` | private | `main` | no | Unclassified data-oriented repository; ownership review required. |

### Current-project repository-health exclusions

These repositories are associated with reviewed current projects or shared infrastructure, but are still outside automated health checks until their repository-level monitoring contract or auxiliary topology is explicitly reviewed. Their presence here does not make their project identity undecided.

| Repository | Visibility | Default branch | Archived | Baseline disposition |
| --- | --- | --- | --- | --- |
| `outermesh` | private | `master` | no | Canonical root of the registered supporting Outermesh project; keep outside health monitoring until current required-file/default-branch expectations are reviewed. |
| `outermesh-book` | private | `master` | no | Publication surface associated with the registered Outermesh project; auxiliary topology/monitoring contract still requires review. |
| `outermesh-web` | private | `master` | no | Web surface associated with the registered Outermesh project; auxiliary topology/monitoring contract still requires review. |
| `fortunes-service` | private | `main` | no | Candidate Fortunes service component; reconcile against canonical Fortunes composition. |
| `fortunes-cli` | private | `master` | no | Candidate Fortunes CLI/adapter; reconcile before monitoring. |
| `envuscator-web` | private | `main` | no | Candidate Envuscator web surface; catalogue/topology review required. |
| `actions` | private | `main` | no | Candidate shared automation repository; determine whether `.github` supersedes or delegates any authority. |
| `mobuild` | private | `main` | no | Canonical root of the registered supporting Mobuild coordination project; repository-health expectations remain intentionally unregistered pending monitoring review. |
| `mobuild-project` | private | `main` | no | Component/coordination repository within the registered Mobuild project family; topology and monitoring responsibility require explicit review. |
| `mobuild-warden` | private | `main` | no | Mobile security component within the registered Mobuild project family; topology and monitoring responsibility require explicit review. |
| `bluebell-sdk` | private | `main` | no | Candidate private Bluebell component; reconcile with the public `bluebell` authority boundary. |
| `download` | private | `main` | no | Candidate shared download service; owner and consumers must be documented before monitoring. |
| `keylix-client` | private | `main` | yes | GitHub-archived Keylix mobile adapter; retained as historical topology, not a monitored current surface. |

## Baseline rules

A repository moves from this exclusion list into `metadata/repositories.json` only when all of the following are reviewed:

1. the repository has an explicit responsibility or topology role;
2. classification and lifecycle are supported by current evidence rather than repository age or naming;
3. visibility, default branch, and archive state are verified from GitHub;
4. `monitor` is chosen deliberately;
5. `requiredFiles` contains only files that are genuinely required for that repository type.

An auxiliary repository may be registered with `monitor: false` when retaining topology/state in the registry is useful but health-file checks would create false positives.

Portfolio tier is not a prerequisite for repository-health registration and repository-health inclusion is not evidence of portfolio membership.

## Private repository coverage policy

Routine scheduled and post-merge repository-health runs do **not** require a standing cross-repository credential merely to eliminate `unknown` results.

The default baseline uses the workflow repository token. When that token cannot read a registered private/internal repository, the health tool reports the repository as `unknown`; this is an access limitation, not a warning, error, deletion claim, or lifecycle signal.

A fuller private-repository audit is optional and should be enabled only when there is a concrete need for automated cross-repository verification. When enabled:

- prefer a short-lived GitHub App installation token minted for the run;
- scope it read-only to repository metadata and contents for the reviewed private repository set;
- do not broaden mutation permissions to make health reporting convenient;
- do not treat successful credentialed access as new authority over the inspected repository;
- retain `unknown` rather than weakening or guessing around an access failure.

A long-lived personal access token is not required for the routine baseline and should not be introduced solely to make the report visually all-green.

## Repository creation and lifecycle changes

For a new repository, transfer, public/private split, supersession, or archive event:

1. identify the owning project or explicit organization-level responsibility;
2. update the canonical project registry when project identity or portfolio tier changes;
3. update the responsibility catalogue when the authority model changes;
4. update `metadata/repositories.json` or this exclusion document in the same change;
5. verify GitHub visibility, default branch, and archive state;
6. keep community/mirror/projection repositories distinct from implementation authority;
7. avoid adding required-file expectations until the repository's actual contract supports them;
8. run repository health in non-blocking mode and review drift before making any threshold required.

## Baseline interpretation

Repository health is a bounded evidence source, not an authority-transfer or portfolio-selection mechanism.

- `ok` means the workflow could verify the registered GitHub metadata and required-file contract.
- `warning` or `error` is actionable drift that should be reviewed and, when justified, routed to the owning repository.
- `unknown` means the workflow could not establish the state, commonly because a private repository is inaccessible to its token.
- `skipped` means monitoring is explicitly disabled for that registered repository.

Only concrete warning/error findings should generate repository-local drift work. Unknown access state should generate credential-policy work only when complete private automation is actually required.