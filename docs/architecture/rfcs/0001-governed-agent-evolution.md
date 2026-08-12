# RFC: Governed Agent Evolution

## Metadata

- **Status:** Draft
- **Authors:** Micrantha maintainers
- **Decision owners:** Micrantha organization and affected project maintainers
- **Created:** 2026-08-12
- **Target decision date:** Open
- **Related QART analyses:** [`../qart-governed-agent-evolution.md`](../qart-governed-agent-evolution.md)
- **Resulting ADRs:** Pending
- **Related epics or issues:** Anthesis #57, #26, #151, #155; Keylix #18; project-specific follow-ups pending

## Summary

Micrantha should support governed evolution of agent runtime, context, configuration, and capabilities by composing existing authorities rather than creating a new central control plane.

The core invariant is:

> **An evolving system may propose its successor, but it MUST NOT independently authorize the transition that gives that successor effect.**

The reference composition is:

- **Dubnium** owns runtime execution, observation, candidate generation, activation, health, and rollback.
- **Invokrum** owns deterministic prompt/context composition, manifests, lockfiles, and exact drift evidence.
- **Keylix** owns sender-constrained authorization primitives and proof-of-possession identity for protected network boundaries.
- **Anthesis** owns policy, capability, approval, decision, evidence requirements, attribution, and provenance.
- **`hackelia-micrantha/.github`** owns this cross-repository architecture and responsibility model.
- **`ryjen/governed-agent-evolution`** is a non-authoritative contract laboratory/reference integration used to validate the composition.

The initial design is documentation- and conformance-first. It does not authorize unrestricted recursive self-modification.

## Motivation

Agent systems increasingly modify the same machinery that determines their future behavior: prompts, context assembly, tools, model routing, configuration, and implementation. Ouroboros (arXiv:2608.08311) is motivating prior art because it demonstrates a long-running agent harness that proposes and reviews changes to itself. It also sharpens a security problem: if the mutable runtime can modify the mechanisms that define its own authority, review, identity, or activation, then self-improvement can become self-authorization.

Micrantha already separates execution, context integrity, sender binding, and governance into independent projects. The opportunity is therefore not to add another agent-evolution platform, but to define how those authorities compose when the governed subject is the agent/runtime itself.

Broader review is warranted because the design crosses repository, runtime, cryptographic identity, governance, deployment, and trust-root boundaries.

## Goals

- Define a common lifecycle for proposing, evaluating, authorizing, activating, observing, and rolling back agent evolution.
- Preserve independent authority: execution, context attestation, sender binding, and policy remain separate concerns.
- Bind authorization to the exact authority-relevant candidate state.
- Make stale, substituted, widened, or partially activated candidates fail closed.
- Support bounded automatic approval for low-risk evolution only after policy and conformance evidence justify it.
- Provide an executable reference integration without making the integration laboratory authoritative.

## Non-goals

- Build a new general-purpose agent runtime.
- Create a second Anthesis policy, approval, evidence, or replay model.
- Define custom cryptography or extend DPoP to encode task correctness.
- Make Invokrum responsible for semantic prompt approval.
- Require key rotation for every prompt or configuration change.
- Standardize model-private reasoning state or require chain-of-thought access.
- Enable unrestricted autonomous modification of governance roots, signer custody, publisher trust, or deployment authority.
- Define a vendor-neutral external GAE protocol before a demonstrated interoperability need exists.

## Background and current state

### Existing authority boundaries

The organization repository catalogue already distinguishes architectural authority from runtime dependency and assigns separate responsibilities to Anthesis and Dubnium. Anthesis #57 models adaptation as a governed lifecycle transition rather than an implicit side effect. Anthesis #26 separates runtime mediation from Anthesis authorization. Anthesis #151 defines exact capability invocation authority. Anthesis #155 requires governance to operate on structured and observable state rather than model-private reasoning. Keylix #18 separately explores sender-constrained executor and verifier identities.

Invokrum provides deterministic context composition, exact source/output identities, lockfiles, and drift categories while explicitly remaining mechanism-not-policy. Keylix provides proof-of-possession/sender binding while explicitly remaining separate from application authorization and task correctness.

### Motivating prior art

