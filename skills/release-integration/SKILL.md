---
name: release-integration
description: Apply the Micrantha release, source-exposure, public distribution, Nix flake, and downstream integration strategy across project repositories.
---

# Release integration

## Trigger

Use for `make a release`, `include this in Dubnium/dotfiles`, `apply Micrantha release/integration strategy`, or when a project must move from canonical implementation to a consumable pinned downstream package.

## Inputs

- canonical repository and authorized release revision;
- source-exposure topology (public source or private canonical + public distribution);
- build/package commands, versioning, supported platforms, CLI/man-page contracts;
- public/community distribution repository where applicable;
- downstream consumers such as Dubnium/dotfiles and their lock/update mechanism.

## Workflow

1. Establish release authority, exact canonical revision, version, and source-exposure boundary.
2. Require exact-head build/test/static-analysis evidence and release-readiness review before publication.
3. Build the release artifact from the canonical repository and validate the **artifact contents**, permissions, version identity, executable smoke path, and required documentation.
4. For private implementation, ensure the public distribution surface receives immutable artifacts/contracts/metadata—not buildable private source or internal-only material.
5. Publish checksums/signatures/provenance/SBOM as required by project and organization policy.
6. For CLI tools, include the executable and section-1 man page in conventional paths and verify both after installation.
7. Maintain a public Nix flake that fetches an immutable versioned artifact and pins its cryptographic hash when private-source distribution is intentional. Do not use a source-building public flake for private implementation.
8. Update downstream consumers through committed version/flake lock state; do not point production/system configuration at floating branches or mutable artifacts.
9. Validate the downstream installed command, version, man page, and critical integration path on the actual consumer environment/CI.
10. Record rollback/update instructions and reconcile release notes, public docs, issues, and project status.

## Security boundary

Private source is not a substitute for secure design. Assume distributed binaries can be reverse engineered; never ship secrets or controls that depend on client-side secrecy. Treat the public/community repository as a distribution trust boundary with minimum necessary contents.

## Completion

Complete when the exact authorized revision is represented by an immutable verified release, the distribution surface exposes the intended consumer contract, downstream consumers pin that release, and installed-path validation succeeds with rollback understood.

## References

- `docs/standards/source-exposure-and-distribution.md`
- `docs/standards/releases.md`
- `docs/standards/cli-interoperability.md`
- `docs/standards/ci-cd.md`
- `docs/prompts/releases/release-readiness.md`
- `docs/architecture/repository-topology-and-trust-domains.md`
