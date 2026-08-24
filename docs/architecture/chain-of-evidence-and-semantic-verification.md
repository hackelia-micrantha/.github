# Chain of Evidence and Semantic Verification

## Status

Architecture guidance supporting RFC-0001 (Governed Agent Evolution).

This note incorporates engineering lessons from **SWE-bench Science: Can Coding Agents Resolve Engineering Tasks in Science?** (arXiv:2608.19799, 2026-08-20) without making the benchmark or its scientific domain model a Micrantha dependency.

## Why this matters

SWE-bench Science evaluates 119 repository-level tasks from 98 GitHub repositories across 20 scientific domains. It separates agent-visible public diagnostics from evaluator-only private tests and applies submitted patches to a clean verifier baseline. The strongest reported configuration reaches 47.90% exact Pass@1 while scoring 96.64% on public checks.

The useful architectural signal is not the leaderboard. It is the gap between **locally visible success** and **complete preservation of the intended contract**.

The paper also identifies four recurring failure mechanisms:

1. knowledge or abstraction deficits;
2. misguided exploration or surface-level repair;
3. incomplete repair coverage or system integration;
4. failure to generalize beyond observed cases.

A paired ablation further shows that additional domain guidance is not uniformly beneficial. Guidance can reduce exploration cost, but it can also induce anchoring, scope spillover, or premature reliance on a supplied explanation. The paper therefore emphasizes executable evidence and independent validation.

Micrantha should treat these findings as evidence for stronger verification boundaries around autonomous engineering, not as a requirement to hide all policy or tests from agents.

## Core invariants

### 1. Producer evidence is not promotion evidence

An agent or executor MAY run diagnostics and produce evidence about its own candidate. That evidence MUST NOT be sufficient, by self-assertion alone, to establish that the candidate satisfies the complete governed contract.

For risk classes that require independent verification:

```text
producer(candidate) != authoritative verifier(candidate)
```

The stronger requirement is trust-domain separation, not merely different process names:

```text
trust_domain(producer) != trust_domain(verifier)
```

where the deployment can actually support that separation.

Verifier output remains evidence. Anthesis policy/approval remains the authority that decides whether the evidence is sufficient for a governed transition or external effect.

### 2. Context and knowledge are inputs, not authority

Retrieved memory, prompts, documentation, expert guidance, model-generated analysis, and prior successful runs can constrain investigation, but they are not executable proof.

```text
context != evidence
retrieval != verification
memory != authority
```

A material claim derived from retrieved guidance SHOULD be validated against repository/runtime evidence before it is used to justify a high-impact transition.

This rule is particularly important for governed agent evolution: a system's accumulated experience can improve decisions, but it can also anchor future investigation on stale or misapplied explanations.

### 3. Verification targets semantic invariants, not only commands

A governed task SHOULD identify the behavioral, security, compatibility, or operational invariants that matter, independently of any particular test command.

Examples include:

- an authorization invariant remains true across alternate request paths;
- a state reset produces an equivalent valid outcome;
- ordering changes do not change a commutative result;
- a boundary value does not bypass a validation rule;
- a multi-module capability chain remains complete;
- an existing supported behavior does not regress while a defect is repaired.

Test commands and tools are execution mechanisms. They do not define the entire semantic contract by themselves.

### 4. Agent-visible checks and authoritative verification are separate concerns

Agents SHOULD have enough observable diagnostics to investigate and repair problems efficiently. High-assurance verification MAY additionally use evaluator-only material that the producer cannot mutate or inspect before candidate commitment.

This is an information-flow and oracle-integrity boundary, not a recommendation for secret governance.

Policy SHOULD normally be explainable to the governed actor. What must remain protected is the integrity of the authoritative evaluator, its credentials, its immutable fixtures where necessary, and its evidence path.

### 5. Verification runs from a clean, attributable baseline

Where practical, authoritative verification SHOULD run against:

- the exact submitted candidate identity;
- a clean/frozen baseline or reproducible environment;
- independently resolved verifier configuration;
- evaluator material unavailable for producer mutation;
- explicit environment and tool identities;
- append-only or attributable result evidence.

A verifier that simply reuses arbitrary mutable producer workspace state cannot claim strong independence.

### 6. Generalization requires deliberate perturbation

For non-trivial tasks, verification SHOULD include strategies selected from the risk model rather than merely repeating the producer's visible test cases.

Candidate strategies include:

- boundary cases;
- metamorphic/property-preserving transformations;
- state-reset/restart scenarios;
- alternate execution paths;
- ordering/representation variants;
- cross-module/integration checks;
- regression-preservation checks;
- adversarial or abuse cases.

Testule owns the portable specification of these testability requirements and normalized evidence. Native testing tools remain authoritative for execution.

### 7. Task class can inform routing, but must not mint authority

Host/orchestrator logic MAY classify work such as:

```text
localized-repair
exploratory-diagnosis
integration
security-review
verification
```

The classification can inform model routing, specialist selection, budgets, and required evidence. It is a trusted host/task fact, not a capability grant and not a value that the untrusted agent can widen by self-assertion.

### 8. Reserve verification resources explicitly

