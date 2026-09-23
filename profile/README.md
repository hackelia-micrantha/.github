# Micrantha

**Engineering resilient, understandable, and governable software systems.**

Micrantha develops software and engineering practices spanning agentic AI, security, infrastructure, developer tooling, mobile platforms, and digital ownership. The emphasis is on **explicit authority, replaceable dependencies, reproducible operations, and evidence-backed change**.

[Website](https://micrantha.com) · [Public project and responsibility catalogue](https://github.com/hackelia-micrantha/.github/blob/main/docs/architecture/repository-catalogue.md) · [Engineering standards](https://github.com/hackelia-micrantha/.github/blob/main/docs/standards/README.md) · [Contributing](https://github.com/hackelia-micrantha/.github/blob/main/CONTRIBUTING.md)

> **Status and scope:** The organization contains working software, incubating platforms, experimental research, and public specifications. A public repository or architecture description does not imply that every described capability is implemented, released, supported, or open source. Each project's documentation owns its supported surface and maturity claims.

## Systems and boundaries

Micrantha projects are independently useful components, not a required all-in-one stack. Their integration preserves different kinds of authority:

```text
model / agent       proposes intent; does not grant permission
Anthesis            evaluates policy, capabilities, and approvals for an exact effect
governed tool       enforces the decision and performs the bounded effect
Dubnium             composes runtimes, tooling, scheduling, and operator workflows
Hyperion            provisions and converges service infrastructure
Repora              observes and reconciles explicitly scoped repository state
Invokrum / Modolia  compose exact context / resolve eligible model surfaces
Testule             describes tests and normalizes verification evidence
```

A successful test, a signed artifact, a model response, a checkpoint, or an execution log is **evidence, not authorization**. Local-first execution and data sovereignty are design goals; enforcement, network paths, credentials, and recovery still require explicit controls.

For the detailed boundary model, see [repository topology and trust domains](https://github.com/hackelia-micrantha/.github/blob/main/docs/architecture/repository-topology-and-trust-domains.md) and the [repository responsibility catalogue](https://github.com/hackelia-micrantha/.github/blob/main/docs/architecture/repository-catalogue.md).

## Explore the project families

### Governed AI and developer environments

| Project | Public entry point | Responsibility |
| --- | --- | --- |
| **Anthesis** | [Community and governance contracts](https://github.com/hackelia-micrantha/anthesis-community) | Portable, self-hostable policy and exact-effect governance for agent actions; enforcement must be provided at the actual tool, credential, or runtime boundary. |
| **Dubnium** | [Community contracts and reference material](https://github.com/hackelia-micrantha/dubnium-community) | Rebuildable engineering environments, local model integration, bounded automation, and developer operations. Public contracts are distinct from private operational configuration. |
| **Invokrum** | [Community](https://github.com/hackelia-micrantha/invokrum-community) | Deterministic prompt/context composition, manifests, and locks; context identity is not execution authority. |
| **Modolia** | [Community](https://github.com/hackelia-micrantha/modolia-community) | Deterministic model eligibility and route decisions; provider execution and retries belong to the runtime. |
| **Keylix** | [Community](https://github.com/hackelia-micrantha/keylix-community) | Sender-constrained authentication and proof-of-possession primitives; proof of sender identity does not grant application permission. |
| **Sandcastle** | [Community](https://github.com/hackelia-micrantha/sandcastle-community) | Checkpoint identity and lineage for replaceable mutable workspaces; a checkpoint does not imply trust or isolation. |

### Infrastructure, repository control, and verification

| Project | Public entry point | Responsibility |
| --- | --- | --- |
| **Hyperion** | [Community](https://github.com/hackelia-micrantha/hyperion-community) | Reproducible service infrastructure and GitOps convergence, separate from the workstation/runtime composition owned by Dubnium. |
| **Repora / repoctl** | [Repository and CLI](https://github.com/hackelia-micrantha/repora) | Explicit repository topology, observation, exact plans, stale-safe reconciliation, and execution evidence. |
| **Calathea** | [Open community core](https://github.com/hackelia-micrantha/calathea-community) | Deterministic, local-first project/workflow orientation; the reusable core is separate from private portfolio data and composition. |
| **Testule** | [Community contracts](https://github.com/hackelia-micrantha/testule-community) | Portable testability contracts and normalized evidence while native test tools retain execution responsibility. |

### Mobile, device trust, and field systems

| Project | Public entry point | Responsibility |
| --- | --- | --- |
| **Amaryllis** | [React Native platform](https://github.com/hackelia-micrantha/amaryllis) | On-device multimodal inference and offline-first AI-enabled application interfaces. |
| **Achillea** | [Community](https://github.com/hackelia-micrantha/achillea-community) | Guided outdoor-experience platform and SDK; Asterwild is the first product consumer. |
| **Bluebell** | [Kotlin Multiplatform foundation](https://github.com/hackelia-micrantha/bluebell) | Cross-platform SDK and application structure. |
| **Digitalis** | [Community](https://github.com/hackelia-micrantha/digitalis-community) | Mobile attestation and backend-authoritative secure-configuration experiments. |
| **Envuscator** | [Community](https://github.com/hackelia-micrantha/envuscator-community) | Mobile build-time configuration obfuscation and delivery tooling; obfuscation is not an authorization boundary. |
| **Myosotis** | [Community](https://github.com/hackelia-micrantha/myosotis-community) | Experimental protocols and SDK design for consent-aware, governed field-operated AI tools. |
| **Morifolium** | [Mobile engineering reference](https://github.com/hackelia-micrantha/morifolium) | An incubating mobile delivery golden path covering build, analysis, security, testing, CI, observability, and release. |

### Shared interfaces, research, and creative work

- **Phyllotaxis** — shared design-system substrate: **Venation** (layout), **Chroma** (theme values), **Lamina** (surfaces), and **Cambium** (migration tooling). Individual products retain their own identity and content.
- **MUSICPKG** — [public format, specifications, and conformance tools](https://github.com/hackelia-micrantha/musicpkg-community) for owner-bound digital music and offline playback. Published interoperability drafts do not imply a complete player or end-to-end product.
- **Anthesis Governance Lab** — [independent public testbed](https://github.com/ryjen/anthesis-governance-lab) for synthetic governance scenarios and adversarial validation; lab results do not create product policy.
- **Entanglement of Ages** — [public creative and adaptation material](https://github.com/ryjen/entanglement-of-ages-marketing) for a multi-book speculative-fiction project. Creative canon and publication decisions remain separate from engineering governance.

Additional projects, supporting components, and their authoritative responsibilities are documented in the [public catalogue](https://github.com/hackelia-micrantha/.github/blob/main/docs/architecture/repository-catalogue.md). Not every project has a public implementation repository.

## Engineering standards

The [organization defaults repository](https://github.com/hackelia-micrantha/.github) maintains shared guidance; each project owns its implementation, decisions, validation evidence, release policy, and operational constraints.

| Area | Shared practice |
| --- | --- |
| **Security and trust** | [Security engineering](https://github.com/hackelia-micrantha/.github/blob/main/docs/standards/security.md), [tool-result trust](https://github.com/hackelia-micrantha/.github/blob/main/docs/standards/tool-result-trust.md), and [source exposure and distribution](https://github.com/hackelia-micrantha/.github/blob/main/docs/standards/source-exposure-and-distribution.md): least privilege, explicit trust boundaries, and reviewed public/private publication. |
| **Design and decisions** | [QART → RFC → ADR](https://github.com/hackelia-micrantha/.github/blob/main/docs/engineering/work-items.md), [AI-assisted SDLC](https://github.com/hackelia-micrantha/.github/blob/main/docs/engineering/ai-assisted-sdlc.md), and [risk-adaptive model selection](https://github.com/hackelia-micrantha/.github/blob/main/docs/engineering/ai-model-selection.md). Frontier models are an escalation option, not an automatic requirement. |
| **Testing and delivery** | [Testing](https://github.com/hackelia-micrantha/.github/blob/main/docs/standards/testing.md), [CI/CD](https://github.com/hackelia-micrantha/.github/blob/main/docs/standards/ci-cd.md), and [releases](https://github.com/hackelia-micrantha/.github/blob/main/docs/standards/releases.md): risk-appropriate validation, independent review, reproducible artifacts, and explicit promotion authority. |
| **Tool interoperability** | [CLI standard](https://github.com/hackelia-micrantha/.github/blob/main/docs/standards/cli-interoperability.md): composable stdin/stdout, stable machine contracts, error/exit semantics, man pages, and equivalent domain semantics across CLI and orchestration transports. |
| **Documentation and iteration** | [Documentation](https://github.com/hackelia-micrantha/.github/blob/main/docs/standards/documentation.md), [project-local skills](https://github.com/hackelia-micrantha/.github/blob/main/skills/README.md), and [Compound engineering](https://github.com/hackelia-micrantha/.github/blob/main/docs/engineering/compound-engineering.md): Plan → Work → Review → Compound, turning repeated findings into the smallest reliable durable control. |

Shared standards are defaults, not a claim of uniform repository maturity or a replacement for repository-local contracts. See [governance](https://github.com/hackelia-micrantha/.github/blob/main/GOVERNANCE.md), [lifecycle](https://github.com/hackelia-micrantha/.github/blob/main/docs/governance/repository-lifecycle.md), and [contribution guidance](https://github.com/hackelia-micrantha/.github/blob/main/CONTRIBUTING.md).

**Start here:** [micrantha.com](https://micrantha.com) for the public overview; the [project catalogue](https://github.com/hackelia-micrantha/.github/blob/main/docs/architecture/repository-catalogue.md) for responsibility and status; individual public repositories for documented interfaces and current limitations.
