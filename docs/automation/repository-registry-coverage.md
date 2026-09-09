# Repository registry coverage

This document records the organization-wide repository census used to bound the Micrantha repository-health baseline.

The machine-readable registry in `metadata/repositories.json` remains the monitored set. Repositories listed here are **intentionally excluded from automated health checks until their ownership, lifecycle, or topology is explicitly reconciled**. Exclusion is not a claim that a repository is obsolete, unsupported, or safe to archive.

## Census method

The census is derived from the repositories visible to the organization GitHub installation and records GitHub state directly rather than inferring it from names or old documentation.

For each unregistered repository this document records:

- current visibility;
- current default branch;
- current GitHub archive state;
- the reason it is not yet part of the monitored health baseline.

Repository-local evidence and the canonical responsibility catalogue remain authoritative for implementation ownership and maturity.

## Current exclusions

### Historical or unclassified surfaces

These repositories predate the current responsibility catalogue or do not yet have a reviewed current project identity. They are excluded from health monitoring until a concrete owner/lifecycle decision is made.

| Repository | Visibility | Default branch | Archived | Baseline disposition |
| --- | --- | --- | --- | --- |
| `stimulus` | private | `main` | no | Unclassified historical testing/tooling surface; ownership review required. |
| `micra` | private | `master` | no | Historical project/build tool; ownership and supersession review required. |
| `outermesh` | private | `master` | no | Historical project surface; lifecycle decision required. |
| `outermesh-book` | private | `master` | no | Historical publication surface associated with OuterMesh. |
| `outermesh-web` | private | `master` | no | Historical web surface associated with OuterMesh. |
| `garden` | private | `master` | no | Historical Garden project surface; lifecycle decision required. |
| `garden-library` | private | `master` | no | Historical Garden shared library. |
| `garden-sdk` | private | `master` | no | Historical Garden SDK. |
| `garden-nursery` | private | `master` | no | Historical Garden frontend. |
| `scouter` | private | `master` | no | Historical Scouter project surface; lifecycle decision required. |
| `scouter-backend` | private | `master` | no | Historical Scouter backend. |
| `scouter-frontend` | private | `master` | no | Historical Scouter frontend. |
| `scouter-prototype` | private | `main` | no | Historical Android prototype. |
| `sandbox` | private | `main` | no | Unclassified development-environment experiment; reconcile against Sandcastle/Dubnium before assigning authority. |
| `codemux` | private | `main` | no | Unclassified live-coding tool; ownership review required. |
| `lab-service` | private | `main` | no | Unclassified lab support service; ownership review required. |
| `kredux` | private | `main` | no | Unclassified Kotlin library; ownership/support review required. |
| `pura` | private | `main` | no | Unclassified application repository; lifecycle decision required. |
| `yard` | private | `main` | no | Unclassified data-oriented repository; ownership review required. |

### Current-project auxiliary candidates

These repositories are plausibly related to current Micrantha projects or shared infrastructure, but the current catalogue does not assign them an authoritative role. They remain outside health checks until topology is documented rather than inferred from naming.

| Repository | Visibility | Default branch | Archived | Baseline disposition |
| --- | --- | --- | --- | --- |
| `fortunes-service` | private | `main` | no | Candidate Fortunes service component; reconcile against canonical Fortunes composition. |
| `fortunes-cli` | private | `master` | no | Candidate Fortunes CLI/adapter; reconcile before monitoring. |
| `envuscator-web` | private | `main` | no | Candidate Envuscator web surface; catalogue/topology review required. |
| `actions` | private | `main` | no | Candidate shared automation repository; determine whether `.github` supersedes or delegates any authority. |
| `mobuild-project` | private | `main` | no | Candidate Mobuild component; project identity/topology review required. |
| `mobuild-warden` | private | `main` | no | Candidate mobile security component; project identity/topology review required. |
| `mobuild` | private | `main` | no | Candidate Mobuild platform; current relationship to Envuscator/other mobile projects must be explicit. |
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

## Repository creation and lifecycle changes

For a new repository, transfer, public/private split, supersession, or archive event:

1. identify the owning project or explicit organization-level responsibility;
2. update the responsibility catalogue when the authority model changes;
3. update `metadata/repositories.json` or this exclusion document in the same change;
4. verify GitHub visibility, default branch, and archive state;
5. keep community/mirror/projection repositories distinct from implementation authority;
6. avoid adding required-file expectations until the repository's actual contract supports them;
7. run repository health in non-blocking mode and review drift before making any threshold required.

## Next baseline step

The monitored registry can now be treated as a bounded reviewed subset rather than an accidental partial inventory. The next step for issue #26 is to run and review `Repository health` with non-blocking failure semantics, then create repository-local issues only for justified drift findings.
