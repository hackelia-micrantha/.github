---
name: documentation-sync
description: Keep public repository documentation, READMEs, landing pages, release/install guidance, and public claims synchronized with current implementation, maturity, and public/private boundaries while routing material ambiguity to a human decision queue.
---

# Documentation sync

## Trigger

Use for requests such as `keep public docs current`, `sync documentation`, `review docs/site claims across repos`, `maintain landing pages`, or recurring maintenance of public Micrantha repository surfaces.

Use this skill when the goal is broader than a one-off wording review: the operator wants public surfaces reconciled with implementation repeatedly or across multiple repositories.

## Inputs

- one repository or a bounded repository set;
- current repository visibility and role, without inferring implementation authority from visibility alone;
- project-local documentation/landing-page guidance when present;
- current default-branch implementation, accepted decisions, release/install path, and maturity evidence;
- public surfaces in scope: README, docs entry points, landing/site source, repository description/topics where accessible, release/install docs, examples, generated references, package/community surfaces, and canonical external URLs;
- mutation authorization if edits, commits, publication, deployment, issue updates, or external changes are requested.

## Ownership model

Resolve documentation behavior **project-local first**.

- The owning project remains authoritative for its implementation, architecture, maturity, release path, security boundary, and project-specific documentation rules.
- `hackelia-micrantha/.github` supplies the shared review/maintenance contract.
- The Micrantha meta repository may inventory adoption and coordinate cross-project consistency; it must not become a second editable source of project documentation truth.
- A public/community/distribution repository is not automatically the implementation authority.

When a project has a local `documentation-sync` skill or equivalent contract, use it and treat this shared skill as the default/reference it specializes.

## Workflow

1. **Establish scope and inventory.** Identify the repositories and public surfaces actually in scope. For a cross-repository pass, start from an authoritative registry or explicit repository set rather than broadening opportunistically.
2. **Resolve authority.** For each project, identify implementation authority, release/distribution authority, public surface ownership, project-local documentation rules, and applicable accepted decisions.
3. **Establish current evidence.** Inspect current default-branch implementation, releases/artifacts, supported install path, public/private topology, open migrations, and material current issues/PRs that affect public truth.
4. **Run claim reconciliation.** Apply `docs/prompts/documentation/public-consistency-review.md` to material public claims, links, examples, diagrams, maturity statements, security/privacy claims, and landing-page positioning.
5. **Classify drift.** Separate misleading, stale, ambiguous, missing, inconsistent, and opportunity findings. Prefer the smallest truthful claim supported by current evidence.
6. **Build the human decision queue.** Resolve ambiguity from evidence first. Aggregate only material unresolved decisions using the prompt's structured `DOC-Q*` format. Do not interrupt piecemeal when safe unrelated work can continue.
7. **Apply bounded updates when authorized.** Correct canonical source content first; do not hand-edit generated output when its input/generator is the real source. Do not cross a `BLOCKING-WRITE` or `BLOCKING-CLAIM` decision boundary without human disposition.
8. **Validate.** Re-run applicable link checks, docs/site builds, example or command tests, generated-reference checks, release/install verification, and rendered-page review. Validate the public/rendered result where the surface is a website or generated artifact.
9. **Re-review.** Compare the resulting state against current implementation and the original findings. Confirm that edits did not create cross-repository naming, link, ownership, or release-path contradictions.
10. **Track residual work.** Update an existing owning-project issue for implementation or documentation gaps when one exists; otherwise create the minimum focused follow-up. Keep human decisions distinct from ordinary implementation backlog.
11. **Compound repeated drift.** Recommend deterministic prevention when recurrence is mechanically detectable: link checks, docs builds, generated CLI/API references, version checks, example tests, release-artifact verification, schema-derived reference, or similar gates.

## Human-in-the-loop decision queue

Questions are an output of evidence review, not a substitute for it.

Only queue a question when unresolved ambiguity could materially change:

- a public capability or maturity claim;
- repository/component ownership or canonical source;
- release/install/support path;
- security, privacy, licensing, or distribution wording;
- a destructive or externally visible edit;
- an authorized mutation whose target or effect is not safely bounded.

For each decision include:

- stable short ID (`DOC-Q1`, `DOC-Q2`, ...);
- one decision-oriented question;
- why the answer matters;
- evidence and the precise conflict/gap;
- bounded options when known;
- recommended default only when supported by evidence;
- exact blocked artifact/claim/mutation;
- safe work that can continue meanwhile;
- disposition: `BLOCKING-WRITE`, `BLOCKING-CLAIM`, or `FOLLOW-UP`.

Prefer a small high-information batch, normally 3–7 material questions per review pass when possible. Do not invent questions to fill a quota and do not collapse distinct authority/security decisions merely to reduce count.

In unattended execution, continue all unambiguous read-only work and separately authorized safe mutations, then stop only at the affected decision boundary and return the queue.

## Evidence

A completed pass should identify, as applicable:

- repository/default-branch revision inspected;
- release/artifact/install evidence inspected;
- public surfaces inspected;
- project-local documentation authority used;
- material claim dispositions;
- changes made and their commit/PR evidence;
- validation commands/checks and rendered/public verification;
- unresolved human decisions and exact blocked scope;
- follow-up issues or mechanical drift-prevention opportunities.

Do not claim a public surface is current because CI is generally green or because a source edit appears plausible. Use evidence tied to the affected current revision and public contract.

## Mutation boundary

Read-only by default.

When writes are explicitly authorized:

- mutate only the repositories/surfaces in the approved scope;
- prefer branch/PR workflows unless the project explicitly uses another path;
- preserve project-local style and documentation architecture;
- avoid exposing private implementation details or inaccessible internal links;
- never treat a public repository's visibility as authorization to publish private source or internal operational detail;
- do not publish/deploy merely because source edits were authorized unless publication/deployment was also authorized.

## Completion

Complete when:

- every material public claim in scope is supported, corrected, explicitly qualified, or represented in the human decision queue;
- authorized edits are validated against current implementation and, for sites/generated docs, the rendered result;
- cross-repository names, links, public/private roles, and install/release paths are internally coherent for the reviewed scope;
- unrelated work is not blocked by isolated ambiguity;
- residual implementation/documentation gaps have an owning work item when needed;
- repeated mechanically detectable drift has either a prevention recommendation or an explicit reason automation is not worthwhile.

Valid final states are:

- `CURRENT`
- `CURRENT WITH FOLLOW-UPS`
- `CURRENT WITH HUMAN DECISIONS PENDING`
- `BLOCKED BY IMPLEMENTATION/DECISION`
- `SIGNIFICANT DRIFT REMAINS`

## References

- `docs/prompts/documentation/public-consistency-review.md`
- `docs/prompts/README.md#shared-ambiguity-and-clarification-contract`
- `docs/prompts/architecture/cross-repository-boundaries.md`
- `docs/prompts/project-review/comprehensive-status-review.md`
- `docs/prompts/releases/release-readiness.md`
- `docs/standards/source-exposure-and-distribution.md`
- `docs/standards/testing.md`
- `docs/standards/ci-cd.md`
