# Implementation Completeness Review Prompt

Use this prompt after multiple pull requests, before closing an epic, or whenever merged code may not yet represent a delivered capability.

Apply the [shared validation and static-analysis contract](../README.md#shared-validation-and-static-analysis-contract) when assessing executable software, build logic, configuration, or delivery behavior.

```markdown
# Implementation Completeness Review

Determine whether **[CAPABILITY / EPIC / MILESTONE / ISSUE SET]** is substantively complete, usable, and accurately represented.

## Context

- **Intended outcome:** [OUTCOME]
- **Authoritative requirements or issue:** [SOURCE]
- **Relevant repositories and pull requests:** [SCOPE]
- **Expected maturity:** [PROTOTYPE / INCUBATING / STABLE / MAINTAINED]
- **Mutation authorization:** [READ ONLY / RECONCILE TRACKING]

## Execution boundary

Begin read-only. Treat issue status, pull-request descriptions, release notes, documentation, and demos as claims requiring verification. Do not close issues, change maturity labels, or update public claims unless explicitly authorized.

## Completion principle

A capability is not complete merely because code merged. Completion requires the applicable implementation, integration, layered validation, static analysis, documentation, packaging, user path, security, and operational behavior to agree with the stated outcome and maturity.

Apply expectations appropriate to the declared maturity. A prototype may intentionally lack production operations, but must not be represented as stable.

## Evidence to inspect

Inspect applicable:

- original requirements, acceptance criteria, issue hierarchy, and non-goals;
- all pull requests and commits claimed to deliver the outcome;
- current implementation and integration paths;
- unit/component, contract/integration, end-to-end, security, migration, compatibility, and failure-path tests;
- repository build/task tooling and canonical test/static-analysis commands;
- compile/type checks, linting, source/configuration static analyzers or SAST, and configuration/IaC analysis where applicable;
- CI/CD, packaging, release artifacts, deployment, and configuration;
- README, API, CLI, examples, website, book, one-pager, and demo claims;
- monitoring, logging, audit evidence, rollback, recovery, and ownership;
- known bugs, TODOs, skipped tests, feature flags, mocks, stubs, and temporary compatibility paths;
- downstream consumers and related repositories.

## Completeness dimensions

### 1. Outcome and reachability

Verify that:

- the intended user or system can reach the capability;
- the primary use case works end to end;
- configuration and installation paths are available;
- hidden manual steps or private fixtures are not required unless explicitly part of the contract;
- feature flags, mocks, demo adapters, or local-only assumptions are disclosed.

### 2. Functional behavior

Verify requirements, edge cases, errors, partial failures, compatibility, migration, retries, idempotency, concurrency, and state handling relevant to the outcome.

### 3. Integration and contracts

Confirm:

- upstream and downstream integration works;
- APIs, schemas, protocols, artifacts, and versioning agree;
- repository responsibilities are coherent;
- transitional dual paths have a documented lifecycle;
- downstream examples or consumers use the current contract.

### 4. Validation and static analysis

Assess whether the capability has an appropriate test pyramid: strong fast unit/component coverage at the base, targeted contract/integration coverage at important boundaries, and a smaller end-to-end set for critical supported user or operator paths. Add important negative, failure, migration, security, compatibility, performance, or operational validation according to risk.

Do not demand a layer mechanically when its boundary does not exist. Identify the applicable layers, what meaningful behavior each proves, and any material behavior left unverified.

Assess language- and stack-appropriate compile/type checks, linting, source/configuration static analyzers or SAST, and configuration/IaC analysis where applicable. Verify canonical checks are available through repository build/task tooling and/or CI/CD, and that repositories beyond experimental maturity enforce material checks in CI/CD or an equivalent protected build gate.

Identify validation that exists only locally, is CI-only without a reproducible equivalent, is skipped, stale, disabled, incorrectly scoped, or unexpectedly non-blocking. A green aggregate status does not compensate for a missing required layer or analyzer.

### 5. Security and privacy

Review applicable authentication, authorization, capabilities, trust boundaries, untrusted input, secrets, permissions, supply chain, provenance, logging, retention, isolation, and fail-open behavior.

A missing hardening enhancement is not automatically incompleteness. A violated security invariant or undocumented unsafe boundary is.

### 6. Delivery and operations

Check applicable:

- reproducible build and packaging;
- versioning and release artifacts;
- deployment and upgrade path;
- configuration and secret provisioning;
- observability and audit evidence;
- rollback, recovery, backup, and failure ownership;
- runbooks and known limitations.

### 7. Documentation and claims

Ensure documentation accurately distinguishes:

- implemented;
- validated;
- released;
- experimental or demo-only;
- planned or aspirational;
- supported and unsupported environments.

### 8. Work tracking

Reconcile:

- completed issues that should close;
- closed issues with unmet acceptance criteria;
- umbrella epics whose child work remains;
- duplicate or obsolete follow-up;
- missing bounded issues for material remaining work;
- maturity labels and milestone status.

## Completion classification

Classify the capability as:

- **Complete and verified**
- **Complete for stated maturity with bounded follow-up**
- **Functionally implemented but not delivered**
- **Integrated but insufficiently validated**
- **Partial vertical slice**
- **Prototype or demo-only**
- **Blocked**
- **Misrepresented as complete**
- **Superseded or obsolete**
- **Insufficient evidence**

## Required output

### A. Intended versus delivered outcome

State the authoritative intended outcome, actual current behavior, intended users, and maturity.

### B. Completeness matrix

| Dimension | Status | Evidence | Missing work | Material to completion? |
| --- | --- | --- | --- | --- |
| Outcome and reachability | | | | |
| Functional behavior | | | | |
| Integration and contracts | | | | |
| Validation and static analysis | | | | |
| Security and privacy | | | | |
| Delivery and operations | | | | |
| Documentation and claims | | | | |
| Work tracking | | | | |

### C. Material findings

List only findings that affect completion, maturity, safety, usability, truthful representation, the applicable test pyramid, or required static-analysis/build/CI gates.

### D. Remaining work

Separate:

- completion blockers;
- bounded follow-up compatible with closure;
- deferred enhancements;
- obsolete or duplicate work to close.

For required new work, provide issue-ready titles, outcomes, dependencies, and acceptance criteria. Avoid one issue per minor observation.

### E. Tracking actions

Recommend issues or epics to close, reopen, split, supersede, reprioritize, or update. State whether public maturity and documentation claims should change.

### F. Final assessment

Choose exactly one:

- **Close as complete**
- **Close as complete for stated maturity with bounded follow-up**
- **Keep open for focused completion work**
- **Reopen because acceptance criteria remain unmet**
- **Reclassify as prototype or demo-only**
- **Blocked by a named dependency or decision**
- **Supersede or archive**
- **Insufficient evidence**

Support the conclusion with verified evidence, including the applicable test-pyramid and static-analysis status for executable capabilities.

## Authorized reconciliation mode

When tracking or documentation mutations are authorized:

1. Apply only the actions supported by the completeness review.
2. Preserve unique requirements before closing duplicates or superseded work.
3. Update maturity and public claims conservatively.
4. Create only coherent material follow-up issues.
5. Report the resulting issue, milestone, documentation, validation, and static-analysis state.
```
