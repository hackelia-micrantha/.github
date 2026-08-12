# 🌿 Micrantha

**Engineering resilient software systems.**

Micrantha is an engineering studio and open-source ecosystem focused on secure, observable platforms and disciplined AI-assisted development systems. The work explores how modern software can remain **understandable, operable, and secure** as systems evolve over time.

Core areas of focus include **platform engineering**, **mobile systems**, **infrastructure automation**, and **governed agentic development**.

🌐 [https://micrantha.com](https://micrantha.com)

---

## 🌱 Philosophy

Micrantha treats software as a **living ecosystem**—one that evolves through observation, iteration, and refinement rather than a one-time construction effort.

```mermaid
flowchart LR
  D[Design] --> I[Implementation]
  I --> O[Observation]
  O --> R[Refinement]
  R --> D
```

| Garden element | Engineering meaning |
| --- | --- |
| Soil | Infrastructure and architectural foundations |
| Seed | Initial design and constraints |
| Water | Iteration and engineering effort |
| Sunlight | Observability and real-world feedback |
| Flower | Delivered system |
| Garden | Ecosystem of systems maintained over time |
| Compost | Completed work whose useful ideas feed newer systems |

The objective is simple: build systems that **remain understandable and maintainable as they grow**.

---

## ⚙️ Engineering focus

### Platform engineering

* Reproducible environments and opinionated distributions
* Safe delivery through GitOps and CI/CD
* Secrets management and configuration hygiene
* Observability-first operations
* Explicit runtime, workload, and trust boundaries

### Mobile systems

* Android, iOS, React Native, and Kotlin Multiplatform
* Mobile authentication flows and platform hardening
* On-device inference and governed device capabilities
* Application attestation and secure configuration
* Build-time obfuscation and cryptographic agility

### Agentic development

* Local-first agentic systems and model routing
* Deterministic prompt-overlay composition and attestation
* Deterministic governance of proposed effects
* Bounded, reviewable, and reversible automation
* Traceability from design through execution and evidence
* Context engineering, reusable skills, and governed memory

### Security engineering

* OAuth, PKCE, workload identity, sender constraints, and bounded token lifecycles
* Proof-of-possession for OAuth, MCP, and agentic workloads
* Threat modeling and secure SDLC practices
* Secrets management and supply-chain security
* Security treated as a **system property** rather than a feature

---

## 🗺️ How the projects fit together

Micrantha is easier to understand as several **project families** rather than one dependency graph.

```mermaid
flowchart TB
  C["Agentic"]
  M["Mobile + edge"]
  I["Infrastructure"]
  L["Labs + conformance"]
  X["Stable / compost"]

  I --> C
  I --> M
  L -.-> C
  C -.-> M
```

The boxes are **families, not layers that every system must traverse**:

* **Agentic:** Dubnium, Invokrum, Anthesis, and Keylix
* **Mobile + edge:** Myosotis, Amaryllis, Digitalis, Envuscator, Bluebell, and Eyespie
* **Infrastructure:** Hyperion
* **Labs + conformance:** Anthesis Governance Lab and governed-agent demos
* **Stable / compost:** Fortunes and Veil

Most projects intentionally solve one narrow problem and remain independently useful.

### 1. Governed agentic control plane

The core agentic path has four distinct responsibilities:

```mermaid
flowchart LR
  D["Dubnium"] -->|compose| I["Invokrum"]
  I -->|context| R["Agent / model"]
  R -->|effect| A["Anthesis"]
  A -->|deny| N["No effect"]
  A -->|allow| D
  D -.->|PoP| K["Keylix"]
  K --> S["External service"]
```

Each project answers a different question:

| Project | Responsibility |
| --- | --- |
| **Dubnium** | Where does the agent run, how is work routed, and how are allowed effects executed within bounded capabilities? |
| **Invokrum** | What exact instruction/context set entered the invocation, and can it be reproduced and attested? |
| **Anthesis** | Is a proposed effect permitted, does it require approval, and what evidence records the decision? |
| **Keylix** | When credentials are used, can their use be cryptographically bound to the intended sender instead of remaining replayable bearer credentials? |

**Keylix is conditional defense in depth**, not a mandatory hop for every agent action. It does not replace identity, OAuth token validation, scopes, TLS, or Anthesis policy.

Model routing, specialist selection, memory, and scheduling remain Dubnium capabilities rather than additional peer layers in this diagram.

### 2. Mobile and edge systems

Mobile projects form a separate family. They may integrate with agentic systems, but they are not part of the core agent execution path.

```mermaid
flowchart LR
  APP["Mobile app"] --> MY["Myosotis"]
  MY --> DEV["Device"]
  APP --> AM["Amaryllis"]
  AM --> MODEL["Model"]
  DI["Digitalis"] -.-> APP
  EN["Envuscator"] -.-> APP
  BL["Bluebell"] -.-> MY
  BL -.-> DI
  EY["Eyespie"] -.-> AM
```

**Myosotis is not an MCP/LLM tool registry.** Its current direction is healthcare-first governed mobile capabilities for agentic systems: narrow device operations, device-local policy, explicit operator consent, attributable execution, and deterministic failure behavior.

**Amaryllis** provides on-device multimodal AI and governed component/runtime primitives. **Digitalis** focuses on application trust, attestation, and secure configuration. **Envuscator** adds build-time protection. **Bluebell** provides reusable Kotlin Multiplatform SDK patterns. **Eyespie** remains an experimental consumer of mobile and computer-vision techniques.

### 3. Infrastructure and deployment

Hyperion is infrastructure rather than an application-domain dependency.

```mermaid
flowchart LR
  H["Hyperion"] --> T["OpenTofu / Terraform"]
  T --> A["Ansible"]
  A --> K["K3s"]
  K --> F["Flux + Kustomize"]
  F --> W["Micrantha workloads"]
```

It provides reproducible infrastructure and GitOps patterns that can host Micrantha services without becoming part of their application-level trust model.

### 4. Laboratories and conformance

Laboratory projects exist to **challenge architecture rather than become hidden production dependencies**.

```mermaid
flowchart LR
  GL["Governance Lab"] --> A["Anthesis"]
  GD["Governed Agent Demo"] --> D["Dubnium"]
  GD --> A
```

The Governance Lab exercises policy contracts and adversarial scenarios independently. Governed-agent demos provide vertical integration evidence across runtime and governance boundaries.

### 5. Stable work and compost

**Fortunes** and **Veil** are stable projects with no active product roadmap. They remain useful as completed reference systems, but both are candidates for **composting** when their remaining operational or reference value no longer justifies maintenance.

Composting means retiring the active project while preserving useful patterns, lessons, or reusable components elsewhere in the ecosystem.

---

## 🔭 Current engineering direction — August 2026

* **Invokrum v0.1.0** establishes deterministic local composition, lockfile verification, provenance, and attestable effective context.
* **Keylix** has an accepted v0.1 security design for OAuth DPoP and sender-constrained agent/MCP workloads; implementation remains pre-release.
* **Dubnium** continues to own the local-first runtime, supervisor, model-routing, specialist, memory, scheduling, and bounded-execution concerns.
* **Anthesis** remains the policy, approval, evidence, and provenance authority rather than absorbing runtime responsibilities.
* **Myosotis** is now positioned around governed mobile capabilities, especially healthcare and regulated field workflows.
* **Amaryllis** is an active 0.1.x React Native foundation for on-device multimodal AI and governed AI-enabled UI.
* **Digitalis** and **Envuscator** continue to address different mobile-security phases: runtime/application trust versus build-time hardening.
* **Fortunes** and **Veil** are stable, complete work with no planned feature trajectory and are future compost candidates.

The recurring design principle is **separation of authority**: context composition, policy, execution, credentials, application trust, and infrastructure should remain explicit boundaries rather than collapse into one agent platform.

---

## 🌿 Maturity and lifecycle

**Maturity** describes technical stability. **Lifecycle** describes whether Micrantha is actively investing in the project. They are deliberately separate.

### Maturity

| Stage | Meaning |
| --- | --- |
| **Prototype** | Early exploration or architectural experimentation |
| **Incubating** | Active implementation with stabilizing contracts |
| **Stable** | Reliable interfaces and demonstrated operational usefulness |

### Lifecycle

| State | Meaning |
| --- | --- |
| **Active** | Current design or implementation investment |
| **Maintenance** | Supported with limited feature work |
| **Complete** | No planned feature trajectory; retained while useful |
| **Compost** | Retired as an active project after useful ideas or components are preserved |

---

## 📦 Project map

| Project | Family | Role | Maturity | Lifecycle |
| --- | --- | --- | --- | --- |
| **[Dubnium](https://github.com/hackelia-micrantha/dubnium-community)** | Agentic | Local-first agentic development and operations runtime | Incubating | Active |
| **[Invokrum](https://github.com/hackelia-micrantha/invokrum)** | Agentic | Deterministic prompt-overlay composition and attestation | Incubating | Active |
| **[Anthesis](https://anthesis.micrantha.com)** | Agentic | Governance, approval, provenance, and evidence | Incubating | Active |
| **[Keylix](https://github.com/hackelia-micrantha/keylix)** | Agentic / Security | Sender-constrained OAuth and proof-of-possession primitives | Prototype | Active |
| **[Myosotis](https://github.com/hackelia-micrantha/myosotis-community)** | Mobile / Agentic | Governed mobile capabilities for healthcare and regulated workflows | Prototype | Active |
| **[Amaryllis](https://amaryllis.micrantha.com)** | Mobile / AI | On-device multimodal AI and governed component/runtime primitives | Incubating | Active |
| **[Digitalis](https://github.com/hackelia-micrantha/digitalis-community)** | Mobile / Security | Application attestation, trust, and secure configuration | Prototype | Active |
| **[Envuscator](https://github.com/hackelia-micrantha/envuscator-community)** | Mobile / Security | Build-time configuration obfuscation and delivery hardening | Incubating | Active |
| **[Bluebell](https://github.com/hackelia-micrantha/bluebell)** | Mobile | Kotlin Multiplatform SDK template and patterns | Stable | Maintenance |
| **Eyespie** | Mobile / Lab | Computer-vision and mobile inference experiments | Prototype | Active |
| **[Hyperion](https://hyperion.micrantha.com)** | Infrastructure | Reproducible K3s/GitOps infrastructure stack | Incubating | Active |
| **[Anthesis Governance Lab](https://github.com/ryjen/anthesis-governance-lab)** | Laboratory | Executable governance contracts and adversarial scenarios | Incubating | Active |
| **Dubnium Governed Agent Demo** | Laboratory | Vertical runtime/governance integration testbed | Prototype | Active |
| **[Fortunes](https://fortunes.micrantha.com)** | Reference | Lightweight service and Slack integration | Stable | Complete → Compost |
| **[Veil](https://veil.micrantha.com)** | Reference | Image-obfuscation and privacy experiment | Stable | Complete → Compost |

> Some Micrantha implementations and reference integrations currently live under [`ryjen`](https://github.com/ryjen) while ownership and public distribution boundaries are consolidated. Repository placement is transitional; architectural responsibility should remain explicit.

---

## 🧠 Engineering background and development

Micrantha is informed by more than 15 years of engineering across mobile, backend, infrastructure, platform engineering, and software security, including production mobile systems used by millions of users.

Current public credential and development trajectory:

* **Associate of ISC2** — verified public designation supporting secure-SDLC, secure-design, threat-modeling, and application-security governance work
* **Agentic / AI governance credential** — planned; specific program or provider to be selected
* Continued practical development through Micrantha's governed-agent, application-security, platform, and secure-AI projects

Credential names are kept conservative: planned study is not presented as certification, and public designation follows issuer requirements.

---

## 📊 Operational posture

Micrantha treats **operability as a first-class design constraint**.

Typical practices include:

* GitOps and reproducible infrastructure
* logs, metrics, traces, and structured evidence
* runbooks for known failure modes
* small blast radii and reversible changes
* CI/CD guardrails and supply-chain validation
* incident and integration feedback loops

---

## 🔐 Security posture

Micrantha treats security as an **architectural property of the system**.

Common principles include:

* threat modeling during system design
* explicit trust and authority boundaries
* fail-closed authorization and verification
* sender-constrained credentials where replay resistance matters
* deterministic and attestable agent context where instructions affect authority
* secrets management and rotation
* dependency and supply-chain hygiene
* SBOMs, artifact signing, provenance, and evidence where appropriate

The goal is not to make every project depend on every security component. The goal is to make the applicable trust boundaries **visible, composable, and independently testable**.

---

## 📬 Contact

Ryan Jennings  
Micrantha Software Solutions

🌐 [https://micrantha.com](https://micrantha.com)

---

> Systems that grow without discipline eventually collapse under their own complexity.
