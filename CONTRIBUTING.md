# Contributing to Micrantha projects

This document defines the default contribution and issue-triage conventions for repositories in the `hackelia-micrantha` organization. A repository may refine these rules where its operating model requires it, but should document any differences explicitly.

## Issue prioritization standard

Priority answers one question:

> How soon should this issue consume limited engineering capacity relative to other open work in the same repository?

Priority is **not** severity, size, status, confidence, or architectural importance. Track those dimensions separately.

### Priority levels

| Priority | Meaning | Typical examples |
| --- | --- | --- |
| **P0 — interrupt** | Active work must be displaced because a critical repository capability, security boundary, release path, or required validation gate is currently broken or dangerously exposed. | exploitable vulnerability; data or secret exposure; required branch gate unavailable; production or release blocker; corruption or irreversible-loss risk |
| **P1 — next** | The issue belongs in the repository's small next-up queue. It materially unlocks the current product milestone, removes a high-leverage dependency, or closes a significant security or operability gap. | current milestone blocker; contract required by an active integration; security architecture prerequisite; external-trial readiness |
| **P2 — planned** | Important work with clear value, but it does not displace the current P0/P1 queue. It should be groomed enough to schedule when capacity opens. | bounded architectural improvement; adoption documentation; performance work without an active outage; dependency modernization |
| **P3 — later / explore** | Valid work without a current delivery commitment, or work that remains exploratory, duplicated, blocked, or insufficiently defined. | research spike; optional integration; speculative abstraction; source issue awaiting consolidation |

### Hard rules

- **P0 is exceptional and temporary.** A prerequisite for future work is normally P1, not P0, unless its absence is breaking the repository now.
- **Security does not automatically mean P0.** Use P0 for credible, immediate exposure or failure. Use P1/P2 for hardening and architecture work according to urgency and dependency leverage.
- **Blocked is a status, not a priority.** Preserve the underlying business priority and record the blocker explicitly.
- **An epic is not executable work.** Prioritize the smallest ready slice; keep umbrella issues as coordination surfaces.
- **Priority is repository-global.** Do not call an issue P0 only because it is the highest priority inside one architectural track.
- **Age does not create priority.** Old issues should be revalidated, consolidated, or closed rather than promoted automatically.

### Decision factors

Use judgment rather than a false-precision score. Record the factors that materially drove the decision:

1. **Impact** — security, correctness, operability, user value, or delivery effect.
2. **Urgency** — cost of waiting; active failure versus future risk.
3. **Dependency leverage** — how much ready work the issue unlocks or blocks.
4. **Readiness** — whether scope, dependencies, acceptance criteria, and ownership are clear.
5. **Risk of change** — blast radius, reversibility, migration risk, and verification cost.
6. **Strategic fit** — relationship to the repository's current milestone or product thesis.

A high-impact but poorly understood issue may need a bounded P1/P2 investigation before implementation. A low-risk, ready issue should not leapfrog a more consequential blocker merely because it is easy.

### Required issue fields

Issues entering the active queue should contain:

```markdown
## Priority

P1 — one-sentence repository-global rationale.

## Outcome

What observable result changes when this issue is complete?

## Dependencies

- Ready: ...
- Blocked by: ...
- Unlocks: ...

## Acceptance criteria

- [ ] Verifiable result

## Non-goals

- Explicitly excluded work
```

Use organization-standard labels when available:

- `priority:P0`
- `priority:P1`
- `priority:P2`
- `priority:P3`
- `status:blocked`
- `status:needs-grooming`
- `type:epic`
- `type:spike`

Issue-body priority text remains the durable explanation; labels support filtering and automation.

### Execution order

Priority narrows the queue but does not fully determine execution order. Within a priority level, order work by:

1. active incident or security containment;
2. dependency chain and unblock value;
3. readiness and available ownership;
4. shortest safe path to a verifiable milestone;
5. change risk and rollback capability.

Prefer a small queue:

- P0: only active interrupts;
- P1: normally three to five executable issues per repository;
- P2: ordered planned backlog;
- P3: uncommitted or exploratory backlog.

Umbrella issues, epics, and tracking ledgers do not count as executable P1 work unless their next concrete slice is identified.

### Reprioritization triggers

Review priority when any of these occur:

- a production, CI, release, or security condition changes;
- a dependency becomes ready or blocked;
- an implementation slice merges;
- the current milestone changes;
- an issue proves broader, riskier, or less valuable than expected;
- duplicate work or a stronger consolidation parent is identified;
- an issue has had no meaningful activity across multiple planning cycles.

Every reprioritization should leave a brief rationale in the issue or repository priority ledger. Avoid silently changing labels without updating the underlying reasoning.

### Backlog hygiene

During triage:

- close completed issues even when a larger umbrella remains open;
- close duplicates only after unique requirements and threat findings are preserved;
- split issues whose remaining work has a different priority or outcome;
- demote source SPIKEs after their findings are consolidated;
- distinguish active implementation, coordination epics, and reference material;
- keep one dated repository priority ledger when sequencing spans many issues.

## Pull requests

Pull requests should identify the issue or outcome they advance, describe validation, and state any remaining follow-up. A pull request does not inherit priority merely by being open; stale or speculative pull requests should be reviewed against the current issue queue.