# AI model selection and escalation

Micrantha selects models according to the bounded task, project maturity, consequence, available verification, privacy constraints, and operational cost. Model tier is an implementation choice unless a project-local or governing policy explicitly makes it part of a tested contract.

The default rule is:

> Use the least expensive and least externally dependent model path that can reliably satisfy the task's reasoning requirements under the required evidence and authority controls; escalate when evidence shows that path is insufficient.

This guidance complements [AI-assisted SDLC phase discipline](./ai-assisted-sdlc.md). It does not change execution authority, review, verification, approval, or release requirements.

## Frontier models are not a universal requirement

Micrantha does **not** require a frontier model merely because a task uses AI, invokes a skill, or participates in an agentic workflow.

Experimental, exploratory, low-consequence, easily reversible, or strongly deterministic work can intentionally use local or smaller models when that is sufficient. Examples include:

- prototype/refactoring experiments isolated from canonical state;
- bounded repository classification or metadata generation with deterministic validation;
- candidate plans or QART alternatives that remain proposals until reviewed;
- test generation where native tests/compilers establish the result;
- local development workflows where privacy, latency, offline use, or cost materially favors a local model;
- conformance experiments whose purpose includes measuring model limitations.

An Experimental repository lifecycle is a useful signal that cheaper/local experimentation may be appropriate, but lifecycle alone does not waive security or authority controls. Experimental code can still touch secrets, privileged infrastructure, security boundaries, or irreversible external effects.

## Escalation criteria

Escalate to a stronger model, including a frontier model when appropriate, when one or more of these are material:

- the task requires broad synthesis across a large or unfamiliar system;
- architecture, security, migration, policy, or compatibility reasoning has substantial consequence;
- requirements are materially ambiguous and the current model repeatedly fails to resolve them from available evidence;
- implementation/review cycles repeat without meaningful progress;
- the candidate contains subtle concurrency, state, language/runtime, cryptographic, or distributed-system behavior that exceeds the current model's demonstrated capability;
- deterministic checks cannot decide the relevant semantic property and stronger semantic review is justified;
- the project explicitly defines a minimum model capability/profile for the workflow;
- a controlled comparison against a stronger model is part of evaluation or conformance evidence.

Escalation is a reasoning-quality decision. It must not silently widen filesystem, network, credential, tool, repository, deployment, or approval authority.

## Evidence beats model prestige

A more capable model can reduce reasoning error but does not establish correctness by identity or reputation.

Prefer this evidence order where applicable:

1. schema, type, integrity, and exact-subject checks;
2. compiler/static analysis and deterministic tests;
3. property, invariant, contract, integration, security, migration, and packaging checks appropriate to the boundary;
4. exact diff/artifact inspection;
5. independent semantic verification when deterministic evidence cannot establish the property;
6. human judgment or explicit approval when consequence, policy, or uncertainty requires it.

A deterministic failing check is stronger negative evidence than a frontier model saying the candidate looks correct.

Likewise, a smaller/local model can be entirely adequate when its output is constrained and the decisive properties are externally verifiable.

## Project-local policy

Project repositories own model-selection details for their workflows because the useful trade-offs vary by project.

A project-local skill may declare, when useful:

- a minimum capability/profile rather than a vendor/model name;
- whether local/offline execution is preferred or required;
- context-size or multimodal requirements that are intrinsic to the task;
- an escalation trigger after repeated ambiguity or verification failure;
- whether a second/independent semantic verifier is required;
- privacy/data-residency restrictions on external inference;
- cost/latency ceilings for routine operation;
- a frontier-model requirement for a specific high-consequence boundary, with rationale.

Avoid hard-coding a model vendor or version unless compatibility with that exact model is itself part of the project's contract or experiment. Model availability and capability change faster than project architecture.

Shared organization skills should therefore describe capability/evidence needs and safe escalation semantics. They are not permission to mandate a single inference provider across the ecosystem.

## Experimental posture

For Experimental work, a useful default is:

```text
small/local model
  -> bounded candidate
  -> deterministic/native verification
  -> inspect failure evidence
  -> escalate model only when the reasoning problem warrants it
```

This keeps experimentation cheap, offline-capable where useful, and informative: a weaker model's failure can itself reveal missing contracts, poor task decomposition, or insufficient deterministic tooling.

Do not compensate for a weaker model by granting broader authority, suppressing failing checks, reducing provenance, or allowing self-approval. If a task cannot be made safe and verifiable with the available model/runtime, stop or escalate the task rather than weakening the controls.

## High-consequence posture

For authentication, authorization, cryptography, permissions, policy, sensitive data, destructive migration, release/deployment controls, public compatibility, or agent authority, use stronger reasoning support when it materially improves review quality—but preserve independent evidence and accountable disposition.

A frontier model may be preferred for difficult reasoning in these domains, but the security property remains in the architecture, runtime enforcement, deterministic verification, independent evidence, and human/governance decision where required—not in the model tier.

## Required invariants

- Model selection is risk- and capability-adaptive, not globally fixed.
- Frontier-model use is not required by default for Experimental or low-consequence work.
- Project-local skills own justified model profiles/escalation rules for project-specific workflows.
- Model tier does not create authority or establish correctness.
- Escalation cannot widen execution authority automatically.
- Deterministic evidence is preferred when it can decide the property.
- Independent verification means independence of the relevant trust roots, not merely a different model name.
- Privacy, data residency, availability, cost, and offline operation are legitimate model-selection constraints.
- A weaker model never justifies weaker safety, provenance, review, or verification controls.
