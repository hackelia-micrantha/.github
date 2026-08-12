# RFC 0001: Governed agent actuation

- **Status:** Proposed
- **Owners:** Cross-repository architecture
- **Reviewers:** Repository maintainers for affected boundaries
- **Date:** 2026-08-12

## Context

AI-assisted engineering increasingly fails at a boundary different from simple model knowledge: a model may know the applicable security principle yet fail to apply the correct control at the authoritative implementation boundary, apply it incompletely, or improve apparent security while breaking required functionality.

The SoK *AI Secure Code Generation: Progress, Pitfalls, and Paths Forward* (arXiv:2606.25195) describes this as a knowledge-actuation gap and distinguishes security knowledge from effective implementation and exploit resistance.

Micrantha's existing architecture already separates model reasoning, privileged execution, governance, authorization, and evidence. The missing cross-repository decision is a common model for how those responsibilities compose into an action that can be called governed, functional, and security-effective without collapsing the repositories into one shared implementation.

This RFC establishes that boundary model.

## Decision

Micrantha will treat **actuation** as the transition from proposed intent to an authorized action whose relevant functional and security properties can be verified with attributable evidence.

The cross-repository architecture follows this model:

```text
model / agent reasoning
        |
        | proposed intent
        v
runtime / orchestration
        |
        | structured operation + context
        v
execution contract and capability boundary
        |
        | policy-relevant facts
        v
governance / authorization decision
        |
        | bounded authority
        v
privileged execution
        |
        +--> functional verification
        |
        +--> security / adversarial verification
        |
        v
attributable evidence
        |
        v
governance outcome / residual risk
```

No single repository is required to implement every stage. Cross-repository coupling should occur through stable, versioned contracts rather than shared internal state.

### Responsibility boundaries

#### Runtime / orchestration

The agent runtime or orchestrator owns workflow coordination: gathering context, proposing an operation, invoking bounded capabilities, responding to test feedback, and performing functionality-preserving repair loops.

It does **not** make its own model output authoritative evidence or authorization.

#### Invokrum

Invokrum owns the privileged tool-execution boundary and deterministic capability contract. It is the natural location for machine-readable execution context such as:

- operation identity;
- capability requirements;
- trust classification of relevant inputs;
- security-sensitive operation or sink metadata;
- enforceable invariants and preconditions;
- attributable execution results.

Invokrum should remain independent of any one governance product. Its contracts expose facts and enforcement semantics rather than embedding Anthesis-specific policy logic.

#### Anthesis

Anthesis owns governance semantics: policy requirements, approvals, exceptions, evidence interpretation, provenance, and the distinction between a declared or implemented control and one that has sufficient verification to be considered effective.

Anthesis does not become the privileged execution runtime.

#### Keylix

Keylix is the first concrete adversarial-verification pilot for this architecture. Its OAuth/DPoP scenarios exercise security properties where a superficially compliant implementation can still fail at protocol boundaries such as sender binding, nonce handling, replay, rebinding, or key substitution.

Keylix remains a conformance/security testing system rather than a general governance engine.

#### CI and test harnesses

Executable test infrastructure provides objective feedback for functional and security properties. CI evidence is part of the assurance path, but the runner and harness are therefore part of the relevant trust boundary and must not be treated as infallible.

### Actuation evidence vocabulary

Controls and requirements may progress through the following states:

```text
required -> declared -> implemented -> verified -> effective
```

These states are deliberately distinct:

- **required** — policy or contract says the property must hold;
- **declared** — an implementation or actor claims the control is present;
- **implemented** — an identifiable enforcement mechanism exists at an appropriate boundary;
- **verified** — evidence demonstrates specified functional/security properties against that implementation;
- **effective** — governance accepts the verified mechanism as satisfying the required control for the stated scope and evidence horizon.

`verified` and `effective` are not permanent truths. Evidence can become stale when code, configuration, policy, dependencies, environment, or threat assumptions change.

