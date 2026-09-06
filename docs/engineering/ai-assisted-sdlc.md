# AI-assisted SDLC phase discipline

Micrantha treats AI-assisted engineering as a **workflow and evidence problem**, not as a single long-running model conversation.

This guidance extends [Compound Engineering](./compound-engineering.md) with explicit phase boundaries for non-trivial agentic software work. It is informed in part by Backline's practical report, [Building an AI SDLC on Thin Ice: What Worked and What Backfired](https://backline.ai/blog/building-ai-sdlc-lessons/), but keeps Micrantha's existing authority, evidence, and runtime boundaries authoritative.

## Decision

Use explicit phase-local contexts, durable handoff artifacts, bounded execution, independent verification where required, and risk-adaptive human review.

The governing principle is:

> Agents may reason broadly, but workflow state advances only through explicit validated transitions, and execution authority remains separately governed.

The workflow is not itself proof of correctness. Models, reviewers, tests, policy, runtime isolation, and human judgment provide different kinds of evidence and must not be collapsed into one confidence signal.

## Reference workflow

For non-trivial work, prefer a shape comparable to:

```text
Problem / intent
      |
      v
Research / spike
      |
      v
System design
      |
      v
Increment plan
      |
      v
Bounded implementation
      |
      v
Deterministic verification
      |
      v
Independent / semantic review when required
      |
      v
Risk-appropriate human disposition
      |
      v
Governed external effect
      |
      v
Review -> Compound
```

This is not a mandatory waterfall. A failed verification, new constraint, or unresolved assumption may return work to an earlier phase. Escalation is preferable to silently widening scope, authority, or assumptions.

## Phase-local context

Do not depend on one continuously growing chat or model context as the canonical SDLC state.

Distinct phases should receive the smallest context needed for their role. Examples:

- research receives the problem, constraints, and relevant source evidence;
- system design receives accepted requirements and research results;
- increment planning receives the accepted system design and current repository state;
- implementation receives one bounded increment and its acceptance criteria;
- verification receives the exact candidate plus verification requirements;
- review receives the exact candidate, evidence, and decision context needed for disposition.

Fresh model context is reliability hygiene, not a security boundary. If two phases share credentials, mutable state, authority, or an attacker-controlled trust root, separate sessions do not make them independent.

## Durable phase artifacts

Phase boundaries should use explicit artifacts rather than conversational memory where the result affects later work.

A phase artifact should identify, where material:

- artifact kind and schema/profile version;
- exact producer/run identity;
- exact source/input references or digests;
- objective and acceptance criteria;
- bounded conclusions, decisions, or candidate output;
- unresolved assumptions or `indeterminate` state;
- evidence references;
- validation status and validating evidence;
- supersession/currentness information when relevant.

The following distinctions are mandatory mental models:

```text
artifact exists
  != artifact validated

artifact validated
  != effect authorized

effect authorized
  != effect executed

effect executed
  != outcome verified
```

Repository files, issue text, model output, generated plans, reviewer prose, logs, retrieved memory, and prior phase artifacts remain untrusted observation/content unless a separately owned contract establishes stronger semantics.

## Phase artifacts are control-plane inputs

Persistent agent-generated state can influence every later phase. Treat it accordingly.

A stale, poisoned, mis-bound, or over-broad plan can create durable workflow corruption even when later agents behave correctly relative to that plan. Therefore:

- bind important artifacts to exact source and candidate identities;
- distinguish `proposed`, `validated`, `accepted`, `superseded`, `rejected`, and `indeterminate` states where useful;
- re-resolve current authoritative state before consequential effects when policy-relevant state may have changed;
- do not infer authority from artifact presence, recency, confidence, or model authorship;
- fail closed or escalate when required validation/currentness cannot be established.

## Decompose into independently verifiable increments

Large agent tasks should be split until each implementation unit has a bounded definition of done and a practical verification strategy.

Prefer increments that:

- start from an exact source baseline;
- have a narrow mutation scope;
- produce one attributable candidate state;
- expose deterministic checks where possible;
- can be rejected without contaminating canonical state;
- preserve evidence across repair/retry;
- do not require broad authority merely because the overall project is broad.

This is primarily a correctness and recovery property. Smaller tasks also reduce context pressure, but token count alone is not the reason for decomposition.

## Verification is evidence diversity, not reviewer count

Multiple AI reviewers do not automatically provide independent assurance.

Correlated failure is likely when producer and reviewers share the same model family, prompt assumptions, mutable workspace, test oracle, runtime, or compromised trust root.

Prefer the least expensive reliable evidence path:

1. schema, type, integrity, and exact-subject checks;
2. compiler, static analysis, deterministic tests, and property/invariant checks;
3. exact diff/artifact/workspace inspection;
4. independent semantic verifier where acceptance cannot be decided deterministically;
5. human judgment when consequence or uncertainty requires it.

A deterministic failed check is stronger evidence than contradictory reviewer confidence unless an explicit governed exception process says otherwise.

