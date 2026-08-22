# RFC 0001: Governed agent actuation

- **Status:** Proposed
- **Decision owners:**
  - organization-level boundary — organization owner;
  - `hackelia-micrantha/anthesis` governance/authorization boundary — Anthesis repository steward or explicitly delegated decision owner;
  - `hackelia-micrantha/invokrum` portable invocation/evidence boundary — Invokrum repository steward or explicitly delegated decision owner;
  - `hackelia-micrantha/keylix` sender-binding/conformance boundary — Keylix repository steward or explicitly delegated decision owner;
  - runtime/distribution integration boundary — owning runtime repository steward or explicitly delegated decision owner.
- **Reviewers:** Repository maintainers for affected boundaries
- **Date:** 2026-08-12
- **Last reviewed:** 2026-08-21

## Context

AI-assisted engineering increasingly fails at a boundary different from simple model knowledge: a model may know the applicable security principle yet fail to apply the correct control at the authoritative implementation boundary, apply it incompletely, or improve apparent security while breaking required functionality.

The SoK *AI Secure Code Generation: Progress, Pitfalls, and Paths Forward* (arXiv:2606.25195) describes this as a knowledge-actuation gap and distinguishes security knowledge from effective implementation and exploit resistance.

Micrantha's architecture already separates model reasoning, runtime execution, governance/authorization, protocol security, and evidence. The cross-repository decision is how those responsibilities compose into an action that can be called governed, functional, and security-effective without collapsing repository authority or creating a shared implementation database.

This RFC establishes that boundary model.

## Decision

Micrantha will treat **actuation** as the transition from proposed intent to an explicitly authorized action whose relevant functional and security properties can be verified with attributable, version-bound evidence.

The cross-repository architecture follows this model:

```text
model / agent reasoning
        |
        | proposed intent
        v
runtime / orchestration
        |
        | exact portable invocation + requirements
        v
Invokrum contract boundary
        |
        | non-authoritative requested facts / exact subject identity
        v
Anthesis governance / authorization
        |
        | decision ref + bounded granted authority
        v
runtime / executor enforcement
        |
        +--> functional verification
        |
        +--> security / adversarial verification
        |       |
        |       +--> Keylix or other domain verifier facts
        |
        v
attributable execution / enforcement evidence
        |
        v
Anthesis evidence interpretation / governance outcome / residual risk
```

No single repository is required to implement every stage. Cross-repository coupling occurs through stable, versioned contracts and exact references rather than shared internal state.

## Responsibility boundaries

### Runtime / orchestration

The agent runtime or orchestrator owns workflow coordination and execution materialization: gathering context, proposing an operation, compiling an accepted authority plan into runtime constraints, invoking bounded capabilities, producing candidates, running checks, and coordinating bounded functionality-preserving repair.

The runtime owns actual enforcement mechanisms within its execution boundary. It does **not** make model output authoritative, define Anthesis governance policy, or treat its own evidence as authorization.

### Invokrum

Invokrum owns the portable, model-neutral invocation and execution-evidence boundary. Existing accepted contracts include:

- `invokrum.invocation/v1` — exact task/context subject, declared capability requirements, constraints, budgets, termination conditions, outputs, and evidence requirements;
- `invokrum.execution-evidence/v1` — non-authoritative execution evidence bound to the exact invocation;
- `invokrum.security-requirements/v1` — portable trust/sink/security-property requirements attached by exact digest;
- `invokrum.security-enforcement-evidence/v1` — executor-produced enforcement facts and security-property outcomes bound to exact invocation/execution/requirements artifacts.

Invokrum owns interoperability shape, exact binding, validation, and fail-closed compatibility semantics. It does **not** own runtime execution authority, governance policy/approval, application authorization, or the truth of domain-specific cryptographic properties.

Schema-valid enforcement evidence does not authenticate its own producer. Trusted integrations must bind it to an authenticated executor/enforcement boundary independently.

### Anthesis

Anthesis owns governance and authorization semantics: policy requirements, approval decisions, granted authority, exceptions, evidence interpretation, provenance, residual risk, and trusted-state promotion.

Anthesis's RFC-0054 execution evidence/replay envelope remains the canonical governance-side logical envelope. It explicitly distinguishes what was authorized, what the runtime attempted, and what occurred.

Anthesis does not become the privileged execution runtime or protocol verifier.

### Keylix

Keylix owns sender-constrained OAuth/DPoP security semantics, typed `VerifiedSenderBinding`, replay/nonce/request-binding behavior, and bounded security evidence such as `SenderBindingEvidence`.

The first implemented cross-repository pilot uses:

