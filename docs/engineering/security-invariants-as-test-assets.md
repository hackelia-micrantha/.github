# Security invariants as reusable testing assets

**Status:** exploratory cross-project design note; not a new normative schema, policy engine, test runner, or mandatory CI gate.  
**Decision posture:** compose existing Micrantha testing and governance contracts first; promote only proven reusable semantics.  
**Related standard:** [Testing and validation](../standards/testing.md).

## Problem and principle

Security checks are often scattered among unit tests, integration scripts, code review notes, and threat models. An agent may generate both code and tests, then report success using expectations derived from the same faulty implementation. A readable test alone does not establish a security property.

**Desired chain:**

```text
human-reviewed requirement / threat model / security invariant
    -> project-owned behavioural scenario (Given/When/Then or native equivalent)
    -> Testule plan / scenario / testability needs, if supported
    -> independently executed native component + boundary/host checks
    -> exact-subject, plan-bound evidence + explicit missing/unsupported gaps
    -> Anthesis evaluation of evidence sufficiency, if effect governance applies
    -> separately authorized effect, never authority minted by a test or model
```

The invariant specifies **what must remain true**; the scenario expresses **a representative falsifiable outcome**; the fixture DSL describes **state needed to exercise it**; the runner executes checks; Evidence describes **what was actually observed**. Do not conflate these roles.

## Ownership and reuse

