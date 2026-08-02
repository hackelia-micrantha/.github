# Micrantha organization defaults

This repository contains shared community health files, contribution conventions, workflows, issue forms, and reusable engineering guidance for repositories in the `hackelia-micrantha` organization.

Repositories may refine these defaults when their product, security, or operating model requires it, but should document the difference explicitly.

## Shared guidance

- [Contribution and issue-prioritization standard](CONTRIBUTING.md)
- [Project review prompts](docs/prompts/project-review/README.md)
  - [Comprehensive project status review](docs/prompts/project-review/comprehensive-status-review.md)
  - [Project status refresh](docs/prompts/project-review/status-refresh.md)
- [Security policy](.github/SECURITY.md)
- [Support guidance](.github/SUPPORT.md)
- [Code of conduct](.github/CODE_OF_CONDUCT.md)

## Project review workflow

Use the comprehensive review when a project lacks a trustworthy baseline, has unclear architecture or maturity, or needs backlog reconciliation. Use the status refresh after meaningful merges, releases, incidents, milestone changes, or planning cycles.

Both prompts use the organization priority model defined in [`CONTRIBUTING.md`](CONTRIBUTING.md):

- `P0` — active interrupt;
- `P1` — small executable next-up queue;
- `P2` — planned work;
- `P3` — later or exploratory work.

Priority remains distinct from severity, status, size, confidence, age, and architectural importance.
