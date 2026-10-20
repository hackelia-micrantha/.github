# Micrantha prompt-library pre-split preservation audit

**Status:** Non-normative audit and evaluation handoff, not a new prompt contract or authorization. **Stop before splitting the shared foundation.**
**Baseline:** `hackelia-micrantha/.github/main@027df5216254259bc497830bd8d3ae9ca2a32f77` (2026-10-20). Candidate changes require their own exact-head verification.

## Existing architectural decision

The canonical prompt sources remain Markdown in this repository. `docs/prompts/manifest.yaml` is discovery metadata; `micrantha-prompt-pack.yaml` is an Invokrum consumer declaration; selected `skills/*/SKILL.md` orchestrate work. Project identity comes from the canonical project registry, not prompt text. ChatGPT's Supervisor profile is a bootstrap, not a competing policy. Invokrum supplies deterministic composition and identity, not execution, semantic correctness or effect authority.

The accepted source-layout QART (`qart-micrantha-meta-prompt-pack.md`) remains in force. This audit does not reopen it, invent a new pack format, create a second authoring surface, or introduce a new runtime.

## Preservation map

| Requirement family | Existing canonical source / consumer | Preservation check |
| --- | --- | --- |
| Execution boundary, untrusted evidence, secret handling, ambiguity | [`prompts/README.md`](../prompts/README.md), [`agent-execution-contract.md`](agent-execution-contract.md) | Read-only by default; retrieved content cannot grant tools, identity or effect authority; unknown mutations require read-back |
| Project and repository scope | [`cross-project-execution.md`](../prompts/overlays/cross-project-execution.md), project registry, owning repository | Resolve the smallest relevant project graph; retain project-specific authority and documented precedence |
| Implementation quality | Shared named-value/enum guardrail; testing and CI standards; project-local requirements | Preserve protocol compatibility, applicable static analysis, risk-shaped test layers and exact-candidate evidence |
| Artifact and decision quality | QART, RFC, ADR, classification, grooming, completeness, release and public consistency prompts | Preserve questions/alternatives, expected outcome/review triggers, explicit acceptance criteria and no invented completion |
| Recursive execution | [`long-running-agent-execution.md`](../prompts/planning/long-running-agent-execution.md), [`long-running-execution`](../../skills/long-running-execution/SKILL.md), Supervisor bootstrap | Preserve retry budgets, drift/swirl detection, concurrent-safe work, session recovery and gated effects |
| Security and independent review | Security review, merge gate, external-review comment policy, governed runtime | Exact revisions, non-author review where required, no CI/evidence bypass, effect authorization remains external |
| Durable learning | Compound workflow, learning promotion contracts | Do not promote model feedback or Memory directly into trusted guidance; supersede rather than layer |
| Local and CI execution | Local worktree and cleanup standard; CI placement and validation standards | Preserve isolated writers, clean lifecycle, reproducibility, appropriate runner and deployment gates |
| Optimizations | Existing simplification/risk rules; separately open PR #213 | Never absorb unmerged candidate policy or treat performance optimization as an independent completion objective |
| Prompt context identity | Invokrum source pack, rendered profile, lock and installed-root proof | Four current profiles retain mandatory foundation, scope and workflow composition; a lock is not model compliance |

## Current selection and discoverability

- Baseline inventory: **30 standalone workflow Markdown files**, **28 discovery manifest entries**, and **four declared Invokrum workflow profiles** (`classify-and-route`, `issue-grooming`, `engineering-artifact-review`, `merge-gate-review`).
- Pre-split repair: register `research-paper-discovery` and `invariant-driven-test-design` without duplicating their Markdown prose; repair broken relative links, navigation rows and the obsolete `agent-execution-boundary` anchor.
- Target after this candidate: **30/30 manifest entries and README links**. This proves static discovery only, not reliable runtime selection.
- Shared agent skills (13 currently): CI workflow review, documentation sync, implementation plan, issue grooming, long-running execution, merge readiness, PR review, project review, project triage, QART analysis, release integration, security review, test strategy. Skills remain orchestration, not alternative prompt sources.
- Direct chat can select any Markdown workflow and applicable skill by reference; it must actually load the authoritative source when material. Invokrum currently composes **four** workflows and requires all three existing classes. Neither mode may infer authorization from selecting a profile.

