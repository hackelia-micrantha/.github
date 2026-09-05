# Micrantha repository responsibility catalogue

This catalogue records organization-level project classification, maturity, authoritative responsibility, and important non-responsibilities. It is the default source for deciding where work, contracts, issues, and public claims belong.

Detailed implementation, support, licensing, and release evidence remains in each authoritative repository. When this catalogue conflicts with current repository evidence, treat the conflict as governance drift: correct the catalogue or explicitly change ownership through review rather than silently relying on the inconsistency.

**Catalogue baseline:** 2026-09-04

## How to use this catalogue

Before creating or moving work, determine:

1. Which repository owns the affected contract or outcome?
2. Is the work product implementation, composition, provider integration, laboratory evidence, community packaging, public communication, or shared engineering substrate?
3. Does the change alter another repository's authoritative boundary?
4. Is current repository placement transitional?
5. Which decision owners and repositories must approve the change?

A runtime dependency does not imply governance authority. A laboratory finding does not automatically change a product contract. A public site does not create product truth. A distribution composes components without assuming their internal authority. A trust-domain label describes context; it does not grant permission.

## Classification, role, and lifecycle

Keep these dimensions separate:

- **classification** describes the portfolio/public grouping, where applicable: solution or laboratory;
- **role** describes the primary architectural function: solution, platform, infrastructure, library/protocol, tooling, design-system substrate, laboratory/research, or meta/public surface;
- **lifecycle** describes maturity/support expectations independently of role.

Lifecycle follows the organization lifecycle model. Do not infer maturity from repository visibility, age, recent activity, or public positioning.

## Repository role patterns

### Source and community repositories

Where a project has source and community repositories:

- the **source repository** owns implementation, internal architecture, and declared product contracts unless the project explicitly documents a different split;
- the **community repository** owns explicitly delegated public packaging, documentation, examples, releases, or community-facing material;
- a public/community surface must not make unsupported product claims or silently fork an authoritative contract;
- release, projection, promotion, and synchronization direction must be documented by the project.

Some projects deliberately invert the usual assumption. For example, Calathea's public community repository owns the reusable core and normative product contracts, while its private repository owns private composition and data. The documented project boundary overrides naming convention.

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

### Shared engineering substrate

Shared engineering substrate provides reusable organization capabilities without becoming implementation authority for consuming projects.

Examples include design-system contracts, reusable testing contracts, prompt/context composition, repository-control tooling, and shared standards. Consumers remain responsible for their own product behavior, deployment, release, and repository-local constraints.

## Core organization and public surfaces