Ouroboros treats the agent harness itself as mutable software and gates self-edits through deterministic checks, model review, staged-diff integrity checks, and version control. Its deployment demonstrates that harness self-maintenance is operationally plausible, but its published benchmark results do not establish that recursive self-evolution itself caused capability gains. This RFC therefore treats Ouroboros as a motivating workload and threat signal, not a normative dependency.

## Proposal

### Core lifecycle

```text
observe
  -> classify failure/opportunity
  -> propose candidate
  -> resolve exact candidate identities
  -> evaluate candidate
  -> authorize exact transition
  -> activate atomically/recoverably
  -> observe health and evidence
  -> accept generation or rollback
```

The lifecycle composes Anthesis #57 rather than creating a parallel workflow model. `AdaptationProposed` is the natural Anthesis lifecycle entry point; activation is a governed external effect.

### Evolution classes

Every candidate MUST identify the evolution classes that are authority-relevant:

1. **Context evolution** — prompt overlays, profiles, composition inputs, context assembly.
2. **Runtime evolution** — harness, supervisor/specialist implementation, tool/runtime code.
3. **Configuration evolution** — model/provider routing, limits, feature flags, tool configuration.
4. **Capability evolution** — permissions, accessible effects, scopes, targets, resource or budget bounds.
5. **Authority evolution** — policy roots, trust roots, approval rules, signer custody/policy, publisher trust, activation authority, or evidence-verification requirements.

A candidate MAY span several classes. Classification is policy input; it does not itself grant authority.

Authority evolution is a protected class. It MUST NOT be automatically approved solely by the mutable runtime being governed.

### Candidate subject

The architecture defines a logical `EvolutionCandidate`, not yet a new universal wire schema.

An exact candidate subject SHOULD compose existing identifiers and authority-relevant claims:

```text
EvolutionCandidate
  base_generation
  candidate_code_or_config_identity
  context_identity
    Invokrum manifest/lock digest where applicable
  requested_capability_delta
  runtime/model/provider identity where policy-relevant
  evaluation/evidence references
  activation target
```

The exact representation SHOULD reuse existing Anthesis, Invokrum, Dubnium, and Keylix contracts. A new shared schema is justified only if conformance work demonstrates a gap that cannot be expressed without ambiguity or duplication.

### Exact-binding rule

An authorization decision MUST bind all authority-relevant candidate state needed by policy. If any bound value changes before activation, the decision is stale and MUST NOT authorize the changed candidate.

Examples include:

- base generation;
- candidate code/config digest;
- Invokrum context manifest/lock digest;
- model/provider where policy distinguishes them;
- requested/granted capabilities and constraints;
- target host/runtime/environment;
- signer/workload identity where policy-relevant;
- expiry and approval references.

Evaluation output, prior successful generations, receipts, or activation evidence cannot widen the decision.

## Architecture

```text
                       ┌──────────────────────┐
                       │       Anthesis       │
                       │ policy / approval /  │
                       │ decision / evidence  │
                       └──────────┬───────────┘
                                  │ exact authorization
                                  ▼
┌──────────────────────┐  ┌──────────────────────┐
│       Invokrum       │  │        Keylix        │
│ exact context state  │  │ sender-bound proof  │
│ manifests / locks    │  │ and replay defense  │
└──────────┬───────────┘  └──────────┬───────────┘
           │ candidate identity       │ request identity
           └──────────────┬───────────┘
                          ▼
                 ┌──────────────────┐
                 │     Dubnium      │
                 │ runtime / agent  │
                 │ proposal /       │
                 │ activation       │
                 └────────┬─────────┘
                          │
                   operational evidence
                          │
                          ▼
                 Anthesis interpretation
```

This diagram is a trust/responsibility model, not necessarily a literal request topology.

### Protected authority boundary

The mutable runtime MUST NOT possess unilateral ability to rewrite or bypass all controls that authorize its own successor. Stronger separation SHOULD protect, as applicable:

- Anthesis root policy and approval requirements;
- activation/deployment authorization;
- Keylix signer policy and private-key custody;
- Invokrum publisher trust/acquisition policy;
- trust roots and protected governance configuration;
- independent reviewer/evaluator configuration where it establishes required evidence;
- rollback/recovery controls.

The same physical host MAY contain several components in local development, but documentation MUST state when common-root compromise defeats nominal separation.

## Decision summary

