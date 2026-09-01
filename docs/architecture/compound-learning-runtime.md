# Compound learning runtime boundaries

This document maps the Micrantha **Plan -> Work -> Review -> Compound -> Repeat** practice onto the runtime and governance components that participate in durable engineering learning.

It complements:

- `docs/engineering/compound-engineering.md`;
- `docs/architecture/governed-learning-promotion.md`;
- `docs/prompts/reviews/compound-review.md`.

The central design rule is:

> No single component both observes a lesson and silently turns that lesson into future authority.

## Component model

```text
Scheduler / explicit completion trigger
        |
        v
Supervisor / workflow executor
        |
        +--> Run Ledger / exact evidence
        +--> Memory / historical observations
        |
        v
candidate learning (non-authoritative)
        |
        +--> deterministic control: test / schema / invariant / CI
        |
        +--> Invokrum candidate pack / overlay / lock
        |
        +--> tool/default change
        |
        +--> policy proposal
        |
        v
Sandcastle / Testule / native validation as required
        |
        v
Anthesis or ordinary repository authority
        |
        v
versioned promoted artifact
        |
        +--> Invokrum exact lock for trusted guidance
        +--> repository revision for tests/docs/tools
        +--> Anthesis policy revision where applicable
        |
        v
future run records exact promoted revision
```

## Supervisor

The Supervisor is the primary reasoning and routing participant in Compound.

It may:

- inspect a completed run and accepted review outcome;
- identify repeated findings, failures, successful patterns, or recurring manual intervention;
- classify whether the best durable target is a test, invariant, guidance change, documentation, tooling change, policy proposal, or measurement;
- emit zero or more bounded candidate-learning records;
- request validation through existing execution/evaluation mechanisms.

It must not:

- directly rewrite trusted prompts or policy because it observed a useful lesson;
- infer effective authority from repository, model, memory, tool, or review prose;
- mark its own candidate promoted;
- bypass ordinary repository or Anthesis promotion authority.

A valid terminal Compound result is `no reusable learning`.

## Run Ledger

The Run Ledger is the durable attribution backbone.

It should make relationships such as the following reconstructable without storing full transcripts:

```text
run R14
  -> review finding F7
  -> candidate learning L3
  -> validation V9
  -> promoted artifact P2 / revision G17
  -> future run R31 consumed G17
  -> later equivalent finding prevented or recurred
```

The Run Ledger owns exact run/task/candidate/evidence identity and lifecycle facts. It does not own semantic promotion authority.

Candidate-learning state should extend existing Dubnium run/evidence records rather than create another ledger.

## Memory

Memory has two distinct roles that must remain distinguishable.

### Historical observation memory

Examples:

- previous failures and fixes;
- review findings;
- earlier candidate learnings;
- operational incidents;
- prior solution references.

This content is contextual evidence and is untrusted for instruction authority.

### Current promoted-reference memory

Memory may index or retrieve references to current promoted artifacts, for example:

- exact Invokrum pack/lock revisions;
- accepted architecture decisions;
- current test/invariant identifiers;
- current documentation or runbook revisions;
- current Anthesis policy revisions where appropriate.

Retrieval does not make an artifact current. Current/superseded/revoked state comes from the owning authoritative source.

The memory layer must preserve enough provenance to distinguish:

```text
historical observation
!=
promoted current guidance
!=
policy/effect authority
```

A memory record may suggest that a prior lesson exists. It cannot promote, resurrect, or widen it.

## Memory steward

A memory-steward process may perform bounded maintenance such as:

- duplicate/near-duplicate candidate detection;
- recurrence clustering;
- stale-reference detection;
- supersession-link proposals;
- consolidation proposals;
- retrieval-quality maintenance.

Those actions remain proposals or index maintenance. The steward must not turn retrieval order, semantic similarity, frequency, or confidence into promotion authority.

## Scheduler and governed workflows

The scheduler owns **when** a Compound workflow runs, not **what learning is valid**.

Useful triggers include:

- immediately after a meaningful reviewed/terminal engineering run;
- after an incident or repeated failed verification;
- a deferred re-evaluation when more evidence is required;
- a periodic engineering-hygiene scan for repeated findings, stale promoted references, or candidates that remain unvalidated.

Scheduled Compound work should use the normal workflow executor, evidence, memory, Supervisor, and policy paths. The scheduler must not embed prompts, interpret candidate semantics, or promote artifacts itself.

## Invokrum

Invokrum is the preferred deterministic packaging and identity layer when a compounded learning changes reusable agent prompt/context guidance.