For diagnosis, implementations should be able to represent at least these outcomes:

| Outcome | Expected control/mechanism present | Required security property holds |
| --- | --- | --- |
| Principled success | Yes | Yes |
| Secure by other means | No or different mechanism | Yes |
| Compliant but vulnerable | Yes | No |
| Actuation failure | No | No |

Alternative mechanisms are valid when they preserve the functional contract and satisfy the required security property. Governance must not equate syntactic compliance with security effectiveness.

### Conceptual actuation record

Cross-repository integrations should converge on a small, versionable record capable of identifying:

- action or operation identity;
- actor/workflow identity where available;
- required control/property identifiers;
- policy and contract version or digest;
- relevant trust boundary and security-sensitive operation;
- enforcement point or mechanism;
- functional verification result;
- security/adversarial verification result;
- provenance and evidence references;
- exception/approval reference when applicable;
- residual risk or unresolved verification state.

This is a conceptual interoperability contract, not a mandate for one shared database schema. Each repository may use its own internal representation.

## Invariants

1. **Model output is not authorization.** A model may propose or explain an action but cannot grant itself authority.
2. **Controls execute at authoritative boundaries.** Security instructions in prompts are advisory unless enforced by the component that owns the relevant capability or resource.
3. **Security fixes preserve the functional contract.** A change that blocks an exploit by breaking required behavior is not a successful actuation.
4. **Compliance is not exploit resistance.** Presence of a recommended API, rule, or policy marker is insufficient without appropriate behavioral evidence.
5. **Equivalent defenses are allowed.** Verification should prefer required properties over one syntactic implementation when multiple mechanisms are valid.
6. **Evidence is attributable and version-bound.** Security conclusions must identify the code/configuration/contracts and environment to which they apply.
7. **Cross-repository contracts are versioned.** Integrations depend on stable schemas, protocols, capabilities, and semantics rather than repository internals.
8. **Evidence is minimized.** Secrets, bearer tokens, private keys, unnecessary source content, and sensitive findings must not be embedded in cross-repository evidence.
9. **Denial is safe.** Missing, stale, unverifiable, or ambiguous authority must not silently widen capabilities.
10. **Verification is independent where practical.** The same unconstrained model that generated a claim should not be the only mechanism used to establish that claim as true.

## Security and compliance considerations

### Threats in scope

The architecture must remain robust against at least:

- prompt injection or malicious model output attempting to widen authority;
- confused-deputy behavior and over-broad capabilities;
- attacker-controlled data reaching security-sensitive sinks through unexpected encodings or paths;
- path traversal, symlink escape, or equivalent boundary bypasses where filesystem access is involved;
- stale policy, stale contracts, or stale verification evidence;
- forged, replayed, or misattributed evidence;
- compromised or incorrectly configured runners and test harnesses;
- authentication replay, rebinding, nonce misuse, and suspicious key substitution in applicable authorization flows;
- repair loops that eliminate required functionality in order to satisfy a security test.

### Trust boundaries

The model is treated as untrusted with respect to authorization and evidence. Tool/runtime boundaries, policy decision points, execution hosts, CI runners, evidence stores, and identity systems are explicit trust boundaries whose guarantees must be documented by their owning repositories.

### Evidence handling

Evidence should be content-addressed or otherwise attributable where practical, carry enough provenance to reproduce or invalidate a conclusion, and follow least-data principles. Public coordination artifacts must not expose private repository locations or sensitive implementation findings.

## Alternatives considered

### Security prompting alone

Rejected as an authority mechanism. Prompting remains useful for reasoning quality but cannot establish enforcement or verification.

### One shared cross-repository implementation/schema

Rejected. A universal domain model would create unnecessary coupling between execution, governance, protocol testing, and orchestration. Shared semantics should remain intentionally smaller than repository-local models.

### Put the architecture in Anthesis