| Question | Alternatives | Recommendation | Key trade-off | QART / ADR |
| --- | --- | --- | --- | --- |
| Overall ownership | Cross-project composition; new GAE protocol; single-product ownership | Cross-project composition | More integration coordination for stronger boundaries | QART |
| Evolution identity | New universal envelope; compose existing exact identities | Compose existing identities first | Distributed contract mapping | QART |
| Generation cryptographic identity | Rotate every change; persistent sender; risk-triggered rotation | Persistent sender allowed; re-evaluate authority, rotate at meaningful trust-boundary changes | More nuanced policy | QART / future component ADR |
| Authority roots | Mutable with runtime; externally protected | Externally/protected authority boundary | Operational complexity | QART |
| Activation | Runtime self-promotion; governed exact activation | Governed exact activation with rollback | Extra control path | QART |

## Detailed design

### Components and responsibilities

| Component | Responsibility | Does not own |
| --- | --- | --- |
| Dubnium | Observe runtime behavior; propose runtime/config changes; expose generation identity; activate authorized candidate; health/rollback; execution evidence | Policy authority; prompt composition semantics; sender-binding cryptography |
| Invokrum | Resolve exact prompt/context candidate; deterministic manifest/lock; drift evidence | Semantic approval; runtime activation; authorization |
| Keylix | DPoP/sender-bound identity; replay/nonce/target protections; bounded sender evidence | Task correctness; runtime attestation by implication; application authorization |
| Anthesis | Exact policy decision; capability/approval semantics; evidence requirements; provenance and governance interpretation | Runtime execution, transport, key custody implementation, prompt composition |
| `.github` | Cross-repository architecture, repository ownership, standards | Component implementation contracts |
| `governed-agent-evolution` lab | Scenarios, fixtures, adversarial tests, conformance evidence, reference glue | Any production authority or component contract |

### Interfaces and contracts

#### Runtime generation

Dubnium SHOULD expose a stable runtime-generation identity sufficient to distinguish the currently active generation and candidate base. The implementation format is Dubnium-owned.

A generation identity MUST NOT by itself imply authorization.

#### Context identity

When context is authority-relevant, the candidate SHOULD reference Invokrum's exact resolved manifest/lock identity. A context candidate that changes after authorization MUST fail exact-binding verification or require a new decision.

#### Sender identity

Keylix MAY protect network calls between workload, governance, and capability boundaries. DPoP proof possession MUST NOT be interpreted as proof that the runtime generation is approved. Hosts SHOULD bind sender identity to authenticated workload/runtime context rather than accepting caller-supplied role metadata.

Key rotation SHOULD be considered for meaningful trust-boundary changes such as privilege expansion, signer-compromise response, control-plane role changes, or protected release boundaries. Rotation is not required for every ordinary prompt change.

#### Governance decision

Anthesis SHOULD reuse existing exact capability/approval semantics. `require_approval` is not executable authority. Final authorization MUST identify the exact candidate subject and constraints needed by the activation effect.

### State and consistency

- Candidate proposals are immutable logical subjects once submitted for authorization. A modified candidate is a new subject.
- Decisions are append-only; re-evaluation produces a new linked decision rather than mutating history.
- Activation SHOULD be atomic or recoverable to a previously authorized generation.
- A partially activated candidate MUST NOT be represented as fully accepted.
- Runtime health/evaluation after activation is evidence. It may trigger rollback or a new governance decision but cannot retroactively authorize the activation.
- Stale authorizations MUST fail closed when authority-relevant candidate state differs.

### Failure model

| Failure | Required behavior |
| --- | --- |
| Candidate digest/manifest mismatch | Deny activation; require new candidate/decision |
| Missing/expired/indeterminate authorization | Fail closed |
| Required approval absent or bound to different subject | Fail closed |
| Keylix proof invalid/replayed/wrong target | Reject protected request; do not downgrade silently |
| Invokrum context drift | Block or require re-evaluation according to policy |
| Activation partial/fails health gate | Record evidence and rollback/recover according to Dubnium policy |
| Runtime attempts protected authority evolution without required external approval | Deny and record security evidence |
| Old generation continues acting after replacement | Revoke/expire/limit its authority according to runtime and policy design |

## Security, privacy, and governance

### Assets and sensitive data

