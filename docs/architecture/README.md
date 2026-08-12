# Cross-repository architecture and planning

This directory is the organization-level home for architecture that spans repository ownership boundaries.

It complements, rather than replaces, repository-local design and delivery artifacts.

## What belongs here

Use this area when a decision or architectural contract materially affects more than one repository, especially when it changes:

- responsibility or authority boundaries;
- shared protocols, schemas, or evidence contracts;
- security or governance invariants;
- sequencing across independently owned implementations;
- lifecycle, compatibility, or migration expectations shared across repositories.

Cross-repository decisions that require durable review should be captured as an [RFC](rfcs/README.md). The corresponding coordination surface should normally be an organization-level epic or plan issue.

## What stays in owning repositories

Repository-local artifacts remain authoritative for implementation:

- ADRs and implementation design;
- code and configuration;
- tests and operational evidence;
- delivery issues and pull requests;
- local security controls and threat-model details that do not belong in public organization metadata.

Cross-repository planning must not become a second implementation backlog.

## Decision-to-delivery model

```text
cross-repository problem
        |
        v
organization RFC
        |
        +--> umbrella epic / plan
                  |
                  +--> repository-local issue / ADR
                  |          |
                  |          v
                  |       implementation + tests
                  |
                  +--> repository-local issue / ADR
                             |
                             v
                          implementation + tests
        |
        v
cross-repository validation / evidence
        |
        v
RFC and plan status updated
```

The RFC owns the durable architectural decision: why the boundary exists, what invariants must hold, and which repository owns which responsibility. The umbrella issue owns sequencing, dependencies, outcomes, and links. Repository-local issues own executable work.

## Planning rules

1. **One architectural source of truth.** Do not duplicate the same decision across multiple repositories.
2. **Local implementation authority.** Organization-level planning must not silently redefine a repository's internal contract.
3. **Stable boundaries over shared internals.** Cross-repository coupling should occur through versioned APIs, protocols, schemas, capabilities, or evidence contracts.
4. **Public metadata stays public-safe.** Do not expose private repository URLs, sensitive implementation details, secrets, credentials, or internal security findings in this public repository.
5. **Evidence closes work.** Completion requires the validation appropriate to the decision; an issue checkbox or model assertion is not evidence by itself.
6. **Prefer issues over planning documents for mutable sequencing.** Plans change frequently; durable decisions belong in version-controlled RFCs while sequencing belongs in issues.

## RFCs

See the [RFC index and lifecycle](rfcs/README.md).

Existing organization-wide architectural authority and work-item routing remain defined by [GOVERNANCE.md](../../GOVERNANCE.md) and the [engineering work-item guide](../engineering/work-items.md).
