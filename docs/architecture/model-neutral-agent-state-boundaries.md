# Model-neutral agent state boundaries

- **Status:** Design note — non-normative
- **Date:** 2026-08-12
- **Promotion:** Consider an organization RFC only after a concrete interoperability contract demonstrates a durable normative gap.

## Context

Recent agent architecture work across Micrantha has converged on a useful separation: canonical workflow/task state, runtime working state, durable execution state, identity/authorization, and governance evidence should not be collapsed into prompts, transcripts, or model-private computation.

BDH-CQ (arXiv:2608.09888) is an external research signal reinforcing this direction because it demonstrates useful iterative computation without requiring an externally serialized reasoning sequence. It is not a runtime dependency or normative specification.

The organization-level concern is therefore not how a model reasons internally. It is how independently owned repositories exchange the minimum structured state needed for reproducible, authorized, attributable execution.

## Cross-repository invariant

> Micrantha cross-repository contracts must remain independent of model-private reasoning representations.

A runtime may use token-by-token reasoning, recurrent/opaque computation, specialist delegation, symbolic execution, or another implementation style behind the same external contract.

The architecture should distinguish at least these categories:

```text
canonical workflow / task state
        |
        | compile / materialize
        v
portable invocation context
        |
        +------------------------------+
        |                              |
        v                              v
private runtime working state      authenticated execution principal
        |                              |
        v                              |
observable execution/effects <---------+
        |
        +--> durable execution state
        |
        +--> evidence / provenance
        |
        `--> explicit reviewed learning or memory promotion
```

## Responsibility boundaries

### Calathea

Owns canonical workflow/project state, lifecycle transitions, selected context, expected outputs, and compilation of domain intent into a runtime-neutral invocation request.

Rendered prompts or instructions are derived artifacts, not the canonical source of workflow truth.

### Invokrum

Owns the smallest portable invocation/materialization contract needed across hosts. Candidate state categories include exact task-state identity, selected context, requested capabilities, constraints, budgets, termination conditions, outputs, and evidence requirements.

Invokrum does not standardize model-private working state and does not become a policy engine.

### Keylix

Owns authenticated execution-principal and proof-of-possession semantics at authorization/protocol boundaries. Task/run identifiers provide attribution but are not credentials. Delegation narrows authority and cannot be established by caller-controlled runtime labels.

### Anthesis

Owns governance semantics over structured intent, exact effects, approvals, policy decisions, evidence interpretation, provenance, and residual risk.

Governance must not require visibility into model-private reasoning implementation. Provider/runtime diagnostics may be useful evidence when safely exposed, but they cannot mint or widen authority.

### Private runtime workstream

Owns runtime materialization, supervisor/specialist execution, ephemeral working state, durable operational state, recovery, leases/budgets, and explicit promotion of selected results into durable memory/state.

Public organization metadata must not expose private repository locations or sensitive implementation details.

## State and authority rules

1. **Canonical state is structured.** Workflow/task truth must have an addressable revision where changes can affect execution or authority.
2. **Prompts are derived.** A rendered prompt or instruction artifact may be integrity-bound, but it is not the canonical workflow database.
3. **Working state is runtime-private by default.** Intermediate computation is disposable unless a runtime explicitly promotes a bounded artifact for a defined purpose.
4. **Durable execution state is operational truth.** Recovery, lineage, budgets, leases, completion, and effect status must not depend on reconstructing private model computation.
5. **Memory/learning promotion is explicit.** Runtime output does not automatically become durable project state, policy, or memory.
6. **Identity is authenticated separately.** Actor/run labels in payloads are attribution data until bound to an authenticated execution principal.
7. **Evidence is not authority.** Runtime observations and verification results can support governance but cannot independently create authorization.
8. **Context changes can invalidate authority.** A material task-state revision after authorization requires re-evaluation when the changed fields affect the authorized subject.
9. **Delegation narrows state and authority.** Child executions receive explicitly selected context/capabilities rather than ambient parent state.
10. **Private computation is not a cross-repo schema.** No shared contract should require a `latent_state`, hidden-state dump, complete transcript, or equivalent model-specific representation.

## Current public workstreams

- **Anthesis:** reasoning-independent governance and observable-evidence invariants (`anthesis#155`).
- **Invokrum:** portable invocation-state and execution-evidence boundary (`invokrum#68`).
- **Keylix:** execution-principal and delegated runtime identity (`keylix#19`).
- **Calathea:** structured workflow-state compilation into the Invokrum boundary (`calathea#47`).
- **Private runtime:** runtime state/context/memory lifecycle and recovery work remains tracked privately.

These repository-local issues remain authoritative for implementation details. This note owns only the cross-repository responsibility map and invariants.

## Recommended sequencing

```text
organization invariants
        |
        v
Invokrum portable-contract QART
        |
        +--> Keylix identity/delegation binding
        |
        +--> private runtime state materialization
        |
        `--> Calathea compilation mapping
                    |
                    v
             integration fixtures
                    |
                    v
Anthesis governance/evidence conformance across the resulting observable boundary
```

Practical order:

1. Keep Anthesis's invariant and existing authority/evidence model stable; avoid a new policy surface.
2. Let Invokrum determine the smallest portable contract and vocabulary actually required by multiple hosts.
3. Bind that contract to authenticated execution principals in Keylix and runtime-owned state materialization independently.
4. Update Calathea's existing Invokrum boundary only after the portable contract stabilizes enough to consume.
5. Add cross-repository fixtures that prove stale-state rejection, delegated-scope narrowing, evidence-as-authority rejection, and recovery without model-private state.
6. Promote this note to an RFC only if those integrations reveal a durable organization-level contract that cannot remain repository-local.

## Failure modes to test

- prompt/transcript treated as canonical mutable state;
- stale task revision reused after a material change;
- runtime working state implicitly persisted or promoted;
- complete transcript required for crash recovery;
- caller-supplied run/actor label accepted as authenticated identity;
- specialist inherits unrelated parent context or authority;
- evidence/receipt mistaken for executable authority;
- runtime self-description accepted as governance truth;
- provider/runtime changes require schema changes because the contract encoded private reasoning details.

## Relationship to RFC 0001

RFC 0001, *Governed agent actuation*, remains focused on the transition from proposed intent to authorized, verifiable effects. This note is complementary: it clarifies which state and identity boundaries should exist before and around that actuation path.

If promoted later, this work should either amend RFC 0001 narrowly or become a separate RFC only when the interoperability surface is concrete enough to justify normative organization-level ownership.

## Non-goals

- Standardizing hidden-state or latent-state formats.
- Requiring BDH-CQ or any specific model/runtime architecture.
- Defining one shared Micrantha database schema.
- Moving repository-local implementation authority into the meta repository.
- Publishing private runtime locations or sensitive operational details.
