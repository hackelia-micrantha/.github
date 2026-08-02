# Project Status Refresh Prompt

Use this prompt after a comprehensive review or another reliable baseline. It is optimized for recurring repository reviews and should not re-document the entire project.

```markdown
# Project Status Refresh

Refresh the current status of **[PROJECT / REPOSITORY / REPOSITORY SET]**.

Focus on material changes, unresolved work, regressions, and the next executable priorities.

## Review window

- **Previous baseline:** [DATE / REPORT / ISSUE / COMMIT / RELEASE]
- **Changes since:** [DATE / COMMIT / RELEASE]
- **Current milestone:** [MILESTONE]
- **Repositories in scope:** [REPOSITORIES]
- **Known priority or objective:** [OBJECTIVE]

When no baseline is provided, use the most recent meaningful release, milestone, dated status report, or period of active development. State which baseline was selected and why it is credible.

## Questions to answer

1. What materially changed since the baseline?
2. What became substantively complete?
3. What remains incomplete, blocked, stale, superseded, or uncertain?
4. Did recent work introduce regressions, security risks, architectural drift, overlap, or inconsistency?
5. Do current issues and pull requests represent the remaining work accurately?
6. Is the project closer to the current milestone?
7. What should happen next, in dependency order?

## Evidence

Inspect the most relevant recent evidence:

- commits and changed files;
- open and recently merged or closed pull requests;
- open and recently changed or closed issues;
- recent CI/CD runs, artifacts, releases, tags, and milestones;
- new or changed tests, documentation, schemas, interfaces, and configuration;
- security alerts, permissions, dependency changes, provenance, and release controls;
- related repositories and integration points;
- unresolved findings and execution plans from the previous review.

Inspect older material only when required to understand a change, dependency, contradiction, or unresolved finding.

Do not equate merged code, a closed issue, a passing workflow, or updated documentation with a delivered capability. Verify implementation, integration, validation, documentation, packaging, and user access where applicable.

## Status classification

Classify relevant work as:

- **Completed and verified**
- **Completed with bounded follow-up**
- **In progress**
- **Blocked**
- **Needs validation**
- **Regressed**
- **Superseded**
- **Stale or no longer relevant**
- **Unknown**

Separate verified facts, inferences, questions, and recommendations.

## 1. Material changes

Summarize changes to applicable areas:

- features and capabilities;
- architecture, repository responsibilities, APIs, schemas, protocols, or configuration;
- security controls and trust boundaries;
- tests, fixtures, CI/CD, releases, deployment, and operations;
- UI, UX, CLI, API, onboarding, or developer experience;
- documentation, public messaging, issues, milestones, and planning;
- dependencies and external integrations.

Ignore formatting and mechanical refactoring unless they affect behavior, risk, maintainability, or delivery.

## 2. Completed work

Identify work that became substantively complete during the review window. Verify the observable outcome, acceptance criteria, meaningful tests, integration, documentation, CI, packaging or release state, and absence of unresolved blockers.

Call out merged work that remains incomplete in practice.

## 3. Remaining work

Identify:

- partially completed issues or pull requests;
- missing tests, documentation, packaging, release, migration, deployment, or operational work;
- broken or absent integrations;
- TODOs, stubs, mocks, skipped tests, ignored failures, and temporary workarounds;
- closed issues with unmet acceptance criteria;
- capabilities implemented but not exposed or usable;
- work blocked by decisions, dependencies, access, infrastructure, or external systems;
- old work that should be revalidated, consolidated, superseded, or closed.

Distinguish intentional deferral from accidental incompleteness.

## 4. Regressions and new risks

Check recent changes for:

- functional or compatibility regressions;
- CI, release, deployment, reliability, or performance instability;
- exploitable vulnerabilities, weakened security boundaries, unsafe defaults, or fail-open behavior;
- secret exposure, excessive permissions, dependency or supply-chain risk;
- architectural drift, duplicate responsibilities, or contract divergence;
- documentation, public messaging, UI/UX, accessibility, or developer-experience regressions.

Classify each as an active defect, active exposure, security risk, design concern, maintainability concern, or hardening opportunity. Do not overstate severity without a plausible failure or threat scenario.

## 5. Architecture and consistency

Confirm whether recent work remains consistent with project goals, current milestone, documented architecture, repository boundaries, API and protocol contracts, naming, security assumptions, public positioning, and related repositories.

Identify new overlap, contradiction, responsibility drift, obsolete decisions, or incomplete migrations.

Recommend QART when a consequential design choice remains unresolved. Recommend an ADR only when the decision is sufficiently understood to become authoritative.

## 6. Testing, CI/CD, and operations

Review current CI status, recent failures, new tests, critical paths still untested, flaky or disabled tests, negative and failure-path coverage, local-versus-CI-versus-release differences, reproducibility, artifacts, security scanning, signing, provenance, SBOMs, deployment, rollback, monitoring, and recovery where applicable.

Prioritize validation of high-risk behavior over generic coverage growth.

## 7. Issue and pull-request triage

Classify relevant pull requests as:

- **Merge**
- **Fix before merge**
- **Blocked**
- **Supersede or close**
- **Needs deeper review**

Identify issues that should close, reopen, split, combine, be rewritten, reprioritized, superseded, or converted into an epic, executable task, spike, bug, QART, RFC, ADR, or security review.

Do not create one issue for each minor observation. Group related work into coherent outcomes. An epic is not executable work; identify its next bounded slice.

## 8. Priority refresh

Use the Micrantha organization priority model:

- **P0 — interrupt:** active work must be displaced because a critical capability, security boundary, release path, or required validation gate is broken or dangerously exposed.
- **P1 — next:** belongs in the small next-up queue because it unlocks the current milestone, removes a high-leverage dependency, or closes a significant security or operability gap.
- **P2 — planned:** important, groomed work that should not displace the current P0/P1 queue.
- **P3 — later / explore:** valid but uncommitted, exploratory, duplicated, blocked, or insufficiently defined work.

Priority is not severity, status, size, confidence, age, or architectural importance. `Blocked` is a status, not a priority.

For each proposed item include priority rationale, observable outcome, impact, urgency, dependency leverage, readiness, risk of change, strategic fit, effort, dependencies, blockers, acceptance criteria, non-goals, and execution position.

Keep P1 to a small executable queue—normally three to five issues per repository. Order work by active containment, dependency chain, readiness, shortest safe path to the milestone, and change risk.

## Required output

### A. Status summary

State:

- current project state and maturity;
- selected baseline;
- material changes since that baseline;
- progress toward the current milestone;
- overall health: improving, stable, deteriorating, or unclear;
- most important completed outcome;
- most important remaining gap;
- principal current risk;
- whether the current backlog reflects reality;
- immediate next action.

### B. Change summary

| Area | Previous state | Current state | Evidence | Impact |
| --- | --- | --- | --- | --- |

Include only material changes.

### C. Completed since baseline

For each verified outcome, include evidence and any bounded follow-up.

### D. Incomplete, blocked, regressed, or obsolete work

| Item | Status | Evidence | Missing or broken work | Impact |
| --- | --- | --- | --- | --- |

### E. Key findings

Use only applicable headings: implementation; architecture and consistency; security; testing and CI/CD; operations; UI/UX and developer experience; documentation; issues and pull requests; repository boundaries and overlap.

For each finding include evidence, impact, recommendation, priority, confidence, and whether it is verified or inferred. Omit empty sections.

### F. Open questions and decisions

For each unresolved decision include why it matters, known evidence, plausible alternatives, recommended default when justified, and whether QART, RFC, ADR, spike, or security review is appropriate. Do not ask questions answerable from available evidence.

### G. Pull-request actions

List each relevant open pull request, its classification, reason, and required action.

### H. Issue actions

List issues to close, reopen, split, combine, rewrite, reprioritize, supersede, or create. Use issue-ready titles only for genuinely required new work.

### I. Prioritized next work

| Order | Priority | Item | Type | Rationale | Dependencies | Effort | Acceptance criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |

Limit the primary list to realistic next work. Put optional ideas in a deferred section.

### J. Execution sequence

Organize the next work into immediate stabilization, blocking decisions, next coherent implementation slice, validation and integration, documentation or operational follow-through, and deferred opportunities. Include exit criteria for each phase.

### K. Final assessment

Choose the closest conclusion:

- Ready to merge
- Ready to release
- Ready after minor fixes
- Progressing toward the milestone
- Requires focused completion work
- Blocked by unresolved decisions
- Requires security remediation
- Regressed since the previous review
- Appropriate to supersede or archive
- Insufficient evidence

Support the conclusion with concrete evidence.

## Constraints

- Focus on changes and unresolved work, not full project re-documentation.
- Surface active blockers, regressions, and security risks first.
- Prefer completion and simplification over new scope.
- Do not repeat resolved findings unless they regressed or remain incomplete.
- Explicitly state when the previous review, roadmap, or backlog is no longer authoritative.
- Do not produce a large backlog merely because possible improvements exist.
- Keep recommendations dependency-ordered, bounded, and executable.
```

A compact invocation is:

> Use the previous status review as the baseline. Focus on material changes since **[DATE / COMMIT]**, validate recently completed work, triage current issues and pull requests, and return only material findings and the next executable priorities.