- `KX-DPOP-013` — exact proof-key/token `cnf.jkt` sender binding;
- `KX-OBS-003` — bounded structured sender-binding evidence.

Keylix establishes protocol/security facts. It does **not** establish application authorization, governance acceptance, task correctness, or general execution authority.

### CI and test harnesses

Executable test infrastructure provides objective feedback for functional and security properties. CI evidence is part of the assurance path, so runners, fixtures, harnesses, and verifier identity are part of the relevant trust boundary and must not be treated as infallible.

## Authorization and evidence are distinct

A governed execution must preserve the difference between:

1. **authorization** — the accountable decision that permits a bounded action;
2. **enforcement** — the runtime/executor mechanism that constrains the action;
3. **verification** — evidence about whether required functional/security properties held;
4. **governance interpretation** — whether the evidence is sufficient, fresh, and applicable to satisfy a control or policy requirement.

An executor-side `allow`/`deny` security-enforcement result is evidence about enforcement/property evaluation. It is **not** interchangeable with an Anthesis policy/approval decision.

Evidence, receipts, previous success, cryptographic sender binding, and schema validity cannot mint or widen authority.

## Actuation evidence vocabulary

Controls and requirements may progress through the following conceptual states:

```text
required -> declared -> implemented -> verified -> effective
```

These states are deliberately distinct:

- **required** — policy or contract says the property must hold;
- **declared** — an implementation or actor claims the control is present;
- **implemented** — an identifiable enforcement mechanism exists at an appropriate boundary;
- **verified** — attributable evidence demonstrates specified functional/security properties against the exact relevant subject;
- **effective** — governance accepts the verified mechanism as satisfying the required control for the stated scope and evidence horizon.

This vocabulary is an interoperability/diagnostic model. It does not replace Anthesis's canonical policy-decision vocabulary or require every repository to persist these exact strings.

`verified` and `effective` are not permanent truths. Evidence becomes stale or inapplicable when the bound code, configuration, task state, policy, dependency, environment, identity, or threat assumptions materially change.

For diagnosis, implementations should be able to represent at least these outcomes:

| Outcome | Expected control/mechanism present | Required security property holds |
| --- | --- | --- |
| Principled success | Yes | Yes |
| Secure by other means | No or different mechanism | Yes |
| Compliant but vulnerable | Yes | No |
| Actuation failure | No | No |

Alternative mechanisms are valid when they preserve the functional contract and satisfy the required security property. Governance must not equate syntactic compliance with security effectiveness.

## Conceptual actuation record

Cross-repository integrations should converge on a small, versionable record or linked record set capable of identifying:

- action/operation identity;
- exact task, candidate, artifact, or effect subject identity/version/digest;
- actor/workflow identity where available;
- required control/security-property identifiers;
- policy and contract version/digest;
- **authorization decision reference and outcome**;
- **bounded granted authority/capability scope**, including expiry/revision when relevant;
- approval or exception reference when applicable;
- relevant trust boundary/security-sensitive operation;
- enforcement point/plan identity or digest;
- executor/enforcement decision and failure class where applicable;
- functional verification result;
- security/adversarial verification result;
- provenance/evidence references and verifier identity where applicable;
- freshness/replay applicability;
- residual risk or unresolved/indeterminate state.

The authorization fields are required whenever the action is governed. A policy digest alone is insufficient: evidence must be able to identify the particular decision and granted scope under which execution occurred.

This is a conceptual interoperability contract, not a mandate for one shared database schema. Existing repository-local contracts SHOULD be composed before new shared fields are invented.

## Invariants

1. **Model output is not authorization.** A model may propose or explain an action but cannot grant itself authority.
2. **Authorization is attributable.** Governed execution binds the exact applicable decision and bounded granted scope; policy identity alone is insufficient.
3. **Controls execute at authoritative boundaries.** Security instructions in prompts are advisory unless enforced by the component that owns the relevant capability/resource boundary.
4. **Evidence is not authority.** Execution evidence, verifier results, receipts, cryptographic proofs, and prior success cannot independently grant or widen permission.
5. **Security fixes preserve the functional contract.** A change that blocks an exploit by breaking required behavior is not a successful actuation.
6. **Compliance is not exploit resistance.** Presence of a recommended API, rule, or policy marker is insufficient without appropriate behavioral evidence.
7. **Equivalent defenses are allowed.** Verification should prefer required properties over one syntactic implementation when multiple mechanisms are valid.
8. **Evidence is attributable and version-bound.** Conclusions identify the subject/configuration/contracts/environment to which they apply.
9. **Cross-repository contracts are versioned.** Integrations depend on stable schemas, protocols, capabilities, and semantics rather than repository internals.
10. **Evidence is minimized.** Secrets, bearer tokens, private keys, reusable proofs, raw sensitive identifiers, unnecessary source content, and sensitive findings are not embedded in cross-repository evidence.
11. **Denial is safe.** Missing, stale, unverifiable, unsupported, mismatched, or ambiguous required context cannot silently widen capabilities.
12. **Verification is independent where practical.** The same unconstrained model that generated a claim should not be the only mechanism used to establish that claim as true.
13. **Subject change invalidates prior verification when material.** A repaired/new candidate receives a new attributable identity and must reacquire applicable verification/authorization as required.

