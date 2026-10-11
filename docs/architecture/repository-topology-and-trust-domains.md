# Repository topology and trust-domain patterns

## Purpose

Define the organization-level repository topology vocabulary used when a project exists across multiple hosts, visibility domains, agent workspaces, mirrors, public/community repositories, or recovery stores.

The intent is to prevent each project from inventing a different meaning for `origin`, `mirror`, `public`, `private`, or `sync`.

This document is architectural guidance. Repora owns executable repository topology and state-movement mechanics. Individual projects remain authoritative for disclosure/IP/release policy. Anthesis governs consequential effects where configured. Dubnium owns runtime/forge/storage infrastructure. Sandcastle owns workspace/checkpoint state.

## Core mental model

```text
Project
  -> logical Repository
      -> one or more hosted Endpoints
      -> explicit Roles / Trust domains
      -> explicit directed Relationships
```

A provider is not a trust domain. GitHub, GitLab, Forgejo, Bitbucket, or another host may be canonical, mirror, staging, public, or private only when explicitly configured for that role.

## Vocabulary

### Logical repository

The durable project repository concept independent of any particular hosting provider or transport URL.

### Endpoint

One hosted representation of a logical repository, identified by provider, provider installation where applicable, and repository identity.

Examples:

```text
github:hackelia-micrantha/repora
forgejo:canforge:hackelia-micrantha/dubnium
forgejo:dubnium:hackelia-micrantha/dubnium
```

### Trust domain

A descriptive boundary relevant to policy and disclosure, for example:

- `agent`
- `private`
- `public`
- `recovery`

Trust-domain labels do not grant authority. They describe topology/policy context only.

A label such as `trusted`, `canonical`, `internal`, `private`, or `agent` must never be interpreted as sufficient permission to read, write, project, promote, merge, publish, or otherwise mutate repository state. Classification may constrain policy; it cannot mint authority.

### Canonical

The endpoint currently authoritative for a defined repository state. Canonical is a role, not a provider, and the role does not itself grant write authority.

### Mirror

A directed relationship representing the same permitted Git state elsewhere. Mirror behavior must preserve explicit ref policy and destructive-change controls.

### Projection

A directed relationship that creates a deterministic derived repository representation in another trust/disclosure domain.

Typical use:

```text
private canonical -> clean public/community repository
```

Projection is not history mirroring. Private source history, remotes, credentials, paths, or metadata do not cross the boundary unless explicitly included by a safe contract.

Projection should bind both the exact source tree and the exact materialized target tree. A reviewed source revision alone is not sufficient to claim that the intended public representation was produced.

### Promotion

A directed relationship that moves one exact candidate from a less-authoritative endpoint into a more-authoritative endpoint after review and any required governance.

Typical use:

```text
agent staging -> private canonical
```

Promotion binds exact candidate/base/target state and is stale-safe. It is not implicit pulling or merging, and endpoint role/trust-domain labels do not authorize it.

### Public contribution import

A public contribution is imported as an exact candidate/proposal into the private development flow. It never gains reverse-sync authority over private canonical state.

Where the public repository is a projection, a forward path/transform does not imply an inverse transform. Automatic import is permitted only for explicitly defined deterministic reverse mappings. Generated, many-to-one, one-to-many, lossy, transformed, unknown, or ambiguous mappings are non-importable by default.

A non-importable public contribution may still be retained as a review proposal; it must not mutate private source state by guessing an inverse mapping.

### Archive

A recovery representation such as a Git bundle plus manifest/digest. Archive is not a writable mirror and must not be confused with same-host redundancy.

Archive claims must state their coverage. Git objects/refs may be recoverable while issues, pull requests, packages, actions, users, LFS content, or the forge database remain unsupported, partial, or indeterminate. `repository recoverable` must not be conflated with `forge recoverable`.

### Workspace

A local checkout topology for development/operator convenience. Workspace composition is not repository hosting topology and does not imply dependency or mirroring semantics.

### Overlay

A future relationship in which a public/base repository is combined with private additions. Overlay semantics should be introduced only when a concrete consumer requires them and after projection/promotion semantics are proven.

## Standard patterns

### Pattern A — ordinary public project

```text
canonical -> mirror(s)
```

Use when repository contents and history can be represented equivalently across endpoints.

### Pattern B — private canonical / public projection

```text
private canonical
      |
      | projection
      v
public/community
```

Use when only an allowlisted deterministic subset or derived representation may be public.

The projection should bind exact source, profile, materialized target tree, target/base state, and plan identity.

### Pattern C — agent staging

```text
Sandcastle/workspace
      |
      v
staging endpoint
      |
      | promotion
      v
canonical endpoint
```

