# Micrantha Onboarding Prompt

Use this prompt when you are new to a Micrantha repository and need to understand how to contribute, file work, or make decisions within the engineering methodology.

```markdown
# Micrantha contributor onboarding

Guide **[NEW CONTRIBUTOR]** through the Micrantha engineering methodology for **[REPOSITORY / PROJECT]**.

## Execution boundary

Read-only. Do not modify any repository files during onboarding. The goal is orientation, not mutation.

## Context

- **Repository or project:** [TARGET]
- **Contributor background:** [ROLE / EXPERIENCE / FAMILIARITY]
- **Intended contribution:** [BUG FIX / FEATURE / DOCUMENTATION / INFRASTRUCTURE / GOVERNANCE / UNKNOWN]

## Goals

Answer these questions for the contributor:

1. **Where do I start?** Identify the repository's maturity, current milestone, and where to find its purpose and scope.
2. **How do I file work?** Explain the issue templates, required fields (priority, outcome, acceptance criteria), and the difference between a bug, feature, delivery slice, epic, spike, QART, RFC, and ADR.
3. **How do I get work done?** Walk through the decision-to-delivery flow: classify-and-route → QART (if alternatives are open) → RFC (if broad review needed) → decision → ADR (if durable) → epic or plan → bounded delivery slices → validation → merge.
4. **How do I get work merged?** Explain the merge-gate review, required validation (test pyramid, static analysis, CI gates), and the pull-request expectations.
5. **How do I release?** Summarize the release-readiness dimensions and the release owner's responsibilities.
6. **Where do I find the standards?** Link to the engineering standards (testing, CI/CD, security, releases, documentation, labels) and governance model.
7. **Which prompts exist?** Provide a brief map of the prompt library and when to use each.

## Evidence to inspect

Inspect applicable:
- repository README, CONTRIBUTING.md, and CODEOWNERS;
- repository maturity and classification from the catalogue or registry;
- current milestone and recent work;
- organization standards and governance (linked from README.md);
- prompt library manifest (prompts/manifest.yaml).

## Required output

### A. Repository context

State the repository's purpose, maturity, current milestone, and where its scope is documented.

### B. Contribution path

Based on the contributor's intended contribution, recommend the smallest path:
- Bug fix → file a bug issue → implement → merge-gate review → merge
- New capability → classify-and-route → [QART if alternatives open] → file issue(s) → implement in slices → merge
- Uncertain scope → spike → classify-and-route → proceed
- Cross-boundary change → QART → RFC → decision → ADR → plan → deliver

### C. Standards map

List the applicable standards and where they are defined. State which are organizational defaults and which may have repository-local overrides.

### D. Prompt guide

For each relevant prompt, state its name, when to use it, and what it produces. Keep it to the prompts applicable to the contributor's stated intent.

### E. First action

Identify the smallest, safest first action the contributor can take right now.
```

Compact invocation:

> Onboard **[NEW CONTRIBUTOR]** to **[REPOSITORY]**: explain the contribution path, decision-to-delivery flow, applicable standards, and which prompts to use for their intended work.