## Security and compliance considerations

### Threats in scope

The architecture must remain robust against at least:

- prompt injection or malicious model output attempting to widen authority;
- confused-deputy behavior and over-broad capabilities;
- forged or caller-supplied executor/security facts;
- stale task/policy/authorization/evidence reuse after material subject change;
- attacker-controlled data reaching security-sensitive sinks through unexpected encodings or paths;
- path traversal, symlink escape, or equivalent boundary bypasses where filesystem access is involved;
- forged, replayed, substituted, or misattributed evidence;
- compromised or incorrectly configured runners/test harnesses;
- authentication replay, rebinding, nonce misuse, and key substitution in applicable authorization flows;
- repair loops that eliminate required functionality in order to satisfy a security test;
- evidence or cryptographic identity facts being mistaken for application authorization.

### Trust boundaries

The model is untrusted with respect to authorization and evidence. Tool/runtime boundaries, policy decision points, execution hosts, CI runners, evidence stores, identity systems, and verifier integrations are explicit trust boundaries whose guarantees are documented by their owning repositories.

### Evidence handling

Evidence should be content-addressed or otherwise attributable where practical, carry enough provenance to reproduce/invalidate a conclusion, and follow least-data principles. Public coordination artifacts must not expose private repository locations or sensitive implementation findings.

## Existing implementation evidence

Implementation may precede acceptance of this organization RFC, but it does not by itself make the RFC accepted.

Current evidence demonstrating that the proposed boundary is implementable includes:

- Invokrum ADR-0003 / issue #68: `invokrum.invocation/v1` and `invokrum.execution-evidence/v1`;
- Invokrum ADR-0004 / issue #69 / PR #97: `invokrum.security-requirements/v1` and `invokrum.security-enforcement-evidence/v1`, exact cross-document binding, fail-closed semantics, and a Keylix sender-binding pilot;
- Keylix `KX-DPOP-013`, typed `VerifiedSenderBinding`, and `KX-OBS-003` bounded evidence;
- Anthesis RFC-0054: canonical execution evidence/replay envelope with explicit authority, activity, outcomes, and replay linkage;
- Anthesis evidence-bundle verification work in #126.

These artifacts remain authoritative only within their owning repositories. This RFC defines how their responsibilities compose across repository boundaries.

## Alternatives considered

### Security prompting alone

Rejected as an authority mechanism. Prompting remains useful for reasoning quality but cannot establish enforcement or verification.

### One shared cross-repository implementation/schema

Rejected. A universal domain model would create unnecessary coupling between execution, governance, protocol testing, and orchestration. Shared semantics should remain intentionally smaller than repository-local models.

### Put the architecture in Anthesis

Rejected. Anthesis owns governance semantics but should not become architectural authority for unrelated execution and verification components.

### Put the architecture in Invokrum

Rejected. Invokrum owns portable invocation/evidence interoperability, not execution authority, governance policy, or domain-verifier truth.

### Put the architecture in the agent runtime

Rejected. Orchestration/execution should not own governance or authorization semantics merely because it coordinates effects.

### Rely on CI pass/fail only

Rejected. CI is an execution mechanism, not a complete assurance model. Evidence needs property identity, provenance, subject binding, authorization linkage, and enough context to distinguish functional, security, and governance outcomes.

## Consequences

### Positive

- Security knowledge, authorization, control implementation, verification, and governance acceptance become independently observable.
- Repository responsibilities remain narrow and testable.
- Agent repair loops can optimize joint functional/security correctness instead of security appearance alone.
- Alternative valid defenses can be accepted without hard-coding one implementation pattern into governance.
- Evidence can become a stable interoperability surface without becoming an authorization surface.

### Costs and risks

- Versioned evidence/contracts introduce compatibility work.
- CI/test infrastructure becomes part of the assurance trust model.
- Some properties remain expensive or impossible to prove automatically; `unknown`/`indeterminate` and residual risk need first-class handling.
- Poorly chosen shared fields can create accidental coupling. The interoperability record must remain intentionally small and compose existing contracts first.

