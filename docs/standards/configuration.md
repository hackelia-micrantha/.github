# Configuration and executable-extension trust standard

Configuration is data that selects behavior inside an existing authority boundary. It is not a substitute for identity, policy, approval, provenance, or capability authorization.

This standard defines organization-wide defaults for configuration composition and for language-neutral executable extensions discovered through Unix process conventions such as Git-style PATH subcommands.

It complements:

- [CLI interoperability](cli-interoperability.md) for process and machine-interface semantics;
- [CLI design and UX](cli-design-and-ux.md) for command discovery and extension presentation;
- [Security engineering](security.md) for execution authority, secrets, and supply-chain risk;
- [Tool result trust](tool-result-trust.md) for evidence versus authority;
- [Releases and versioning](releases.md) for artifact identity, signatures, provenance, SBOMs, and rollback.

Repository-local standards may be stricter. They must not weaken the authority boundaries below without an explicit reviewed security exception.

## Core invariants

Preserve these distinctions:

```text
configuration value != authority
discovery           != executable identity
executable identity != provenance
provenance          != principal identity
principal identity  != capability grant
capability request  != authorization
authorization       != successful execution
```

A schema-valid, signed, known, installed, or PATH-discovered executable does not gain authority merely from that property.

A lower-trust configuration source MUST NOT widen a higher-authority boundary.

## Configuration classes

Classify configuration by what it is allowed to decide.

### Authoritative / governed configuration

This class controls trust, authority, security, deployment, or protected resource admission.

Examples include:

- trusted plugin/extension registries;
- accepted artifact signer or provenance identities;
- Keylix execution-principal/profile policy;
- Capability Gateway capability/provider registration;
- Anthesis policy and approval requirements;
- repository/provider allowlists;
- credential, signer, or service identity selection;
- filesystem, network, process, device, and sandbox ceilings;
- privileged service/socket ownership.

Authoritative configuration MUST come from an explicitly trusted owner such as reviewed deployment configuration, a governed registry, or another repository-defined authority.

It MUST fail closed when required values are missing, ambiguous, unverifiable, stale beyond the documented policy, or supplied only by a lower-trust layer.

### Product / domain configuration

This class selects application semantics within an already-authorized boundary.

Examples include:

- feature or algorithm selection;
- bounded service behavior;
- non-secret resource limits inside an admitted ceiling;
- domain mappings and typed operation defaults.

Product configuration MUST NOT mint new authority. A request to exceed an authoritative ceiling is a denial or validation error, not a precedence conflict.

### User / repository composition

This class captures project- or user-owned preferences and local composition.

Examples include:

- output/rendering preferences;
- local workspace selection;
- project-specific paths within an admitted root;
- non-authoritative aliases;
- extension-local behavior that cannot widen host authority.

Repository content is untrusted input when it crosses a trust boundary. Merely committing a configuration file does not make it host policy.

### Ephemeral invocation overrides

CLI flags and environment variables may override ordinary values when the owning contract permits it.

They MUST remain bounded by the same authority ceiling as the underlying operation. A command-line option or environment variable MUST NOT:

- register a new trusted executable;
- select an unapproved credential, signer, provider, or capability;
- widen filesystem/network/process authority;
- replace an authenticated principal;
- disable required provenance verification;
- bypass policy, approval, or target binding.

### Defaults

Defaults are non-authoritative fallback values. A default MUST NOT silently create authority merely because no stronger configuration was supplied.

## Precedence and authority ceilings

For ordinary values within one authority class, prefer the conventional precedence:

```text
CLI > environment > repository/user config > defaults
```

A repository MAY use a different deterministic order when its domain requires one.

**Precedence applies only among values that are eligible to decide the same thing.** It does not cross authority classes.

For example:

```text
authoritative allowedRoot = /srv/workspaces

CLI --workspace=/srv/workspaces/project-a   -> eligible
CLI --workspace=/etc                       -> denied
repo config allowedRoot=/                   -> ignored/denied as authority input
```

Where multiple authoritative sources exist, their precedence or intersection MUST be explicitly defined by the owning architecture. Security-sensitive composition SHOULD prefer narrowing/intersection semantics over last-writer-wins.

## Schema, parsing, and merge semantics

Supported configuration surfaces MUST define:

- a schema or typed contract where practical;
- a configuration/contract version;
- accepted locations and discovery rules;
- deterministic merge semantics;
- unknown-field behavior;
- canonicalization rules when equality, hashing, signatures, policy, or approval binding depends on exact values;
- compatibility and migration rules;
- reload/restart behavior.

Security-sensitive configuration SHOULD reject unknown fields unless forward compatibility is explicitly designed and tested.

Merging maps/lists MUST define whether values replace, append, intersect, or merge by key. Do not use implicit deep-merge behavior for authority-bearing values.

A configuration parser MUST bound input size, nesting, includes, recursion, and expansion according to risk.

## Provenance and explainability

