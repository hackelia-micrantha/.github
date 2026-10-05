# QART: How should the Micrantha prompt library be packaged for Invokrum?

## Status

Decided

## Context

Issue #29 requires the canonical engineering prompt library in this repository to become a deterministic Invokrum consumer pack without moving prompt ownership into Invokrum or creating a second editable source of truth.

Current evidence:

- `docs/prompts/README.md` owns shared prompt-library contracts and selection guidance.
- `docs/prompts/manifest.yaml` owns prompt discovery metadata, not prompt prose.
- `docs/prompts/overlays/cross-project-execution.md` is the canonical Micrantha/Ryjen scope overlay.
- Invokrum `invokrum.dev/v1` accepts pack-relative local files, explicit ordered classes, profiles, cardinality, and deterministic lock/manifest evidence.
- Invokrum #114 proved the required cross-project scope layer can be fail-closed and deterministically ordered without giving Invokrum semantic project authority.
- Invokrum #61 proved an installed immutable root can feed ordinary composition after acquisition.
- Invokrum pack v1 has no semantic version field; distributed content identity is provided separately by exact bundle subject and lock evidence.

## Question

How should this repository represent, distribute, and version the Micrantha Meta Prompt Pack while keeping the existing Markdown prompt library canonical?

## Decision drivers

1. Preserve one editable source of prompt truth.
2. Bind exact prompt bytes into deterministic Invokrum composition and drift evidence.
3. Keep Invokrum generic and project/runtime authority outside the pack.
4. Support source-checkout use immediately and immutable distribution later.
5. Minimize migration and maintenance overhead.

## Constraints and invariants

- Canonical prompt prose remains owned by this repository.
- `docs/prompts/manifest.yaml` remains discovery metadata rather than duplicated prose.
- Invokrum source paths cannot escape the pack root or use symlink tricks.
- Runtime task/project evidence must not silently become trusted prompt authority.
- Ordinary composition must remain offline.
- A generated distribution artifact may copy canonical bytes, but it must not become an independently editable source.

## Assumptions and evidence gaps

| Statement | Classification | Evidence or validation |
| --- | --- | --- |
| A pack entry point at repository root can reference `docs/prompts/**` directly | Fact | Invokrum v1 pack-relative path contract |
| The first slice does not need a dynamic project overlay inside the distributed pack | Decision assumption | Live project materialization remains tracked by meta #45 |
| Exact Git revision plus bundle subject/lock identity is sufficient before semantic pack releases are introduced | Recommendation | Revisit if external distribution needs a user-facing compatibility channel |

## Alternatives

### Alternative A: Root source pack over canonical files

Place one Invokrum pack declaration at repository root. Its overlays reference existing canonical Markdown files directly. Source-checkout consumption uses that pack in place. Distribution tooling later stages those exact files into an immutable Invokrum bundle without committing copied prompt prose.

- **Benefits:** no duplicate editable content; direct lock coverage of canonical bytes; minimal migration; pack-relative containment works naturally.
- **Costs and limitations:** repository root is the pack root for source-checkout use; immutable install requires a staging/package step because the whole repository is not a valid minimal bundle candidate.
- **Security/governance:** preserves prompt authority here and keeps install/publisher trust separate from composition.
- **Compatibility:** uses existing `invokrum.dev/v1`; no schema extension.
- **Reversibility:** Easy.

### Alternative B: Commit a dedicated self-contained pack directory

Create a `packs/micrantha-meta/` tree containing copied prompt Markdown plus `pack.yaml`.

- **Benefits:** directly installable directory/archive shape.
- **Costs and limitations:** creates duplicate editable prompt prose and synchronization risk.
- **Security/governance:** ambiguous source authority if copies drift.
- **Reversibility:** Moderate because consumers may bind to the copied layout.

### Alternative C: Migrate prompt prose into pack-native files

Move normative prompt text into a dedicated pack tree and make documentation render/link to those files.

- **Benefits:** pack-native source layout and clean distribution boundary.
- **Costs and limitations:** broad migration, documentation churn, changed authoring model, and unnecessary risk for the first slice.
- **Security/governance:** can preserve one source, but only after a larger authority migration.
- **Reversibility:** Difficult relative to current need.

### Alternative D: Defer packaging

Continue using documentation files manually and rely only on synthetic Invokrum conformance.

- **Benefits:** no implementation work.
- **Costs and limitations:** keeps copy/paste composition, weak attribution, and no exact consumer-pack identity.
- **Reversibility:** Easy, but fails issue #29's outcome.

## Comparison

