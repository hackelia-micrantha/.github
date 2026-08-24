# Public Documentation and Claims Consistency Review Prompt

Use this prompt to reconcile websites, READMEs, books, one-pagers, whitepapers, screenshots, demos, and release messaging with current implementation and maturity.

Do **not** use this prompt for cross-repository ownership or boundary questions — use [cross-repository boundary review](architecture/cross-repository-boundaries.md). Do **not** use it for general project status — use the [project reviews](project-review/README.md).

```markdown
# Public Documentation and Claims Consistency Review

Review **[PUBLIC SITE / README / BOOK / ONE-PAGER / WHITEPAPER / COMMUNITY REPOSITORY]** against the current implementation of **[PROJECT / ECOSYSTEM]**.

## Context

- **Public artifacts in scope:** [ARTIFACTS]
- **Implementation repositories:** [REPOSITORIES]
- **Intended audience:** [TECHNICAL / CUSTOMER / COMMUNITY / HIRING / INVESTOR]
- **Current maturity and milestone:** [MATURITY / MILESTONE]
- **Known sensitive boundaries:** [PRIVATE / COMMERCIAL / SECURITY / TRANSITIONAL]
- **Mutation authorization:** [READ ONLY / UPDATE PUBLIC MATERIAL]

## Execution boundary

Begin read-only. Treat public copy, diagrams, screenshots, issue comments, generated site content, and repository descriptions as claims requiring evidence. Do not publish, deploy, change domains, or expose private implementation details unless explicitly authorized.

## Core rule

Public materials must clearly distinguish:

- implemented;
- integrated;
- validated;
- released or deployed;
- experimental or demo-only;
- planned or proposed;
- unsupported or deprecated.

Do not strengthen a claim because implementation appears likely. Do not weaken accurate technical positioning merely because production maturity is incomplete; label maturity precisely instead.

## Evidence to inspect

Inspect applicable:

- source implementation, configuration, schemas, and public interfaces;
- current releases, packages, deployment state, and working demos;
- project and organization READMEs;
- architecture documents, QART, RFC, ADR, roadmap, and maturity model;
- open issues, pull requests, known limitations, and migration status;
- websites, books, one-pagers, whitepapers, diagrams, screenshots, and example commands;
- repository ownership, public/private/community boundaries, domains, and download links;
- security, privacy, licensing, support, and commercial claims;
- related repositories and integration testbeds.

## Review dimensions

### 1. Product identity and audience

Confirm that name, purpose, intended users, primary outcome, maturity, and call to action are consistent and understandable for the intended audience.

### 2. Capability claims

For each material claim determine:

- implementation status;
- integration and validation status;
- availability to the stated audience;
- evidence;
- required qualifier or correction.

Flag claims that confuse architecture intent with delivered behavior, demos with products, or internal capability with public availability.

### 3. Architecture and repository map

Verify:

- component and repository names;
- product, distribution, library, adapter, laboratory, demo, and community roles;
- dependency and trust directions;
- public/private and transitional ownership;
- diagrams against current interfaces and release flows.

A simplified public diagram may omit internal detail, but must not reverse ownership or imply nonexistent integration.

### 4. Installation, examples, and links

Test or verify applicable:

- repository, documentation, download, package, workflow, and domain links;
- commands, configuration, environment variables, and examples;
- version references;
- prerequisites and supported platforms;
- screenshots and output against current UI, CLI, API, or workflow behavior.

### 5. Maturity and support

Check that terms such as prototype, incubating, stable, maintained, production-ready, supported, secure, private, reproducible, deterministic, or self-hostable have evidence and consistent definitions.

State known limitations without turning the page into an internal backlog.

### 6. Security and privacy claims

Review claims about:

- encryption, authentication, authorization, isolation, privacy, on-device behavior, self-hosting, data retention, provenance, signing, attestation, approvals, governance, or fail-closed behavior;
- customer-controlled runners or infrastructure;
- absence of data collection or external transmission;
- compliance or certification.

Require precise scope and evidence. Avoid absolute claims such as “secure,” “private,” or “never leaves the device” without conditions and boundaries.

### 7. Commercial, licensing, and distribution boundaries

Confirm which components are open source, source-available, private, licensed, community, hosted, or commercial. Verify that public copy does not promise unavailable adapters, support, entitlements, or distribution channels.

### 8. Terminology and narrative consistency

Identify inconsistent names, acronyms, maturity labels, architecture terms, goals, and calls to action across artifacts. Recommend one authoritative term and source.

### 9. Public credibility and UX

Review information hierarchy, readability, navigation, accessibility, visual consistency, code formatting, diagram legibility, responsive behavior, empty or broken sections, and whether the strongest verified outcome is visible early.

Separate credibility or usability problems from cosmetic preference.

## Finding classification

- **Misleading:** materially overstates, reverses, or falsely represents implementation, security, availability, or maturity.
- **Stale:** was accurate but no longer reflects current state.
- **Ambiguous:** can reasonably be interpreted more broadly than evidence supports.
- **Missing:** omits a material limitation, integration, user path, or current outcome.
- **Inconsistent:** conflicts with another authoritative artifact.
- **Opportunity:** stronger verified evidence or positioning is available.

## Required output

### A. Public positioning summary

State the apparent product narrative, actual current outcome, intended audience, maturity, and largest credibility gap or opportunity.

### B. Claim verification matrix

| Public claim | Artifact/location | Actual status | Evidence | Classification | Recommended wording/action |
| --- | --- | --- | --- | --- | --- |

Include only material claims.

### C. Architecture and ownership consistency

Summarize repository roles, diagrams, public/private boundaries, and any required corrections.

### D. Link, example, and interface findings

List broken, stale, unsafe, unsupported, or misleading links, commands, screenshots, and examples.

### E. Security, privacy, and support findings

Identify claims requiring correction, qualification, evidence, or removal.

### F. Recommended content changes

Provide dependency-ordered changes grouped as:

- must fix before publication;
- high-value credibility or clarity improvements;
- bounded optional polish.

For substantive wording changes, provide replacement copy. Avoid rewriting unaffected content.

### G. Final assessment

Choose exactly one:

- **Consistent and publishable**
- **Publishable after minor corrections**
- **Requires focused implementation/documentation reconciliation**
- **Contains materially misleading claims**
- **Requires architecture or ownership clarification**
- **Requires security or legal claim review**
- **Appropriate to archive or redirect**
- **Insufficient evidence**

## Authorized update mode

When edits and publication are explicitly authorized:

1. Correct misleading and stale claims first.
2. Preserve established visual style unless a redesign is required for usability.
3. Update authoritative source content rather than generated output where possible.
4. Validate links, builds, and deployment previews.
5. Re-review the rendered result on relevant form factors.
6. Publish only through the established workflow and report the production URL or immutable artifact.
```
