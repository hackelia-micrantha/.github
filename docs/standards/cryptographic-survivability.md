# Cryptographic survivability standard

This standard defines how Micrantha projects should reason about long-lived confidentiality, authenticity, ownership, recovery, and cryptographic migration.

It complements the general [security engineering standard](security.md). It does not define custom cryptographic primitives and does not replace project-specific threat models.

## External baseline

NIST finalized the first three post-quantum cryptography standards in August 2024:

- FIPS 203 — ML-KEM for key establishment;
- FIPS 204 — ML-DSA for digital signatures;
- FIPS 205 — SLH-DSA for digital signatures.

NIST says organizations should begin migration now. Its current PQC project overview uses the transition timeline in draft NIST IR 8547 and states that NIST will deprecate and ultimately remove quantum-vulnerable algorithms from its standards by 2035, with higher-risk systems moving earlier. IR 8547 itself remains a draft transition document as of 2026.

The 2035 date is a migration/deprecation horizon. It is **not** a prediction of when a cryptographically relevant quantum computer will exist.

References:

- https://csrc.nist.gov/Projects/Post-Quantum-Cryptography
- https://csrc.nist.gov/pubs/ir/8547/ipd
- https://www.nccoe.nist.gov/applied-cryptography/migration-to-pqc

## Security objective

For material protected state, architecture should make this statement as true as practical:

> Compromise of durable ciphertext should not imply durable future decryptability.

This does not mean ciphertext can destroy itself after an attacker copies it. Once an attacker possesses all bits required for an offline attack, infrastructure-side revocation cannot reach those copies.

Cryptographic survivability instead combines:

- appropriate data encryption;
- resilient key establishment/wrapping and signatures;
- crypto-agility;
- narrow key authority;
- zero-access/client-side boundaries where useful;
- explicit retention and recovery semantics;
- controlled cryptographic erasure;
- migration before protected data outlives vulnerable algorithms.

## Required risk inputs

Projects using material cryptography should identify, at the smallest useful boundary:

- protected asset or data class;
- confidentiality horizon;
- authenticity/non-forgeability horizon where relevant;
- sensitivity/classification;
- expected retention and backup lifetime;
- current cryptographic suite/profile and version;
- key classes and custody;
- transport/key-exchange dependencies;
- signature/provenance dependencies;
- recovery and escrow dependencies;
- external cryptographic providers or protocols;
- migration, rotation, rewrap, and revocation paths.

A project does not need a universal schema for all of these fields. It does need enough explicit structure to make migration and residual risk reviewable.

## Confidentiality horizon

Long-lived secrets should have an explicit confidentiality horizon rather than assuming the currently deployed public-key cryptography remains sufficient indefinitely.

Conceptually:

```text
data class
  -> required secrecy lifetime
  -> current crypto dependency graph
  -> migration deadline
```

A useful policy representation may resemble:

```yaml
classification: customer-sensitive
confidentiality_horizon: 25y

cryptography:
  crypto_agility: required
  pq_key_protection: required
  zero_access_storage: preferred
  crypto_erasure: supported
```

Projects may use different vocabulary where their domain requires it.

## Cryptographic inventory

Inventory must follow the dependency graph rather than only the obvious storage cipher.

Include applicable:

- TLS and other transport key establishment;
- SSH;
- VPN/tailnet credentials and handshakes;
- PKI and certificates;
- JWT/JWS/COSE signing;
- package, release, artifact, provenance, and commit signing;
- KMS/HSM/TPM/Secure Enclave/StrongBox key profiles;
- database and object encryption;
- envelope encryption and key wrapping;
- client/device identity keys;
- recovery and escrow material;
- backup repositories, snapshots, WAL, object versions, and cold archives;
- encrypted exports;
- CI artifacts and caches containing protected state;
- external SaaS/provider cryptographic dependencies;
- historical formats that remain recoverable.

An application using AES-256 for payload encryption is not automatically post-quantum safe if the payload key is durably wrapped or exchanged using a quantum-vulnerable asymmetric primitive.

## Crypto agility

Where cryptography is material:

