# Repository lifecycle and maturity

This document defines the default lifecycle and maturity model for Micrantha repositories and projects. Maturity describes demonstrated stability and support; classification describes a repository's role. They are related but must not be conflated.

## Classification and maturity are separate

A repository may be classified as a:

- solution or product;
- distribution;
- service or application;
- library or SDK;
- provider-specific adapter;
- laboratory or testbed;
- demo or reference integration;
- community packaging or documentation surface;
- website or public documentation surface;
- governance, automation, or organization meta repository.

Classification identifies intended responsibility. Maturity identifies how much evidence, stability, and support currently exist.

## Lifecycle stages

| Stage | Meaning | Public wording |
| --- | --- | --- |
| **Proposed** | Purpose and ownership are being considered; implementation may not exist. | Proposed, planned, or under consideration |
| **Experimental** | Research, prototype, spike, or testbed work with unstable behavior and no support promise. | Experimental or prototype |
| **Incubating** | Active development toward a coherent supported outcome; architecture and contracts are stabilizing. | Incubating; interfaces may change |
| **Active** | Actively used or developed with defined ownership, validation, and release practices, but not necessarily a stable public contract. | Active; support scope stated explicitly |
| **Stable** | Supported contracts, release process, migration policy, and operational expectations are documented and evidenced. | Stable or production-ready within the declared scope |
| **Maintenance** | Mature capability receives security, compatibility, and bounded corrective work; major expansion is not expected. | Maintained; limited-change scope stated |
| **Superseded** | A successor or replacement has become authoritative; the repository remains available for migration or history. | Superseded by the named successor |
| **Archived** | No active development or support commitment. The repository is read-only or treated as historical. | Archived and unsupported |

The public aliases **Prototype** and **Maintained** map to **Experimental** and **Maintenance** respectively. New documentation should prefer the canonical names above.

## General requirements

Every repository that is more than a private scratch space should identify:

- purpose and intended users;
- classification;
- maturity stage;
- repository steward or ownership rule;
- authoritative responsibilities and explicit non-responsibilities;
- current support and compatibility expectations;
- security reporting path;
- license where applicable;
- successor or archival status when no longer active.

The [repository catalogue](../architecture/repository-catalogue.md) records organization-level ownership and maturity. Repository-local documentation remains authoritative for detailed implementation and support evidence.

## Stage expectations

### Proposed

Minimum evidence:

- problem or opportunity statement;
- provisional classification and owner;
- overlap check against existing repositories;
- decision on whether a new repository is necessary;
- expected public/private and licensing posture.

Proposed work should not be described as implemented or available. A repository may remain uncreated while the proposal is evaluated.

Exit to Experimental or Incubating when purpose, owner, initial scope, and repository boundary are accepted.

### Experimental

Expected:

- clear experiment, prototype, or research question;
- explicit unstable and unsupported status;
- bounded success or learning criteria;
- enough setup information to reproduce the intended experiment where practical;
- sensitive-data and security boundaries appropriate to the experiment;
- an exit decision: incubate, consolidate, supersede, or archive.

Experimental repositories may use simplified CI and documentation, but must not imply production readiness. Security-sensitive experiments still require safe defaults and responsible disclosure handling.

Exit to Incubating when the project has a committed product or laboratory direction, defined ownership, and a credible path to repeatable validation.

### Incubating

Expected:

- README with purpose, use cases, architecture, maturity, and known limitations;
- repository steward and decision authority;
- defined contracts or explicit contract-development plan;
- issue backlog with a small executable P1 queue;
- formatting, linting, unit testing, and relevant integration validation;
- dependency and secret-handling posture;
- release or demonstration process appropriate to the repository type;
- QART, RFC, ADR, and threat-model records where material;
- documented relationship to community, adapter, laboratory, or distribution repositories.

Incubating projects may make breaking changes. Changes should be deliberate, documented, and accompanied by migration guidance when consumers exist.

Exit to Active when the repository is delivering repeatable value with maintained CI, ownership, issue triage, and operational or integration evidence.

### Active

Expected:

- current roadmap or milestone;
- maintained CI and required quality gates;
- regular dependency and security maintenance;
- supported installation, development, and troubleshooting paths;
- versioned releases or a documented continuous-delivery model;
- compatibility, migration, and rollback expectations;
- observability and recovery appropriate to the system;
- public claims aligned with implemented behavior;
- periodic status and completeness reviews.