- policy and approval roots;
- signer/private-key capabilities;
- runtime/deployment authority;
- prompt/context packs that influence authority or execution behavior;
- provider/model credentials and routing configuration;
- candidate/evaluation artifacts that may contain source or sensitive operational data;
- evidence and provenance records.

### Threat and misuse scenarios

The conformance plan MUST cover at least:

- candidate changes after review but before activation;
- stale approval reused for a modified candidate;
- context changed after authorization;
- model/provider or tool surface secretly widened;
- agent attempts to weaken policy/approval rules;
- agent attempts to replace or bypass independent review/evaluation requirements;
- valid sender proof from an unauthorized runtime generation;
- stolen bearer token without proof key;
- old generation continues to invoke effects after replacement;
- rollback attempts to activate an unapproved generation;
- common-host/root compromise defeating nominal separation;
- successful evaluation incorrectly treated as authorization.

### Trust and authorization boundaries

The governing principle is separation between **proposal/evidence** and **authority**. A component may produce evidence about itself, but that evidence is not self-interpreting authority.

For high-risk evolution, independent controls SHOULD exist outside the mutable runtime's ordinary write boundary.

### Evidence, provenance, audit, and retention

A governed evolution trace SHOULD be sufficient to answer:

1. Which base generation proposed the change?
2. What exact candidate code/config/context was evaluated?
3. Which sender/workload identities participated?
4. Which evaluations and evidence were considered?
5. Which policy and approvals authorized activation?
6. What exact generation was activated?
7. What happened during post-activation evaluation?
8. Was the generation accepted, rolled back, or superseded?

Raw model-private reasoning is neither required nor authoritative evidence.

## Operational design

### Initial safety posture

The first implementation SHOULD be propose/review/activate rather than unrestricted recursive evolution:

```text
observe
  -> propose
  -> independent context/evaluation evidence
  -> Anthesis decision
  -> human approval where required
  -> Dubnium activation
```

Policy MAY later allow narrowly classified low-risk automatic transitions once deterministic conformance, rollback, and monitoring are demonstrated.

### Health and rollback

Dubnium owns activation mechanics. The reference architecture requires:

- exact candidate-to-active verification;
- a durable previous known-good generation where practical;
- explicit activation result state;
- bounded post-activation evaluation/health criteria;
- rollback that itself respects authorization policy when rollback would change authority-relevant state.

Emergency recovery MAY use a separately protected operator path. Emergency controls must be auditable and must not become an undocumented general bypass.

## Compatibility, migration, and rollout

This architecture is additive. Existing standalone consumers of Dubnium, Invokrum, Keylix, or Anthesis do not need to implement governed evolution.

Initial rollout:

1. Accept architecture and repository boundaries.
2. Reconcile existing component issues and identify only missing contracts.
3. Add the `governed-agent-evolution` lab as a Proposed transitional repository in the repository catalogue. The organization registry intentionally remains scoped to `hackelia-micrantha/*` repositories.
4. Implement one deterministic low-risk context-evolution scenario.
5. Add adversarial exact-binding and stale-authority scenarios.
6. Expand to runtime/config evolution.
7. Consider bounded automatic approval only after evidence supports it.

No compatibility promise is made for a standalone GAE wire protocol because none is defined in this RFC.

## Alternatives considered

### Alternative: New standalone GAE protocol/product

- **Benefits:** One central schema and lifecycle; potentially reusable externally.
- **Costs and risks:** Premature duplication of Anthesis, Invokrum, Keylix, and Dubnium contracts; new authority ambiguity and release burden.
- **Reason not selected:** No demonstrated contract gap currently requires a fifth canonical layer.
- **Reconsider when:** External implementations require stable vendor-neutral interoperability or composition proves persistently ambiguous.

### Alternative: Put the model entirely in Anthesis

- **Benefits:** Central governance documentation.
- **Costs and risks:** Anthesis would absorb runtime/context/identity responsibilities it explicitly does not own.
- **Reason not selected:** Violates existing responsibility boundaries.
- **Reconsider when:** Not expected; only if project responsibilities are explicitly redefined through organization governance.

### Alternative: Put the model entirely in Dubnium

- **Benefits:** Direct implementation path.
- **Costs and risks:** Mutable runtime could become authority over its own evolution; tight coupling to one distribution.
- **Reason not selected:** Weakens separation of duties.
- **Reconsider when:** Not expected for authorization semantics.

