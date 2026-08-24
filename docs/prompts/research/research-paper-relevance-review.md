# Research Paper Relevance Review

Use this prompt to evaluate a paper, preprint, technical report, benchmark paper, or academic result for concrete relevance to Micrantha projects.

The goal is not to summarize the paper exhaustively. The goal is to determine what is credible, what is materially relevant, what changes the engineering model, and what—if anything—should happen next.

Apply the shared execution, ambiguity, priority, and artifact-selection contracts from [`../README.md`](../README.md).

## Invocation

```markdown
Review this research paper for Micrantha relevance.

Paper/source: <URL, identifier, PDF, citation, or uploaded file>
Repositories/projects in scope: <optional; infer from authoritative Micrantha metadata when omitted>
Current question or motivation: <optional>

Produce an evidence-backed assessment that separates the paper's claims from demonstrated evidence, maps materially relevant findings to Micrantha projects, identifies gaps against current implementation and accepted design, and recommends only actions justified by the evidence.

Do not create or modify repository state unless mutations are explicitly authorized.
```

## Required review method

### 1. Establish the paper and evidence quality

Identify:

- title, authors, publication/preprint venue, date, and stable identifier;
- problem statement and claimed contribution;
- methodology, datasets, benchmarks, systems, or experiments used;
- baselines and comparison conditions;
- key assumptions and threat/trust model where relevant;
- evaluation limitations, external-validity risks, missing controls, and conflicts between claims and evidence;
- whether important conclusions are replicated, benchmark-only, simulated, synthetic, prototype-only, or production-observed.

Do not treat peer review, citation count, benchmark wins, or author reputation as substitutes for inspecting the evidence.

For each major conclusion, classify confidence as:

- **high** — directly supported by strong, relevant evidence;
- **medium** — plausible and supported, but constrained by methodology or transfer risk;
- **low** — speculative, weakly evaluated, or dependent on assumptions that do not map cleanly to Micrantha.

### 2. Extract decision-relevant takeaways

Separate:

- findings that materially alter an engineering or security mental model;
- findings that validate an existing Micrantha direction;
- findings that challenge an existing assumption or design;
- useful mechanisms, evaluation methods, metrics, datasets, or testing techniques;
- interesting observations with no current engineering consequence.

Prefer a small number of high-signal takeaways. Do not manufacture implications merely to populate every category.

### 3. Build a Micrantha relevance matrix

Inspect authoritative project metadata, repository docs, accepted ADRs/specifications, open issues, and implementation evidence as needed.

For each plausibly affected repository or project, report:

| Project/repository | Relevance | Why | Existing coverage | Gap or opportunity | Confidence |
| --- | --- | --- | --- | --- | --- |

Use relevance levels:

- **direct** — the paper affects a current capability, contract, threat surface, architecture choice, or planned milestone;
- **adjacent** — useful to evaluation, design, or future extension but does not presently require change;
- **none** — no meaningful present connection.

Explicitly include `none` when appropriate rather than forcing cross-project applicability.

### 4. Analyze architecture and security implications

Where relevant, examine effects on:

- authority, capability, identity, authentication, authorization, and delegation boundaries;
- policy evaluation and enforcement points;
- provenance, evidence, auditability, accountability, and replay/reconstruction;
- sandboxing, isolation, state management, runtime boundaries, and failure containment;
- supervisor/specialist orchestration and provider/tool boundaries;
- model/tool input trust, prompt injection, confused-deputy, ambient authority, and data exfiltration risks;
- deterministic versus probabilistic controls;
- CLI/process contracts, Unix composability, API/transport contracts, or shared domain semantics;
- observability, incident response, recovery, and governance requirements;
- performance, cost, latency, availability, or operational complexity where material.

Distinguish a new invariant or contract requirement from an implementation technique. Prefer durable semantic contracts over coupling Micrantha directly to a paper-specific mechanism.

### 5. Perform gap analysis against current state

For each material takeaway, determine whether Micrantha already:

- implements the behavior;
- plans it in an accepted issue/RFC/ADR;
- partially covers it but lacks enforcement or evidence;
- contradicts it intentionally for documented reasons;
- has no corresponding capability or decision.

Do not create duplicate work. Reuse or amend existing issues and authoritative artifacts when they already own the outcome.

When implementation evidence disagrees with backlog or documentation, report the inconsistency before recommending new work.

### 6. Classify actions

Classify each candidate action as exactly one of:

