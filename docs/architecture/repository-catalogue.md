# Micrantha repository responsibility catalogue

This catalogue records organization-level project classification, maturity, authoritative responsibility, and important non-responsibilities. It is the default source for deciding where work, contracts, issues, and public claims belong.

Detailed implementation, support, licensing, and release evidence remains in each authoritative repository. When this catalogue conflicts with current repository evidence, treat the conflict as governance drift: correct the catalogue or explicitly change ownership through review rather than silently relying on the inconsistency.

**Catalogue baseline:** 2026-08-03

## How to use this catalogue

Before creating or moving work, determine:

1. Which repository owns the affected contract or outcome?
2. Is the work product implementation, composition, provider integration, laboratory evidence, community packaging, or public communication?
3. Does the change alter another repository's authoritative boundary?
4. Is current repository placement transitional?
5. Which decision owners and repositories must approve the change?

A runtime dependency does not imply governance authority. A laboratory finding does not automatically change a product contract. A public site does not create product truth. A distribution composes components without assuming their internal authority.

## Repository role patterns

### Source and community repositories

Where a project has source and community repositories:

- the **source repository** owns implementation, internal architecture, and declared product contracts;
- the **community repository** owns explicitly delegated public packaging, documentation, examples, releases, or community-facing material;
- the community repository must not make unsupported product claims or fork an authoritative contract without an accepted decision;
- release and synchronization direction must be documented by the project.

### Engine and provider adapters

- the **provider-neutral engine or core repository** owns shared behavior and contracts;
- each **adapter** owns provider-specific authentication, entitlement, packaging, and execution behavior;
- adapter limitations must not silently weaken the engine's security or evidence guarantees;
- commercial or private delivery rights are governed by the applicable license and repository policy, not by this catalogue alone.

### Product and laboratory repositories

- the **product or solution repository** owns supported behavior and public contracts;
- a **laboratory** owns scenarios, fixtures, test harnesses, generated evidence, and experimental integration code;
- laboratories may discover product defects or propose contract changes, but the authoritative product repository accepts or rejects those changes;
- laboratories should remain independently runnable where their purpose is contract or compatibility validation.

### Distribution and component repositories

- a **distribution** owns composition, supported integration versions, defaults, operator workflows, and distribution-level behavior;
- included components retain authority over their own contracts and security boundaries;
- the distribution may constrain or wrap component behavior, but cross-boundary changes require the affected component's decision process.

## Core organization and public surfaces