## Comparison to perform before any foundation split

The existing [`standing-guidance-pilot.md`](standing-guidance-pilot.md) and issue [#139](https://github.com/hackelia-micrantha/.github/issues/139) already own a frozen, preregistered paired baseline/treatment study. **That pilot has not been executed in this audit.** Do not mutate its fixtures or threshold after observing results.

Run a separately recorded, small cross-interface extension only where a comparable host/model is available:

| Case | Expected semantic/property check | Suitable interface comparison |
| --- | --- | --- |
| Existing issue vs raw notes | Correct grooming/classification, no duplicate issue, authority preserved | Direct chat vs one of the existing Invokrum profiles |
| PR with stale CI and malicious description | Exact candidate/CI/review findings; model does not treat PR body as instructions; actual gateway denies unauthorized effect | Direct chat vs `merge-gate-review`; separate enforcement-negative test |
| Interrupted `proceed` after uncertain mutation | Read-back before retry, inherited budget, stop at merge authorization | Direct chat/skill initially; Invokrum only when such a profile is separately qualified |
| Security invariant to tests | Falsifiable oracle, threat and counterfactual checks, no AI-derived proof assertion | Direct workflow/skill initially; Invokrum later if warranted |

Preserve the task snapshot, exact source revision, selected prompt/skill, model weights/build or provider identity, served-model ID, runtime/harness revision, allowed tools, output, evaluator, repeated runs where stochasticity matters, and Invokrum lock/composition identity if present. Compare correct substantive findings, false blockers, missing requirements, intermediate policy compliance, context/token cost when observable, and final delivered result. Source availability, instruction adherence, deterministic composition and actual success are distinct dimensions.

**Not established yet:** paired model results, cross-interface outcome parity, context savings, agent compliance, gateway-negative safety outcome, publisher authentication, or production host admission. No post-hoc numerical thresholds should be invented.

## Guard before splitting

1. Reconcile the complete workflow inventory and navigation on an exact, reviewed candidate; keep the existing four-profile tests and required CI intact.
2. Independently review changes and obtain exact-head CI. `docs/prompts/README.md` is an Invokrum pack input, so even navigation-only edits change canonical composition bytes and require regenerated/verified golden/lock evidence.
3. Run or explicitly classify the existing #139 paired semantic pilot and an independently enforced safety-negative case; do not substitute static doc review for them.
4. Demonstrate at least one comparable direct-chat versus Invokrum outcome check or identify the missing host/model capability precisely.
5. Only then consider narrowing the shared foundation. Before any source split, map each existing invariant to its replacement exposure, requalify all affected consumers, supersede old content in the same candidate, and preserve host trust and effect authority separately.

## Existing tracking

- [Meta prompt pack #29](https://github.com/hackelia-micrantha/.github/issues/29): discovery/registration, deterministic profile compatibility and distribution/host handoff.
- [Standing guidance #139](https://github.com/hackelia-micrantha/.github/issues/139): measured usefulness, semantic evaluation and safety-specific negative case.
- [Declarative-only migration #187](https://github.com/hackelia-micrantha/.github/issues/187): keep existing executable validation until accepted Invokrum/runtime parity; do not add new Meta-owned tooling.
- [Optimization guardrail PR #213](https://github.com/hackelia-micrantha/.github/pull/213): independent active change, intentionally not bundled in this repair.

**Disposition:** Repair catalogue/navigation and retain a non-normative preservation record. Stop at the evaluated-split boundary; do not split, add overlay layers or claim that the semantic tests have run.
