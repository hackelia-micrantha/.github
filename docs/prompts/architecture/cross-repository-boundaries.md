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
- where context identity, runtime execution, governance, cryptographic sender binding, domain observation, verification, and trusted-state promotion belong when an agentic workflow spans repositories;
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

### 3. Dependency, authority, and contract direction

Map:

- build-time and runtime dependencies;
- control, data, and artifact flows;
- API, schema, protocol, and event ownership;
- policy, approval, evidence, verification, and execution boundaries where applicable;
- release and synchronization flows;
- circular dependencies or reverse ownership.

Prefer explicit contracts over shared internal implementation when repositories require independent evolution.

For agentic systems, map the **authority chain separately from the runtime dependency graph**. At minimum identify which repository or component owns:

- prompt/context composition identity;
- execution and operational run state;
- policy and approval decisions;
- verifier/check execution and verifier identity;
- governance interpretation and trusted-state promotion;
- cryptographic sender or workload binding;
- domain-specific postcondition observation;
- evidence storage/provenance and replay semantics.

A consumer dependency does not transfer the producer's authority. A runtime that calls a governance service does not become policy authority; a context-integrity library does not become workflow truth; a sender-binding library does not become application authorization; a domain observer does not become governance authority.

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
- agent, policy, approval, executor, verifier, and observer trust domains;
- dependency compromise and repository takeover blast radius.

### 6. Agentic state-integrity and authority drift

Where repositories participate in one long-running or effectful agent workflow, check for boundary collapse such as:

- executor or provider self-report directly becoming trusted completion;
- supervisor synthesis being treated as independent verification merely because it aggregates specialist output;
- verifier/evaluator roles silently inheriting executor mutation authority where separation is security-relevant;
- context manifests, lockfiles, prompt attestations, or memory summaries being treated as task truth or authorization;
- sender binding, signatures, attestations, checksums, or evidence-bundle integrity being overclaimed as semantic task correctness or application authorization;
- provider submission receipts being treated as proof that the intended external state was realized;
- evidence, prior success, replay, or recovery state minting new authority;
- verification for one task/candidate/artifact/effect revision being reused after the subject materially changes;
- unavailable or inconclusive verification being converted into success;
- full transcripts or model scratch history becoming the canonical cross-repository workflow state.

When verification is required, identify:

- the exact verification subject;
- who produced the result;
- who or what verified it;
- what capability the verifier had;
- which repository defines the acceptance/evidence requirement;
- which repository interprets the verification result;
- how rejected, superseded, and indeterminate outcomes remain attributable;
- how retry or recovery reconstructs current state without relying on ambiguous transcript interpretation.

The producing component must not, by its own assertion alone, satisfy a verification requirement intended to establish its result as trusted.

### 7. Migration and lifecycle

For transitional boundaries identify:

- authoritative target;
- work remaining before migration;
- compatibility period;
- data, issue, release, and documentation migration;
- redirect or deprecation plan;
- archive criteria;
- rollback or coexistence strategy.

Avoid indefinite dual authority.

### 8. Work tracking

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

Provide a Mermaid diagram showing relevant control, data, authority, contract, artifact, verification, and release flows. Distinguish authoritative dependencies from transitional or test relationships.

### E. Overlap and boundary findings

| Finding | Classification | Evidence | Impact | Recommendation |
| --- | --- | --- | --- | --- |

### F. Target boundary model

Describe the recommended responsibility, contract, dependency, trust, verification, public/private, and lifecycle model. Prefer the smallest change that removes material ambiguity.

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
- **Agentic authority or state-integrity boundary requires clarification**
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
