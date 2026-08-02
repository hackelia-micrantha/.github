# Project review prompts

These prompts provide a shared Micrantha method for evidence-backed project reviews, backlog correction, and dependency-ordered prioritization.

## Choose a prompt

| Prompt | Use when | Expected output |
| --- | --- | --- |
| [Comprehensive project status review](comprehensive-status-review.md) | First review, milestone audit, architecture drift, unclear maturity, or an unreliable backlog | Project model, capability matrix, architecture and security findings, corrected backlog, and phased execution plan |
| [Project status refresh](status-refresh.md) | A credible prior review or release baseline exists and the goal is to determine what changed and what happens next | Material change summary, completed and unresolved work, PR/issue actions, and a small next-up queue |

## Operating model

The prompts follow the organization-wide conventions in [`CONTRIBUTING.md`](../../../CONTRIBUTING.md):

- priority is repository-global and distinct from severity, status, size, confidence, and architectural importance;
- `P0` is an exceptional active interrupt;
- `P1` is a small queue of executable next work;
- blocked work retains its underlying priority and records the blocker separately;
- epics coordinate work but do not replace bounded executable slices;
- issue bodies preserve the durable rationale, outcome, dependencies, acceptance criteria, and non-goals.

## Recommended workflow

1. Run the comprehensive review when no trustworthy baseline exists.
2. Store the dated result in the project repository or a tracking issue.
3. Convert only the highest-value findings into coherent issues or decision artifacts.
4. Keep the repository's P1 queue small and dependency-ordered.
5. Use the status refresh after meaningful merges, releases, incidents, milestone changes, or planning cycles.
6. Close, consolidate, supersede, or demote work when evidence changes.

## Review artifact guidance

Use the smallest artifact that resolves the uncertainty:

| Need | Artifact |
| --- | --- |
| Observable implementation outcome | Task, bug, or vertical-slice issue |
| Coordination across bounded child work | Epic |
| Unknown feasibility or evidence | Spike |
| Alternatives and trade-offs remain open | QART analysis |
| A proposal needs broader review | RFC |
| A decision is understood and should become authoritative | ADR |
| Threats or controls require focused analysis | Security review or threat model |

Do not create an artifact solely because the prompt mentions it. The review should recommend one only when it advances a concrete decision or outcome.

## Scope controls

A useful invocation should identify:

- repositories in scope;
- current milestone or target outcome;
- expected project maturity;
- baseline date, commit, release, or prior review for a refresh;
- known constraints such as security, compatibility, platform, or delivery boundaries.

When reviewing several repositories, require the reviewer to distinguish shared ecosystem findings from repository-local work and to assign priority within each repository rather than inventing one ambiguous cross-repository queue.