Long-running agents can consume most available time/tokens/compute before reaching validation. Orchestration SHOULD support reserving enough budget for required verification rather than treating verification as best-effort residual work.

The concrete budget contract remains owned by the existing Anthesis/Dubnium/Plano path. Modolia remains a deterministic route resolver and must not become a runtime budget authority.

## Reference flow

```text
Task / objective
    |
    +--> exact source + environment baseline
    +--> declared invariants / required evidence
    +--> bounded context / retrieved knowledge
    |
    v
Executor workspace
    |
    +--> public diagnostics / self-checks
    +--> candidate artifact
    |
    v
Candidate commitment
    |
    v
Independent verifier workspace
    |
    +--> clean baseline
    +--> exact candidate
    +--> protected evaluator inputs where required
    +--> boundary / metamorphic / integration / regression checks
    |
    v
Verifier evidence
    |
    v
Anthesis policy / approval
    |
    +--> retain / promote / activate
    +--> reject / rework
    +--> escalate / require human approval
```

The flow intentionally separates **evaluation** from **authorization**. A perfect verifier result does not grant deployment, merge, publication, or capability authority by itself.

## Responsibility mapping

| Component | Responsibility in this pattern | Explicit non-responsibility |
| --- | --- | --- |
| Anthesis | Evidence requirements, semantic policy interpretation, approval/decision, provenance | Executing tests or owning workspaces |
| Dubnium | Bounded agent-run lifecycle, candidate commitment, runtime isolation, invoking verifier stages, resource enforcement | Deciding semantic policy locally |
| Testule | Portable testability contracts, invariant/oracle strategies, environment requirements, normalized verification evidence | Replacing native test frameworks or governance |
| Sandcastle | Persistent checkpoint identity/lineage for mutable execution state and reproducible forks/restores | Claiming isolation or semantic correctness |
| Keylix | Sender-constrained executor/verifier workload identity at protected network boundaries | Task correctness or evidence sufficiency |
| Invokrum | Exact/versionable context composition and context drift evidence | Treating prompt/context integrity as semantic approval |
| Modolia | Deterministic model-surface eligibility and route decision | Runtime provider behavior, budgets, or correctness |
| Plano/Dubnium integration | Runtime provider routing, retries/fallback, runtime budget mechanics as defined by host contracts | Widening Modolia constraints or Anthesis authority |
| governed-agent-evolution lab | Deterministic conformance scenarios that compose the contracts | Production authority or a new canonical protocol |

## Evidence shape

Do not create a new universal schema solely for this note. Existing component contracts should compose fields equivalent to:

```yaml
verification:
  subject:
    base_revision: ...
    candidate_revision: ...
    context_identity: ...
  producer:
    workload_identity: ...
  verifier:
    workload_identity: ...
    build_identity: ...
    environment_identity: ...
  requirements:
    plan_ref: ...
    invariant_refs: []
  observations:
    evidence_refs: []
    failed_requirements: []
    indeterminate_requirements: []
  provenance:
    policy_ref: ...
    source_refs: []
```

The important property is attributable separation and exact subject binding, not this example field layout.

## Required conformance scenarios

Cross-project conformance should eventually cover at least:

1. producer-visible checks pass but an independent generalization case fails;
2. producer attempts to modify evaluator-only material after candidate commitment;
3. verifier accidentally runs against producer-mutated workspace state rather than the committed candidate;
4. verifier identity is self-asserted by the executor;
5. verifier returns success but Anthesis approval is missing;
6. retrieved guidance suggests an incorrect repair and executable evidence contradicts it;
7. candidate changes after verifier evidence is emitted;
8. integration repair fixes one module while breaking a dependent module;
9. reset/restart changes behavior that appeared correct in a warm workspace;
10. required verification cannot run because capability or budget is unavailable and the result becomes `indeterminate`/fail-closed rather than silently passing.

## Relationship to RFC-0001

RFC-0001's core invariant remains authoritative:

> An evolving system may propose its successor, but it must not independently authorize the transition that gives that successor effect.

This note strengthens the evidence side of that rule:

> A mutable producer may inspect and evaluate its own candidate, but high-assurance promotion must be able to require evidence produced through an independently controlled verification path bound to the exact candidate.

For governed evolution, an additional knowledge rule applies:

> Prior memory, retrieved guidance, or successful generations may inform a candidate but cannot substitute for executable evidence required by policy.

## Non-goals

- Hide Anthesis policy from agents as a security mechanism.
- Require private tests for every project or every risk level.
- Require a separate physical machine for every verification step.
- Treat different process names or different model providers as sufficient independence under a shared compromised root.
- Make Keylix responsible for test-oracle secrecy.
- Make Sandcastle responsible for runtime isolation.
- Make Testule an authorization engine.
- Make Modolia or Plano determine business correctness.
- Capture or require model-private chain-of-thought.

## Source

- Zhipeng Xu, Jiahao Lu, Yining Zheng, Yuxin Wang, Xipeng Qiu. **SWE-bench Science: Can Coding Agents Resolve Engineering Tasks in Science?** arXiv:2608.19799v1, 2026-08-20. https://arxiv.org/abs/2608.19799
