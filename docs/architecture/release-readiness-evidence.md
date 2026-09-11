# Release-readiness evidence boundary

This document describes the executable evidence boundary used by `tools/release_readiness.py`. The normative policy remains in:

- `docs/standards/source-exposure-and-distribution.md`;
- `docs/standards/releases.md`;
- `docs/standards/cli-interoperability.md`;
- `docs/standards/security.md`.

The checker does not replace repository-owned build, package, release, signing, or language-specific validation.

## Model

```text
repository-owned release/build tooling
  -> build the real candidate artifact/package
  -> inspect generated output
  -> exercise the supported clean-consumer path
  -> normalize bounded evidence
            |
            v
metadata/release-readiness.schema.json
            +
metadata/repositories.json
            |
            v
tools/release_readiness.py
  -> posture/readiness decision
```

The registry is authoritative for repository topology and source/distribution posture. The evidence document reports what the candidate release actually did. A project must not copy its own posture classification into the evidence document as a second authority.

## Producer responsibilities

Repository-owned release tooling should generate evidence only after exercising the real candidate path. It is responsible for language/package-specific facts such as:

- whether the package compiled implementation source;
- whether acquisition required private repository credentials;
- whether release inputs were immutable and cryptographically pinned;
- what files and permissions appeared in the generated package/archive;
- whether executable/man-page smoke checks passed;
- whether a clean/cache-miss consumer path succeeded;
- normalized release identity claims extracted from the surfaces the project can inspect;
- whether the generated artifact contains prohibited private/security/development material.

The organization checker does not fetch arbitrary URLs or infer those facts from prose.

## Normalized identity

`release.canonicalIdentity` is a project-normalized release identity such as `0.3.0`. `identityClaims` contains only mechanically discovered surfaces that the producer can normalize to that identity, for example:

```json
{
  "canonicalIdentity": "0.3.0",
  "identityClaims": {
    "executable": "0.3.0",
    "archive": "0.3.0",
    "package": "0.3.0",
    "manPage": "0.3.0",
    "provenance": "0.3.0"
  }
}
```

A raw tag such as `v0.3.0` may be normalized by repository-owned tooling when the project's release contract explicitly defines that mapping. The organization checker compares normalized identities rather than inventing per-project version parsing rules.

Missing mechanically unavailable claims are not fabricated. A supplied claim that disagrees with the canonical identity fails readiness.

## Public binary distribution

For a public surface declared `distributionMode=binary`, evidence must show at minimum:

- acquisition mode is binary;
- implementation source is not compiled by the public package path;
- immutable acquisition is cryptographically pinned;
- no private source credential is required;
- a clean/cache-miss consumer path succeeds without private credentials;
- generated artifacts do not contain private implementation source;
- generated artifacts contain no credentials, signing keys, private security corpus, or development-only material.

This is the expected Invokrum-style topology after its public binary distribution is operational.

## Public source distribution

For `distributionMode=source`, source-building is expected rather than suspicious. Evidence must show the source acquisition is immutable and credential-free for the public consumer path.

This permits public canonical projects such as Repora and public source projections such as Keylix community without confusing source exposure with canonical implementation authority.

## CLI completeness

When `cli` evidence is present, the checker requires:

- the executable path to exist in the inspected artifact list and be executable;
- the section-1 man page at `share/man/man1/<name>.1`;
- non-mutating smoke checks to have passed;
- required operator/verification documentation to be present.

A project that is not a CLI omits the `cli` object.

## Clean-consumer evidence

Public consumer surfaces must exercise a clean/cache-miss or equivalent acquisition path with private credentials unavailable. A warm Nix/store/package cache is not sufficient evidence because it can hide an invalid private-source authority dependency.

`cleanConsumer.privateCredentialsAvailable=false` is an observation about the test environment. It is not a credential-discovery mechanism and must never contain credential values.

## Artifact inspection

The evidence schema records bounded booleans rather than artifact bodies. Do not embed package contents, secret candidates, private source snippets, fuzz corpora, or signing material in the evidence document.

The repository-owned producer should retain enough local/CI diagnostics to explain a failure while keeping organization-level evidence minimal.

## Verification

Run from a checkout of this repository:

```bash
python tools/release_readiness.py path/to/release-readiness.json
```

Use another registry only for explicit fixture/testing work:

```bash
python tools/release_readiness.py \
  --registry metadata/repositories.json \
  path/to/release-readiness.json
```

A successful result means the supplied candidate evidence is mechanically consistent with the declared repository posture and cross-project release invariants represented by the checker. It does **not** grant release, signing, deployment, governance, or runtime authority.

## Deliberate boundary

The first executable profile intentionally does not define a universal package parser, network fetcher, signature verifier, or exception engine. Project-specific package inspection remains repository-owned. Any future exception mechanism must be explicit, reviewable, bounded to named checks, and must not turn the checker into an authority-bypass surface.
