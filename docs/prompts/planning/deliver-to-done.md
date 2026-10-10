# Deliver to Done — Outcome-Driven Supervisor Entry Point

Use this entry point when the operator asks to **deliver an end-to-end capability**, **finish a complex project outcome**, or **take a substantial task to verified completion**. It specializes existing Micrantha execution for *outcome ownership*, not for additional execution or effect authority.

This is an **orchestration entry point**, not a second workflow contract. Compose the current [Supervisor operating profile](../../engineering/chatgpt-supervisor-operating-profile.md), [agent execution contract](../../engineering/agent-execution-contract.md), [long-running execution skill](../../../skills/long-running-execution/SKILL.md), [long-running execution prompt](long-running-agent-execution.md), [cross-project overlay](../overlays/cross-project-execution.md), and the narrowest relevant planning, debugging, review, security, CI, [implementation completeness](../reviews/implementation-completeness.md), and delivery prompts.

Do **not** select for a trivial one-step task or ordinary status inquiry. Use [proceed](proceed.md) to continue an already scoped run without changing its completion contract. Read-only by default; selection does not grant mutation, merge, release, deployment, deletion, credential, permission, external-communication, or acceptance-closure authority.

## Compact invocation

> Deliver **[OUTCOME]** to the stated **[MATURITY / CONSUMER]**. Establish an evidence-backed completion contract, recover current authoritative state, select the shortest safe critical path, and continue all authorized inspect/implement/review/fix/validate/integrate/verify transitions without generic continuation prompts. Verify the consumer-facing result and stop only at a verified terminal outcome or precise authority, policy, evidence, or bounded-indeterminate boundary. Do not mistake PRs, CI, or infrastructure activity for delivery.

## Execution overlay

1. **Anchor the outcome.** Resolve the intended consumer and observable result, acceptance criteria, expected maturity, authoritative requirements/decisions, constraints, non-goals, and available authority. Distinguish prototype, integrated candidate, merge-ready, released, and deployed states. Resolve non-material gaps from evidence; escalate materially different interpretations at the affected transition. Keep this small completion contract stable unless intent is explicitly changed.
2. **Recover current evidence.** Refresh the owning project and *minimal relevant* repository/consumer graph: main/base, exact candidate, existing issues/PRs/reviews, CI, contracts, delivery state, and prior handoff. Check uncertain writes by read-back before retry; do not replay effects or reconcile branches with unrelated main changes merely for freshness.
3. **Own the critical path.** Identify the earliest unmet prerequisite on the shortest safe path to the consumer outcome. Prefer restoring security/correctness and critical infrastructure, removing blocking dependencies, completing integration, then proving delivery. Reuse active work and established designs. Separate completion blockers from optional polish; choose one reversible and independently verifiable slice at a time.
4. **Execute to evidence.** For each substantive loop, identify the unmet criterion, causal hypothesis, single intervention, expected proof, and consequence if it fails. Apply only authorized changes; verify against the *exact resulting candidate* with risk-shaped testing/static analysis and independent review where policy requires it. Diagnose infrastructure, oracle, implementation, and authority failures separately. Re-review after repair; never edit evidence or weaken gates to pass.
5. **Enforce convergence.** Ask whether the next action serves the original consumer outcome rather than the last tool result (**drift/momentum**). If guidance already covers a failure, correct non-compliance rather than restating it. If a third attempt repeats the same lever/readers without new evidence (**swirl**), change approach or escalate. Remove superseded material instead of layering, avoid fixture-only over-fitting, and do not expand into speculative services or new issues. Inherit the existing retry budgets across recovery.
6. **Prove actual delivery.** Apply the [implementation completeness review](../reviews/implementation-completeness.md) to the stated maturity. Where applicable, verify the consumer's reachable end-to-end path, integration contracts, failure/security cases, exact-head validation, package/install/accessibility, operational recovery, and accuracy of public claims. A merged PR, green CI, or running process is not sufficient evidence of a usable product. Declare absent layers not applicable only with rationale.
7. **Gate consequential effects.** Check exact subject identity, fresh evidence, unresolved blockers, independent review/policy, and **separate explicit authorization** before merge, release, publish, deploy, delete, permissions/credentials, external communication, or consequential closure. If blocked, continue independent useful work; never treat permission to implement or "proceed" as effect authority. Verify every authorized effect by external read-back.
8. **Recover and close out.** Use the existing compact run ledger for exact revisions, completed versus missing evidence, current gate, uncertain effects, retry usage, and next eligible transition. Do not depend on chat continuity or claim autonomous work after the session ends. Reconcile existing issues/docs only within authorized scope; run a bounded Compound assessment *after* the outcome decision, without inventing learning artifacts.

## Terminal outcome classification

Choose the first accurate state; do not equate individual milestones with completion:

- **Complete — verified:** the exact requested consumer outcome and applicable acceptance evidence are verified.
- **Complete for stated maturity:** the declared prototype/incubating/etc. scope is verified and bounded enhancements are explicitly non-blocking.
- **Ready — authority required:** all feasible pre-effect gates are satisfied, but the requested next consequential effect lacks explicit authority.
- **Blocked — external dependency / decision:** a named missing capability, required evidence, policy approval, or material decision prevents the next transition.
- **Indeterminate — bounded:** applicable evidence or retry budget cannot determine the effect/candidate state reliably; no unsafe retry.
- **Superseded:** current authoritative evidence shows the outcome was already delivered or replaced.

A terminal report must identify the intended versus observed outcome, exact subject/revision, verification evidence, any consequential effects and read-back, the smallest remaining delivery gap, and the exact next eligible transition or boundary. Avoid manufacturing work solely to populate closeout.

## Example invocation

> Deliver the Supervisor Gateway phone-MCP consumer path to an integrated, tested candidate. Reconcile existing contracts and work first; prioritize authentication, governed action invocation and observable result over optional UI polish. Continue authorized slices, verify the user path end to end, and report the exact remaining delivery or approval gate.
