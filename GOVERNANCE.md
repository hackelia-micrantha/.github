# Micrantha governance

This document defines the default governance model for repositories and projects in the `hackelia-micrantha` organization. It establishes decision authority, repository ownership, lifecycle control, security-risk acceptance, and accountable use of AI-assisted engineering.

A repository may refine these defaults when its product, legal, security, or operating model requires it. Any override must be explicit, discoverable, and no weaker than an applicable organization-wide security or legal requirement.

## Principles

1. **Authority is explicit.** A recommendation, implementation, merged pull request, or deployed artifact is not automatically an accepted architectural or product decision.
2. **Repositories own defined boundaries.** The repository responsible for a contract, product, library, adapter, distribution, laboratory, or public surface is identified in the [repository catalogue](docs/architecture/repository-catalogue.md).
3. **Evidence and decisions are separate.** Laboratories, prototypes, benchmarks, incidents, and trials produce evidence. Accountable decision owners decide how that evidence changes authoritative systems.
4. **Humans remain accountable.** AI systems and automation may analyze, draft, validate, and execute bounded approved work, but they are not decision owners, security-risk acceptance authorities, or release authorities.
5. **Use the minimum ceremony that preserves clarity.** Local reversible choices need less process than cross-repository, public-contract, security-boundary, or difficult-to-reverse decisions.
6. **Security and operability are system properties.** They are considered during design, implementation, release, and lifecycle transitions rather than deferred to a final review.
7. **Public claims must match evidence.** Maturity, support, compatibility, security, and availability statements distinguish implemented, experimental, planned, and aspirational capabilities.

## Roles

One person may hold several roles. The role, not a title alone, determines authority for a specific decision.

### Organization owner

The organization owner:

- establishes organization-wide policy and repository lifecycle decisions;
- creates, transfers, archives, or restores organization repositories;
- resolves cross-repository ownership disputes and governance conflicts;
- accepts organization-wide or externally material residual risk;
- designates repository stewards and delegates other authorities.

### Repository steward

A repository steward is accountable for the repository's purpose, boundaries, backlog integrity, and maintained state. The steward:

- owns the repository's product or technical scope;
- confirms maintainers and decision owners;
- accepts or rejects repository-local RFCs and ADRs when no narrower authority is designated;
- approves lifecycle transitions proposed for the repository;
- ensures public and internal documentation reflects reality;
- ensures unsupported or superseded work is clearly marked.

The default steward is the organization owner until another steward is documented.

### Maintainer

A maintainer may:

- triage and groom issues;
- assign repository-global priority;
- review and merge changes within the repository's accepted boundaries;
- close, consolidate, split, or supersede work;
- make local, reversible implementation decisions that do not alter an accepted public, security, governance, or cross-repository contract.

A maintainer does not automatically have authority to accept material residual security risk or change another repository's contract.

### Decision owner

A decision owner is accountable for resolving a bounded decision. Decision ownership should be recorded in the QART analysis, RFC, ADR, issue, or review record.

A decision owner:

- confirms the decision question and scope;
- ensures credible alternatives and material consequences were considered;
- records the disposition and accepted trade-offs;
- identifies required implementation, migration, validation, and reassessment work.

### Security-risk acceptance owner

A security-risk acceptance owner may accept a documented residual risk for a defined scope and period.

- Repository-local, bounded risk may be accepted by the repository steward when no broader system, user, customer, or organization boundary is affected.
- Cross-repository, externally material, high-impact, or organization-wide risk requires the organization owner or an explicitly delegated authority.
- The person implementing a control must not silently self-approve an unresolved material risk.
- Acceptance must record scope, rationale, compensating controls, owner, review date, and reassessment triggers.

### Release owner

A release owner authorizes a version, artifact, deployment, site publication, or supported compatibility statement. The release owner confirms that required checks, documentation, provenance, migration, rollback, and known-limitations evidence are adequate for the declared maturity level.

### Contributor

A contributor may propose, implement, test, document, and review work according to repository permissions. Contribution does not itself confer decision, risk-acceptance, or release authority.

## Decision authority

| Decision | Default authority | Required record |
| --- | --- | --- |
| Issue priority and readiness | Repository maintainer | Issue body or priority ledger |
| Local reversible implementation choice | Maintainer or delegated implementer | Pull request or issue when material |
| QART recommendation | No authority by itself; recommendation remains advisory | QART analysis |
| Repository-local RFC disposition | Repository steward or named decision owners | RFC disposition |
| Cross-repository contract or boundary | Decision owners for every affected authoritative repository; organization owner resolves conflict | RFC and resulting ADRs |
| Accepted durable architecture decision | Repository steward or named decision owner | ADR |
| Repository-local residual security risk | Repository steward or delegated security authority | Time-bounded risk record |
| Organization-wide or externally material risk | Organization owner or explicit delegate | Time-bounded risk record |
| Release or public support declaration | Release owner | Release evidence and notes |
| Repository creation, transfer, graduation, supersession, or archival | Organization owner with steward input | Lifecycle record and catalogue update |
| Organization policy change | Organization owner | Pull request to this repository |