## Delivery plan

### Phase 1: Architecture foundation

- **Outcome:** QART, RFC, repository classification, and explicit ownership/non-ownership.
- **Scope:** Documentation and planning only.
- **Validation:** Cross-repository boundary review against current project contracts/issues.
- **Rollback:** Revert organization documentation; no runtime behavior changes.

### Phase 2: Contract reconciliation

- **Outcome:** Existing component issues are updated or narrowly scoped children are created only for real contract gaps.
- **Scope:** Dubnium generation lifecycle, Invokrum evolution-context provenance, Keylix sender profile where needed, Anthesis exact candidate authorization mapping.
- **Validation:** Each project accepts its own contract changes; no central lab contract overrides them.
- **Rollback:** Component changes remain independently versioned and revertible.

### Phase 3: Reference conformance

- **Outcome:** One deterministic end-to-end context-evolution scenario in `ryjen/governed-agent-evolution`.
- **Scope:** Fixtures, adapters/glue, positive and negative exact-binding tests.
- **Validation:** Candidate substitution, stale approval, context drift, and unauthorized-generation tests fail closed.
- **Rollback:** Lab-only; no production deployment dependency.

### Phase 4: Runtime evolution

- **Outcome:** Governed runtime/config generation activation with health and rollback evidence.
- **Scope:** Dubnium-led implementation with Anthesis governance and optional Invokrum/Keylix integration as authority-relevant.
- **Validation:** Exact activation identity and rollback tests.
- **Rollback:** Restore previously authorized generation.

## Validation and success measures

- Organization and project ownership can be determined unambiguously from the catalogue/RFC.
- A reference candidate can be reconstructed from exact runtime, context, decision, and evidence identities.
- Modifying an authority-relevant candidate after authorization causes activation to fail closed.
- Possession of a valid sender credential cannot substitute for Anthesis authorization.
- Successful evaluation cannot authorize activation by itself.
- A protected authority-evolution attempt requires stronger external approval/control.
- The lab demonstrates at least one positive and one adversarial flow without defining a competing production contract.

## Risks

| Risk | Impact | Mitigation or contingency | Owner |
| --- | --- | --- | --- |
| Contract duplication across repositories | High | Compose existing contracts first; lab remains non-authoritative | `.github` + project owners |
| Common-root compromise undermines separation | High | Document deployment assumptions; separate key/policy/activation roots for higher-risk profiles | Operators/project owners |
| Policy misses a hidden capability expansion | High | Treat model/provider/tool/capability deltas as explicit policy input | Anthesis + Dubnium |
| Evolution complexity outruns observability/recovery | High | Start with deterministic low-risk scenario and require rollback evidence | Dubnium |
| Key rotation creates operational fragility | Medium | Rotate at meaningful trust-boundary changes, not every edit | Keylix consumers/operators |
| Lab becomes accidental product authority | Medium | Catalogue non-responsibilities; contract changes must land in authoritative repos | `.github` owner |

## Unresolved questions

1. Which existing Anthesis object(s) should carry the exact evolution-candidate subject without creating a parallel envelope?
2. What minimum runtime-generation contract should Dubnium expose for conformance and activation verification?
3. Which context changes are authority-relevant enough to require an Invokrum identity in the authorization subject?
4. What exact trust-boundary changes require Keylix key rotation versus re-authorization under the existing sender identity?
5. What minimum independent post-activation health evidence is required before a generation is considered accepted?

These questions should be answered through component-owned contract reconciliation and the first deterministic lab scenario, not by expanding this organization RFC into component implementation specifications.

## Decision and disposition

- **Disposition:** Draft / pending review
- **Decision date:**
- **Conditions of acceptance:** Cross-repository responsibility review; no conflicting authority model introduced; catalogue classification accepted.
- **Required ADRs:** Determine after review; avoid duplicating the accepted RFC unless a narrower durable decision needs separate recording.
- **Required specifications:** None initially; component-specific contracts only as demonstrated necessary.
- **Next executable slice:** Classify `ryjen/governed-agent-evolution` in the repository catalogue, reconcile existing Anthesis, Dubnium, Invokrum, and Keylix work against this RFC, then execute the first deterministic lab scenario after RFC disposition.