Agents should normally lack direct canonical credentials when a staging/promotion boundary exists.

### Pattern D — public contribution into private development

```text
public PR/commit
      |
      | import exact candidate
      v
private review/workspace
      |
      | promotion
      v
private canonical
```

Never implement this as automatic reverse mirroring. If a public path came from a non-invertible projection, treat its change as review-only unless an explicit deterministic import mapping exists.

### Pattern E — sovereign resilience

```text
canonical -> mirror
     |
     +-> archive -> independent encrypted backup
```

A same-host mirror improves availability but is not independently sufficient disaster recovery. Archive manifests should identify exactly which Git and forge/application state classes are covered.

### Pattern F — public core / private overlay

```text
public base + private overlay -> internal product
```

Deferred as a standard executable pattern until a concrete project needs it.

## Cross-project ownership

| Concern | Owner |
| --- | --- |
| Repository identity, endpoint topology, relationship planning/apply | Repora |
| Forgejo service, storage, networking, credentials, backups | Dubnium / hosting system |
| Effect-time authorization, approval, policy, evidence sufficiency | Anthesis |
| Workspace/checkpoint state, lineage, integrity observations | Sandcastle |
| Public/private/IP/disclosure classification | Owning project |
| Testing/semantic verification requirements | Testule / owning project as applicable |

## Security invariants

1. **No relationship implies its inverse.** A projection from private to public does not authorize public-to-private mutation.
2. **Provider is not authority.** Hosting on Forgejo/GitHub/etc. does not establish trust level.
3. **Trust-domain/role is not authority.** Labels classify topology/policy context; they do not grant repository capabilities.
4. **Observation is not authority.** A checkpoint, mirror status, public PR, or successful validation may be evidence but cannot independently authorize a consequential repository effect.
5. **Exact state binding.** Promotion/projection decisions bind policy-relevant candidate, source, target, profile, plan state, and where applicable materialized target-tree identity.
6. **Stale authority fails closed.** Changed candidate/base/target/materialization/policy-relevant state requires fresh planning/re-evaluation.
7. **No ambient canonical credentials for agents where avoidable.** Prefer staging credentials plus a bounded effector.
8. **Clean public materialization.** Private history and metadata do not cross disclosure boundaries by default.
9. **Forward projection does not imply inverse import.** Ambiguous or generated transforms are non-importable unless an explicit deterministic reverse mapping exists.
10. **Recovery is explicitly scoped and independently verified.** A copy on the same machine is not sufficient proof of recoverability, and Git recovery does not imply forge/application recovery.

## Initial Micrantha reference topology

The first reference scenario is Dubnium:

```text
Agent/Sandcastle
  -> Dubnium Forgejo staging
  -> Repora promotion
  -> private canonical endpoint (initially existing canonical; future CanForge candidate)
  -> Repora projection
  -> hackelia-micrantha/dubnium-community
  -> public contributions imported as proposals

private canonical
  -> mirror/archive
  -> independent backup
```

CanForge should be modeled as a Forgejo installation/endpoint, not as a bespoke Repora provider type. Vanilla Forgejo remains the architectural compatibility target so CanForge is an integration target rather than a dependency.

## Recommended adoption sequence

For the initial Repora workstream:

1. define repository/endpoint/trust-domain semantics and keep classification separate from authority;
2. generalize canonical role semantics;
3. support generic Forgejo installations without making any particular installation required;
4. prove deterministic private-to-public projection first;
5. add staging-to-canonical promotion after the lower-risk projection mechanics are understood;
6. add public contribution import only after projection mappings can explicitly describe invertibility;
7. add archive coverage independently;
8. defer overlays until a concrete consumer exists.

This is implementation guidance, not semantic coupling between the relationship types.

## Related work

- `hackelia-micrantha/repora#149` — repository topology/trust-domain epic.
- `hackelia-micrantha/repora#147` — local workspace manifests/bootstrap.
- `hackelia-micrantha/repora#30` — optional Anthesis pre-apply integration.
- `ryjen/dubnium#248` — sovereign Git hosting.
- `ryjen/dubnium#528` / `#536` — private/public product boundary and publication gate.
- `ryjen/dubnium#922` — constrained Forgejo staging endpoint.
- `hackelia-micrantha/anthesis#203` — effect-time authority freshness/state dependencies.
- `hackelia-micrantha/sandcastle#19` — checkpoint state identity for stale-state/TOCTOU detection.

## Adoption rule

Do not create topology issues in every repository preemptively. Adopt these patterns when a project gains a second endpoint, trust domain, public/private split, staging boundary, or recovery requirement. The executable model should remain centralized in Repora rather than reimplemented per project.