- **adopt** — evidence is strong enough and fit is clear enough to change implementation, contract, or accepted design;
- **experiment** — potentially valuable, but requires a bounded spike, benchmark, prototype, threat-model exercise, or validation step;
- **document** — primarily changes rationale, architecture notes, threat models, standards, or public/internal explanation;
- **monitor** — relevant but premature, insufficiently validated, or blocked on ecosystem maturity;
- **reject/defer** — weak evidence, poor fit, excessive cost, architectural conflict, or no current need.

For every `adopt` or `experiment` recommendation, state:

- expected outcome;
- repository owner;
- acceptance or success criterion;
- important non-goals;
- dependency or blocker, if any;
- confidence and implementation cost/risk.

### 7. Route work to the authoritative repository

For cross-repository findings:

1. identify the authoritative owner of the contract, policy, protocol, or capability;
2. place shared semantics there;
3. put integration work in consuming repositories only when they have independently testable outcomes;
4. avoid duplicating normative text across repositories;
5. identify whether a meta-repository, community/specification repository, runtime repository, or implementation repository should own the artifact.

If repository ownership itself is unclear or contested, recommend the [Cross-Repository Boundary Review](../architecture/cross-repository-boundaries.md) before creating implementation work.

### 8. Select the smallest responsible artifacts

Use the library's artifact-selection rules. In particular:

- use a **spike/experiment** when feasibility or transferability is unknown;
- use **QART** when alternatives and trade-offs remain unresolved;
- use an **RFC** when a consequential proposal needs broad or cross-boundary review;
- use an **ADR** only when the decision is already sufficiently understood;
- use a **security review/threat model** for changed threats or controls;
- use a **specification/contract change** for normative behavior;
- use an **implementation issue** for a bounded observable outcome.

Do not generate one issue per paper takeaway. Consolidate related work by outcome and repository ownership.

### 9. Prioritize without overstating publication importance

Assess action priority using Micrantha's shared P0–P3 model. Publication novelty or academic prominence does not itself raise priority.

Consider:

- evidence strength;
- relevance to current milestones;
- security or correctness impact;
- whether the finding exposes a broken invariant or missing control;
- implementation cost and dependency ordering;
- reversibility and experimentation cost;
- overlap with existing planned work.

A strong paper with low current project relevance may correctly result in `monitor` or P3. A modest paper exposing a concrete current security gap may justify P1 or, exceptionally, P0.

## Required output

### Executive assessment

Provide:

- the paper's core contribution in 2–4 sentences;
- overall evidence quality;
- overall Micrantha relevance;
- the most important engineering consequence, if any;
- a concise recommendation: act now, experiment, document, monitor, or no action.

### Evidence and limitations

| Claim/finding | Evidence | Limitations / transfer risk | Confidence |
| --- | --- | --- | --- |

### Key takeaways

List only decision-relevant takeaways, each with a short explanation of why it matters or why it does not.

### Micrantha relevance matrix

Use the project/repository relevance table defined above.

### Architecture and security implications

Describe changed invariants, contracts, threat surfaces, runtime boundaries, or evaluation requirements. State explicitly when the paper does not justify an architectural change.

### Current-state gap analysis

For each material implication, report current implementation/design evidence and whether the result is already covered, partially covered, planned, intentionally divergent, or genuinely missing.

### Recommended actions

| Action | Classification | Owner | Outcome / success criterion | Priority | Confidence | Cost/risk |
| --- | --- | --- | --- | --- | --- | --- |

### Artifact routing

Identify issue, spike, QART, RFC, ADR, specification, documentation, security-review, or no-artifact outcomes. Consolidate aggressively.

### Final recommendation

End with three explicit buckets:

- **Do now** — only work justified for the current execution queue;
- **Do later / monitor** — worthwhile but not current execution work;
- **Do not pursue** — findings that are interesting but not sufficiently useful, supported, or aligned.

If no repository mutations are authorized, provide issue/doc-ready recommendations without making changes. If mutations are explicitly authorized, preserve this review as the rationale baseline and apply only the bounded approved actions.

## Follow-on prompt routing

When the paper exposes broader uncertainty, invoke the appropriate existing prompt rather than expanding this review indefinitely:

- broad repository mismatch or stale backlog → [Comprehensive Project Status Review](../project-review/comprehensive-status-review.md);
- existing baseline and incremental changes → [Project Status Refresh](../project-review/status-refresh.md);
- cross-repository ownership ambiguity → [Cross-Repository Boundary Review](../architecture/cross-repository-boundaries.md);
- agent/tool authority or security implications → [Agentic Workflow Security Review](../security/agentic-workflow-security-review.md);
- unresolved alternatives → [QART Decision Analysis](../decisions/qart-analysis.md);
- consequential proposal needing review → [RFC Development](../decisions/rfc-development.md);
- implementation work needing issue form → [Issue Grooming](../issues/issue-grooming.md).