- identify algorithm suites/profiles by explicit versioned identifiers;
- keep business identity/state independent of one algorithm where practical;
- provide a path to rotate or replace keys without rewriting unrelated domain state;
- provide a path to rewrap content keys without re-encrypting large payloads when the threat model permits;
- define downgrade/fallback behavior explicitly;
- fail closed when a required cryptographic profile is unavailable rather than silently falling back to a weaker profile;
- preserve enough profile/version evidence to validate historical artifacts.

Do not design custom KEMs, signatures, hybrid combiners, ZK protocols, or cryptographic formats merely to claim agility. Prefer reviewed standards and protocol-specific constructions.

### Application-level agility contract

For application-facing cryptographic design, assess agility as a set of separate concerns rather than one maturity score:

- operation coupling — whether callers must name algorithms or algorithm-specific parameters for ordinary use;
- key-creation coupling — whether creation permanently binds application logic to one algorithm/profile;
- provider coupling — whether algorithm semantics are inseparable from one library, KMS, HSM, device, or execution backend;
- decoupling mechanism — where algorithm/provider choices are configured and versioned;
- selection authority — which trusted principal or policy may choose or change accepted cryptographic profiles;
- algorithm migration — whether an existing logical cryptographic role can move to a new algorithm/profile without rewriting unrelated domain state;
- provider migration — whether custody/execution can move independently of algorithm/profile where the security model permits.

Use this vocabulary diagnostically. A deliberately fixed protocol version may be safer than a generic abstraction when interoperability, algorithm-confusion resistance, or standards constraints require one explicit profile.

#### Stable role, exact cryptographic instance

Prefer a stable **logical role/reference** over coupling business identity to one algorithm or provider, but never let that stable reference erase the exact cryptographic instance actually used.

Conceptually:

```text
logical role / purpose
  -> versioned key instance
       -> exact algorithm/profile
       -> exact provider/custody class
       -> lifecycle state
```

A new algorithm normally means fresh key material and a new version. Historical signatures, ciphertext, envelopes, proofs, or ownership transitions must remain attributable to the exact key/profile/provider version that produced them.

Do not universally claim that two cryptographically different keys have the same security identity merely because an API preserves one opaque key name. In protocols where a public key or thumbprint participates directly in identity, sender binding, ownership, or authorization, preserve the protocol-specific identity transition explicitly.

#### Rotation, transformation, and provider migration

Keep these lifecycle operations distinct:

- **rotation** — fresh key material under the same algorithm/profile;
- **algorithm/profile transformation** — fresh cryptographic material or a reviewed compatible reconfiguration under a different algorithm/profile while preserving the intended logical role and version history;
- **provider/custody migration** — moving execution or custody to another provider, with re-keying when export is impossible or undesirable.

A single workflow may coordinate more than one operation, but evidence should state which transitions occurred.

For high-consequence or irreversible transitions, support a deterministic preflight where practical. It should establish feasibility, expected old/new profiles and providers, export/rewrap/re-key behavior, data-continuity requirements, destructive steps, rollback limits, and policy/approval requirements before mutation.

#### Intent and substitution boundaries

Intent-based selection may be useful only when candidate algorithms share a genuinely compatible caller-visible operational contract. A common primitive name alone is insufficient if algorithms differ in required context, nonce/IV handling, prehash behavior, message limits, encoding, or other caller obligations.

Where a standards-constrained protocol requires explicit algorithm/profile identifiers, preserve that explicit profile rather than inventing a local generic intent layer.

Cryptographic-selection policy is trusted control-plane state. Untrusted request, model, tool, repository, or provider content must not:

- choose the governing policy;
- widen the accepted profile/template set;
- force a weaker fallback;
- select a provider outside the authorized custody/assurance class;
- turn a discovery result or catalog entry into approval.

Discovery and inventory describe what is available; policy and authorization determine what may be used.

#### Current operations versus historical compatibility

Treat creation of new cryptographic commitments differently from historical compatibility.

When policy retires or deprecates a profile, projects may need to deny new forward/producer operations such as signing or encryption while temporarily retaining bounded reverse/consumer operations such as signature verification or decryption for historical data.

Historical validity does not imply current authority:

```text
historically valid signature / ciphertext / proof
  != currently accepted profile
  != current authorization
```

