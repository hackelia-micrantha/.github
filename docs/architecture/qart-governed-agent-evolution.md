# QART: How should Micrantha govern agent evolution across runtime, context, identity, and authority boundaries?

## Status

Ready for decision

## Context

Agent systems are beginning to modify their own prompts, context assembly, tools, routing, configuration, and implementation. Ouroboros (arXiv:2608.08311) is useful motivating evidence: it treats the harness as mutable software and gates self-edits through reviewed commits, while also exposing the security consequence that a mutable agent can otherwise modify the machinery that determines its own effective behavior.

Micrantha already has separate authorities that cover most of this problem:

- Dubnium owns agent runtime execution, supervisor/specialist orchestration, activation, and recovery.
- Invokrum owns deterministic prompt/context composition, exact manifests, lockfiles, and drift evidence.
- Keylix owns sender-constrained authorization primitives and proof-of-possession identities; it does not own application authorization.
- Anthesis owns actor, capability, policy, approval, evidence, attribution, provenance, and governance decisions.
- `hackelia-micrantha/.github` owns cross-repository architecture and responsibility boundaries.

Related existing work includes Anthesis #57 (governed lifecycle and adaptation), Anthesis #26 (agent harness boundaries), Anthesis #151 (capability-bound invocation profile), Anthesis #155 (reasoning-independent governance), and Keylix #18 (sender-constrained executor/verifier profiles).

A new private repository, `ryjen/governed-agent-evolution`, currently exists without implementation. The proposed role is a contract laboratory/reference integration, not a fifth authority or runtime.

## Question

> How should Micrantha compose its existing runtime, context, cryptographic identity, and governance authorities so an agent can propose changes to itself without independently authorizing the transition that gives those changes effect?

## Decision drivers

1. Preserve independent authority and prevent self-authorization or authority laundering.
2. Reuse existing component contracts instead of creating parallel policy, identity, context, evidence, or runtime models.
3. Make every authority-relevant transition exactly attributable, replayable, and fail-closed.
4. Keep component implementations independently useful and replaceable.
5. Support incremental adoption before any recursive autonomous evolution is enabled.

## Constraints and invariants

- An evolving system may propose its successor but MUST NOT independently authorize the transition that gives the successor effect.
- Runtime evidence, prior success, evaluation output, or possession of an existing credential MUST NOT mint or widen authority.
- Anthesis remains the policy/approval authority; Dubnium does not become a policy engine.
- Invokrum remains mechanism-not-policy; exact context integrity does not imply semantic approval.
- Keylix sender binding does not imply task correctness or application authorization.
- Governance MUST NOT depend on access to model-private reasoning state.
- Authority-relevant state changes require re-evaluation against the exact candidate subject.
- Governance roots, signing policy/key custody, publisher trust, and activation authority require stronger protection than ordinary prompt/config evolution.

## Assumptions and evidence gaps

| Statement | Fact, assumption, or unknown | Evidence or validation needed |
| --- | --- | --- |
| Existing Anthesis contracts can express candidate authorization without a new policy model | Assumption | RFC mapping against #57, #26, #151 and current RFCs |
| Invokrum manifests/locks are sufficient to identify authority-relevant prompt/context state | Assumption | Define reference candidate and verify exact drift detection |
| Keylix identity need not rotate on every generation | Assumption | Threat analysis for privilege expansion and signer persistence |
| Dubnium can expose an atomic/recoverable generation activation boundary | Assumption | Runtime design/implementation follow-up |
| A standalone GAE protocol is unnecessary for the first version | Recommendation pending RFC | First conformance scenario using composed existing contracts |

## Alternatives

### Alternative A: Cross-project composition of existing authorities

- **Mechanism and boundary:** Define an organization-level architecture/RFC describing a composite evolution candidate and lifecycle. Each project retains its existing contract authority. `ryjen/governed-agent-evolution` validates composition through scenarios and conformance evidence.
- **Benefits:** Minimal duplication; strongest separation of duties; preserves independent projects; lets each component evolve on its own schedule.
- **Costs and limitations:** Integration semantics are distributed; version compatibility must be explicit; initial reference flow requires coordination across repos.
- **Security, privacy, and governance:** Strongest fit with least-authority and independent authorization. Allows hardened roots to remain outside the mutable runtime.
- **Operations and ownership:** `.github` owns architecture; component repos own contracts; lab owns fixtures/evidence only.
- **Compatibility and migration:** Additive; existing component users do not need to adopt the full stack.
- **Delivery effort and maintenance:** Moderate but bounded to docs/contracts first.
- **Reversibility:** Easy to moderate — the organization architecture can be revised without migrating a new central runtime.
- **Evidence required:** End-to-end benign and adversarial evolution scenarios.

### Alternative B: New standalone governed-agent-evolution protocol/product

- **Mechanism and boundary:** Define a fifth canonical protocol/schema layer that owns evolution requests, decisions, generations, and evidence envelopes.
- **Benefits:** Centralized conceptual model; potentially easier external consumption if standardized later.
- **Costs and limitations:** High risk of duplicating Anthesis authority, Invokrum identity, Keylix identity, and Dubnium lifecycle state; creates another versioned contract surface prematurely.
- **Security, privacy, and governance:** New control-plane ambiguity; possible authority conflicts.
- **Operations and ownership:** Requires new maintainership and release lifecycle.
- **Compatibility and migration:** Components need adapters to the new model.
- **Delivery effort and maintenance:** High.
- **Reversibility:** Difficult once external consumers depend on it.
- **Evidence required:** Proof that existing contracts cannot compose cleanly or that external interoperability requires a standalone standard.

