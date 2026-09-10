# Source exposure and distribution standard

Micrantha repositories must treat source visibility, implementation disclosure, and artifact distribution as explicit security and product decisions rather than incidental consequences of repository hosting.

Public source is not inherently insecure, and private source is not a security boundary. However, modern automated analysis materially lowers the cost of repository-scale reconnaissance, dependency correlation, implementation mapping, and candidate vulnerability discovery. Visibility therefore belongs in the threat model and release design.

## Core principles

1. Security properties must remain valid if an attacker understands the design.
2. Source privacy may raise attacker cost and protect implementation/IP, but must not substitute for secure design, least privilege, cryptographic integrity, validation, or isolation.
3. Public consumers should be able to understand supported contracts, verify releases, and operate the software without requiring access to internal implementation details unless source availability is itself a product requirement.
4. Repository visibility and distribution authority are separate concerns. A public distribution repository may expose interfaces, documentation, metadata, and verified artifacts without becoming the canonical implementation repository.
5. Release artifacts are product interfaces. Their contents must be intentional, minimal, inspectable, and validated after packaging.

## Repository roles

Projects may use one repository or a split topology depending on risk and product requirements.

### Public-source project

Use when source availability is an explicit project property or when broad review, ecosystem contribution, portability, and inspectability outweigh implementation-disclosure concerns.

The public repository may own implementation, tags, releases, packages, and documentation directly.

### Private canonical + public distribution project

Use when implementation confidentiality, reverse-engineering cost, security-sensitive defensive logic, commercial/IP concerns, or controlled disclosure are material.

Recommended topology:

```text
private canonical repository
  -> reviewed release revision
  -> hardened build/release pipeline
  -> signed/provenance-linked artifacts
  -> public distribution repository
  -> package managers / Nix flakes / consumers
```

The private canonical repository owns implementation truth and release authorization. The public distribution repository owns the public installation and verification surface without redefining upstream implementation maturity.

## Public distribution surface

A public distribution repository should expose the minimum complete consumer contract, typically including applicable items from this list:

- CLI/API/schema contracts;
- section-1 man pages for command-line tools;
- examples and integration documentation;
- release notes and compatibility information;
- version and platform metadata;
- checksums;
- signatures, attestations, or provenance;
- SBOMs where required by product or supply-chain policy;
- package-manager metadata and Nix flakes;
- verification and rollback instructions.

It should not automatically receive implementation source, internal architecture, private tests, security regression corpora, unpublished vulnerability research, defensive heuristics, operator credentials, internal build metadata, or other material merely because it is useful during development.

## Binary-oriented public packaging

When a project intentionally keeps implementation private, public package definitions must consume reviewed release artifacts rather than rebuilding from exported implementation source.

For Nix, prefer a flake that:

- fetches an immutable versioned release artifact;
- pins its cryptographic hash;
- installs the binary and required public documentation such as man pages;
- exposes a stable `packages` and `apps` interface;
- is consumed through committed `flake.lock` state in downstream systems;
- does not require access to the canonical private repository at evaluation or build time.

A source-building public flake is incompatible with an intentional private-implementation boundary because it necessarily publishes the buildable source.

## Release artifact contract

For binary-distributed command-line tools, installation should be complete and Unix-native. A release package should normally contain:

```text
bin/<tool>
share/man/man1/<tool>.1
LICENSE
README or operator documentation when useful
provenance / verification metadata as applicable
```

Packaging tests must inspect the generated archive or package, not only the source tree, and assert that required files are present with appropriate permissions.

Supported Nix packages should similarly install the executable and man page into conventional output paths and exercise both in smoke tests.

## Reverse-engineering posture

If executable code is distributed to an untrusted machine, assume a sufficiently motivated analyst can eventually recover substantial implementation behavior.

Controls may increase analysis cost, including stripped symbols, avoiding unnecessary internal strings and source paths, optimized release builds, compartmentalization, and selective obfuscation where justified. These are cost-amplification measures, not guarantees of secrecy.

Never embed secrets, private signing keys, privileged credentials, hidden authorization decisions, or other controls whose security depends on remaining unrecoverable from a client binary.

## AI-era threat model

Repository-scale AI analysis changes attacker economics but not foundational security principles.

Threat reviews for public or previously public implementations should consider that an attacker can automate:

- architecture and trust-boundary reconstruction;
- untrusted-input tracing;
- dependency and version correlation;
- security-control location and gap analysis;
- diff analysis between releases;
- fuzz-target and parser discovery;
- candidate exploit generation and prioritization.

Projects should respond by strengthening deterministic controls and minimizing unnecessary disclosure, not by assuming obscurity makes unsafe logic acceptable.

## Public history and cutovers

Removing source from the current branch of a public repository does not make previously published history private.

Before converting an existing public-source project to private implementation:

1. inventory what has already been disclosed through Git history, releases, forks, mirrors, package registries, caches, archives, and documentation;
2. decide whether the goal is merely to stop future disclosure or whether legal/security requirements justify history replacement;
3. avoid destructive history rewriting as a routine cleanup mechanism;
4. rotate any secret that was ever committed rather than relying on history deletion;
5. establish a clean distribution boundary for all future releases.

Historical implementation exposure should be treated as known prior disclosure. The new boundary primarily protects future implementation evolution.

## Security-sensitive material

Keep the following private by default when disclosure would materially increase attack capability and public availability is not required by the product contract:

- unpublished vulnerability details and exploit reproductions;
- internal red-team findings;
- high-value fuzz corpora derived from confidential failures;
- private defensive heuristics intended specifically to increase attacker cost;
- internal trust-bootstrap material;
- operational secrets and credentials;
- sensitive incident evidence.

Public security claims, protocol contracts, cryptographic algorithms, and trust assumptions should remain reviewable enough for consumers to evaluate the system. Do not hide weak security reasoning behind implementation confidentiality.

## Decision criteria

Before making implementation source public, evaluate:

- whether openness is a product/community requirement;
- contribution and ecosystem value;
- interoperability requirements;
- security-sensitive implementation detail;
- reverse-engineering and cloning cost;
- commercial/IP constraints;
- consumer need for local reproducible source builds;
- supply-chain verification requirements;
- maintenance cost of a split canonical/distribution topology.

Record material decisions in the repository architecture or an ADR/RFC when the choice affects security, licensing, contribution model, or release topology.

## Release readiness

For projects using a private canonical + public distribution topology, release readiness additionally requires:

- the public artifact corresponds to an explicitly authorized canonical revision;
- no private implementation source is unintentionally included in the distribution repository or artifact;
- package definitions consume immutable reviewed artifacts rather than unpublished source;
- signatures/checksums/provenance identify the exact artifact;
- public documentation accurately describes supported contracts without exposing unnecessary internals;
- downstream consumers pin an immutable version or lock state;
- required operator documentation, including man pages for CLIs, is packaged with the release;
- prior public-source history and residual disclosure are understood when performing a visibility cutover.

## Relationship to other standards

This standard complements:

- [Security engineering](security.md) for threat modeling and control design;
- [Releases and versioning](releases.md) for release authority and artifact evidence;
- [CLI interoperability](cli-interoperability.md) for executable and man-page contracts;
- [CI/CD](ci-cd.md) for least-privileged build and publication pipelines;
- [Repository topology and trust domains](../architecture/repository-topology-and-trust-domains.md) for canonical, public, mirror, and distribution roles.