| Repository or surface | Classification / role | Maturity | Authoritative responsibility | Does not own |
| --- | --- | --- | --- | --- |
| [`hackelia-micrantha/.github`](https://github.com/hackelia-micrantha/.github) | Organization governance / meta | Active | Organization defaults, governance, lifecycle, work-item conventions, prompt library, inherited issue/PR templates, shared engineering standards, public organization profile | Repository-specific implementation, licenses, CODEOWNERS, releases, branch rules, or deployment configuration |
| [`hackelia-micrantha/hackelia-micrantha`](https://github.com/hackelia-micrantha/hackelia-micrantha) | Ecosystem coordination / meta | Active | Ecosystem registry, project relationships, aggregate maturity/status model, distribution and integration coordination | Organization-wide GitHub policy or project implementation |
| [`hackelia-micrantha/web`](https://github.com/hackelia-micrantha/web) | Public website / public surface | Active | `micrantha.com` presentation, public navigation, and evidence-backed ecosystem communication | Product contracts, maturity by assertion, repository ownership, or support promises unsupported by authoritative projects |
| [`profile/README.md`](../../profile/README.md) | GitHub organization profile / public surface | Active | Concise public organization overview and project map | Canonical lifecycle or responsibility rules; it projects this catalogue and governance model |

## Solutions, platforms, and product systems

| Project and locations | Classification / role | Maturity | Authoritative responsibility | Does not own |
| --- | --- | --- | --- | --- |
| **Anthesis** — [`anthesis`](https://github.com/hackelia-micrantha/anthesis), [`anthesis-community`](https://github.com/hackelia-micrantha/anthesis-community) | Solution / governance platform | Incubating | Actor, policy, capability, approval, decision, evidence, attribution, provenance, and trusted-state promotion contracts for governed effects | Agent planning, model routing, general memory, OS distribution, or effect execution itself |
| **Dubnium** — source currently outside the organization plus [`dubnium-community`](https://github.com/hackelia-micrantha/dubnium-community) | Solution / infrastructure + agentic distribution | Active | Reproducible workstation/distribution composition, local model/runtime integration, supervisor-specialist orchestration, bounded executor integration, operator experience, and distribution defaults | Anthesis policy/trusted-state authority or component-internal contracts |
| **Achillea** — [`achillea`](https://github.com/hackelia-micrantha/achillea), [`achillea-community`](https://github.com/hackelia-micrantha/achillea-community) | Laboratory / platform | Incubating | Platform and SDK contracts for guided outdoor experiences; Asterwild is the first product consumer | Generic mobile platform standards or unrelated game/product behavior |
| **Amaryllis** — [`amaryllis`](https://github.com/hackelia-micrantha/amaryllis) | Solution / mobile inference platform | Active | React Native/on-device multimodal inference APIs, packaging, offline-first context interfaces, and governed AI-enabled UI integration | General tool registry, unrelated computer-vision applications, or governance authority for external agentic effects |
| **Envuscator** — source including [`mobuild-envuscator`](https://github.com/hackelia-micrantha/mobuild-envuscator), public [`envuscator-community`](https://github.com/hackelia-micrantha/envuscator-community) | Solution / tooling | Incubating | Provider-neutral mobile build-time configuration obfuscation, transformation, generation/runtime integration, and bounded delivery workflows | General application security, runtime attestation, or hosted custody of customer source by implication |
| **Fortunes** — service and related component repositories | Solution / service | Stable | Fortune service behavior, web/Slack integration, and deployment contract | Organization-wide service architecture standards or unrelated chat integrations |
| **Veil** — source and public service surfaces | Solution / service | Experimental | Image concealment/privacy utility behavior and service integration | Mobile build obfuscation, general computer-vision inference, or broader security guarantees |

## Reusable engineering, context, testing, and security components

| Project and locations | Classification / role | Maturity | Authoritative responsibility | Does not own |
| --- | --- | --- | --- | --- |
| **Invokrum** — [`invokrum`](https://github.com/hackelia-micrantha/invokrum), [`invokrum-community`](https://github.com/hackelia-micrantha/invokrum-community) | Tooling / context composition | Incubating | Deterministic prompt/context composition, strict schema/compatibility validation, canonical manifests and locks, composition integrity, and host-independent contracts | Governance policy, task/workflow truth, execution authority, verifier conclusions, or task completion |
| **Keylix** — [`keylix`](https://github.com/hackelia-micrantha/keylix), [`keylix-community`](https://github.com/hackelia-micrantha/keylix-community) | Library/protocol / sender-constrained security | Incubating | JWK/thumbprint primitives, OAuth DPoP proof construction/verification, replay/nonce contracts, verified sender binding, conformance, and bounded adapters | Identity-provider policy, token-validity decisions by itself, application authorization, task correctness, workflow state, or trusted-state promotion |
| **Repora** — [`repora`](https://github.com/hackelia-micrantha/repora) | Tooling / repository control | Incubating | Explicit repository topology, observation, exact planning, stale-safe reconciliation, managed repository artifacts, posture collection, and durable execution evidence | Repository disclosure policy, general governance authorization, forge administration not explicitly implemented, or arbitrary mutation |
| **Calathea** — [`calathea-community`](https://github.com/hackelia-micrantha/calathea-community) reusable core; [`calathea`](https://github.com/hackelia-micrantha/calathea) private composition | Tooling / portfolio orientation | Incubating | Public reusable core owns deterministic portfolio/workflow contracts and executable; private repository owns portfolio data, dogfood configuration, and intentionally non-public extensions | General project truth, repository governance, or authority to execute prioritized work |
| **Modolia** — [`modolia`](https://github.com/hackelia-micrantha/modolia), [`modolia-community`](https://github.com/hackelia-micrantha/modolia-community) | Library/tooling / model-surface resolution | Incubating | Versioned model-surface registry schema, deterministic constraint evaluation, candidate ranking, route decisions, and replayable resolution records | Runtime provider routing, retries/fallback, model execution, or the authority that establishes governance constraints |
| **Testule** — [`testule`](https://github.com/hackelia-micrantha/testule) | Library/tooling / testability contracts | Incubating | Language-neutral test plans, testability/data/environment/capability contracts, adapters, evidence normalization, gap analysis, and agent-accessible bounded testing capabilities | Replacing native test runners, CI/release authority, or treating evidence as authorization |
| **Phyllotaxis** — [`phyllotaxis`](https://github.com/hackelia-micrantha/phyllotaxis) | Shared substrate / design system | Experimental | Shared semantic design tokens and themed UI substrate; Venation owns layout/primitives, with Chroma, Lamina, and Cambium as named design-system concerns | Product-specific information architecture, content, application behavior, or forcing identical branding across sites |

## Laboratory, infrastructure, templates, and reference integrations

| Project and locations | Classification / role | Maturity | Authoritative responsibility | Does not own |
| --- | --- | --- | --- | --- |
| **Anthesis Governance Lab** — currently transitional at [`ryjen/anthesis-governance-lab`](https://github.com/ryjen/anthesis-governance-lab) | Laboratory / contract testbed | Active | Canonical scenarios, fixtures, test harness behavior, compatibility reports, evidence bundles, and adversarial governance validation | Anthesis product contracts, risk acceptance, or production policy decisions |
| **Governed agent evolution/reference integrations** — bounded cross-repository lab work | Laboratory / reference integration | Experimental | End-to-end evidence for exact candidate binding, independent verification, promotion, rejection, and authority separation | Independent product authority or a fifth control plane |
| **Hyperion** — [`hyperion`](https://github.com/hackelia-micrantha/hyperion), [`hyperion-community`](https://github.com/hackelia-micrantha/hyperion-community) | Laboratory / infrastructure | Active | GitOps-first reproducible K3s infrastructure using OpenTofu, Ansible, Flux, Kustomize, and domain-specific deployment-state observation | Product-level governance semantics, trusted-state promotion, or deployed application contracts |
| **Sandcastle** — [`sandcastle`](https://github.com/hackelia-micrantha/sandcastle), [`sandcastle-community`](https://github.com/hackelia-micrantha/sandcastle-community) | Laboratory / execution-state infrastructure | Experimental | Persistent mutable-workspace checkpoints, identity/lineage, save/restore/fork/diff semantics, transient-state exclusion, storage abstraction, and retention | Runner scheduling, model execution, semantic memory, governance approval policy, or strong isolation merely from a container backend |
| **Bluebell** — [`bluebell`](https://github.com/hackelia-micrantha/bluebell) | Laboratory / KMP library | Incubating | Reusable Kotlin Multiplatform SDK/application structure and cross-platform architecture | Product behavior of consumers |
| **Digitalis** — [`digitalis`](https://github.com/hackelia-micrantha/digitalis), [`digitalis-community`](https://github.com/hackelia-micrantha/digitalis-community) | Laboratory / mobile trust bootstrap | Incubating | Backend-authoritative attestation, deterministic policy experiments, protected configuration delivery, fixtures, and public laboratory material | General mobile identity or organization-wide configuration policy |
| **Myosotis** — [`myosotis`](https://github.com/hackelia-micrantha/myosotis), [`myosotis-community`](https://github.com/hackelia-micrantha/myosotis-community) | Laboratory / governed field-tool platform | Research | Protocols and SDK architecture for governed field-operated AI tools with device-local policy, consent, provenance, and deterministic failure behavior | Dubnium orchestration, Amaryllis inference behavior, or ambient agent execution authority |
| **Morifolium** — [`morifolium`](https://github.com/hackelia-micrantha/morifolium) | Laboratory / mobile platform reference | Incubating | Versioned mobile platform-engineering golden path for build, analysis, testing, CI, security, observability, and release practice | Product-specific mobile application behavior |
| **Eyespie** — source and distribution material | Laboratory / application | Incubating | Eyespie gameplay/application behavior, computer-vision integration, and release/build surfaces | General SDK contracts of Amaryllis, Digitalis, Bluebell, or Envuscator |

## Shared engineering principles

### Unix composability

Micrantha command-line tools should expose narrow, stable interfaces that compose through standard process boundaries where practical:

- structured stdin/stdout for machine composition;
- human-readable output kept distinct from stable machine output;
- meaningful exit semantics and correct broken-pipe behavior;
- no hidden ambient mutation when a plan/review boundary is appropriate;
- man pages for supported operator-facing commands.

The normative contract is [`docs/standards/cli-interoperability.md`](../standards/cli-interoperability.md). The same semantic contracts may be consumed by a supervisor or orchestrator; orchestration should not require a second incompatible result model merely because the caller is an agent.

### Repository topology and trust domains

Repository topology is explicit rather than inferred from provider names or visibility:

```text
logical repository
  -> endpoint(s)
  -> explicit role / trust domain
  -> directed mirror, projection, promotion, import, or archive relationship
```

Canonical, private, public, agent, mirror, or recovery labels describe topology and policy context. They do not grant read, write, publish, merge, or promotion authority.

A private/public project split should normally be modeled as an explicit projection or documented source/community boundary rather than an informal bidirectional sync. See [`repository-topology-and-trust-domains.md`](./repository-topology-and-trust-domains.md).

## Authority relationships

### Governed agentic execution

For workflows spanning several Micrantha repositories, keep these responsibilities explicit:

- **Dubnium** owns runtime execution, bounded executor/specialist lifecycle, operational run state, runtime observations, and accepted verifier/check execution.
- **Invokrum** owns reproducible context identity and exact composition evidence.
- **Modolia** owns deterministic model-surface resolution when used; runtime/provider execution remains outside it.
- **Anthesis** owns policy, approval, required-evidence interpretation, provenance, and trusted-state promotion where governance applies.
- **Keylix** owns cryptographic sender binding and proof-of-possession primitives where used.
- **Testule** owns portable verification/testability requirements and normalized testing evidence where adopted.
- **Sandcastle** owns exact mutable-workspace/checkpoint state and lineage where adopted.
- **Calathea** may own deterministic portfolio/workflow prioritization state for its consumers; a priority decision does not authorize execution.
- **Repora** may execute reviewed repository-topology/reconciliation operations within its own supported contracts; topology labels or repository evidence do not independently authorize mutation.

The durable state-integrity rule is:

> A component that produces a result must not, by its own assertion alone, satisfy a verification requirement intended to establish that result as trusted.

Where verification is required:

- bind it to the exact task, candidate, artifact, source baseline, or effect revision being evaluated;
- reject stale verification after material subject change;
- preserve rejected, superseded, unavailable, and indeterminate outcomes instead of converting missing evidence into success;
- keep evidence separate from authority so receipts, logs, signatures, prior success, or proof-of-possession cannot mint permission;
- keep durable task/workflow state distinct from complete transcripts, model-private reasoning state, or advisory memory.

### Dubnium and Hyperion

- Hyperion owns reusable provisioned infrastructure and GitOps deployment patterns.
- Dubnium owns the trusted workstation/device environment, local agentic runtime, and distribution/operator behavior.
- They may interoperate without one subsuming the other's authority.

### Mobile integration dependencies

- Bluebell provides reusable KMP architecture patterns.
- Amaryllis provides local mobile inference capability.
- Digitalis provides attestation/secure-configuration behavior where integrated.
- Envuscator provides build-time configuration protection where integrated.
- Morifolium provides a reference engineering golden path.
- Product applications own their final composition and user-visible behavior; dependencies retain authority over their own contracts.

## Transitional repository placement

Some implementations and reference integrations remain under [`ryjen`](https://github.com/ryjen) or in repositories whose final public/private split is still being consolidated.

Transitional placement must record:

- current location;
- intended authoritative owner;
- migration or transfer condition;
- issue and release handling during transition;
- public link that should remain stable;
- date or trigger for reassessment.

Repository location alone does not override documented architectural responsibility. Conversely, intended future ownership must not be described as completed until transfer and operational responsibility actually change.

## Unclassified or newly created repositories

A repository not listed here is not automatically a solution, laboratory, supported product, or public project. Before making ecosystem claims, add a catalogue entry that identifies:

```markdown
## Repository classification proposal

- Repository:
- Purpose:
- Classification:
- Role:
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
