# Release and versioning standard

A release is an accountable statement that a specific source revision produced identified artifacts or deployment state with declared support, compatibility, and security properties.

## Release authority

Repository release authority follows [`GOVERNANCE.md`](../../GOVERNANCE.md). The release owner confirms that required evidence exists for the exact revision and artifacts being published. Automation may perform publication but does not independently authorize the release.

## Versioning

Use Semantic Versioning for public libraries, APIs, CLIs, packages, and contracts unless the repository documents a better domain-specific scheme.

- **Major** — incompatible change to the declared supported contract.
- **Minor** — backward-compatible capability addition.
- **Patch** — backward-compatible correction or security fix.

Pre-1.0 versions may evolve quickly, but breaking changes must still be intentional and documented. A `0.x` version is not permission to conceal compatibility impact.

Applications, continuously delivered services, operating-system configurations, datasets, websites, or model artifacts may use date, build, channel, or revision-based identities. The scheme must remain monotonic or otherwise unambiguous and traceable to source.

## Release channels

Repositories may define:

- development or nightly;
- alpha;
- beta;
- release candidate;
- stable;
- maintenance or long-term support.

Each channel should state its stability, support, compatibility, and upgrade expectations. Promotion between channels should reuse or identify the same artifacts where practical rather than silently rebuilding different content.

## Required release record

A release should identify:

- version or immutable release identity;
- source commit and tag;
- release date and owner;
- supported platforms, configurations, and consumers;
- changes, fixes, security impact, and known limitations;
- compatibility, migration, upgrade, and rollback implications;
- artifacts and checksums;
- provenance, SBOM, and signatures when required;
- validation evidence and unresolved exceptions;
- deprecations and support window.

Release notes should describe externally meaningful outcomes rather than reproduce the commit log.

## Tags and branches

- Protect or restrict release tags according to repository risk.
- Use annotated or signed tags when authenticity requirements justify them.
- Do not move or overwrite published stable tags.
- Record hotfix and maintenance branch policy where supported versions diverge.
- Treat a tag as a reference, not proof that artifacts were correctly built or published.

## Artifacts

Release artifacts should be:

- built from the intended source revision;
- reproducible or at least provenance-linked;
- named with version, platform, architecture, and format where applicable;
- validated after packaging, not only before it;
- accompanied by checksums and stronger integrity evidence according to risk;
- free of secrets, credentials, development-only material, and unintended personal data;
- retained or mirrored according to support commitments.

For mobile, native, container, Nix, package-registry, and provider-adapter releases, validate installation or consumption through the supported channel.

## Supply-chain evidence

Use the level appropriate to the artifact and maturity:

- checksums for downloadable assets;
- SBOMs for distributable software and container images;
- provenance or build attestations for higher-risk release pipelines;
- signing for artifacts, tags, packages, or metadata where identity and tamper resistance are material;
- immutable digests for deployed images and generated release evidence.

Document the verification procedure. Evidence users cannot verify is incomplete.

## Compatibility and migration

Before release, identify:

- public API, schema, command, configuration, data, file-format, policy, and deployment changes;
- backward and forward compatibility;
- mixed-version behavior;
- required data or configuration migration;
- deprecation period and successor;
- rollback limits and irreversible changes.

Breaking changes require an accepted decision or explicit release authority appropriate to their scope. Update consumers, community surfaces, and integration testbeds in dependency order.

## Security releases

Security fixes should minimize disclosure risk while preserving enough information for users to assess urgency and affected versions.

- Coordinate patch, credential rotation, publication, and disclosure.
- Avoid publishing exploit details before users have a reasonable remediation path.
- Identify affected and fixed versions accurately.
- Do not misclassify an unverified mitigation as a complete fix.
- Backport according to the declared support policy and risk.

## Release readiness

Use the organization [release-readiness prompt](../prompts/releases/release-readiness.md) or an equivalent gate for material releases. At minimum confirm:

- version identity is correct;
- required checks ran on the release revision;
- artifacts were packaged and consumed successfully;
- security and dependency findings are dispositioned;
- compatibility, migration, rollback, and known limitations are documented;
- public documentation matches the released capability;
- publication credentials and targets are scoped correctly.

## Publication authority across repositories

The authoritative implementation repository owns product or contract release identity. Community, website, adapter, and distribution repositories publish their own packaging or integration releases without redefining upstream component maturity.

When GitHub and GitLab both participate, document which repository or registry is authoritative for source, tags, packages, release notes, and mirrors. Mirrors must not create conflicting release histories.

## Rollback, yanking, and revocation

Define how to:

- stop or pause publication;
- yank or deprecate a package without erasing history;
- revoke a signing identity or compromised artifact;
- roll back a deployment or configuration;
- communicate a broken or unsafe release;
- preserve evidence for incident review.

Do not delete published evidence merely to make a failed release disappear.

## Deprecation and end of support

Deprecation should identify the affected surface, replacement, migration path, warning period, final supported version, and end-of-support date where applicable.

A repository moving to Superseded, Maintenance, or Archived must update release channels and public documentation according to the [repository lifecycle](../governance/repository-lifecycle.md).