### Alternative C: Keep governed evolution inside Anthesis or Dubnium

- **Mechanism and boundary:** Put the end-to-end model inside one product repository.
- **Benefits:** Faster initial implementation and fewer repositories touched.
- **Costs and limitations:** Collapses responsibility boundaries and makes one project appear authoritative over contracts it should consume.
- **Security, privacy, and governance:** Increased confused-deputy/self-governance risk; easier for execution and authorization to become coupled.
- **Operations and ownership:** Simpler short-term, worse long-term ownership.
- **Compatibility and migration:** Creates product-specific coupling.
- **Delivery effort and maintenance:** Low initially, high as integrations expand.
- **Reversibility:** Moderate to difficult.
- **Evidence required:** None supports this over the existing repository catalogue model.

## Comparison

| Criterion | Cross-project composition | New standalone protocol | Single-product ownership |
| --- | --- | --- | --- |
| Outcome fit | Strong | Potentially strong but premature | Partial |
| Security and governance | Strongest separation | New authority ambiguity | Weakest separation |
| Reliability and recovery | Explicit per owner | Central model may help | Product-specific |
| Operability and ownership | Clear distributed ownership | New owner required | Simple but misleading |
| Compatibility and migration | Additive | Adapter/migration burden | Tight coupling |
| Complexity and maintenance | Moderate | High | Low initially, high later |
| Cost and delivery | Moderate | High | Low initially |
| Reversibility | Good | Poorer | Moderate |

## Recommendation

Choose **Alternative A: cross-project composition of existing authorities** with high confidence.

The organization-level RFC should define the lifecycle, trust invariants, candidate subject, responsibility matrix, and compatibility requirements, but SHOULD NOT introduce a new policy engine, universal evidence envelope, sender identity scheme, or runtime protocol unless a concrete interoperability gap is demonstrated.

Recommended evolution classes:

1. **Context evolution** — prompts, overlays, profiles, context assembly.
2. **Runtime evolution** — harness, supervisor/specialist implementation, tool code.
3. **Configuration evolution** — model/provider routing, tool configuration, limits.
4. **Capability evolution** — requested/granted effect surface or privilege.
5. **Authority evolution** — policy roots, trust roots, signer/publisher trust, approval rules.

Authority evolution receives the strongest protection and MUST NOT be automatically approved by the evolving runtime.

The candidate subject SHOULD compose existing exact identities rather than duplicate them. A logical candidate includes:

```text
EvolutionCandidate
  base runtime generation
  candidate code/config identity
  Invokrum context manifest/lock identity
  requested capability delta
  runtime/model identity where policy-relevant
  evaluation/evidence references
```

The exact normative representation should be selected by the component authorities after mapping existing contracts.

## Trade-offs

### Accepted

- Cross-repository coordination and explicit compatibility mapping are accepted in exchange for preserving security boundaries.
- The first implementation may be less convenient than a monolithic self-edit pipeline.
- A lab/reference repo remains non-authoritative and may duplicate small amounts of glue code for conformance.

### Rejected

- Allowing a runtime to self-authorize an authority-relevant change.
- Treating successful evaluation as executable authority.
- Treating Invokrum integrity or Keylix sender proof as semantic authorization.
- Creating a fifth canonical governance/control plane before a demonstrated contract gap exists.

### Residual risks and mitigations

| Risk | Mitigation | Acceptance owner |
| --- | --- | --- |
| Common-root compromise undermines apparent separation | Distinct deployment/key/trust roots where meaningful; document shared-root limitations | Component owners |
| Candidate changes between review and activation | Exact digest/manifest binding and activation verification | Dubnium + Anthesis |
| Stale authority survives material candidate change | Re-evaluate authority-relevant state and fail closed on mismatch | Anthesis |
| Prompt/config changes hide capability expansion | Classify policy-relevant model/tool/capability deltas explicitly | Anthesis + Dubnium |
| Lab begins defining production contracts | Catalogue non-responsibilities and conformance-only scope | `.github` owner |

### Revisit triggers

- External implementations need a vendor-neutral GAE wire protocol.
- Existing component contracts cannot represent a required exact transition without duplication or ambiguity.
- Cross-project integration becomes operationally brittle enough to justify a dedicated versioned interoperability package.

## Decision path

Needs RFC review, then an ADR only for durable organization-level decisions not sufficiently captured by the accepted RFC/catalogue.

## Decision outcome

- **Decision:** Recommend cross-project composition of Dubnium, Invokrum, Keylix, and Anthesis under an organization-level governed-agent-evolution architecture.
- **Date:** 2026-08-12
- **Decision owners:** Micrantha organization/project maintainers
- **Disposition:** Ready for RFC review
- **RFC:** `docs/architecture/rfcs/0001-governed-agent-evolution.md`
- **ADR:** Pending RFC disposition
- **Follow-up work:** Catalogue the lab, reconcile component issues, then implement one deterministic reference scenario.
