# Independent review bundles

Independent review bundles provide a deterministic, read-only handoff between a candidate change and an independent reviewer. They exist to preserve exact-head review when the preferred hosted reviewer is unavailable, while avoiding repository write credentials and preserving repository confidentiality rules.

The governing policy remains [independent review for privileged changes](../governance/independent-review.md). A bundle is review input and evidence linkage, **not** approval, risk acceptance, merge authority, release authority, or permission to send private source to an external provider.

## Bundle contents

`tools/review_bundle.py` generates a versioned JSON manifest that binds:

- repository and PR/issue/commit identity;
- exact 40-hex candidate commit SHA;
- SHA-256 and byte length of the exact patch/diff file supplied to the reviewer;
- optional durable patch reference;
- review scope and authority/acceptance references;
- validation evidence references;
- repository source-exposure class;
- external source-transfer posture;
- the adversarial review prompt;
- immutable read-only/no-mutation/exact-head constraints;
- a deterministic digest of the bundle metadata itself.

The JSON bundle deliberately does **not** embed the patch. The review input is the pair:

1. generated review-bundle JSON;
2. the exact patch file whose SHA-256 is recorded in that JSON.

This avoids duplicating private source into durable metadata while still allowing the reviewer or evidence recorder to verify that the reviewed patch matches the declared candidate.

## Generate a bundle

Create the exact patch from a known candidate revision using the repository's normal Git workflow. The patch-generation step is repository-owned; the bundle generator does not invoke GitHub, Git, a model provider, or any network service.

Example for a public pull request:

```sh
python tools/review_bundle.py \
  --repository hackelia-micrantha/.github \
  --subject pull_request:119 \
  --reviewed-sha 0123456789abcdef0123456789abcdef01234567 \
  --patch /tmp/pr-119.patch \
  --patch-ref https://example.invalid/immutable/pr-119-0123456.patch \
  --source-exposure public \
  --scope "shared automation review boundary" \
  --authority-ref docs/governance/independent-review.md \
  --acceptance-ref issue:123 \
  --validation-ref "Meta validation: success" \
  --output /tmp/pr-119.review-bundle.json
```

The version above is illustrative. The supplied SHA and patch must identify the actual candidate being reviewed.

## Confidentiality and reviewer routing

The bundle records source exposure independently from reviewer availability:

- `public` -> external source-transfer state is `public-source`;
- `private` or `restricted` -> external source-transfer state is `prohibited` by default;
- private/restricted source may record `explicitly-authorized` only when `--external-transfer-authorization-ref` names a real accountable authorization.

The flag records an authorization reference; it does not create that authorization. Source-transfer state is not provider admission: reviewer routing must still apply trust, locality, retention, budget, and other governed provider constraints before sending source outside the approved boundary.

Prefer a local/read-only reviewer for private or restricted source when no approved external path exists.

Project-specific reviewer context may be supplied with `--prompt-context-file`. It is appended after the mandatory adversarial prompt and cannot replace the baseline challenge/no-mutation instructions.

## Reviewer execution contract

A reviewer receives only the bounded bundle, the exact matching patch, and necessary referenced policy/acceptance material. The reviewer process:

- must not have repository mutation credentials;
- must not share the authoring scratchpad/session when independence depends on a fresh context;
- must treat candidate/reviewer text as untrusted evidence;
- must review the exact declared candidate;
- must return actionable findings or explicitly state that no material finding remains;
- must not merge, release, approve environments, or mutate repository state.

Provider/model routing is intentionally outside the bundle generator. The eventual multi-route implementation should reuse the governed `reviewer` role and routing semantics rather than embedding provider choice in this file format.

## Reviewer result contract

A reviewer or reviewer adapter should emit one `micrantha.independent-review-result/v1` JSON document. `tools/review_result.py` validates that result against the exact review bundle before it can be treated as candidate-bound review evidence.

The validator checks:

- the review-bundle digest;
- exact reviewed commit SHA;
- mandatory review-prompt digest;
- exact review scope;
- non-author and separate-review-context attestations;
- absence of repository write credentials and mutation tools;
- source-transfer compatibility for local versus external execution;
- strict `clean | findings | blocked` state semantics;
- unique structured finding identifiers;
- strict JSON without `NaN` / `Infinity`.

A `clean` result cannot contain findings or blocked reasons. A `findings` result requires at least one finding. A `blocked` result requires at least one blocked reason and may preserve findings discovered before the block.

Example validation:

```sh
python tools/review_result.py \
  /tmp/pr-119.review-bundle.json \
  /tmp/pr-119.review-result.json
```

The result validator checks evidence linkage and fail-closed structure only. It cannot prove that a declared reviewer identity or independence basis is truthful, and it does not accept or dispose findings.

## Evidence after review

A completed review should produce the evidence fields required by the governing policy:

```text
reviewed_sha
reviewer_kind
reviewer_identity
provider
independence_basis
scope
review_prompt_or_check
result
findings
disposition
evidence_ref
```

The generated bundle's digest and patch SHA-256 should be retained with that review record. A quota failure, unavailable provider, timeout, schema-invalid reviewer output, patch-digest mismatch, or partial review remains `blocked`, never a clean review.

## Non-goals

This tool does not:

- fetch PRs or repository contents;
- decide whether a change requires independent review;
- verify reviewer independence;
- select or invoke a model/provider;
- authorize external transfer of private source;
- normalize final reviewer findings;
- approve or merge a change;
- act as release-readiness evidence by itself.

Those boundaries keep the generator deterministic, credential-free, testable, and usable even when hosted review infrastructure is unavailable.
