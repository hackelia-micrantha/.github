# Micrantha prompt-pack: authenticated distribution handoff

**Scope:** [meta prompt-pack #29](https://github.com/hackelia-micrantha/.github/issues/29).
**State:** candidate qualification contract; **not** an authorized release, a configured publisher, or proof of live host admission.

This is the Micrantha-specific **producer/consumer handoff** for the root-level `micrantha-prompt-pack.yaml`. Use Invokrum's existing [bundle v1](https://github.com/hackelia-micrantha/invokrum/blob/main/docs/bundle-format-v1.md) and [authenticated local install](https://github.com/hackelia-micrantha/invokrum/blob/main/docs/install-cli.md); do not create another bundle schema, signer, trust store, or package registry. The [pack-layout QART](qart-micrantha-meta-prompt-pack.md) remains authoritative for source ownership and pack structure.

## Contract at the boundary

| Actor | Must supply or establish | Must **not** infer |
| --- | --- | --- |
| `.github` producer | Clean, explicitly selected 40-hex source commit; unchanged canonical pack + referenced file bytes; canonical `invokrum.pack-bundle/v1` manifest and `sha256:<subject>` | That source checkout or digest alone authenticates the publisher |
| Separately authorized publisher | Ed25519 signature over Invokrum's versioned **exact subject** message; public key identity distributed through an independently trusted channel | Signing/publishing authority from CI, PR merge, or the pack |
| Consuming host | Explicit expected subject + **out-of-band trusted** key fingerprint + verified Invokrum CLI/version + supported Linux store and local candidate; authorization and rollback policy | Trust from README, pack metadata, GitHub URL, release name, bundled key, or CLI arguments sourced from the candidate |
| Invokrum local installer | Subject and file-integrity verification; Ed25519 assertion; explicit host trust-policy match; `invokrum.installation/v2` authenticated evidence; immutable installed root | Freshness, revocation, update selection, or permission to run an agent |
| Host at use time | Current independently owned allow/revocation/rollback policy; pinned installed subject and exact pack/profile lock or composed output identity; policy and capability gates | That `installation/v2` proves publisher **still** trusted or grants effect authority |

Producer staging copies only `SOURCES` enumerated by [the installed-root proof](../../tools/verify_prompt_pack_installed_root.py) and fails on missing/linked files. The producer records source Git commit **separately**; Invokrum's bundle v1 subject binds canonical manifest/file bytes, **not** the Git commit. Associate subject, source revision, exact manifest digest, and selected profile lock digest in the review/release evidence without inventing new fields inside an Invokrum manifest.

## Pre-publication qualification (read-only/local)

Use a clean, exact source checkout and a pinned **authenticated-capable** Invokrum CLI. The existing CI uses a pinned `v0.2.1` executable for **digest-only** tests; do not describe that proof as authenticated or silently replace the executable without verifying its compatibility, provenance and release policy.

A trusted host or release process must provide all three external publisher inputs for an authenticated candidate, **after** a separately authorized signer signs the exact subject:

```sh
python tools/verify_prompt_pack_installed_root.py \
  --invokrum /trusted/path/invokrum \
  --pack-root /trusted/clean/source-checkout \
  --publisher-public-key /trusted/publisher.ed25519.pub \
  --publisher-signature /trusted/bundle-subject.sig \
  --trusted-key-sha256 '<host-approved-64-lowercase-hex-fingerprint>' \
  --output /private/qualified-pack.json
```

Invokrum's CLI accepts an unprefixed 64-lowercase-hex SHA-256 key fingerprint for `--trusted-key-sha256` (distinct from the `sha256:<bundle-subject>` flag). The selected fingerprint must come from an **independent host trust decision**, not the candidate.\n\nThe opt-in harness regenerates the canonical candidate from `SOURCES`, recomputes the subject and calls **Invokrum**, not a second signature verifier. It requires the exact v2 `verified-and-authorized` receipt for the host-pinned public-key fingerprint and subject; verifies installed-root containment, byte-identical composition of every declared profile, deterministic lock/verify, and exact reinstall reuse; and rejects corrupt signatures, unrecognized trusted identities, altered candidate files, and missing required overlays. The harness never creates a signing key, issues signatures, publishes an artifact, or claims host freshness. The raw signature and trust inputs remain caller-owned and outside the pack.

In the default CI mode (no publisher inputs), the harness continues testing digest-only installation and records `publisher_authentication: not-provided`. **This is not production signed-distribution acceptance.** A partially supplied publisher option set fails before installation. Do not allow v1 or unsigned evidence to satisfy a v2 acceptance gate.

## Effect and release gate

Before publishing or authorizing a consumer to use a new revision, require evidence of:

1. **Source-to-subject binding:** clean exact Git revision; staged paths and bytes match canonical source; manifest is canonical; digest/subject agree; chosen profile output + lock identities come from the installed root.
2. **Authenticated publisher:** an owner-approved signer with an independently obtained public-key fingerprint; actual valid signature for the subject; v2 `verified-and-authorized` evidence at the exact expected fingerprint/subject. A changed signing key or mechanism needs a new explicit host trust decision.
3. **Fail-closed negative cases:** wrong signature, unauthorized key, subject mismatch, mutated or missing file, and v1-to-v2 provenance substitution fail without replacing an accepted installed root. The generic installer already owns these invariants; this proof exercises them for Micrantha's source candidate.
4. **Host admission:** out-of-band expected subject and trusted publisher policy are still valid; host explicitly rejects unapproved, revoked, unknown or older-than-minimum subjects and preserves an authorized recovery revision. There is **no** built-in Invokrum freshness, revocation, mutable-channel lookup, or rollback-selector claim. Until the host supplies those controls, record this as a **blocked production-consumption gate**, not a published safe default.
5. **Effect authority:** independent review and exact-head CI for candidate changes; separate authorization for signing, release, publication, host policy change, deployment, and model/tool effects. A successful installation does not grant any of them.

Do not put signing secrets or privileged CI environment credentials into the candidate, unit tests, or evidence artifact. Test-only keys must never become a publisher trust root. Do not treat the public `invokrum` executable version/release as a release of the **Micrantha prompt pack**.

## Ownership and next transition

- `.github` #29: source candidate/staging and evidence, pack compatibility, and distribution handoff;
- Invokrum: generic signed subject verification and immutable local install; see [publisher-trust status](https://github.com/hackelia-micrantha/invokrum/blob/main/docs/security/publisher-trust.md);
- [meta #45](https://github.com/hackelia-micrantha/hackelia-micrantha/issues/45) / [Dubnium #1180](https://github.com/ryjen/dubnium/issues/1180): caller-provided project context, current trust/freshness/revocation, rollback and host integration.

**Next externally gated step:** qualify the opt-in authenticated path using an approved publisher key and an authenticated-capable pinned executable, under independent review. Until then #29 remains partially delivered: this handoff is a **qualified local path**, not a distributed/published pack or live host admission.
