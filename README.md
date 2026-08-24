# Micrantha organization defaults

This repository contains shared governance, community health files, contribution conventions, issue and pull-request templates, engineering prompts, standards, automation, and reusable guidance for repositories in the `hackelia-micrantha` organization.

Repositories may refine these defaults when their product, legal, security, or operating model requires it, but should document the difference explicitly. Repository-local implementation and evidence remain authoritative within the boundaries assigned by the organization governance model.

## Governance and ownership

- [Organization governance](GOVERNANCE.md)
- [Contribution and issue-prioritization standard](CONTRIBUTING.md)
- [Repository lifecycle and maturity](docs/governance/repository-lifecycle.md)
- [Repository responsibility catalogue](docs/architecture/repository-catalogue.md)
- [Organization architecture RFCs](docs/architecture/rfcs/README.md)
- [Security policy](.github/SECURITY.md)
- [Support guidance](.github/SUPPORT.md)
- [Code of conduct](.github/CODE_OF_CONDUCT.md)

The governance model defines accountable roles, decision authority, repository and contract ownership, security-risk acceptance, release authority, lifecycle control, and boundaries for AI-assisted or agentic engineering.

The repository catalogue distinguishes architectural authority from runtime dependency. A laboratory produces evidence without silently redefining a product contract; a distribution composes components without assuming their internal authority; a public site projects evidence rather than creating product truth.

## Engineering standards

- [Standards overview](docs/standards/README.md)
  - [Testing and validation](docs/standards/testing.md)
  - [CI/CD](docs/standards/ci-cd.md)
  - [Security engineering](docs/standards/security.md)
  - [CLI interoperability](docs/standards/cli-interoperability.md)
  - [Releases and versioning](docs/standards/releases.md)
  - [Documentation](docs/standards/documentation.md)
  - [Labels and work-item taxonomy](docs/standards/labels.md)

The standards define minimum outcomes according to repository classification, maturity, risk, supported surface, and deployment model. Repository-local standards may be stricter or may document a justified alternative control, but cannot silently weaken security, compatibility, release, support, or public-maturity claims.

## Shared automation and metadata

- [Automation foundation](docs/automation/README.md)
- [Machine-readable repository registry](metadata/repositories.json)
- [Repository registry schema](metadata/repositories.schema.json)
- [Workflow starter templates](workflow-templates/)
- [Reusable mise CI workflow](.github/workflows/reusable-mise-ci.yml)
- [Reusable Nix CI workflow](.github/workflows/reusable-nix-ci.yml)
- [Repository-health workflow](.github/workflows/repository-health.yml)

The automation layer is read-only by default. Starter templates help repositories adopt common workflow structure; repositories still own their tasks, test coverage, runner trust decisions, required checks, and release policy. Shared reusable workflows do not inherit secrets or perform deployment, release, approval, label, or repository-setting mutations.

The repository registry is an advisory machine-readable projection of the canonical responsibility catalogue. A weekly health report checks registered location, visibility, default branch, archival state, and minimal required files without opening issues or modifying repositories. Private-repository coverage requires an explicitly configured read-only token.

## Engineering work and decisions

- [Engineering work-item guide and decision templates](docs/engineering/work-items.md)
  - [QART template](docs/engineering/templates/qart.md)
  - [RFC template](docs/engineering/templates/rfc.md)
  - [ADR template](docs/engineering/templates/adr.md)
- [Engineering prompt library](docs/prompts/README.md)
  - [Project review prompts](docs/prompts/project-review/README.md)
  - [Pull-request merge-gate review](docs/prompts/pull-requests/merge-gate-review.md)
  - [CI failure triage and repair](docs/prompts/ci/ci-failure-triage.md)
  - [Classify and route engineering work](docs/prompts/planning/classify-and-route.md)
  - [Next executable slice](docs/prompts/planning/next-executable-slice.md)
  - [Issue grooming](docs/prompts/issues/issue-grooming.md)
  - [QART decision analysis](docs/prompts/decisions/qart-analysis.md)
  - [RFC development](docs/prompts/decisions/rfc-development.md)
  - [QART-to-ADR conversion](docs/prompts/decisions/qart-to-adr.md)
  - [Engineering artifact review](docs/prompts/reviews/engineering-artifact-review.md)
  - [Implementation completeness review](docs/prompts/reviews/implementation-completeness.md)
  - [Cross-repository boundary review](docs/prompts/architecture/cross-repository-boundaries.md)
  - [Release readiness review](docs/prompts/releases/release-readiness.md)
  - [Public documentation consistency review](docs/prompts/documentation/public-consistency-review.md)
  - [Agentic workflow security review](docs/prompts/security/agentic-workflow-security-review.md)

## Inherited issue and pull-request defaults

Repositories without local overrides inherit specialized forms for bugs, features, security intake, engineering delivery slices, design proposals, and epics or plans, plus the organization pull-request template and issue chooser guidance.

Use the most specific issue form that fits:

- bug for an observable defect;
- feature for a requested capability;
- security for non-sensitive public intake, with detailed reports handled privately;
- engineering delivery slice for bounded cross-cutting implementation, integration, migration, infrastructure, or refactoring work;
- design proposal for material unresolved design questions without prematurely assuming RFC status;
- epic or plan for coordination across bounded workstreams and outcomes.

A repository that defines local files under `.github/ISSUE_TEMPLATE/` may stop inheriting the organization issue-template directory. Local overrides should therefore copy or deliberately replace the shared chooser and required forms rather than accidentally removing them.

The pull-request template requires the outcome, authority and related decisions, scope, validation evidence, security and governance impact, compatibility and rollback behavior, documentation and release effects, and remaining work.

## Decision-to-delivery workflow

Use the comprehensive project review when a project lacks a trustworthy baseline, has unclear architecture or maturity, or needs backlog reconciliation. Use the status refresh after meaningful merges, releases, incidents, milestone changes, or planning cycles.

For new work:

```text
classify the material
  -> gather evidence or run a bounded spike when facts are missing
  -> use QART when credible alternatives remain open
  -> use an RFC only when broad or cross-boundary review is warranted
  -> obtain accountable disposition
  -> record accepted durable decisions in ADRs
  -> coordinate larger outcomes through epics or plans
  -> deliver bounded implementation slices
  -> validate, release, operate, and update public evidence
```

Prioritization for tracked engineering work follows [`CONTRIBUTING.md`](CONTRIBUTING.md):

- `P0` — active interrupt;
- `P1` — small executable next-up queue;
- `P2` — planned work;
- `P3` — later or exploratory work.

Priority remains distinct from severity, status, size, confidence, age, and architectural importance. Blocking is recorded as status while preserving the underlying priority. Intake reporters are not expected to determine repository-global priority; maintainers assign it during grooming and triage.

## Repository lifecycle

Maturity is evidence-based and separate from repository classification:

- **Proposed**
- **Experimental**
- **Incubating**
- **Active**
- **Stable**
- **Maintenance**
- **Superseded**
- **Archived**

The public aliases `Prototype` and `Maintained` map to `Experimental` and `Maintenance`. Lifecycle changes should update the repository, the [catalogue](docs/architecture/repository-catalogue.md), registry, and relevant public documentation together.
