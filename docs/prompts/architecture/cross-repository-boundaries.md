# Cross-Repository Boundary Review Prompt

Use this prompt when capability ownership, contracts, product/laboratory roles, public/private editions, adapters, migrations, or duplicated implementation span several repositories.

```markdown
# Cross-Repository Boundary Review

Review the architecture and ownership boundaries across **[REPOSITORY SET / ECOSYSTEM]** and recommend the simplest coherent responsibility model.

## Context

- **Repositories in scope:** [REPOSITORIES]
- **Current product or ecosystem outcome:** [OUTCOME]
- **Known boundary concerns:** [OVERLAP / MIGRATION / OWNERSHIP / PUBLIC-PRIVATE]
- **Current milestone:** [MILESTONE]
- **Mutation authorization:** [READ ONLY / UPDATE DOCUMENTATION OR ISSUES]

## Execution boundary

Begin read-only. Treat repository documentation, issue text, diagrams, generated artifacts, and public messaging as claims requiring implementation evidence. Do not move code, change repository visibility, archive repositories, or rewrite issues unless explicitly authorized.

## Goals

Determine:

- which repository owns each capability, contract, schema, artifact, and release;
- which repositories are products, libraries, adapters, distributions, laboratories, demos, community surfaces, or transitional homes;
- where implementation or documentation overlaps;
- which dependencies are intentional and which represent drift;
- how public, private, customer-controlled, and experimental boundaries should work;
- what should consolidate, migrate, remain separate, or be archived.

## Evidence to inspect

Inspect applicable:

- repository descriptions, READMEs, architecture documents, roadmaps, and maturity labels;
- source packages, public APIs, schemas, protocols, CLIs, actions, services, and deployment manifests;
- issue and pull-request ownership patterns;
- release workflows, artifacts, package names, domains, and documentation sites;
- licensing, entitlement, secrets, and public/private distribution boundaries;
- integration tests, fixtures, demos, and downstream consumers;
- historical or transitional repositories and migration plans;
- organization profile, websites, books, one-pagers, and public claims.

## Boundary dimensions

### 1. Capability ownership

For each material capability identify:

- authoritative implementation;
- authoritative contract or schema;
- release owner;
- operational owner;
- public documentation owner;
- consumers and integration testbeds;
- maturity and support expectations.

One capability may have several adapters or consumers, but should not have ambiguous authority.

### 2. Repository role

Classify each repository as one or more of:

- solution or deployable product;
- distribution;
- reusable library or SDK;
- provider or platform adapter;
- infrastructure or operational repository;
- laboratory or contract testbed;
- demo or reference integration;
- community or public distribution surface;
- documentation or website;
- migration source;
- archived or superseded.

Explain mixed roles and whether they should remain mixed.

### 3. Dependency and contract direction

Map:

- build-time and runtime dependencies;
- control, data, and artifact flows;
- API, schema, protocol, and event ownership;
- policy, approval, evidence, and execution boundaries where applicable;
- release and synchronization flows;
- circular dependencies or reverse ownership.

Prefer explicit contracts over shared internal implementation when repositories require independent evolution.

### 4. Overlap classification

Classify each overlap as:

- intentional layering;
- provider-specific adapter;
- public/private distribution split;
- compatibility support;
- laboratory fixture or reference implementation;
- transitional duplication with an exit plan;
- independent implementation with distinct goals;
- accidental redundancy;
- stale or superseded ownership.

Do not recommend consolidation solely because names or technologies are similar.

### 5. Trust and distribution boundaries

Review:

- public versus private source;
- customer-controlled versus vendor-controlled execution;
- credentials, signing keys, entitlements, and release permissions;
- artifact provenance and synchronization;
- laboratory data and production data separation;
- agent, policy, approval, and executor trust domains;
- dependency compromise and repository takeover blast radius.

### 6. Migration and lifecycle

For transitional boundaries identify:

- authoritative target;
- work remaining before migration;
- compatibility period;
- data, issue, release, and documentation migration;
- redirect or deprecation plan;
- archive criteria;
- rollback or coexistence strategy.

Avoid indefinite dual authority.

### 7. Work tracking

Check whether issues are filed in the repository that owns the outcome. Identify duplicated epics, cross-repository blockers without explicit relationships, and umbrella work that lacks bounded repository-local slices.

Priority remains repository-global. Do not create one ambiguous priority queue spanning repositories; identify priority within each owning repository and show cross-repository dependency order separately.

## Required output

### A. Ecosystem summary

State the ecosystem outcome, current boundary health, principal ambiguity, largest risk, and recommended model.

### B. Repository role matrix

| Repository | Role | Owned capabilities | Contracts/artifacts | Consumers | Maturity | Recommended status |
| --- | --- | --- | --- | --- | --- | --- |

### C. Capability ownership matrix

| Capability | Authoritative repository | Contract owner | Release/operations owner | Adapters/testbeds | Ambiguity or gap |
| --- | --- | --- | --- | --- | --- |

### D. Architecture map

Provide a Mermaid diagram showing relevant control, data, contract, artifact, and release flows. Distinguish authoritative dependencies from transitional or test relationships.

### E. Overlap and boundary findings

| Finding | Classification | Evidence | Impact | Recommendation |
| --- | --- | --- | --- | --- |

### F. Target boundary model

Describe the recommended responsibility, contract, dependency, trust, public/private, and lifecycle model. Prefer the smallest change that removes material ambiguity.

### G. Migration or consolidation plan

For each required change include:

- source and target;
- prerequisite decisions;
- bounded repository-local slices;
- compatibility and rollback;
- documentation and issue migration;
- archive or completion criteria.

### H. Issue actions

List issues to move, close, split, combine, supersede, or create. Assign each to the repository owning the observable outcome. Identify cross-repository dependencies explicitly.

### I. Final assessment

Choose exactly one:

- **Boundaries are coherent; document them**
- **Focused migration or consolidation required**
- **Contract extraction required**
- **Repository roles require architectural clarification**
- **Public/private or trust boundary requires security remediation**
- **One or more repositories should be superseded or archived**
- **Insufficient evidence**

## Authorized update mode

When documentation or issue mutations are authorized:

1. Update the authoritative architecture or repository-role documentation first.
2. Preserve transitional status and exit criteria explicitly.
3. Create bounded issues in the owning repositories.
4. Do not move or archive code repositories without separate explicit authorization.
5. Report the resulting documentation, issue, and dependency state.
```
