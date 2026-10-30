# October 2026 research reconciliation: agent memory and software delivery

Status: **research-to-engineering decision note, not an adopted new policy or implementation**. Source: [Engineering Research Tracker](https://docs.google.com/spreadsheets/d/1nRcfGZR__FESRpcGJfMlZqnrl3XyatoSzTMTBqg6qP8/edit), `Papers!247–254` and `Project Integrations!145–151`. This note consolidates findings; repository issues and existing RFCs/ADRs remain authoritative for work and exact contracts.

## Explain it to a human

An agent can remember something accurately and still use it incorrectly: the memory may be stale, private, outside the current task's purpose, already forgotten, or capable of revealing a sensitive fact only when combined with other records. Likewise, generating many code changes does not prove those changes shipped safely or were used. Improve the existing ownership, evidence and tests before adding a memory engine or another AI delivery control plane.

## Architectural boundaries

| Concern | Owning boundary | Existing work |
| --- | --- | --- |
| Stored memory, revisions, provenance, lifecycle and enumerated derived deletion closure | Dubnium Memory API; canonical source owners retain authority | [Dubnium #1283](https://github.com/ryjen/dubnium/issues/1283), [#617](https://github.com/ryjen/dubnium/issues/617) |
| Raw/BM25/embedding/hybrid retrieval and exact eligibility before prompt exposure | Memory API filtering followed by Supervisor Observation ingress | [Dubnium #939](https://github.com/ryjen/dubnium/issues/939), [#898](https://github.com/ryjen/dubnium/issues/898) |
| Cumulative, purpose-bound information exposure across authorized reads and contexts | Anthesis policy/evidence; not inferred from model text | [Anthesis #280](https://github.com/hackelia-micrantha/anthesis/issues/280), [#203](https://github.com/hackelia-micrantha/anthesis/issues/203), [#204](https://github.com/hackelia-micrantha/anthesis/issues/204) |
| Promotion of candidate memories/lessons into trusted guidance | Explicit governed action, not retrieval confidence | [Anthesis #208](https://github.com/hackelia-micrantha/anthesis/issues/208) |
| Independent security/forgetting fixtures and semantic outcome checks | Governance Lab and Testule, distinct from production authority | [Lab #79](https://github.com/ryjen/anthesis-governance-lab/issues/79), [Testule #30](https://github.com/hackelia-micrantha/testule/issues/30) |
| Exact run lineage, budgets, required verification and observed consumer outcome | Dubnium Run Ledger / resource routing, Anthesis envelope, shared meta delivery contracts | [Dubnium #414](https://github.com/ryjen/dubnium/issues/414), [#887](https://github.com/ryjen/dubnium/issues/887), [Anthesis #140](https://github.com/hackelia-micrantha/anthesis/issues/140), [meta #144](https://github.com/hackelia-micrantha/.github/issues/144) |
| Research tracker states and source-keyed advancement | Engineering Research Tracker; no blind ranked queue mutation | [Portfolio #90](https://github.com/hackelia-micrantha/hackelia-micrantha/issues/90) |

The relevant authority distinctions are non-negotiable:

```text
source record and revision
  -> authenticated-scope candidate retrieval
  -> policy/lifecycle admissibility: allow | deny | unresolved
  -> actual model-prompt exposure (log IDs, never payload by default)
  -> task-scoped inference/output
  -> independently verified result
  -> separately authorized consequential effect, if any
```

Retrieved evidence, a citation, a model's refusal, a learned lesson, a prior authorization and an outcome prediction are **not** permissions or evidence that an effect was safely performed.

## Memory evidence reviewed

| Paper | Research signal | Engineering treatment | Limitation |
| --- | --- | --- | --- |
| [Agent Zero Memory](https://arxiv.org/abs/2608.29606) | Hybrid/lexical search over timeline, derived graph and curated documents can improve specific recall tasks. The controlled LongMemEval gpt-5.6-sol configurations compared hybrid 95.2%, embedding-only 94.0%, grep 93.6%, lexical 93.4%. | In #939, compare raw source/BM25/QMD/hybrid at equal scope and budget; verify source was actually opened and claims entailed by it. | External benchmark leaderboards are not shared-harness experiments; no remove-one-store ablation, full indexing/update cost or calibrated citation correctness. |
| [ReFind](https://arxiv.org/abs/2608.12888) | Agent-directed lexical search, session/time ranking and neighboring-turn expansion can rival more elaborate memory stores on chat recall. Six-benchmark mean 58.2 vs reused HippoRAG2 53.2. | Cap multi-search variants and compare the **no-new-store** baseline first. Enforce scope on every expanded neighbor. | About five model calls and 70–100K aggregate tokens per evaluated LongMemEval task; no Dubnium RTX3060 latency/cost proof. |
| [The Right Memory in the Wrong Context](https://arxiv.org/abs/2610.07309) | Relevance differs from **request-conditioned admissibility**. With trusted namespace tags, frozen top-20 required-evidence recall improved .432→.533 across 3,767 queries. | Explicit `allow/deny/unresolved`, separate returned IDs from prompt-exposed IDs, preserve legitimate history and positive recall. | Namespace labels assumed trusted; text-only eligibility verifiers overdeny anchors; output refusal cannot repair prior exposure. |
| [Deployment-Time Memorization](https://arxiv.org/abs/2606.10062) | Raw-only forgetting leaves derived summary recoverability (~19–22% in N=50 deletion study); tested derivative remediation recorded zero exact-canary recovery. | #1283/#79 enumerate Memory-owned raw/summary/index/cache/restore closure, pending/indeterminate status and a benign retained-fact control. | N=50 deletion sample, synthetic exact canaries; zero observed is not semantic, physical, backup or universal erasure. v2 frontier has ~60% reduced extraction, replacing outdated v1 headlines. |
| [MemCut](https://arxiv.org/abs/2610.21405) | A secret may be derivable from **multiple surviving records** after its original and derivatives are deleted. Top-20 candidate cleanup left 39–76% residual success in synthetic settings. | An optional model-free alternate-sufficient-evidence fixture under #79: count candidate reach, native retrieval versus annotated residual derivability and benign collateral retention. | 456 designed facts/15 fictional episodes; benchmark gives the reader annotated relevant evidence and assumes perfect source-to-derivative deletion. It does not authorize deleting other owners' legitimate records. |
| [MemJoin](https://arxiv.org/abs/2610.24359) | Independently allowable cross-session facts can combine into an unrequested sensitive relation (5.9–13.9% complete disclosure in synthetic memory cases). | #280/#898 paired unnecessary-disclosure, legitimately needed answer and task-completion controls; observe cumulative purpose and prompt/output separately. | 288 constructed cases, fixed reader; suppressing link cues increases some refusals. The reference output critic has hidden evaluator policy labels unavailable to deployment. |

### Minimum useful independent memory fixtures

Use a single shared synthetic corpus, exact source IDs, revisions, principal, tenant, purpose and policy-state labels; do not create a parallel production dataset. Required positives: permitted current fact, permitted history/superseded fact, unrelated benign fact retained after deletion, and task completion without memory. Negatives: wrong-tenant highly ranked hit, missing/forged scope, denied or unresolved policy, deleted canonical/summary/index/cache/rollback, retrieved-but-unopened or opened-but-unsupported citation, multi-source residual secret after ordinary lookup fails, and an unnecessary cross-session relation. Record **candidate / admissible / prompt-exposed / answer-disclosed** IDs separately and test legitimate recall, false denial, abstention and collateral utility. Use authoritative source owner/policy at effect time; never infer authorization from similarity or LLM text.

Deletion closure applies to **enumerated Memory-owned derivative substrates**, not every legal source that might help infer the same fact. Residual inference risks require an owner policy decision; model output cannot expand a deletion grant. No model-based permission verifier is an unconditional authoritative gate.

## Delivery and financial evidence reviewed

| Research | What it establishes | What it does not establish |
| --- | --- | --- |
| [Bhati, *Beyond Code Generation*](https://arxiv.org/abs/2609.04681) | A **secondary synthesis** proposing Production-Qualified Change (PQC), Total Cost to Deliver and Verification Tax as useful engineering lenses. | No original validated standard, Micrantha savings estimate or new field experiment. A lower verification ratio can be gamed by skipping necessary gates. |
| [Cui et al., professional developer RCT](https://doi.org/10.1287/mnsc.2025.00535) | The cited three-trial study of 4,867 developers reports a pooled **26.08% completed-task increase**, SE 10.3 percentage points. | Does not directly demonstrate autonomous-agent product releases, revenue or lower security-review workload. |
| [Demirer et al., NBER W35275](https://www.nber.org/papers/w35275) | September 2026 **revised abstract**, >500K developers: cumulative commits +30% / +180% / +240% with successive coding-AI generations, versus +80% projects and +30% releases at the latest generation; four marketplaces show more new apps without aggregate usage lift. | Observational matched adoption, not randomized tool assignment or a Micrantha forecast. **Full revised methods PDF unavailable at this review**; earlier June authors' methodology describes the *older* >100K sample (+180% commits/+50% projects/+30% releases). Keep `Papers!254` Triaged / Read Now until actual revised methods can be read. |

For a delivery decision, link (where applicable) `candidate revision -> qualified gates and independent evidence -> accepted change -> user-reachable effect -> observed adoption/use or operational value`. A merged PR, green CI or release by itself does not establish consumer usefulness or recurring billing cessation. Track attributable model, tool, CI, review, remediation, recovery and incident costs only when observable; unknown cost is not zero. Prefer **net future avoidable spend and consumer-verified effects** over code/PR counts. Keep security and independent verification as non-compensating gates.

Source owners: [meta #144](https://github.com/hackelia-micrantha/.github/issues/144), [meta cost-of-delay guardrail](../../CONTRIBUTING.md#financial-impact-and-cost-of-delay-guardrail), [Deliver to Done](../prompts/planning/long-running-agent-execution.md), [implementation completeness](../prompts/reviews/implementation-completeness.md), Dubnium Run Ledger #414 and Anthesis #140. This evidence is suitable for **read-only outcome calibration**, not a new orchestration/control plane or individual developer productivity rating.

## Priority and next acceptance

1. **P1 security implementation already owned:** #1283 enumerated deletion closure remains the operative safety work. Do not create another Memory security epic.
2. **P2 conditional, small verification:** #939 raw lexical vs semantic retrieval and source-open fidelity; #898 prompt exposure; Lab #79 multi-source forgetting; Anthesis #280 purpose-limited cumulative exposure, with matched legitimate utility.
3. **P2 optional outcome reporting:** #144 stage-qualified delivery/adoption and measured attributable cost under existing budgets/evidence.
4. **Research-only pending:** NBER September full identification/robustness review. Never claim a methods review from the revised abstract or reclassify `Papers!254` as Reviewed.
5. **Queue safety:** The nine `Reading Queue` entries have stale status/identities. Portfolio #90 owns source-keyed compare-and-set or exclusive single-writer reconciliation; do not advance them by positional row overwrite.

No source in this note demonstrates an exploit in Micrantha, requires a new memory graph, delegates policy authority to an LLM or authorizes merge, release, deployment, paid changes or deletion of external data. References are author-reported unless an explicitly named independent evaluation is available.