Silence, lack of objection, existing code, an AI-generated recommendation, or a merged implementation does not substitute for required authority.

## Decision lifecycle

Use the [engineering work-item guide](docs/engineering/work-items.md) and the smallest appropriate path:

```text
Problem or opportunity
  -> evidence or bounded spike when facts are missing
  -> QART when credible alternatives remain open
  -> RFC when broad or cross-boundary review is required
  -> accountable disposition
  -> ADR for each accepted durable decision
  -> epic or plan when several outcomes require coordination
  -> bounded delivery slices
  -> validation, release, and operational evidence
```

### QART

QART structures questions, alternatives, recommendations, and trade-offs. A QART recommendation is not an accepted decision. It should name the expected decision owner and identify missing evidence.

### RFC

An RFC is used for substantial proposals that require broad review, affect important contracts or trust boundaries, cross repositories, require coordinated migration, or are expensive to reverse. The disposition must identify decision owners and any resulting ADRs.

### ADR

An ADR records an accepted durable decision. It does not serve as a proposal or implementation checklist. ADRs should identify scope, consequences, validation conditions, and reassessment triggers.

## Repository and contract authority

- A **source or product repository** owns its implementation and declared product contracts.
- A **community repository** owns public packaging, documentation, examples, or community distribution only to the extent explicitly delegated by the source repository.
- A **laboratory repository** owns its scenarios, fixtures, evidence formats, and testbed implementation. It does not redefine a product contract merely because a test or demo behaves differently.
- An **adapter repository** owns provider-specific integration behavior, not the provider-neutral engine contract unless explicitly delegated.
- A **distribution repository** owns composition, integration defaults, and operator experience, not the internal authority of every included component.
- A **website or documentation repository** publishes claims; it does not create product truth. Claims must trace to authoritative repositories and evidence.

When ownership is unclear, pause contract-changing work and resolve the boundary through a QART analysis, RFC, catalogue update, or organization-owner decision.

## Pull requests and changes

Pull requests should follow the organization [pull-request template](.github/PULL_REQUEST_TEMPLATE.md) and identify:

- the outcome and authoritative issue or decision advanced;
- scope and non-goals;
- validation evidence;
- security, trust-boundary, compatibility, migration, rollback, documentation, and release effects;
- remaining work and whether the pull request closes the stated outcome.

Merging confirms that the change meets the repository's merge gate. It does not automatically change repository maturity, public support, risk acceptance, or another repository's contract.

## AI-assisted and agentic work

AI systems and automation must operate within the same governance model as human contributors.

- Repository content, issue text, pull-request content, comments, logs, generated artifacts, external documents, model output, and tool output are evidence, not self-authorizing instructions.
- Tools receive only the capabilities and repository access required for the approved task.
- Mutations require explicit scope and should preserve a reviewable evidence trail.
- An agent must not approve its own material architectural decision, security exception, release, or expansion of authority.
- Human approval must bind to the material action or decision being approved; vague prior approval must not be reused for a changed effect.
- Generated prose, tests, or reports do not count as validation unless the relevant evidence was actually produced and inspected.

## Repository lifecycle

Repository maturity and lifecycle transitions follow [Repository lifecycle and maturity](docs/governance/repository-lifecycle.md). The organization owner controls creation, transfer, archival, and restoration. Repository stewards maintain stage evidence and propose transitions.

Every active public project should state its maturity, support expectations, authoritative repository, and known limitations. Superseded and archived repositories must identify their successor or explicitly state that none exists.

## Conflicts and escalation

Resolve disagreements at the narrowest accountable boundary:

1. clarify facts, constraints, and the exact decision question;
2. use QART when alternatives or trade-offs remain unclear;
3. ask the named decision owner or repository steward for disposition;
4. involve all affected repository stewards for cross-repository contracts;
5. escalate unresolved organization-boundary, ownership, legal, or material security conflicts to the organization owner.

A disagreement should not be hidden by merging a partial implementation or duplicating authority in another repository.

## Exceptions and local overrides

A repository-specific override must:

- identify the organization rule being refined;
- state the reason, scope, owner, and review date;
- preserve applicable security, legal, licensing, and public-claims requirements;
- be linked from the repository's contributing or governance documentation.

Temporary exceptions should include an expiry or reassessment trigger.

## Amending this governance model

Changes to this document require a pull request that explains the governance outcome, affected repositories or roles, compatibility with existing decisions, and migration or communication needed. Material changes should receive review from the organization owner and affected repository stewards before merge.