| Concern | Owner / canonical surface | Constraint |
| --- | --- | --- |
| Organization testing expectations, archetypes, documentation | `hackelia-micrantha/.github` | No new execution framework or universal DSL mandate |
| Application/domain invariant and expected effect | Owning product repository, grounded in requirements and threat model | Reviewable by domain/security owners, not inferred as authoritative from implementation |
| Recurring governed failure-mode catalogue and policy-facing mappings | Anthesis gotcha registry [#219](https://github.com/hackelia-micrantha/anthesis/issues/219) | Registry/finding signals are not enforcement authority |
| Versioned scenario, data, environment and composition semantics | Testule [#7](https://github.com/hackelia-micrantha/testule/issues/7) | Reuse `TestPlan`, `TestabilityContract`, `TestScenario`, `Evidence`; no new `SecurityInvariant` core type without a demonstrated gap |
| Independent verifier requirement and evidence gaps | Testule [#30](https://github.com/hackelia-micrantha/testule/issues/30); Anthesis [#199](https://github.com/hackelia-micrantha/anthesis/issues/199) | Testule describes evidence; Anthesis decides whether it meets governed policy requirements |
| AI-assisted invariant falsification and oracle qualification | Testule [#57](https://github.com/hackelia-micrantha/testule/issues/57) | Proposed properties/tests are untrusted until reviewed and reproduced; a failed assertion may indict the oracle |
| Native test/fuzz/mutation execution | Native toolchain and authorized bounded runtime | Not a Testule or Anthesis host-action bypass |
| Initial application proof | Dubnium [#1687](https://github.com/ryjen/dubnium/issues/1687) | No-effect Gateway pilot, not physical-host production qualification |

A stable identifier/reference to a reviewed invariant may be reused by different projects. Reuse the *meaning and provenance*, not fixture code that presumes one product's identities or persistence model. Preserve versioning: materially changed expectations receive a new revision, not a silent edit that retroactively changes old evidence.

## Example: governed runner cancellation

Illustrative invariant `CAP-AUTH-001` (**example identifier only; not a registered standard**):

> A read-only actor cannot cause runner cancellation, including when authorization infrastructure is unavailable. A denial alone does not prove the absence of effects.

Human-readable, implementation-independent example:

```gherkin
Feature: Runner cancellation authorization
  Scenario: Read-only actor denied without host effect
    Given a running job and a read-only actor
    When that actor requests cancellation
    Then the operation is denied
    And no cancellation is dispatched
    And the runner remains running
    And denial evidence is recorded
```

A testable scenario should record, without necessarily creating a new DSL syntax:

- **Subject and exact identity:** source revision, built artifact when relevant, test plan/fixture revision, policy version, authenticated actor, requested capability/resource/arguments.
- **Preconditions and controls:** test runner/job, explicit clock, provider, scheduler, persistence state, deterministic fault/authorization responses; avoid hidden privileged defaults.
- **Positive control:** the eligible authorized operation succeeds when safely simulated or performed in an explicitly authorized isolated environment; a checker that always denies is not sufficient.
- **Negative properties:** deny on read-only identity, missing/unavailable policy, stale approval, replay/substitution and relevant races. Choose cases according to the actual contract.
- **Oracles:** response and ledger assertions; provider-dispatch instrumentation at the real composition boundary; independently observed host state at separately governed physical qualification. An injected mock reporting zero invocations does not rule out bypass.
- **Evidence:** native command and outcome; exact subject/environment/plan/verifier; specific test layer and observable effect; skipped/unsupported and inconclusive cases explicitly retained.

For some products a small typed scenario table is clearer and more enforceable than Gherkin. Only adopt a Gherkin runtime if communication and defect discovery gains justify step-definition and dependency cost.

## AI exploration and oracle independence

Use AI as an **untrusted scenario/property proposer**, never as the sole source of requirements or the acceptance oracle.

1. Start from a human-reviewed threat model, domain contract, and versioned positive/negative invariants, *not* the implementation diff alone.
2. Have AI propose edge cases, state transitions, alternative attack paths, adversarial fixtures and mutants; record generator/model/context identity for provenance.
3. Reject proposals that widen authority, assume ungrounded behaviour, expose secrets, or silently change expected outcomes. Keep generated harnesses outside the authoritative checkout.
4. Check the proposed oracle itself using vulnerable/negative and legitimate/secure positives, including a materially different secure implementation. An overconstrained oracle must not report a secure alternative as vulnerable.
5. Run bounded native tests/fuzzing/property checks in an approved environment; reduce and replay failures at exact revisions with recorded seeds/inputs. Missing isolation, timeout or harness error is **inconclusive**, not secure.
6. Independently review discovered vulnerabilities and promote only justified regression cases; neither verifier evidence nor model confidence authorizes deployment, merge, publication, or other effects.

Separate these classes in any report: **specification/fixture-only**, **executed component**, **integrated real boundary**, **physical/operational**, **oracle validity**, and **indeterminate**. These are conceptual distinctions, not a proposal to extend current Testule Evidence enums. Use existing supported native evidence and explicit limitation notes until conformance is available.

## Smallest useful proof and evaluation

Start with [Dubnium #1687](https://github.com/ryjen/dubnium/issues/1687), reusing existing Go Gateway fixture/conformance tests. Pick one policy-denial invariant, express it as reviewer-readable behaviour, and add *only missing* negative oracles. Compare native table-driven tests against a thin declarative scenario representation; do not add a new interpreter solely to parse the example.

Prove:
- existing production/fixture authority, no-effect cutover, and CI gates remain unchanged;
- reviewers can trace requirement → scenario → executed check → evidence class and revision;
- a known failure/mutation is actually detected, while a legitimate alternate implementation passes;
- actual test cost, readability, diagnosis quality and maintenance overhead are recorded;
- untested real-host effects stay explicitly unqualified.

**Decision:** retain native tests, adopt a thin local DSL, or defer. Report an evidence-backed choice; do not turn a pilot into a P0/P1 dependency or a mandatory portfolio rollout.

## Open questions

- Does the current Testule `TestScenario` composition support stable external invariant references and exact-oracle identity without changing its existing alpha schemas?
- How should Anthesis registry/gotcha identifiers be referenced without treating a registry entry as a test oracle or a policy grant?
- Which security invariants require physical-state observation beyond contract/component tests, and how are those requirements declared and gated without introducing a privileged CI bypass?
- Can deliberate oracle mutations and alternate secure implementations establish useful falsification confidence at acceptable maintenance cost?

Resolve these through existing owner issues: Testule #7/#30/#57 and Anthesis #199/#219. Escalate schema changes only if the bounded consumer demonstrates that the existing contracts cannot express the requirement.