Where independent verification is required, independence is a trust property. Different persona names, sessions, or model aliases are insufficient by themselves.

## Risk-adaptive human review

AI output volume can exceed human line-by-line review capacity. The response should be to allocate human attention by consequence, not to remove human accountability or claim that workflow automation guarantees quality.

A useful default classification is:

| Change class | Typical examples | Review posture |
| --- | --- | --- |
| Low consequence | docs, generated metadata, mechanical cleanup with strong deterministic checks | automated verification may be sufficient; spot review as appropriate |
| Normal engineering | ordinary feature/refactor/API work | focused human review of design, diff, and evidence |
| High consequence | authentication, authorization, cryptography, policy, permissions, migrations, release/deployment controls, sensitive data, public compatibility, agent authority | explicit human review/approval plus independent evidence appropriate to the boundary |

Risk classification must not be caller/model self-asserted when it changes required controls. The owning repository/governance policy defines the effective review requirements.

Human review should focus on load-bearing questions that automation cannot establish reliably: architecture fit, requirement interpretation, residual risk, policy/authority disposition, compatibility decisions, and whether evidence is sufficient for the intended effect.

## Execution authority is narrower than reasoning authority

An agent may inspect or reason about a broad system without receiving broad mutation authority.

Direct access to APIs, databases, logs, repositories, shells, network destinations, credentials, or deployment controls should be mediated through task-scoped capabilities and runtime enforcement.

Prefer:

```text
accepted task / grant
  -> narrow execution-authority projection
  -> isolated runtime
  -> bounded tools/data/network/filesystem/process/secrets/devices/resources
  -> candidate + evidence
  -> STOP at new consequential transition
  -> fresh governed-effect decision
```

Do not treat "local", "ephemeral", "containerized", or "read-only by convention" as proof of least privilege. Enforcement must live outside untrusted model/repository/tool content.

## Escalation and revision

Agents should escalate rather than silently reinterpret the task when they encounter:

- materially ambiguous requirements;
- missing evidence required for the next transition;
- a required control the runtime cannot enforce;
- repeated verification rejection without material progress;
- policy conflict or an authority boundary that blocks the proposed path;
- a newly discovered architectural decision that materially changes scope.

Escalation may request clarification, additional evidence, a revised plan, a stronger verifier, or an explicit governance decision. It must not become a route for widening authority automatically.

## Cross-repository decision state

Durable architectural decisions that affect multiple repositories should live in the repository or organization surface that owns the decision, with consuming runs using exact references where practical.

Do not force every agent to reconstruct organization architecture from repository-local prose on every run. Conversely, do not make a global decision log a second implementation source of truth.

Use the existing responsibility model:

- `.github` owns shared engineering guidance and cross-repository responsibility boundaries;
- `hackelia-micrantha/hackelia-micrantha` may coordinate adoption/research without becoming a second normative source;
- repository-local issues, ADRs, RFCs, tests, and code remain authoritative for repository-owned behavior;
- Anthesis owns policy, approval, evidence sufficiency, and governed lifecycle semantics;
- Dubnium owns bounded runtime execution, durable run state, recovery, and runtime evidence;
- Sandcastle may own exact mutable-workspace/checkpoint isolation where used;
- Testule/native tooling owns executable verification mechanisms within their assigned contracts.

## Relationship to Compound Engineering

The SDLC phase discipline and the Compound loop compose as:

```text
Plan / phase work
  -> bounded implementation
  -> verification / review
  -> disposition
  -> Compound
       -> candidate learning
       -> validation
       -> separately promoted durable control
  -> Repeat
```

A successful phase artifact or reviewer finding is not automatically future guidance. Promotion remains explicit and proportional to the target, as defined by Compound Engineering.

## Required invariants

- Problem/intent is explicit before solution work materially commits the system.
- Canonical workflow state is external to model context where it affects recovery, authority, or later transitions.
- Phase handoffs use explicit attributable artifacts for material decisions/results.
- Agent-produced phase artifacts are untrusted proposals/evidence until their required validation succeeds.
- Large work decomposes into bounded independently verifiable increments.
- Agent escalation cannot widen authority.
- Reviewer multiplicity is not treated as evidence independence.
- Deterministic evidence is preferred over semantic confidence where it can decide the property.
- Human review depth scales with consequence and policy, not generated diff volume alone.
- Reasoning access does not imply execution authority.
- Runtime authority is task-scoped, least-privilege, externally enforced, and cannot silently cross a new consequential boundary.
- Workflow quality reduces dependence on any one model invocation but does not guarantee software correctness.

## Non-goals

- A universal agent framework or workflow engine.
- One mandatory phase taxonomy for every trivial change.
- Treating files as automatically trusted state.
- Requiring an LLM reviewer when deterministic verification is sufficient.
- Requiring hidden tests for all work.
- Claiming separate chats/personas provide security isolation.
- Replacing repository-local architecture, testing, review, or release ownership.
- Giving models authority because they produced a good plan or passed their own checks.
