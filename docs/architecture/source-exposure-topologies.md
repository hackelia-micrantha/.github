# Source exposure and distribution topologies

> **Status:** non-normative architecture guide.  
> **Normative policy:** [`../standards/source-exposure-and-distribution.md`](../standards/source-exposure-and-distribution.md)  
> **Release contract:** [`../standards/releases.md`](../standards/releases.md)  
> **CLI contract:** [`../standards/cli-interoperability.md`](../standards/cli-interoperability.md)

This guide makes Micrantha repository topology easier to reason about without turning repository names or GitHub visibility into authority.

The important rule is that these questions are independent:

1. Is implementation source intentionally public?
2. What role does this repository play?
3. Which repository owns implementation truth?
4. Which repository/release process authorizes releases?
5. How do downstream consumers obtain the product?

A `-community` suffix answers none of those questions by itself.

## Machine-readable dimensions

The repository registry may classify a repository with the following orthogonal fields:

```yaml
sourceExposure: public | private | none
repositoryRole: canonical | distribution | projection | mirror | internal | meta
implementationAuthority: owner/repository | null
releaseAuthority: owner/repository | null
distributionMode: source | binary | package | closure | internal | none
canonicalRepository: owner/repository | null
publicDistributionRepository: owner/repository | null
```

During migration these fields are optional. Once any primary posture field is present, `sourceExposure`, `repositoryRole`, and `distributionMode` must be declared together.

`visibility` remains separate. It describes GitHub access, not product authority or source-disclosure intent.

## Topology A — public-source canonical project

Use this when the authoritative implementation is deliberately public.

```text
public canonical repository
  implementation authority
  release authority
  sourceExposure=public
  repositoryRole=canonical
  distributionMode=source
        |
        v
source-building package / flake
        |
        v
consumers
```

Typical examples include a reusable open-source tool or SDK whose public repository is also implementation truth.

A source-building Nix flake is appropriate here because source availability is part of the intended product boundary.

## Topology B — private canonical + public binary distribution

Use this when implementation remains private but unauthenticated/public consumers should be able to install releases.

```text
private canonical repository
  sourceExposure=private
  repositoryRole=canonical
  implementation/release authority
        |
        | authorized reviewed release
        v
immutable binary artifact
  + checksums/signature/provenance
  + public CLI/schema/man-page contracts
        |
        v
public distribution repository
  sourceExposure=none
  repositoryRole=distribution
  distributionMode=binary
        |
        v
binary-oriented package / Nix flake
        |
        v
consumers
```

**Invokrum** is the reference migration for this topology. The production Anthesis CLI is expected to use the same broad distribution shape once its Rust-native product boundary is stable.

A public source-building flake that recompiles the intentionally private implementation would contradict this topology.

## Topology C — private canonical + public source projection

Use this when canonical authority remains private but selected implementation/contracts are deliberately projected as public source.

```text
private canonical repository
  sourceExposure=private
  repositoryRole=canonical
        |
        | reviewed one-way projection
        v
public projection repository
  sourceExposure=public
  repositoryRole=projection
  distributionMode=source
        |
        +--> public consumers
        +--> public contribution/reconciliation path
```

**Keylix** demonstrates why public source exposure does not imply public canonical authority.

The projection must have a documented reconciliation/publication direction. It must not silently become a second implementation truth.

## Topology D — public canonical reusable core + private composition

Use this when the reusable implementation itself is intentionally public while private repositories hold product data, deployment composition, or non-public extensions.

```text
public reusable core
  sourceExposure=public
  repositoryRole=canonical
  distributionMode=source
        |
        +--> external consumers
        +--> private composition repository
                  sourceExposure=private
                  repositoryRole=internal
                  distributionMode=internal
```

**Calathea** is the reference case: the public reusable core owns deterministic reusable semantics while private composition must not fork that public canonical behavior.

This topology is not a private-canonical/public-community split even if repository naming looks similar.

## Topology E — private canonical + curated public contract/community projection

