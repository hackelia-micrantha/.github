# Micrantha organization defaults

This repository contains shared community health files, contribution conventions, workflows, issue forms, and reusable engineering guidance for repositories in the `hackelia-micrantha` organization.

Repositories may refine these defaults when their product, security, or operating model requires it, but should document the difference explicitly.

## Shared guidance

- [Contribution and issue-prioritization standard](CONTRIBUTING.md)
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
- [Security policy](.github/SECURITY.md)
- [Support guidance](.github/SUPPORT.md)
- [Code of conduct](.github/CODE_OF_CONDUCT.md)

## Inherited issue forms

Repositories without local overrides inherit specialized forms for bugs, features, security intake, engineering delivery slices, design proposals, and epics or plans.

Use the most specific form that fits. The engineering delivery form is for bounded cross-cutting implementation, integration, migration, infrastructure, or refactoring work; it should not replace a direct bug, feature, or security report.

## Decision-to-delivery workflow

Use the comprehensive project review when a project lacks a trustworthy baseline, has unclear architecture or maturity, or needs backlog reconciliation. Use the status refresh after meaningful merges, releases, incidents, milestone changes, or planning cycles.

For new work, classify the material first, resolve open alternatives through QART, use an RFC only when broad review is warranted, record accepted durable decisions in ADRs, coordinate larger outcomes through epics or plans, and deliver bounded implementation slices with validation evidence.

All prompts and issue templates use the organization priority model defined in [`CONTRIBUTING.md`](CONTRIBUTING.md):

- `P0` — active interrupt;
- `P1` — small executable next-up queue;
- `P2` — planned work;
- `P3` — later or exploratory work.

Priority remains distinct from severity, status, size, confidence, age, and architectural importance. Blocking is recorded as status while preserving the underlying priority.