Active does not automatically mean stable public API. Contract stability must be stated explicitly.

Exit to Stable when the declared supported surface has sufficient evidence, compatibility policy, release discipline, and operational confidence.

### Stable

Expected:

- explicit supported scope and compatibility guarantees;
- versioning and deprecation policy;
- reproducible release artifacts where applicable;
- checksums, provenance, SBOMs, or signing according to supply-chain risk;
- migration and rollback procedures;
- security response and patch process;
- operational runbooks, diagnostics, and ownership where deployed;
- evidence that primary, failure, compatibility, migration, and security paths are validated;
- known limitations and support boundaries.

Stable claims are scoped. A stable library API does not make every experimental adapter stable, and a stable engine does not automatically make a distribution or hosted deployment stable.

Transition to Maintenance when the supported capability is mature and expected work narrows to corrective, security, and compatibility changes.

### Maintenance

Expected:

- defined supported versions and support window;
- security and dependency update process;
- bounded change policy;
- current ownership or explicit best-effort status;
- deprecation and successor information if retirement is likely;
- continued validation for supported releases.

New major features should normally be proposed in a successor, extension, or renewed Active phase rather than silently expanding a maintenance-only repository.

Transition to Superseded when a successor becomes authoritative, or to Archived when support ends without a successor.

### Superseded

Required:

- prominent successor link and effective date;
- migration or compatibility guidance where consumers exist;
- explanation of which responsibilities moved and which remain;
- closed or transferred active issues and pull requests;
- public documentation updated to stop presenting the repository as authoritative;
- security-support window during migration, if any.

A superseded repository may remain writable for migration fixes, but new capability work belongs in the successor unless explicitly justified.

Transition to Archived after the migration/support window ends and remaining historical value is preserved.

### Archived

Required:

- prominent archived and unsupported notice;
- successor link or explicit statement that none exists;
- final release or commit reference where useful;
- no active roadmap or misleading support claims;
- preservation of unique architecture, security, incident, and decision evidence;
- repository archival setting where appropriate.

Restoration requires an accountable owner, current security and dependency review, refreshed purpose, and an explicit transition to Experimental, Incubating, Active, or Maintenance.

## Lifecycle transitions

The repository steward proposes maturity changes. The organization owner authorizes repository creation, transfer, all maturity-stage changes, supersession, archival, and restoration. Stable and Maintenance transitions should include a focused readiness review.

A transition record should state:

```markdown
## Lifecycle transition

- Repository or project:
- Previous stage:
- New stage:
- Effective date:
- Steward:
- Evidence:
- Support and compatibility impact:
- Security impact:
- Migration or successor:
- Catalogue and public documentation updated:
```

Lifecycle stage must be based on current evidence, not repository age, code volume, aspirations, or the number of closed issues.

## Graduation checks

Before advancing a stage, confirm:

1. the repository has a coherent authoritative responsibility;
2. ownership and decision authority are current;
3. documentation and public claims match implementation;
4. validation is appropriate to the declared support scope;
5. security, dependency, and supply-chain controls match the risk;
6. release, migration, rollback, and recovery expectations are understood;
7. known limitations and unresolved risks are visible;
8. cross-repository contracts and community/public surfaces are aligned.

A project may advance some components independently. Record component-level maturity explicitly instead of inflating the whole repository's stage.

## Regression and emergency changes

A project may regress to an earlier stage when evidence no longer supports its current claim—for example, ownership loss, broken release paths, unsupported dependencies, unresolved security exposure, or major contract redesign.

A temporary incident does not necessarily change maturity, but public availability and support claims should be corrected immediately when a material capability is unavailable or unsafe.

## Public claims

Use these categories consistently:

- **Implemented** — present in the authoritative repository and validated within a stated scope.
- **Experimental** — implemented for research, demonstration, or learning without a support promise.
- **Planned** — accepted or prioritized but not yet implemented.
- **Aspirational** — a possible direction without a delivery commitment.

Do not present planned or aspirational behavior in present tense. Do not infer maturity from a polished website, demo, release tag, or generated documentation alone.

## Local overrides

A repository may define additional lifecycle stages or stricter requirements. It should map them to this organization model and document differences in its README or governance material.