| Criterion | A: root source pack | B: copied pack tree | C: migrate source | D: defer |
| --- | --- | --- | --- | --- |
| One editable source | Strong | Weak | Strong after migration | Strong |
| Exact canonical-byte identity | Strong | Weak unless continuously reconciled | Strong | None |
| Minimal change | Strong | Moderate | Weak | Strong |
| Install/distribution ergonomics | Moderate; generated staging needed | Strong | Strong | None |
| Authority clarity | Strong | Weak | Strong | Strong |
| Invokrum v1 compatibility | Strong | Strong | Strong | N/A |
| Reversibility | Strong | Moderate | Weak | Strong |

## Recommendation

Choose **Alternative A**.

Use a root-level `micrantha-prompt-pack.yaml` with three exactly-one classes for the first slice:

1. `foundation` → `docs/prompts/README.md`;
2. `scope` → `docs/prompts/overlays/cross-project-execution.md`;
3. `workflow` → one selected canonical workflow prompt.

Initial workflow profiles are:

- `classify-and-route`;
- `issue-grooming`;
- `engineering-artifact-review`.

Do not add a static `project` class to this distributed source pack. Live project resolution/materialization is a host concern tracked by meta #45. A host may later build a derived exact composition that adds caller-resolved project context, but that must not mutate the canonical source pack or elevate runtime evidence into prompt authority.

For version/identity:

- the stable logical pack id is `micrantha-meta-prompts`;
- source-checkout identity is the exact repository revision plus Invokrum lock/manifest identity;
- immutable distribution identity is the `invokrum.pack-bundle/v1` subject;
- do not invent a pack-schema version field or overload the pack id with Git SHAs;
- introduce semantic pack release tags only when an external compatibility/distribution requirement justifies them.

For immutable distribution, stage the declared pack entry point and exact referenced canonical files into a temporary/release candidate. The staging step must copy bytes exactly, verify them against the source revision, and produce bundle evidence; generated copies are artifacts, not editable source.

Confidence: high. The remaining uncertainty is release automation shape, not the pack source/layout decision.

## Expected outcomes and review plan

| Expected outcome | Supporting/weakening evidence | Review trigger | Reconsider if |
| --- | --- | --- | --- |
| Prompt edits produce deterministic Invokrum drift | lock/verify changes on canonical source edit | first pack CI fixture | canonical edits can occur without identity change |
| No prompt prose is duplicated in source | repository review | each pack expansion | a consumer requires a committed copied tree |
| Hosts can consume exact profiles without bespoke copy/paste | CLI/RPC fixture | first host integration | host contract cannot use the root pack safely |
| Distribution can remain generated | bundle/install proof | first published pack bundle | staging cannot preserve exact-byte/source provenance |

## Trade-offs

### Accepted

- Source checkout and immutable installed-bundle layouts are not identical.
- Initial composition includes the full prompt-library README as the shared foundation because it currently owns several shared contracts.
- The first slice does not solve live project-context materialization.

### Rejected

- A second editable prompt tree.
- Invokrum-specific policy or project registry logic in Invokrum core.
- Runtime network fetching during composition.
- Inventing version fields outside the v1 schema.

### Residual risks and mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| README foundation contains catalogue text beyond strict shared rules | keep exact source for first slice; split canonical shared contracts only under a separately reviewed refactor if composition quality warrants it | .github |
| Generated distribution staging could alter bytes | byte-for-byte copy plus bundle digests and lock verification | release tooling |
| Pack/profile catalogue can drift from `manifest.yaml` | repository-local tests validate initial workflow registration and source existence | .github |
| Host may confuse prompt identity with authority | document boundary and preserve meta #45/Anthesis effect controls | host/governance owners |

### Revisit triggers

- Invokrum v2 adds a first-class composition/import mechanism that removes the root-layout trade-off.
- External consumers need semantic compatibility/version negotiation beyond exact revision/bundle identity.
- The shared README becomes too broad or unstable as a foundation overlay.
- Live host integration demonstrates that project context belongs in a different canonical composition boundary.

## Decision path

Ready for local implementation choice.

## Decision outcome

- **Decision:** Root-level source pack referencing canonical files directly; generated immutable distribution only.
- **Date:** 2026-10-04
- **Decision owners:** Micrantha meta-repository maintainers
- **Disposition:** Accepted
- **RFC:** Not required; no new cross-project public contract is introduced.
- **ADR:** Not required yet; revisit after the first production consumer or semantic release contract makes the layout expensive to change.
- **Follow-up work:** Implement the first three profiles, deterministic validation/fixtures, and later generated bundle/install proof under issue #29.
