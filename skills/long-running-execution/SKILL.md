---
name: long-running-execution
description: Carry a non-trivial engineering task through bounded review, repair, validation, gate, effect, and verification loops without repeated continuation prompts.
---

# Long-running execution

## Trigger

Use for operator intent such as:

- `proceed in loops`;
- `continue until blocked`;
- `run this to completion`;
- `review -> fix -> validate -> re-review`;
- `fix loop to proceed`;
- a non-trivial repository task where repeated `proceed` messages would otherwise be needed.

Do not use for a trivial one-step task or to bypass an explicit approval, merge, release, deployment, deletion, permission, credential, or external-communication gate.

## Inputs

Resolve from the invocation and authoritative repository/project state where possible:

- goal and desired terminal outcome;
- repository/system scope;
- exact starting work item, candidate, or revision;
- accepted constraints and project-local decisions;
- mutation authority already granted;
- consequential-effect authority already granted, if any;
- required validation, review, and evidence;
- applicable project-local skills, policy overlays, and retry limits.

Ask only when missing information is materially ambiguous and blocks the next safe transition. Do not ask for generic continuation confirmation after each successful substep.

## Execution model

Treat the run as:

```text
Goal + Graph + Policy + State + Evidence + Budget
```

Use the shared default graph unless a project-owned workflow defines a stronger one:

```text
discover
  -> snapshot
  -> plan
  -> review
  -> fix
  -> validate
  -> re-review
  -> gate
  -> execute
  -> verify
  -> closeout
```

On validation or verification failure:

```text
failure -> diagnose/classify -> repair/recover -> validate
```

On missing authority, policy conflict, material ambiguity, unavailable required evidence, or exhausted budget:

```text
current state -> blocked/escalate
```

## Workflow

1. **Discover authoritative state.** Inspect current code, issues, pull requests, branch/revision state, CI, accepted decisions, and repository-local policy needed for the goal. Do not reconstruct canonical state from conversation memory when an authoritative source exists.
2. **Snapshot the exact subject.** Record the candidate/revision identity when later evidence or approval must bind to it.
3. **Select bounded work.** Reuse accepted work items and architecture. Decompose only as needed for a reversible, independently verifiable increment.
4. **Compose task-specific skills.** Use specialized skills such as `implementation-plan`, `pr-review`, `merge-readiness`, `security-review`, `test-strategy`, `release-integration`, or project-local skills where they govern a transition. Preserve the strictest authority, evidence, and completion requirement of all composed skills.
5. **Review before repair.** Classify findings and failed evidence before mutating implementation. Distinguish correctness/design defects, stale or missing evidence, test/oracle problems, environment/infrastructure failure, nondeterminism, policy blockers, and material ambiguity.
6. **Repair minimally.** Make the smallest coherent change that addresses the causal finding without widening authority or scope.
7. **Validate the exact changed candidate.** Prefer deterministic and mechanically decidable evidence first. Treat material candidate changes as invalidating stale candidate-bound evidence.
8. **Re-review after green validation.** Tests are evidence, not semantic completion. Re-check the candidate against the goal, architecture, security boundaries, compatibility, acceptance criteria, and unintended scope changes.
9. **Continue while useful work remains.** If CI, builds, reviews, or another external check is pending, perform independent review, documentation reconciliation, issue cleanup, evidence gathering, or other safe work that does not depend on the pending result. Do not stop merely because one branch of the graph is waiting.
10. **Bound retries.** After the same causal failure twice without materially new evidence, change the hypothesis or escalate. Default repeated tool/infrastructure retry budget is three. Default implementation repair-cycle budget is six unless project policy defines another bound.
11. **Evaluate the gate separately.** Before merge, release, publication, deployment, destructive deletion, permission/credential mutation, external communication, or consequential acceptance closure, verify exact subject identity, current sufficient evidence, zero unresolved blockers, applicable policy, and explicit authority for that effect.
12. **Execute only authorized effects.** Use expected-head/candidate protection where supported. Do not infer effect authority from prior successful reasoning, green CI, issue ownership, or write access.
13. **Verify the resulting effect.** Confirm the intended externally observable state rather than treating an API/workflow success response as outcome proof.
14. **Close out or escalate precisely.** Report the resulting revision/state, evidence, effects, and remaining non-blocking work; or report the exact blocked transition and the smallest missing decision/capability.

## Run ledger

Maintain a compact run ledger when it materially helps recovery, handoff, auditability, multi-session continuity, or external runtime integration.

Track at least:

- goal;
- current graph state;
- exact subject/revision;
- unresolved blocking findings;
- evidence obtained/missing;
- active policy gates and effect authority;
- retry/investigation counters;
- blockers;
- next eligible transitions.

Do not persist state merely for ceremony. Conversation history may provide context but must not become the only canonical state when correctness, recovery, or authority depends on exact state.

## Evidence

Prefer, in order appropriate to the property:

1. schema/type/integrity/exact-subject checks;
2. compiler/static analysis/deterministic tests/property checks;
3. artifact/diff/runtime inspection;
4. independent semantic verification where necessary;
5. human disposition where consequence, policy, or uncertainty requires it.

Multiple model reviewers do not become independent evidence merely because they use different sessions, personas, or aliases.

## Mutation boundary

Read-only by default unless the invocation authorizes writes.

Write authority for a bounded task does not imply merge, release, deployment, deletion, permission/credential, or external-communication authority. Treat those as separately governed effects unless the invocation or authoritative project policy explicitly grants them.

Never use exhausted retry budgets, urgency, a confident model conclusion, or successful validation as justification to widen authority or weaken acceptance criteria.

## Completion

Complete only when one of these is true:

1. the requested terminal outcome has been reached and the resulting effect/state has been verified; or
2. the run is precisely blocked/escalated at a specific transition with the current exact subject, evidence already obtained, work already completed, retries/investigation performed, and the smallest requirement for continuation.

A pending check is not itself a completion condition while independent useful work remains.

## References

- `docs/engineering/agent-execution-contract.md`
- `docs/engineering/ai-assisted-sdlc.md`
- `docs/prompts/planning/long-running-agent-execution.md`
- `docs/prompts/README.md`
- `skills/pr-review/SKILL.md`
- `skills/merge-readiness/SKILL.md`
- `skills/test-strategy/SKILL.md`
- `skills/security-review/SKILL.md`
- `skills/release-integration/SKILL.md`