Rejected. Anthesis owns governance semantics but should not become architectural authority for unrelated execution and verification components.

### Put the architecture in the agent runtime

Rejected for the inverse reason: orchestration should not own governance or authorization semantics merely because it coordinates execution.

### Rely on CI pass/fail only

Rejected. CI is an execution mechanism, not a complete assurance model. Evidence needs property identity, provenance, and enough context to distinguish functional, security, and governance outcomes.

## Consequences

### Positive

- Security knowledge, control implementation, verification, and governance acceptance become independently observable.
- Repository responsibilities remain narrow and testable.
- Agent repair loops can optimize joint functional and security correctness instead of security appearance alone.
- Alternative valid defenses can be accepted without hard-coding one implementation pattern into governance.
- Evidence can become a stable interoperability surface between execution and governance systems.

### Costs and risks

- Versioned evidence/contracts introduce schema and compatibility work.
- CI/test infrastructure becomes part of the assurance trust model.
- Some properties will remain expensive or impossible to prove automatically; `unknown` and residual risk need first-class handling.
- Poorly chosen shared fields could create accidental coupling. The interoperability record must remain intentionally small.

## Rollout / implementation plan

### Phase 0 — architecture and vocabulary

- Review and accept or revise this RFC.
- Establish an umbrella issue as the mutable coordination surface.
- Create repository-local design/implementation issues without duplicating the RFC.

### Phase 1 — narrow pilot

Use an authentication/security-conformance flow as the first end-to-end pilot:

1. identify a concrete security property and functional contract;
2. represent the execution/security context at the capability boundary;
3. execute positive and adversarial verification;
4. produce attributable evidence;
5. map the evidence to governance control state without requiring governance-specific logic in the executor.

Keylix and Invokrum are suitable public components for this pilot; Anthesis consumes/interprets the resulting evidence semantics.

### Phase 2 — runtime verification loop

Add a generic orchestration pattern:

```text
propose -> authorize -> execute -> functional test -> adversarial test
                  ^                                  |
                  +---------- minimal repair <-------+
```

Repairs must remain bounded by the original functional contract and capability authorization.

### Phase 3 — CI and governance integration

- standardize evidence transport/versioning;
- ingest verification evidence into governance decisions;
- gate only where policy explicitly requires the evidence;
- preserve human review and exception paths for high-impact or unverifiable cases.

### Phase 4 — hardening and measurement

- provenance and anti-replay hardening;
- evidence freshness/invalidation rules;
- compatibility and conformance suites for shared contracts;
- metrics for joint functionality/security outcomes and actuation failure modes.

## Success criteria

The architecture should make it possible to measure, per relevant scope:

- joint functional + security pass rate;
- proportion of required controls reaching `verified` and `effective`;
- `compliant but vulnerable` rate;
- adversarial bypass/regression rate;
- evidence completeness and provenance linkage;
- stale/invalidated evidence detection;
- repair-loop regressions against the functional contract.

No target percentage is set in this RFC; repository-local baselines and risk appetite determine thresholds.

## Rollback strategy

Until an integration is explicitly adopted by an owning repository, shared actuation/evidence contracts remain additive and feature-gated. Repository-local behavior can fall back to its prior interfaces without weakening an already-required security control.

Breaking changes to an adopted cross-repository contract require versioning or a migration path. Superseding this RFC does not invalidate historical evidence; evidence retains the semantics/version under which it was produced.

## Approval

Acceptance requires review from maintainers representing the affected execution, governance, and verification boundaries. Repository-local implementation decisions remain subject to each repository's own governance.

## Related decisions and work items

- [Cross-repository architecture and planning](../README.md)
- [Engineering work-item guide](../../engineering/work-items.md)
- [RFC template](../../engineering/templates/rfc.md)
- *AI Secure Code Generation: Progress, Pitfalls, and Paths Forward*, arXiv:2606.25195 — https://arxiv.org/abs/2606.25195
