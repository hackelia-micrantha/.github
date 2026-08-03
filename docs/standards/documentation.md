# Documentation standard

Documentation is part of the supported product surface. It should help users, operators, contributors, reviewers, and future maintainers understand what exists, what is authoritative, how it behaves, and what remains uncertain.

## Core requirements

Every non-scratch repository should document the applicable subset of:

- purpose, intended users, and supported use cases;
- classification and maturity;
- authoritative responsibilities and explicit non-responsibilities;
- installation, setup, and first supported use;
- architecture, components, contracts, state, and trust boundaries;
- configuration and environment requirements;
- development, testing, and CI commands;
- security model and reporting path;
- deployment, operation, observability, recovery, and troubleshooting;
- versioning, release, migration, compatibility, and support policy;
- known limitations, experimental areas, and planned work;
- contributing and decision-making process;
- license and ownership where applicable.

Keep the README useful as an entry point. Move detailed material into focused documents rather than creating an unbounded README.

## Documentation by maturity

### Experimental

Minimum:

- question or purpose;
- unsupported and unstable status;
- setup or reproduction path where practical;
- success or learning criteria;
- sensitive-data and safety limitations.

### Incubating

Add:

- architecture and use cases;
- current integration boundaries;
- development and validation instructions;
- known limitations and breaking-change posture;
- QART, RFC, ADR, or threat-model links where material;
- relationship to community, adapter, distribution, or laboratory repositories.

### Active

Add and maintain:

- supported installation and operation;
- compatibility and migration guidance;
- troubleshooting and ownership;
- current release model and roadmap;
- public contracts and failure behavior;
- periodic reconciliation between documentation and implementation.

### Stable and Maintenance

Require:

- explicit supported scope and versions;
- versioning and deprecation rules;
- migration and rollback procedures;
- release verification and integrity instructions;
- operational runbooks where deployed;
- security response and patch expectations;
- archived or superseded documentation preserved and linked when it exists.

## Public claims

Classify claims consistently:

- **Implemented** — present in the authoritative repository and validated within the stated scope.
- **Experimental** — implemented for research or demonstration without a support promise.
- **Planned** — accepted or prioritized but not implemented.
- **Aspirational** — possible direction without a delivery commitment.

Do not write planned or aspirational behavior in present tense. Do not infer production readiness from a polished demo, website, diagram, release tag, or generated document.

Public websites, organization profiles, community repositories, one-pagers, and presentations should project authoritative repository evidence. They do not independently create product truth.

## Architecture documentation

Architecture documentation should identify:

- system context and actors;
- repository and component responsibilities;
- data and control flow;
- state ownership and consistency;
- public and internal contracts;
- trust, authorization, approval, and execution boundaries;
- dependency direction;
- failure, retry, recovery, and rollback behavior;
- deployment and operational ownership;
- material alternatives and accepted decisions.

Use diagrams when they improve understanding, but accompany them with text that explains authority and boundaries. A dependency arrow does not imply ownership.

## Decision records

Use the organization work-item and decision guidance:

- QART for unresolved alternatives and trade-offs;
- RFC for substantial proposals requiring broad review;
- ADR for accepted durable decisions;
- issues and epics for delivery outcomes and sequencing.

Link decisions to implementation and follow-up. Do not rewrite history to make an earlier proposal appear inevitable; preserve supersession and changed assumptions.

## User and operator guidance

User documentation should include supported prerequisites, common path, errors, limitations, compatibility, and recovery. Operator documentation should include configuration, health, metrics, logs, alerts, failure modes, backup or recovery, upgrades, rollback, and escalation.

Troubleshooting guidance should explain how to distinguish likely causes and collect safe diagnostics. Do not instruct users to publish secrets or sensitive data.

## Security documentation

Document the applicable:

- assets and trust boundaries;
- authentication, authorization, delegation, and approvals;
- sensitive-data and secret handling;
- threat assumptions and residual risks;
- secure defaults and failure posture;
- evidence, logging, retention, and privacy;
- private vulnerability-reporting path.

Public security documentation should provide useful boundaries without disclosing active secrets or unnecessary exploit detail.

## Examples and generated content

- Keep examples executable or clearly illustrative.
- Pin or identify versions when behavior changes materially.
- Do not use real credentials or personal data.
- Validate generated commands, configuration, schemas, and API examples.
- Mark placeholders visibly.
- Treat AI-generated documentation as a draft requiring evidence-backed human review.

## Docs-as-code validation

Where documentation is a supported surface, automate applicable:

- Markdown formatting and linting;
- internal and external link checks;
- code, configuration, and schema examples;
- diagram syntax;
- API or CLI reference generation drift;
- spelling or terminology checks;
- public-claim consistency and stale-version detection.

Do not block critical fixes on unreliable external-link checks without a documented fallback, but do not ignore persistent documentation failures.

## Change requirements

A change should update documentation when it affects:

- user-visible behavior;
- public or cross-repository contracts;
- configuration, prerequisites, or defaults;
- security, privacy, or trust boundaries;
- migration, compatibility, release, or support;
- deployment, observability, recovery, or troubleshooting;
- repository responsibility or maturity;
- known limitations or public claims.

Documentation follow-up may be separate only when the existing material remains safe and accurate and the follow-up has an owner and bounded deadline.

## Supersession and archival

When a document, decision, repository, or capability is superseded:

- preserve the historical material;
- add a prominent successor link and effective date;
- stop presenting the old source as authoritative;
- update inbound indexes and public surfaces;
- retain unique security, architecture, incident, and migration evidence.

## Review checklist

A documentation review should verify:

1. authority and intended audience are clear;
2. current behavior and maturity are represented accurately;
3. instructions are complete enough for the declared use case;
4. security-sensitive material is safe;
5. compatibility, migration, and limitations are visible;
6. links and examples resolve;
7. duplicate sources of truth are avoided;
8. planned and implemented claims are distinguished;
9. ownership and update triggers are understood.