Use this when a project wants public documentation, schemas, examples, interoperability material, or community discussion without exposing implementation source or necessarily distributing an executable.

```text
private canonical repository
  sourceExposure=private
  repositoryRole=canonical
        |
        | explicit allow-listed publication
        v
public projection/community repository
  sourceExposure=none or public   # depends on what is deliberately published
  repositoryRole=projection
  distributionMode=none/source/package
```

**Sandcastle** currently uses this broad boundary. Automated publication remains a separately governed effect and must fail closed.

A public projection is not automatically a package repository.

## Topology F — multi-repository engine, adapters, and public distribution

Some projects have more than one private implementation authority because different repositories own different bounded contexts.

```text
private engine/core authority ----+
private provider adapters --------+----> reviewed release set
private entitlement/delivery -----+              |
                                                 v
                                    public docs / verification /
                                    release metadata / facade
```

**Envuscator** is an example where engine/runtime, provider adapters, delivery/entitlement, and public community surfaces must be modeled as explicit edges instead of collapsed into one `canonical` repository.

For these systems, registry metadata should describe the authority edges that actually exist. Do not manufacture a single canonical repository merely to simplify a diagram.

## Choosing a Nix/package surface

| Source posture | Appropriate downstream package shape |
| --- | --- |
| public canonical source | source-building flake/package is normally appropriate |
| private canonical + public binary distribution | public flake fetches immutable release artifacts and pins hashes |
| private canonical + public source projection | source-building public package is allowed only for deliberately projected source |
| private internal-only component | trusted build/materialization boundary; distribute closure/image/package as needed |
| curated public docs/contracts only | no executable package is implied |

Nix reproducibility does not require public implementation source. For a private implementation, reproducibility can be split between a private canonical build/release pipeline and a public artifact package that verifies immutable bytes and provenance.

## Release identity

For one immutable release, avoid multiple independent version authorities:

```text
canonical source revision/tag
  = executable --version
  = archive/package metadata
  = man-page release metadata
  = public package/flake version
  = checksum/signature/provenance subject
  = downstream pinned package identity
```

If a man page or generated package cannot safely derive a version from the canonical release identity, omitting redundant static version text is safer than allowing drift.

## Authority does not flow through packaging

These statements remain true in every topology:

- package installation is not capability or effect authorization;
- artifact validity is evidence, not runtime authority;
- a public distribution repository does not become implementation authority merely because it hosts releases;
- a mirror or projection does not become release authority merely because it contains source;
- private source does not make an insecure design secure;
- signing keys and privileged credentials belong at protected release/effect boundaries, never in distributed binaries or ordinary PR workflows.

## Publication and history

Changing the forward boundary does not erase earlier disclosure.

If implementation source was previously public:

- treat public Git history, forks, caches, downloaded archives, and derived analysis as prior disclosure;
- do not claim that deleting files from the current branch makes them secret again;
- use the new boundary to protect future implementation evolution;
- make history rewriting a separate explicit decision if it is ever required.

## Anti-patterns

Avoid:

- interpreting `-community` as `distribution`, `projection`, or `canonical` without metadata;
- interpreting `visibility=public` as `sourceExposure=public`;
- exporting private implementation source solely so a public Nix flake can build it;
- requiring ordinary downstream endpoints to possess private source credentials when they only need released artifacts;
- allowing a public projection to silently fork canonical contracts;
- using package/signature validity as governance authorization;
- duplicating release versions independently in Cargo/npm metadata, Nix, man pages, release workflows, and provenance;
- publishing private Git history when a clean curated public surface is intended.

## Rollout

Machine-readable rollout is tracked by `.github#66`; ecosystem classification is tracked by `hackelia-micrantha/hackelia-micrantha#35`.

The migration order should be evidence-driven:

1. classify projects with active packaging/release work;
2. validate reference topologies (Invokrum, Keylix, Calathea, curated projection);
3. add release/readiness checks for contradictions that are mechanically decidable;
4. migrate remaining repositories incrementally;
5. only make posture metadata universally required once the registry is complete enough to avoid a flag-day migration.