Each project must define retention, archival, compromise, destruction, and historical-verification semantics appropriate to its protocol and recovery model.

Research basis:

- Rameshan and Messmer, *An Assessment Framework for Application-Level Cryptographic Agility*, arXiv:2606.13425.
- Rameshan and Messmer, *Intent-Based Cryptographic API Design for Cryptographic Agility*, arXiv:2606.13445.

## Post-quantum migration

FIPS 203/204/205 are deployable standards, but adoption must still respect protocol, library, platform, hardware, interoperability, and operational maturity.

Projects should:

1. discover quantum-vulnerable public-key dependencies;
2. prioritize by confidentiality/authenticity horizon and blast radius;
3. make algorithms replaceable before migration becomes urgent;
4. use standardized PQ or reviewed hybrid profiles when supported by the surrounding protocol/ecosystem;
5. retain deterministic migration and rollback evidence;
6. remove obsolete vulnerable authority from backups/recovery paths, not only live systems.

Do not infer a specific "Q-day" from the 2035 migration target.

## Zero-access and client-side encryption

Where a service should not possess durable plaintext authority, prefer a design in which encryption/decryption occurs at a trusted client or narrowly trusted boundary and the service stores only ciphertext plus bounded metadata.

Conceptually:

```text
trusted client
  -> random content/data key
  -> authenticated symmetric encryption
  -> PQ-ready/versioned key wrap
  -> untrusted storage

storage does not possess:
  - plaintext
  - raw content key
  - durable private unwrap key
```

Use precise terminology:

- **zero-access/client-side encryption** describes a trust architecture in which the service does not possess plaintext/key authority;
- a **zero-knowledge proof** is a separate cryptographic mechanism for proving a statement without revealing the witness.

Do not conflate them.

## Envelope encryption and key hierarchy

Prefer small, replaceable cryptographic authority over monolithic long-lived keys.

A common pattern is:

```text
object payload
  -> random DEK
  -> authenticated encryption

DEK
  -> wrapped under tenant/object/epoch/purpose authority
```

Depending on the domain, key hierarchy may use:

- per-object DEKs;
- per-tenant KEKs;
- short-lived epochs;
- device keys;
- recovery roots;
- independently scoped signing keys.

The hierarchy should minimize blast radius and permit targeted rotation or destruction.

## Cryptographic erasure

Destroying a controlling key can make retained ciphertext unrecoverable **only when the architecture controls every required decryption path**.

A valid crypto-erasure claim must identify:

- which ciphertext/object population is affected;
- which key material is required;
- which copies/escrow/recovery paths exist;
- whether an attacker could already possess the plaintext or usable key;
- what evidence establishes key destruction or revocation;
- what backups retain historical key material.

Do not claim physical erasure of arbitrary ciphertext copies.

Do not claim that an already copied ciphertext can detect cryptanalysis or self-destruct.

## Backups and recovery

Cryptographic migration is incomplete if old backups preserve vulnerable key authority.

Backup/recovery design should record applicable:

- cryptographic profile used for stored backup material;
- key-wrapping/key-exchange dependencies;
- escrow and recovery-key profile;
- age and retention horizon;
- whether restore reintroduces retired keys or algorithms;
- rewrap/migration strategy;
- deletion/tombstone replay before restored data becomes queryable;
- validation that a restored system does not silently downgrade its crypto posture.

Historical ciphertext may remain in storage after a migration; the important question is whether historical key authority remains sufficient to recover it.

## Agent and AI systems

Treat AI models and autonomous agents as powerful untrusted principals, not cryptographic roots of trust.

Models/agents should not receive a reusable root/master key merely because they can request a protected operation.

Prefer typed, narrow authority such as:

```text
operation: decrypt
resource: object/48982
purpose: invoice-analysis
expires: 2026-09-30T09:00:00Z
output-policy: bounded
```

over:

```text
/customer/master-key
```

Applicable controls include:

