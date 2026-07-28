# Prompt: QART analysis

```text
Analyze the supplied design or planning problem using QART: Questions, Alternatives, Recommendations, and Trade-offs.

The goal is to improve decision quality before producing RFCs, ADRs, plans, or implementation issues.

## Decomposition

1. Identify each independently decidable question.
2. Split questions when they have different decision owners, evidence requirements, reversibility, trust boundaries, or delivery consequences.
3. Do not embed a preferred implementation in the wording of a question.
4. Identify questions that require a spike or evidence gathering before a recommendation is responsible.

## For each QART slice

### Question
State one neutral and bounded decision question.

### Context
Summarize the current state, trigger, relevant prior decisions, and why the decision matters now.

### Decision drivers
Rank the material criteria, including where relevant:
- security and trust boundaries;
- reliability and recovery;
- operability and observability;
- compatibility and migration;
- maintainability;
- performance and capacity;
- cost and delivery effort;
- governance and auditability;
- reversibility.

### Constraints and assumptions
Separate established constraints from assumptions that need validation.

### Alternatives
Include:
- the proposed approach;
- at least one credible alternative;
- the current-state or defer option when viable.

For each alternative analyze:
- mechanism and boundaries;
- advantages;
- disadvantages;
- security and governance impact;
- failure modes;
- operational impact;
- compatibility and migration impact;
- delivery complexity;
- long-term maintenance;
- reversibility;
- evidence required.

### Comparison
Provide a concise decision matrix. Do not use numeric scoring unless the weights and evidence justify it.

### Recommendation
Recommend an option only when supported by available evidence. State confidence and assumptions.

### Trade-offs
Identify:
- accepted trade-offs;
- rejected trade-offs;
- residual risks;
- mitigation requirements;
- revisit triggers.

### Decision path
State whether the slice is:
- ready for decision;
- blocked on evidence;
- part of an RFC;
- ready to become an ADR after acceptance;
- local and reversible enough to remain an implementation choice.

## Final synthesis

Produce:
1. QART slice inventory
2. Dependency order between decisions
3. Recommended RFC boundary, if any
4. ADR candidates, clearly marked as undecided or accepted
5. Delivery implications
6. Missing evidence and proposed spikes

Do not write an ADR as though a recommendation has already been accepted.

Source material:
<PASTE DESIGN PROBLEM, NOTES, OR DISCUSSION HERE>
```
