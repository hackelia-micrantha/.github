# Label and work-item taxonomy

Labels support filtering, triage, reporting, and bounded automation. They do not replace the durable rationale, outcome, dependencies, acceptance criteria, ownership, or evidence in an issue or pull request.

Repositories should use the smallest useful subset of this taxonomy. Do not create labels that remain ambiguous, duplicate another dimension, or require constant manual maintenance without decision value.

## Naming convention

Use `dimension:value` for organization-standard dimensions:

```text
priority:P1
status:blocked
type:epic
area:ci
maturity:incubating
```

Use lowercase values and hyphens for multiword terms. Preserve established ecosystem terms and product names where case matters only in prose, not labels.

## Priority

Priority labels are mutually exclusive:

- `priority:P0` — active interrupt;
- `priority:P1` — small executable next-up queue;
- `priority:P2` — planned work;
- `priority:P3` — later, exploratory, duplicated, or uncommitted work.

Priority follows [`CONTRIBUTING.md`](../../CONTRIBUTING.md). `Blocked` is not a priority. The issue body should record the repository-global rationale because labels alone do not explain why capacity should be allocated.

Umbrella epics may have priority for coordination, but the next executable slice must be identified separately.

## Status

Status labels describe workflow state and may coexist when meanings are not contradictory:

- `status:needs-grooming` — outcome, scope, dependencies, or acceptance criteria are incomplete;
- `status:needs-evidence` — a decision or implementation claim lacks required evidence;
- `status:needs-decision` — material alternatives or authority remain unresolved;
- `status:blocked` — cannot proceed because a named dependency or condition is unresolved;
- `status:ready` — sufficiently understood and unblocked for its next action;
- `status:in-progress` — actively being worked;
- `status:needs-review` — awaiting accountable review;
- `status:needs-validation` — implementation exists but required evidence is incomplete;
- `status:deferred` — valid but intentionally not scheduled;
- `status:superseded` — replaced by a named issue, decision, PR, or repository.

Avoid using labels for terminal GitHub states already represented by open, closed, merged, or draft unless reporting requires it.

`status:ready` and `status:blocked` are normally mutually exclusive. Remove stale state labels when conditions change.

## Work-item type

Use one primary type where possible:

- `type:bug` — incorrect observable behavior;
- `type:feature` — new user, operator, or system capability;
- `type:delivery` — bounded cross-cutting implementation, integration, migration, infrastructure, or refactoring outcome;
- `type:epic` — coordinates a larger outcome across bounded child work;
- `type:spike` — reduces uncertainty and produces evidence;
- `type:design` — explores or proposes architecture or system behavior;
- `type:qart` — resolves one bounded decision through alternatives and trade-offs;
- `type:rfc` — substantial proposal requiring broad review;
- `type:adr` — accepted durable decision record;
- `type:security` — security vulnerability, hardening, threat analysis, or control work;
- `type:documentation` — documentation is the primary outcome;
- `type:maintenance` — dependency, compatibility, cleanup, or routine corrective work;
- `type:release` — release preparation, publication, or support action.

Security may also be represented as an area or impact on another primary type. Use `type:security` when security work is the main outcome rather than automatically adding it to every security-relevant change.

## Area

Area labels identify ownership or technical surface. They are repository-specific, but common values include:

- `area:architecture`
- `area:ci`
- `area:release`
- `area:security`
- `area:documentation`
- `area:dependencies`
- `area:infrastructure`
- `area:mobile`
- `area:android`
- `area:ios`
- `area:web`
- `area:api`
- `area:data`
- `area:observability`
- `area:governance`

Prefer a few meaningful ownership or contract boundaries over one label per directory. Multiple area labels are acceptable for genuinely cross-cutting work.

## Maturity

Maturity labels follow the [repository lifecycle](../governance/repository-lifecycle.md):

- `maturity:proposed`
- `maturity:experimental`
- `maturity:incubating`
- `maturity:active`
- `maturity:stable`
- `maturity:maintenance`
- `maturity:superseded`
- `maturity:archived`

Use maturity labels primarily for repositories, components, milestones, or dedicated lifecycle issues. Do not add a maturity label to every implementation issue unless it materially affects triage.

## Impact and risk

Severity, user impact, confidence, effort, and change risk are separate from priority. Repositories may add dimensions such as:

- `severity:critical`, `severity:high`, `severity:medium`, `severity:low`;
- `risk:high`, `risk:medium`, `risk:low`;
- `confidence:low`;
- `breaking-change`;
- `security-sensitive`;
- `release-blocker`.

Define these locally before using them. Do not infer `priority:P0` from `severity:critical` without assessing current exposure, urgency, and repository-global capacity.

## Dependencies and relationships

Use GitHub issue and pull-request links for exact relationships:

- blocked by;
- blocks or unlocks;
- parent epic;
- duplicate;
- supersedes or superseded by;
- related RFC, ADR, QART, release, or repository.

Labels such as `blocked` or `duplicate` may support filters, but the linked source remains authoritative.

## Pull-request labels

Pull requests may reuse type, area, risk, and release labels. Avoid assigning issue priority automatically to a PR; a PR advances an outcome but does not become urgent merely because it is open.

Useful PR-only labels may include:

- `breaking-change`;
- `needs-release-note`;
- `dependencies`;
- `automated`;
- `do-not-merge` for an explicit temporary gate with a written reason.

Do not use `do-not-merge` as a substitute for draft state, failing required checks, or unresolved review findings.

## Automation rules

Automation may apply or remove labels when the rule is deterministic and reversible. It should not:

- assign priority without an accountable rationale;
- accept security risk;
- infer decision acceptance from merged code;
- mark an epic complete solely because known child issues closed;
- remove a human-applied governance or release hold without authority;
- create labels that do not exist consistently across intended repositories.

When inherited issue templates reference labels, those labels must exist in the consuming repository. Prefer templates without mandatory labels unless organization automation ensures label availability.

## Repository adoption

When adopting the taxonomy:

1. inventory existing labels and usage;
2. map meanings before renaming;
3. preserve issue history and saved-filter needs;
4. create only the subset the repository will maintain;
5. update issue forms, templates, automation, and documentation together;
6. remove obsolete labels after open work is migrated;
7. document local additions or changed meanings.

## Review cadence

Review the taxonomy when labels become unused, contradictory, overly numerous, or disconnected from planning and reporting. A smaller accurate taxonomy is better than comprehensive but unreliable metadata.