The distinction is:

```text
Memory: what has been observed before?
Invokrum: what exact composed guidance/context package is this invocation using?
```

A prompt/guidance candidate should be able to flow as:

```text
candidate learning
  -> candidate Invokrum overlay / pack change
  -> deterministic composition
  -> exact lock digest
  -> representative + adversarial evaluation
  -> ordinary/Anthesis-governed promotion as required
  -> promoted pack/lock revision
  -> future Dubnium invocation records exact lock
```

Invokrum owns deterministic prompt/context composition, lock identity, compatibility, and attestation semantics. It does not decide that a candidate is authorized to become trusted guidance.

A successful or frequently retrieved candidate must not be automatically inserted into a trusted pack.

## Sandcastle

Sandcastle provides exact state mechanics for stronger evaluation.

Useful Compound applications include:

- freeze the exact candidate prompt/tool/code state;
- restore a known historical failure baseline;
- materialize hostile/adversarial fixture state;
- run a fresh verifier against an immutable candidate;
- prove candidate identity did not change between evaluation and disposition;
- preserve checkpoint lineage for stale-state and TOCTOU reasoning.

Sandcastle checkpoint existence or integrity is evidence. It is not semantic correctness, task completion, or promotion authority.

Existing Sandcastle checkpoint/verifier/hostile-state work should be reused before creating Compound-specific checkpoint abstractions.

## Anthesis

Anthesis governs promotion when the target changes trusted persistent control or governance-relevant state.

It may require, depending on target class:

- exact candidate and target revision binding;
- representative or adversarial validation;
- accountable approval;
- policy revision identity;
- supersession/revocation lineage;
- effect-time freshness/revalidation.

Anthesis does not become the memory system, prompt composer, scheduler, or Run Ledger.

## Events and observability

Events may project Compound lifecycle facts for observability and later analysis, for example:

```text
engineering.learning.proposed
engineering.learning.validated
engineering.learning.rejected
engineering.learning.promoted
engineering.learning.superseded
engineering.finding.recurred
engineering.finding.prevented
```

These are projections of authoritative component state. The event stream is not the candidate ledger or promotion authority.

## Durable-target routing

| Finding type | Preferred durable target | Primary owner |
| --- | --- | --- |
| deterministic defect | test / invariant / schema / CI | owning repository |
| repeated review ambiguity | shared guidance or prompt overlay | `.github` + Invokrum packaging where applicable |
| missing operator knowledge | docs / runbook / semantic help | owning repository |
| unsafe tool/default behavior | implementation/config change | owning runtime/tool repository |
| authority or policy gap | policy proposal | Anthesis / owning governance contract |
| repeated but not yet preventable pattern | historical candidate + measurement | Run Ledger / Memory; later consumer |

Prefer a deterministic control over a reminder when the behavior is mechanically decidable.

## Security invariants

1. Repository, issue, PR, web, tool, model, and memory content is observation data unless independently established otherwise.
2. Candidate-learning text cannot choose actor identity, credentials, protected destinations, capabilities, approval, or policy revision.
3. Memory retrieval order or frequency cannot decide which guidance is current.
4. Invokrum lock identity proves exact composition, not authorization or correctness.
5. Sandcastle checkpoint identity proves exact state, not semantic validity or authority.
6. Scheduler timing cannot bypass validation or promotion authority.
7. Events and metrics cannot mint or resurrect authority.
8. Future runs consume exact promoted revisions and record them separately from the observations that originally motivated them.

## Recommended implementation sequence

1. Wire the shared Compound review prompt into Micrantha workflow discovery.
2. Extend Dubnium run/evidence state with non-authoritative candidate-learning records.
3. Make Dubnium context assembly distinguish historical memory from exact promoted guidance references.
4. Define Invokrum candidate-pack/overlay evaluation and promoted-lock consumption semantics.
5. Define the minimum Anthesis promotion profile for trusted persistent guidance/policy.
6. Reuse Sandcastle/Testule/native verification when the target class needs stronger evaluation.
7. Add optional scheduled recurrence/staleness review after enough runtime evidence exists.
8. Add event/measurement projections only after canonical state is stable.

## Non-goals

- a global self-improving-agent database;
- automatic prompt or policy mutation;
- making Memory the canonical prompt store;
- making Invokrum a governance engine;
- making Sandcastle a semantic verifier or workflow service;
- making the scheduler a learning engine;
- treating model self-review as independent promotion evidence;
- storing chain-of-thought or full transcripts as the learning record.
