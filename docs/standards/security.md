# Security engineering standard

This standard defines engineering controls for Micrantha repositories. It complements the vulnerability-reporting instructions in `.github/SECURITY.md`; it does not replace them.

Security is a system property created by architecture, implementation, delivery, operations, and governance. A security label or scan does not prove that a trust boundary is correct.

## Security ownership

Each repository should identify the owner of material security decisions, residual-risk acceptance, incident response, and release blocking. Organization-wide authority follows [`GOVERNANCE.md`](../../GOVERNANCE.md).

Risk acceptance must be explicit, scoped, time-bounded where appropriate, and attributable to a human decision owner. An automated tool, model, laboratory, or pull-request author cannot accept its own residual risk.

## Threat-model triggers

Perform or refresh focused threat analysis when a change materially affects:

- authentication, authorization, delegation, approval, or identity;
- trust boundaries among users, services, agents, tools, runners, devices, or repositories;
- secrets, keys, tokens, signing identities, or sensitive configuration;
- personal, regulated, customer, or security-sensitive data;
- executable content, plugins, package installation, build systems, or supply-chain inputs;
- network exposure, tenancy, isolation, or resource limits;
- policy enforcement, audit evidence, provenance, or bypass paths;
- persistence, recovery, deletion, migration, or retention;
- privileged mobile, infrastructure, or deployment capabilities.

Use the smallest artifact that resolves the risk: issue analysis, QART slice, threat model, RFC, ADR, or focused security review.

## Core requirements

### Least privilege and authority

- Grant only the capability, resource, scope, and lifetime required.
- Separate proposal, authorization, execution, and evidence responsibilities where material.
- Prevent confused-deputy behavior by binding requests to the initiating actor, intended resource, and approved parameters.
- Make delegation explicit, bounded, revocable, and attributable.
- Treat administrative, release, signing, and deployment authority as separate capabilities.

### Secure defaults and failure posture

- Default to denial or a safe non-effect state at authorization and verification boundaries.
- Define fail-open, fail-closed, quarantine, retry, override, and recovery behavior explicitly.
- Avoid silent fallback that weakens authentication, policy, integrity, or encryption.
- Bound retries, resource consumption, and recursive or agentic execution.

### Input and data handling

- Treat repository content, prompts, logs, files, schemas, network responses, user data, and generated output as untrusted until validated for the consuming boundary.
- Validate structure, type, size, encoding, path, origin, freshness, and authorization as applicable.
- Prevent traversal, injection, unsafe deserialization, command construction, and unintended interpretation across language or protocol boundaries.
- Minimize collection and retention of sensitive data.
- Redact secrets and personal data from logs, evidence, errors, tests, and artifacts.

### Secrets and cryptographic material

- Do not commit secrets, private keys, production tokens, or sensitive credential material.
- Use scoped secret stores and short-lived credentials where supported.
- Separate development, CI, release, and production identities.
- Rotate credentials after suspected exposure and preserve only non-sensitive incident evidence.
- Document key ownership, rotation, revocation, recovery, and algorithm-agility expectations where cryptography is material.

### Dependency and supply-chain controls

- Use lockfiles or equivalent reproducible resolution.
- Review new privileged, executable, native, build-time, and release dependencies more carefully than ordinary libraries.
- Pin third-party CI actions and verify downloaded artifacts where practical.
- Generate SBOM, provenance, checksums, or signatures according to release and supply-chain risk.
- Define vulnerability triage, update, exception, and end-of-support handling.
- Avoid executing install scripts or generated code with broader privileges than required.

### Isolation and resource boundaries

- Isolate untrusted workloads from persistent credentials, private networks, host devices, and reusable runner state.
- Apply filesystem, process, network, device, tenant, and resource limits appropriate to the threat model.
- Treat containers as a boundary aid, not proof of isolation.
- Avoid running untrusted fork code on privileged or persistent self-hosted infrastructure.

## Agentic and AI-assisted systems

Agentic workflows require explicit control boundaries:

1. **Actor** — who or what requested the action.
2. **Proposal** — the exact intended effect and parameters.
3. **Policy** — the rules and context used to evaluate it.
4. **Approval** — accountable authorization where required.
5. **Execution** — the bounded capability that performs the effect.
6. **Evidence** — attributable records of inputs, decisions, approvals, execution, and result.
7. **Recovery** — cancellation, rollback, containment, or remediation.

Required properties should include, according to risk:

- least-privilege tools and scoped credentials;
- deterministic gates for material effects;
- separation between generated instructions and trusted policy;
- prompt-injection and untrusted-content resistance;
- approval binding to the exact action or digest;
- replay and stale-approval protection;
- provenance and tamper-evident evidence;
- bounded memory access and sensitive-context handling;
- bypass detection and fail-closed behavior;
- human override that is authenticated, attributable, and auditable.

A supervisor/specialist pattern does not by itself provide authorization. The supervisor, memory system, policy authority, and executor must have separate, explicit responsibilities.

## Logging, evidence, and privacy

Security evidence should answer who requested, who approved, what was evaluated, what changed, when it occurred, and which code/configuration/policy versions were involved.

Logs and evidence must not become a second secret store. Apply classification, access control, redaction, retention, integrity protection, and deletion rules. Record hashes or references instead of sensitive payloads when sufficient.

## Security validation

Validation should test protected invariants and denial behavior, including applicable:

- unauthorized and cross-tenant access;
- malformed, oversized, stale, replayed, or tampered input;
- approval mismatch and bypass attempts;
- secret and sensitive-data leakage;
- dependency, runner, and build-boundary failures;
- degraded dependencies and partial execution;
- rollback, revocation, and incident containment.

Security tools support review but do not replace architecture analysis, manual inspection, or boundary-level tests.

## Vulnerability and incident handling

- Follow the repository or organization private reporting path.
- Do not place exploit details, secrets, or affected-user data in public issues.
- Contain active exposure before broad cleanup.
- Preserve enough evidence for diagnosis without spreading sensitive material.
- Track remediation, credential rotation, release impact, disclosure, and prevention work separately when needed.
- Convert incident learning into tests, controls, documentation, or decisions.

## Security exceptions

An exception should record:

```markdown
## Security exception

- Control or requirement:
- Scope and affected assets:
- Rationale:
- Compensating controls:
- Residual risk:
- Risk owner:
- Approval date:
- Expiry or review date:
- Removal plan:
```

Expired exceptions are unresolved findings. They must not silently become permanent architecture.