## Rollout / implementation plan

### Phase 0 — architecture and authority

- Review and disposition this RFC through the named decision-owner roles above.
- Maintain the umbrella issue as the mutable coordination surface.
- Keep repository-local ADRs/issues authoritative for implementation.
- Ensure affected public repositories are present in the canonical repository catalogue/registry before routing cross-repository work.

### Phase 1 — concrete sender-binding pilot

The first interoperability pilot is now concrete rather than hypothetical:

1. Keylix owns `KX-DPOP-013` exact sender binding and `KX-OBS-003` safe evidence projection.
2. Invokrum carries exact invocation/security requirements and executor-produced property/enforcement evidence without defining Keylix semantics.
3. The positive fixture binds exact requirements/invocation/execution/evidence and reports satisfied properties.
4. The controlled wrong-key fixture reports `KX-DPOP-013 = violated` while the bounded evidence-projection property remains satisfied, producing deterministic denial.
5. Anthesis consumes these facts through its existing evidence/replay authority and decides their governance meaning; it does not import Keylix/Invokrum internals.

### Phase 2 — Anthesis control-effectiveness mapping

Map verified external security-property evidence into governance interpretation without creating a second evidence envelope or policy vocabulary:

- reuse RFC-0054 authority/evidence/replay linkage;
- reuse the portable evidence-bundle verification surface where appropriate;
- distinguish property verification from policy result;
- represent stale/failed/indeterminate evidence explicitly;
- determine whether `required -> implemented -> verified -> effective` needs only a profile/spec mapping or a narrow existing-RFC amendment.

### Phase 3 — runtime joint verification loop

Extend the existing bounded runtime evaluation transaction:

```text
candidate -> functional verification
          -> security/adversarial verification
          -> joint classification
          -> retain/reject/escalate
          -> at most bounded authorized repair -> new candidate -> reverify
```

Repairs remain bounded by the functional contract, consumed budget, and applicable capability/authorization scope. Security verification never grants repair authority.

### Phase 4 — hardening and measurement

- provenance/producer-authentication hardening;
- evidence freshness/invalidation and replay rules;
- compatibility/conformance suites for shared contracts;
- metrics for joint functionality/security outcomes and actuation failure modes.

## Success criteria

The architecture should make it possible to measure, per relevant scope:

- joint functional + security pass rate;
- proportion of required controls reaching a verified/effective governance interpretation;
- compliant-but-vulnerable rate;
- adversarial bypass/regression rate;
- evidence completeness, producer attribution, authorization linkage, and provenance;
- stale/invalidated evidence detection;
- repair-loop regressions against the functional contract;
- unauthorized-execution detection when policy identity exists but no matching decision/grant exists.

No target percentage is set in this RFC; repository-local baselines and risk appetite determine thresholds.

## Rollback strategy

Until an integration is explicitly adopted by an owning repository, shared actuation/evidence contracts remain additive and feature-gated. Repository-local behavior can fall back to prior interfaces without weakening an already-required security control.

Breaking changes to an adopted cross-repository contract require versioning or a migration path. Superseding this RFC does not invalidate historical evidence; evidence retains the semantics/version under which it was produced.

## Approval and disposition

Acceptance requires explicit disposition by the decision-owner role for every affected authoritative repository. Maintainer review, implementation, merge, silence, or absence of objection does not substitute for that disposition.

The disposition record must identify:

- each affected repository and accountable decision owner;
- accepted trade-offs;
- resulting repository-local ADRs or existing ADRs that satisfy the decision;
- implementation/migration/validation obligations;
- any residual risk requiring separate acceptance.

Repository-local implementation decisions remain subject to each repository's own governance.

## Related decisions and work items

- [Cross-repository architecture and planning](../README.md)
- [Repository responsibility catalogue](../repository-catalogue.md)
- [Engineering work-item guide](../../engineering/work-items.md)
- [RFC template](../../engineering/templates/rfc.md)
- Coordination epic: `hackelia-micrantha/.github#11`
- Anthesis workstream: `hackelia-micrantha/anthesis#156`
- Invokrum portable invocation/evidence boundary: `hackelia-micrantha/invokrum#68`
- Invokrum security requirements/enforcement evidence: `hackelia-micrantha/invokrum#69`, PR #97
- Keylix pilot workstream: `hackelia-micrantha/keylix#20`
- *AI Secure Code Generation: Progress, Pitfalls, and Paths Forward*, arXiv:2606.25195 — https://arxiv.org/abs/2606.25195