A consumer SHOULD retain enough non-secret provenance to answer:

- which source supplied an effective value;
- which schema/version parsed it;
- which higher-authority ceiling constrained it;
- whether a value was defaulted, inherited, overridden, narrowed, ignored, or denied;
- which immutable configuration identity/digest was used for a consequential decision.

Where useful, expose a read-only `config explain`, `config status`, or `doctor` surface. Such diagnostics MUST redact secrets and MUST NOT turn provenance claims into authorization.

For consequential effects, bind the effective authoritative configuration identity to the resulting evidence when that identity can materially affect the outcome.

## Secrets and credentials

Ordinary configuration SHOULD contain secret references, not secret values.

Prefer:

- credential/service names;
- opaque secret references;
- file-descriptor or service-mediated access;
- deployment-owned credential bindings.

Do not allow repository/user config, environment variables, extension manifests, or model/tool output to select arbitrary private-key paths, agent sockets, credential helpers, signing executables, or privileged token sources unless the owning security design explicitly makes that selection part of the authorized contract.

Diagnostics MUST NOT print resolved secret values.

## Filesystem and reload safety

For authority-bearing local configuration, define and test as applicable:

- expected owner/group and permission mode;
- symlink policy and path containment;
- atomic write/update behavior;
- partial-write handling;
- stale-read and reload semantics;
- rollback or last-known-good behavior;
- whether runtime reload is allowed or restart is required.

A privileged process MUST NOT search an untrusted user's configuration paths merely for convenience.

When verification and execution are separated in time, bind the operation to the exact parsed configuration identity/digest or revalidate before the effect.

## Namespacing

Project and extension configuration SHOULD be namespaced to avoid accidental cross-component interpretation.

An extension must not be able to create configuration keys in another extension's or the host's authority namespace merely by choosing the same key names.

Shared keys require an explicitly owned shared schema.

# Executable extension trust profile

Unix process boundaries are the preferred language-neutral extension mechanism where process composition fits the architecture. An extension may be implemented in any language that satisfies its contract.

A Git-style executable name or PATH entry is a **discovery candidate**, not a trust record.

## Discovery and resolution

Hosts supporting executable extensions MUST define deterministic resolution and collision behavior.

According to risk, they SHOULD provide:

- an inventory of selected, shadowed, duplicate, and rejected candidates;
- a way to explain the exact selected executable;
- fail-closed behavior when a trusted/governed extension has ambiguous resolution;
- built-in/terminal namespace rules that prevent unexpected argument reinterpretation.

Do not reconstruct child execution through a shell string. Preserve argv boundaries.

For trusted/governed profiles, resolve once to an exact executable/artifact identity and execute that selected object rather than re-resolving mutable PATH state after verification.

Implementations SHOULD use an OS-appropriate technique that minimizes verification/execution TOCTOU risk. The contract is the invariant; this standard does not require one system-call API across platforms.

## Extension manifest v1

A supported trusted extension profile SHOULD expose or install a versioned manifest containing at least:

```text
manifest/schema version
logical command namespace
extension/product identity + version
supported host/domain protocol versions
exact executable/artifact digest or immutable identity
install/discovery source
input/output schema references
requested capability/effect names
extension-owned configuration namespace/schema
required execution/sandbox profile
provenance/signing claims where applicable
```

The manifest declares requirements and claims. It grants nothing.

The host MUST validate compatibility before treating the extension as eligible.

Manifest content originating from a repository, PATH executable, package, or downloaded artifact remains untrusted until verified according to the selected trust profile.

## Trust profiles

Do not impose one provenance mechanism on every local script.

A host MAY define profiles such as:

### Local / unverified

Suitable for low-risk user-owned extensions where ordinary Unix execution is intentionally sufficient.

Properties may include:

- PATH discovery;
- no claim of verified publisher provenance;
- no privileged credential inheritance;
- no automatic admission to protected capabilities.

### Declaratively installed

Suitable when a trusted deployment/package system already binds the extension to an immutable reviewed artifact.

Examples include a reviewed Nix/system configuration selecting an exact package/store identity.

The deployment identity is evidence about installation/provenance; it still does not grant a consequential capability.

### Sigstore-verified

Use Sigstore when publisher/build provenance and tamper-evident artifact identity are required.

Verification policy SHOULD bind the exact artifact digest to accepted Sigstore verification material and expected identity attributes such as issuer/subject or an equivalent workload identity policy.

For keyless signing, a Sigstore bundle can carry the signature/certificate plus timestamp and transparency-log verification material needed for later verification. Retain the verification material required by the selected policy.

Sigstore verification proves only the properties actually checked: artifact integrity and the accepted signing/provenance identity. It does **not** prove runtime correctness, user intent, approval, or authorization.

Do not require public-transparency-log publication for artifacts whose confidentiality model forbids it without a reviewed private/custom Sigstore design.

### Governed

