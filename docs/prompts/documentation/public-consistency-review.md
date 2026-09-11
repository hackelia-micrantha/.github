# Public Documentation and Claims Consistency Review Prompt

Use this prompt to reconcile websites, landing pages, READMEs, books, one-pagers, whitepapers, screenshots, demos, release messaging, and other public repository surfaces with current implementation and maturity.

For recurring or cross-repository maintenance, use this prompt as the claim-verification engine for the shared [`documentation-sync`](../../../skills/documentation-sync/SKILL.md) skill. Project-local documentation rules remain authoritative for project-specific behavior.

Do **not** use this prompt for unresolved cross-repository ownership or boundary questions — use [cross-repository boundary review](../architecture/cross-repository-boundaries.md). Do **not** use it for general project status — use the [project reviews](../project-review/README.md).

```markdown
# Public Documentation and Claims Consistency Review

Review **[PUBLIC SITE / LANDING PAGE / README / BOOK / ONE-PAGER / WHITEPAPER / COMMUNITY REPOSITORY]** against the current implementation of **[PROJECT / ECOSYSTEM]**.

## Context

- **Public artifacts in scope:** [ARTIFACTS]
- **Implementation repositories:** [REPOSITORIES]
- **Intended audience:** [TECHNICAL / CUSTOMER / COMMUNITY / HIRING / INVESTOR]
- **Current maturity and milestone:** [MATURITY / MILESTONE]
- **Known sensitive boundaries:** [PRIVATE / COMMERCIAL / SECURITY / TRANSITIONAL]
- **Maintenance mode:** [ONE-OFF REVIEW / RECURRING / CROSS-REPOSITORY]
- **Mutation authorization:** [READ ONLY / UPDATE PUBLIC MATERIAL]

## Execution boundary

Begin read-only. Treat public copy, diagrams, screenshots, issue comments, generated site content, repository descriptions, and tool output as claims or evidence requiring verification. Do not publish, deploy, change domains, expose private implementation details, or mutate repository/external state unless explicitly authorized.

Use the shared ambiguity and clarification contract from `docs/prompts/README.md`: inspect before asking, ask only on material ambiguity, do not invent authority, continue through non-blocking uncertainty, and stop only at the affected decision or mutation boundary when interaction is unavailable.

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

Treat implementation, accepted decisions, current releases, and authoritative project contracts as the source of truth. Existing public prose is evidence, not authority.

## Evidence to inspect

Inspect applicable:

- current default-branch implementation, configuration, schemas, and public interfaces;
- accepted architecture decisions, QART, RFCs, ADRs, and specifications;
- current releases, packages, deployment state, and working demos;
- project and organization READMEs;
- open issues, pull requests, known limitations, and migration status;
- websites, landing pages, books, one-pagers, whitepapers, diagrams, screenshots, and example commands;
- repository ownership, public/private/community boundaries, domains, and download links;
- security, privacy, licensing, support, and commercial claims;
- related repositories and integration testbeds;
- project-local documentation/skill guidance when present.

Prefer exact current evidence over copied summaries, historical branches, or ambient green CI.

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

For private-canonical/public-distribution topologies, clearly distinguish implementation authority from the public artifact/package/community surface. Do not imply that a public distribution repository contains or authorizes private implementation source merely because it is the public install path.

### 8. Terminology and narrative consistency

Identify inconsistent names, acronyms, maturity labels, architecture terms, goals, and calls to action across artifacts. Recommend one authoritative term and source.

### 9. Public credibility and UX

Review information hierarchy, readability, navigation, accessibility, visual consistency, code formatting, diagram legibility, responsive behavior, empty or broken sections, and whether the strongest verified outcome is visible early.

Separate credibility or usability problems from cosmetic preference.

## Recurring and cross-repository maintenance mode

When reviewing a set of public repositories or running periodically:

1. Establish the public surface inventory before editing: repository README, repository description/topics where accessible, docs entry points, landing/site source, release/install docs, generated references, package/community surfaces, and canonical external URLs.
2. Resolve each project's documentation authority locally first. Shared guidance coordinates the review; it does not replace project-owned architecture, maturity, release, or security truth.
3. Classify drift per repository, then reconcile cross-repository names, links, release paths, public/private roles, and shared terminology.
4. Prefer updating canonical source content rather than generated output. If generated content drifts, fix its authoritative input or generator when feasible.
5. Continue safe, unambiguous maintenance even when another repository has a blocked claim or decision.
6. Track repeated drift patterns and recommend mechanical prevention: link checks, docs builds, generated CLI/API references, example tests, version checks, release-artifact verification, or other deterministic gates.
7. Re-review affected rendered/public surfaces after changes. A source diff alone is not sufficient evidence for a landing page or generated site.

The goal is not to make every repository say the same thing. The goal is for each public surface to say the smallest accurate thing supported by its owning project while remaining coherent with the wider ecosystem.

## Human-in-the-loop ambiguity gate

Do not ask humans to resolve questions that repository evidence can answer. When material ambiguity remains after inspection, aggregate it into a bounded **human decision queue** rather than interrupting piecemeal.

A question belongs in the queue only when two or more plausible interpretations could materially change a public claim, ownership boundary, maturity statement, supported workflow, security/privacy statement, release/install path, destructive edit, or authorized mutation.

For each question provide:

| Field | Requirement |
| --- | --- |
| ID | Stable short identifier for the current review, such as `DOC-Q1` |
| Question | One decision-oriented question, not a request for broad explanation |
| Why it matters | The public claim, mutation, or boundary controlled by the answer |
| Evidence/conflict | Current evidence and the specific unresolved contradiction or gap |
| Options | Bounded plausible choices when known |
| Recommended default | Preferred answer only when evidence supports one; otherwise `none` |
| Blocked scope | Exact artifact/claim/mutation that must wait |
| Safe continuation | Work that can continue without the answer |

Use these dispositions:

- **BLOCKING-WRITE** — do not mutate the affected source/public surface until answered.
- **BLOCKING-CLAIM** — do not publish or strengthen the affected claim; unrelated edits may continue.
- **FOLLOW-UP** — non-blocking uncertainty; state the working assumption and continue.

Prefer a small set of high-information questions, normally grouped into 3–7 material decisions per pass when possible. Do not manufacture questions to reach a quota, and do not suppress additional questions when separate authority/security decisions genuinely require human disposition.

If interaction is unavailable, finish all unaffected read-only analysis and authorized unambiguous edits, then return the queue. Never silently choose between conflicting authoritative sources.

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

### G. Human decision queue

List only unresolved material questions using the structured ambiguity format above. If none remain, state `No material human decisions required`.

### H. Maintenance/prevention opportunities

Identify repeated drift that can be reduced mechanically, with the owning repository and proposed validation/generation mechanism.

### I. Final assessment

Choose exactly one:

- **Consistent and publishable**
- **Publishable after minor corrections**
- **Current with human decisions pending**
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
4. Do not edit through a material human-decision boundary until it is resolved.
5. Validate links, commands, examples, builds, documentation generation, and deployment previews as applicable.
6. Re-review the rendered result on relevant form factors.
7. Reconcile cross-repository links/names when the change affects ecosystem navigation or install paths.
8. Publish only through the established workflow and report the production URL or immutable artifact when publication itself was authorized.
9. Record unresolved material drift in the owning project's existing issue when possible; create a focused issue only when no suitable work item exists.

## Completion

The review is complete when every material public claim in scope is either supported, corrected, explicitly qualified, or represented in the human decision queue; authorized changes have been revalidated against current evidence; and unrelated work has not been blocked merely because one ambiguity remains.
```