- short-lived, resource/purpose-bound capabilities;
- separate authorization and key-execution components;
- opaque key handles instead of raw secret material;
- no ambient KMS/HSM/keystore authority in lower-trust agent runtimes;
- bounded plaintext exposure;
- zeroization of ephemeral plaintext/key material where practical;
- strict egress and output controls where required;
- deterministic subject/digest binding for signing and rewrap operations;
- attributable evidence for actor, capability, policy, subject, operation, result, and relevant runtime/model identity.

Do **not** scrub the attribution needed to investigate agent behavior. Minimize secrets and plaintext while preserving non-secret provenance.

## AI-assisted crypto agility

AI can be useful for:

- inventory discovery;
- dependency classification;
- migration-plan generation;
- explaining cryptographic blast radius;
- identifying likely stale configurations;
- proposing rewrap/rotation work;
- correlating repository, infrastructure, and backup evidence.

AI must not be the sole authority for:

- selecting whether a downgrade is acceptable;
- deciding that a migration succeeded;
- accepting residual risk;
- minting broad key authority;
- asserting that key destruction or secure deletion occurred.

A safer pattern is:

```text
inventory / evidence
      |
      v
AI analysis / proposal
      |
      v
deterministic validator
      |
      v
policy / human approval when required
      |
      v
narrow executor
      |
      v
independent verification + evidence
```

## Quantum-compromise blast radius

Projects with long-lived protected state should be able to reason about the consequences of one or more classical asymmetric primitives becoming insecure.

Conceptually:

```text
assume primitive/profile P is broken
    |
    v
find wrapping / exchange / signing edges using P
    |
    v
find reachable keys, objects, identities, backups, and historical artifacts
    |
    v
classify readable / forgeable / still-protected / indeterminate state
```

The dependency calculation should be deterministic and evidence-backed. An AI system may explain or prioritize the result, but it should not invent the graph or decide reachability by semantic judgment alone.

Useful output can include:

- affected objects/data classes;
- oldest/newest vulnerable material;
- backup/archive exposure;
- affected signing/provenance chains;
- migration blockers;
- independent/PQ protection still in force;
- uncertainty or missing inventory.

## Evidence

Material cryptographic lifecycle events should preserve bounded non-secret evidence where useful:

- exact subject/object/profile;
- old and new suite/profile IDs;
- key handle or opaque identity, not raw key;
- actor/requester;
- policy/approval reference where required;
- operation type: generate, wrap, unwrap, rewrap, rotate, revoke, destroy, recover;
- result and verifier;
- timestamp/epoch;
- implementation/configuration revision.

Evidence must not become a second secret store.

## Threat-model triggers

Refresh focused analysis when a change affects:

- long-lived protected data;
- key hierarchy or custody;
- crypto provider or secure hardware;
- asymmetric algorithm/profile;
- encrypted backup/recovery;
- owner/device identity;
- signing/provenance;
- zero-access/client-side encryption;
- agent access to plaintext or key operations;
- deletion/crypto-erasure claims;
- migration/downgrade/fallback behavior.

## Validation

Where applicable, test:

- unsupported/retired profile rejection;
- downgrade resistance;
- stale key/profile replay;
- cross-tenant/object key confusion;
- unauthorized unwrap/decrypt/sign requests;
- rewrap without payload corruption;
- old-key retirement after migration;
- restore from historical backup without re-enabling retired authority;
- key destruction/crypto-erasure evidence;
- hardware/KMS unavailable with no insecure fallback;
- copied ciphertext remaining non-self-describing and non-self-destructive;
- quantum-compromise blast-radius fixtures using synthetic dependency graphs.

## Exceptions

A project that intentionally retains a quantum-vulnerable asymmetric dependency beyond its relevant migration horizon should record:

- affected asset/data;
- required confidentiality/authenticity lifetime;
- algorithm/profile;
- reason migration is blocked;
- compensating controls;
- harvest-now/decrypt-later exposure where applicable;
- owner;
- review/expiry date;
- migration/removal plan.

## Non-goals

This standard does not:

- predict quantum-computer timelines;
- require every project to implement PQC immediately;
- require a custom KMS, HSM, KEM, signature scheme, ZK system, or blockchain;
- claim that encrypted data can self-destruct after offline theft;
- guarantee deletion from third-party copies outside project control;
- make AI a cryptographic or risk-acceptance authority.
