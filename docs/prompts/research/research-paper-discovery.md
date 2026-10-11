# Research Paper Discovery

Use this prompt to discover, triage, and queue external research that is likely to change, challenge, validate, simplify, or provide useful evaluation methods for current Micrantha projects.

The goal is not to collect papers broadly. The goal is to maximize **decision-relevant information gain** while avoiding duplicate, low-signal, or already-covered work.

Apply the shared execution, ambiguity, priority, and artifact-selection contracts from [`../README.md`](../README.md).

## Invocation

```markdown
Discover research papers relevant to Micrantha.

Current portfolio scope: <optional; infer from canonical registry when omitted>
Time horizon: <optional; default to recent work plus older foundational gaps>
Research themes or questions: <optional>
Tracker / reading queue: <optional; use current canonical tracker when available>

Find papers likely to materially affect architecture, security, governance, runtime, evaluation, tooling, or roadmap. Deduplicate against already tracked/reviewed work, score candidates by expected information gain and current project relevance, identify uncovered research questions, and produce a prioritized reading queue.

Do not create or modify repository state unless mutations are explicitly authorized.
```

## Required discovery method

### 1. Establish current portfolio state

Before searching, inspect enough authoritative Micrantha state to know what research questions matter now:

- canonical project registry and project relationships;
- active architecture/security/runtime issues and accepted RFC/ADR/spec direction;
- current research tracker and reviewed-paper conclusions;
- current execution priorities and unresolved cross-project questions.

Do not search from generic agent keywords alone.

### 2. Build research questions from current architecture

Derive explicit research questions that could:

- falsify or challenge a current assumption;
- expose a broken or incomplete security invariant;
- validate or simplify an existing architecture;
- supply a missing evaluation method, benchmark, or control;
- reveal a new failure mode or trust-boundary problem;
- materially change implementation order or priority.

Consider, where relevant:

- agent harness/runtime architecture;
- authority, capability, identity, authentication, authorization, and delegation;
- effect identity, retries, reconciliation, and exactly-once behavior;
- memory, retrieval, persistence, poisoning, promotion, and state recovery;
- independent verification, evidence integrity, auditability, provenance, and trace capture;
- prompt injection, confused deputy, cross-agent influence, and adversarial tool use;
- sandboxing, isolation, execution containment, and boundary escape;
- model/harness/provider supply chain and artifact integrity;
- recursive/self-improving agents and candidate-promotion discipline;
- autonomous software engineering and secure-SDLC evaluation;
- inference/runtime efficiency relevant to local-first systems;
- observability, incident response, rollback, and long-running workflows.

### 3. Search multiple fronts

Use primary research sources where possible. Search broadly enough to cover:

- recent arXiv/preprints;
- peer-reviewed venues;
- relevant technical reports from credible research/security organizations;
- benchmark or systems papers with strong empirical evidence;
- older foundational work only when it fills a current tracker gap.

Prefer primary sources over summaries.

### 4. Deduplicate by research question, not just title

For each candidate, compare against the existing tracker by:

- stable identifier / DOI / arXiv ID;
- title and authors;
- core mechanism or contribution;
- research question already covered;
- existing project integration already justified.

Reject or downgrade papers that merely repeat evidence already well represented unless they provide stronger methodology, contradictory findings, or materially broader external validity.

### 5. Score expected information gain

Use a compact 1-5 score for:

- **Portfolio relevance** — likelihood of affecting a current Micrantha project or invariant;
- **Novelty** — new mechanism, failure mode, or evaluation method relative to tracked work;
- **Evidence strength** — methodology, controls, baselines, realism, sample size, replication quality;
- **Security/correctness impact** — consequence if the finding is true;
- **Actionability** — ability to turn the result into a concrete experiment, contract, threat-model, or implementation decision;
- **Redundancy penalty** — overlap with already-reviewed work.

Compute an overall priority from the above, but do not let a numeric score override clear architectural importance.

### 6. Prefer decision-changing papers

Promote papers that could plausibly:

- reveal a broken invariant;
- challenge an accepted design;
- expose an unmodeled trust boundary;
- provide a missing negative/control experiment;
- justify removing or simplifying machinery;
- justify adding a bounded experiment;
- change what must be measured or independently verified.

A popular or highly cited paper with no likely project consequence may remain low priority.

### 7. Identify research-coverage gaps

Before finalizing the queue, ask:

> What important research question implied by the current Micrantha architecture has no adequate paper in the tracker?

Produce explicit gap searches for uncovered questions.

Examples may include:

- execution attestation / independent effect observation;
- capability/delegation composition and revocation;
- audit-log completeness vs integrity;
- memory poisoning and retrieval-triggered persistence;
- multi-agent collusion or cross-agent confused deputy;
- sandbox containment for tool-using agents;
- supply-chain compromise of model/harness artifacts;
- changing authority/environment state during evaluation;
- reconciliation after ambiguous external effects.

Do not assume these examples remain gaps; verify against the current tracker.

### 8. Triage candidates

Classify each discovered candidate as exactly one of:

- **Read Now** — high expected information gain for current work;
- **Skim** — useful architecture/evaluation context, but unlikely to alter current priorities;
- **Watch** — promising but premature, weakly evaluated, or dependent on unavailable ecosystem support;
- **Reject / redundant** — already covered, weak evidence, poor fit, or no plausible current project consequence.

For every rejected candidate, give a short reason.

### 9. Queue conservatively

A discovery pass should produce a **small, ranked queue**, not an exhaustive bibliography.

Default target:

- 3-7 `Read Now`;
- 0-5 `Skim`;
- a small `Watch` set only when useful;
- record notable rejected/redundant candidates separately rather than crowding the queue.

When a tracker exists, do not add duplicates and do not leave stale reviewed items in the reading queue.

### 10. Route follow-up correctly

Discovery identifies what to read; it does not perform the full relevance review.

For each queued paper, record:

- stable source;
- why it matters;
- likely projects/questions affected;
- expected information gain;
- recommendation and priority.

When the paper reaches the front of the queue, use [Research Paper Relevance Review](research-paper-relevance-review.md).

## Required output

### Discovery thesis

State the current research questions driving the search and the largest uncovered evidence gaps.

### Candidate shortlist

| Paper | Stable source | Research question | Likely project relevance | Expected information gain | Evidence signal | Redundancy | Triage |
| --- | --- | --- | --- | --- | --- | --- | --- |

### Recommended reading queue

Rank only the papers worth reading next.

For each, include:

- why now;
- what result could change a Micrantha decision;
- likely owner projects;
- priority.

### Rejected / redundant candidates

Include only notable exclusions and a short reason.

### Coverage gaps

List research questions that remain insufficiently covered after discovery.

### Tracker changes

If mutations are authorized, update the canonical Papers and Reading Queue artifacts, preserving exact source identifiers and deduplication. Do not mark a paper Reviewed during discovery.

## Follow-on routing

- chosen paper -> [Research Paper Relevance Review](research-paper-relevance-review.md);
- broad architectural mismatch -> project review / architecture prompts;
- changed agent/tool threat boundary -> Agentic Workflow Security Review;
- unresolved design alternatives -> QART;
- strong implementation implication -> smallest responsible issue/spike/RFC after paper review.