A governed extension combines verified eligible executable identity with an authenticated execution principal and policy-controlled effect boundary.

A typical Micrantha flow is:

```text
PATH / package / registry discovery
        |
        v
deterministic candidate resolution
        |
        v
exact artifact identity / digest
        |
        +--> deployment provenance and/or Sigstore verification
        |
        v
eligible executable
        |
        +--> Keylix authenticated/sender-constrained execution principal
        |
        v
host admission policy
        |
        v
constrained process execution
        |
        +--> exact governed effect request
                |
                v
          Capability Gateway
                |
                v
             Anthesis
                |
                v
          domain provider / worker
```

Not every local extension needs every stage.

## Keylix boundary

Where an extension invokes a protected capability through a Keylix-supported authenticated transport/profile, use Keylix to establish the effective sender-constrained execution principal and delegation binding.

Caller-supplied manifest/config fields MUST NOT create or replace that principal.

Keylix proof-of-possession or execution-principal binding does not decide whether the requested effect is acceptable. Governance and effect authority remain with the owning policy/capability system.

Until a required Keylix profile is released and supported for the target boundary, do not represent a design proposal or pre-release profile as production identity evidence.

## Capability Gateway boundary

Executable extensions MAY request consequential effects through a project's Capability Gateway when that gateway owns the effect.

The extension:

- supplies bounded typed intent;
- does not receive provider credentials or privileged worker authority;
- cannot widen capability names/targets from configuration;
- cannot treat prior successful requests, signatures, or cached decisions as new authority.

The Capability Gateway remains an effect boundary, not a plugin loader, package manager, generic process broker, or arbitrary executable registry.

Provider registration remains owned by the gateway/deployment architecture. A project may require declarative/static provider registration even while user-facing CLI extensions are dynamically PATH-discovered.

## Process execution hygiene

For trusted/governed extension execution, apply according to risk:

- construct an explicit environment allowlist or deny sensitive inherited variables;
- do not pass ambient SSH/GPG/cloud/provider credentials unless explicitly delegated;
- set close-on-exec on non-delegated file descriptors and explicitly document passed descriptors;
- bind working directory and filesystem roots where they affect authority;
- bound output, execution time, subprocess fan-out, and resource use;
- preserve signal/cancellation semantics;
- keep stdout/stderr contracts from the CLI interoperability standard;
- prefer direct structured IPC or exact argv over shell source;
- use sandboxing such as namespaces, Landlock/seccomp, containers, or WASI/WASM only where the threat model justifies it.

WASM/component-model plugins are an optional stronger isolation profile, not the universal extension ABI.

## Evidence and observability

For governed/trusted execution, evidence SHOULD identify as applicable:

- logical extension/command identity;
- exact executable/artifact digest;
- discovery/install source;
- selected trust profile;
- Sigstore verification identity/result or equivalent provenance reference;
- Keylix principal/delegation reference where used;
- effective non-secret configuration identity;
- requested capability/effect;
- policy/decision reference;
- result/verification identity.

Do not log raw credentials, DPoP proofs, private keys, secret configuration values, or unbounded extension output.

## Validation

Test the applicable positive and negative properties.

### Configuration

- deterministic merge/precedence;
- authority ceiling cannot be widened by CLI/env/repository/user config;
- unknown/malformed security-sensitive fields fail safely;
- canonicalization produces stable identities;
- secret references do not leak resolved values;
- stale/changed authoritative configuration invalidates or revalidates bound effects.

### Extension resolution and provenance

- built-in and extension collision behavior;
- duplicate/shadowed candidate reporting;
- longest-prefix/subtree behavior where supported;
- executable replacement between discovery/verification/execution is prevented or detected;
- digest mismatch;
- invalid, expired, unavailable, or policy-rejected provenance;
- unsupported protocol/schema version;
- unsigned local profile remains distinguishable from verified profiles.

### Identity and authority

- caller metadata cannot spoof the Keylix/effective execution principal;
- valid Sigstore verification with wrong Keylix principal is rejected where principal binding is required;
- valid artifact and principal can still be denied by policy;
- denied capability cannot be obtained through alternate config precedence;
- retries/replay do not mint authority.

### Process boundary

- sensitive environment variables are absent unless explicitly delegated;
- non-delegated FDs are closed;
- stdout/stderr remain bounded and contract-correct;
- cancellation/timeout works;
- sandbox profile, when required, is actually enforced.

Canonical conformance fixtures SHOULD be reusable across implementation languages.

## Adoption

Projects adopting this standard should document:

- configuration classes and authority owners;
- configuration locations and precedence;
- extension discovery/naming/resolution rules;
- supported trust profiles;
- manifest/schema versions;
- provenance verification policy;
- Keylix profile/transport when used;
- Capability Gateway effects exposed to extensions;
- environment/FD/sandbox execution policy;
- migration and rollback from existing extension mechanisms.

Adoption MUST NOT be represented as complete until installed/runtime behavior matches the documented profile.