| Repository or surface | Classification | Maturity | Authoritative responsibility | Does not own |
| --- | --- | --- | --- | --- |
| [`hackelia-micrantha/.github`](https://github.com/hackelia-micrantha/.github) | Organization governance and community-health meta repository | Active | Organization defaults, governance, lifecycle, work-item conventions, prompt library, inherited issue/PR templates, public organization profile | Repository-specific implementation, licenses, CODEOWNERS, releases, branch rules, or deployment configuration |
| [`hackelia-micrantha/web`](https://github.com/hackelia-micrantha/web) | Public website | Active | `micrantha.com` presentation, public navigation, and evidence-backed ecosystem communication | Product contracts, maturity by assertion, repository ownership, or support promises unsupported by authoritative projects |
| [`profile/README.md`](../../profile/README.md) | GitHub organization profile | Active | Concise public organization overview and project map | Canonical lifecycle or responsibility rules; it projects this catalogue and governance model |

## Solutions and deployable systems

| Project and locations | Classification | Maturity | Authoritative responsibility | Does not own |
| --- | --- | --- | --- | --- |
| **Anthesis** — [`anthesis`](https://github.com/hackelia-micrantha/anthesis), public/community surfaces including [`anthesis-community`](https://github.com/hackelia-micrantha/anthesis-community) | Governance and provenance solution | Incubating | Actor, policy, capability, approval, decision, evidence, attribution, and provenance contracts for authorizing agentic effects | Agent planning, model routing, general memory, operating-system distribution, or effect execution itself |
| **Dubnium** — [`dubnium`](https://github.com/hackelia-micrantha/dubnium), [`dubnium-community`](https://github.com/hackelia-micrantha/dubnium-community) | Agentic development distribution | Incubating | Reproducible distribution composition, model/runtime integration, supervisor-specialist orchestration, bounded executor integration, operator experience, and distribution defaults | Anthesis policy authority, independent laboratory truth, or internal contracts of composed components |
| **Envuscator** — source and community surfaces including [`envuscator-community`](https://github.com/hackelia-micrantha/envuscator-community) | Mobile build-time configuration-obfuscation solution | Incubating | Provider-neutral obfuscation model, local execution, protected configuration transformation, and customer-controlled build boundary | General application security, hosted custody of customer source by implication, or provider-specific adapter behavior outside delegated contracts |
| **Amaryllis** — [`amaryllis`](https://github.com/hackelia-micrantha/amaryllis) and public surfaces | Mobile inference SDK and toolkit | Experimental | Mobile/on-device inference APIs, SDK behavior, packaging, and supported platform integrations | General tool registry, unrelated computer-vision applications, or governance authority for agentic effects |
| **Fortunes** — source and public service surfaces | Service and Slack integration | Stable | Fortune service behavior, Slack integration, and its deployment contract | Organization-wide service architecture standards or unrelated chat integrations |
| **Veil** — source and public service surfaces | Image privacy and obfuscation service | Experimental | Image concealment/privacy utility behavior and service integration | Mobile build obfuscation, general computer-vision inference, or security guarantees beyond its declared scope |

## Laboratory, infrastructure, templates, and reference integrations

| Project and locations | Classification | Maturity | Authoritative responsibility | Does not own |
| --- | --- | --- | --- | --- |
| **Anthesis Governance Lab** — currently transitional at [`ryjen/anthesis-governance-lab`](https://github.com/ryjen/anthesis-governance-lab) | Contract laboratory and executable testbed | Incubating | Canonical scenarios, fixtures, test harness behavior, compatibility reports, evidence bundles, and laboratory release artifacts | Anthesis product contracts, risk acceptance, or production policy decisions |
| **Dubnium Governed Agent Demo** — integration material currently spans Dubnium and Anthesis work | Reference integration and governed-agent testbed | Experimental | End-to-end demonstration evidence for planning, governance, approval, bounded execution, and audit flow | Independent product authority; it does not redefine Anthesis or Dubnium contracts |
| **Hyperion** — [`hyperion`](https://github.com/hackelia-micrantha/hyperion) | Reproducible infrastructure laboratory and stack | Incubating | K3s, GitOps, cluster, infrastructure, deployment, and operational patterns declared by the repository | Product-level governance semantics or application contracts deployed onto the infrastructure |
| **Bluebell** — [`bluebell`](https://github.com/hackelia-micrantha/bluebell) | Kotlin Multiplatform SDK template | Stable | Reusable KMP project structure, build conventions, publishing pattern, and template validation | Product behavior of repositories generated from or inspired by the template |
| **Digitalis** — source and [`digitalis-community`](https://github.com/hackelia-micrantha/digitalis-community) | Mobile attestation and secure-configuration laboratory | Experimental | Attestation experiments, secure configuration-delivery contracts under test, fixtures, and public laboratory material | General mobile identity, Eyespie product behavior, or organization-wide configuration policy |
| **Myosotis** — source and [`myosotis-community`](https://github.com/hackelia-micrantha/myosotis-community) | MCP and LLM tool-registry laboratory | Experimental | Tool metadata, discovery, registry experiments, and related integration evidence | Dubnium orchestration, Amaryllis inference behavior, or tool execution authorization |
| **Eyespie** — source and distribution material | Computer-vision and mobile-inference laboratory/application | Experimental | Eyespie gameplay/application behavior, MediaPipe and platform integration, and its release/build surfaces | Amaryllis general SDK contract, Digitalis attestation contract, Bluebell template contract, or Envuscator engine contract |

## Authority relationships

### Anthesis and Dubnium

- Dubnium proposes, plans, and executes effects within its runtime and distribution boundary.
- Anthesis evaluates governed effects and returns allow, approval-required, or deny decisions with attributable evidence.
- Dubnium must not treat model intent or supervisor authority as a substitute for Anthesis decisions where governance is required.
- Anthesis must not silently become a general agent runtime, planner, or executor.
- Shared integration contracts require accepted decisions in both authoritative projects.

### Anthesis and Governance Lab

- The lab validates public contracts, scenarios, evidence properties, and compatibility.
- A failing laboratory scenario is evidence of a possible product, fixture, versioning, or expectation defect; it is not self-interpreting.
- Product-contract changes are accepted in Anthesis and then reflected in the lab.
- Laboratory-only experimental scenarios must be labeled so they are not mistaken for supported contract requirements.

### Dubnium and Hyperion

- Hyperion owns reusable infrastructure and deployment patterns.
- Dubnium owns distribution composition and operator behavior.
- Dubnium may consume Hyperion patterns without making Hyperion responsible for agent-runtime semantics.
- Shared runner, cluster, Nix, or GitOps changes should identify whether the authoritative outcome is infrastructure-wide or distribution-specific.

### Eyespie integration dependencies

- Bluebell provides reusable KMP template/build patterns.
- Amaryllis provides mobile inference SDK capabilities when adopted.
- Digitalis provides attestation or secure-configuration behavior when integrated.
- Envuscator provides build-time configuration protection when integrated.
- Eyespie owns its final application composition and user-visible behavior; dependencies retain authority over their own contracts.

## Transitional repository placement

Some implementations and reference integrations remain under [`ryjen`](https://github.com/ryjen) or in repositories whose final public/private split is still being consolidated.

Transitional placement must be recorded with:

- current location;
- intended authoritative owner;
- migration or transfer condition;
- issue and release handling during transition;
- public link that should remain stable;
- date or trigger for reassessment.

Repository location alone does not override documented architectural responsibility. Conversely, intended future ownership must not be described as completed until transfer and operational responsibility actually change.

## Unclassified or newly created repositories

A repository not listed here is not automatically a Solution, Laboratory, supported product, or public project. Before making ecosystem claims, add a catalogue entry that identifies:

```markdown
## Repository classification proposal

- Repository:
- Purpose:
- Classification:
- Maturity:
- Steward:
- Owns:
- Does not own:
- Depends on:
- Publishes:
- Public/private and licensing posture:
- Overlap or migration from existing repositories:
```

Private experiments and empty repository reservations may remain uncatalogued while Proposed, but they must not be used as evidence of implemented capability.

## Change control

Update this catalogue when:

- a repository is created, transferred, renamed, split, merged, superseded, or archived;
- source/community or engine/adapter boundaries change;
- a contract moves between repositories;
- project maturity changes;
- a transitional repository moves into the organization;
- public documentation or release ownership changes materially.

Changes that alter authority or a cross-repository contract should link the relevant QART, RFC, ADR, lifecycle record, or organization-owner decision. Editorial corrections and evidence refreshes may use a normal documentation pull request.
