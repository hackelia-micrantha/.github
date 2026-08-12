# Cross-repository RFCs

RFCs in this directory record durable architecture decisions whose authority or impact crosses repository boundaries.

Use the organization [RFC template](../../engineering/templates/rfc.md) as the baseline structure.

## Lifecycle

An RFC should use one of these statuses:

- **Proposed** — under development or review; not yet architectural authority.
- **Accepted** — approved and authoritative for the scope it defines.
- **Superseded** — replaced by a newer accepted decision; retain the document and link its successor.
- **Rejected** — considered and deliberately not adopted; retain the rationale when useful.

Implementation progress does not change an accepted RFC back into a planning document. Track delivery and dependencies in issues.

## Index

| RFC | Status | Decision |
| --- | --- | --- |
| [0001 — Governed agent actuation](0001-governed-agent-actuation.md) | Proposed | Define cross-repository boundaries for turning agent intent and security requirements into authorized, executable, verifiable actions. |

## Numbering and scope

- Allocate the next four-digit number when opening an RFC pull request.
- Prefer one coherent cross-repository decision per RFC.
- Link related umbrella issues and repository-local work rather than embedding mutable implementation backlogs.
- Repository-local architecture should normally use an ADR in the owning repository instead.
