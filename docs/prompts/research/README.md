# Research prompts

These prompts translate external research into evidence-backed Micrantha engineering decisions without treating publication claims as implementation requirements.

See the [complete engineering prompt library](../README.md) for project review, planning, architecture, security, decision, issue, and delivery workflows that may follow from a research review.

## Choose a prompt

| Prompt | Use when | Expected output |
| --- | --- | --- |
| [Research paper relevance review](research-paper-relevance-review.md) | A paper, preprint, technical report, or academic result may affect Micrantha architecture, security, governance, runtime, tooling, or roadmap | Evidence assessment, key takeaways, project relevance matrix, gap analysis, action classification, repository ownership, and prioritized recommendations |

## Operating model

Research is **external evidence**, not project authority. A paper can motivate investigation, experiments, threat-model updates, or engineering work, but it does not override accepted Micrantha specifications, ADRs, security invariants, repository ownership, or implementation evidence.

Use the shared ambiguity and agent-execution contracts in [`../README.md`](../README.md). Reviews are read-only by default. Creating or modifying issues, RFCs, ADRs, documentation, experiments, or implementation requires explicit mutation authorization.

## Recommended workflow

1. Inspect the primary paper and distinguish claims from demonstrated evidence.
2. Extract only the findings that could materially affect Micrantha.
3. Map those findings to concrete repositories, contracts, threat surfaces, or capabilities.
4. Compare the paper against existing implementation and accepted design evidence before declaring a gap.
5. Classify candidate actions as `adopt`, `experiment`, `document`, `monitor`, or `reject/defer`.
6. Route consequential uncertainty to the smallest responsible artifact: spike, QART, RFC, ADR, threat model, specification change, or implementation issue.
7. Run the relevant project-review or security prompt when a paper implies broader repository reconciliation.

## Scope controls

A useful invocation should identify the paper or stable source, the repositories or ecosystem area of interest when known, and any current architectural or security question that motivated the review. When scope is omitted, derive likely relevance from authoritative Micrantha metadata and report repositories with no meaningful relevance explicitly rather than forcing connections.
