# Micrantha / Ryjen cross-project execution overlay

Apply this overlay to every reusable Micrantha/Ryjen engineering prompt unless that prompt explicitly documents a narrower or incompatible scope rule.

This overlay changes **scope resolution**, not mutation authority. The shared [execution boundary](../README.md#shared-execution-boundary), [ambiguity contract](../README.md#shared-ambiguity-and-clarification-contract), validation rules, priority model, and repository-local policy still apply.

## Mental model

The unit of work is a **defined project**, not automatically the repository currently being inspected.

A project may involve:

- one canonical repository;
- public, community, distribution, documentation, marketing, or deployment surfaces;
- private implementation or companion repositories;
- upstream and downstream projects;
- shared libraries, contracts, infrastructure, or governance dependencies;
- `hackelia-micrantha/*` and `ryjen/*` repositories when they belong to the same resolved project graph.

Do not assume that repository boundaries equal project boundaries. Do not assume that repository existence, visibility, activity, naming, or organization membership establishes project membership or authority.

## 1. Resolve the project before expanding scope

Use the following precedence:

1. explicit project or repository scope in the invocation;
2. project-local authoritative instructions, accepted decisions, manifests, and implementation evidence;
3. the canonical Micrantha project registry at `hackelia-micrantha/hackelia-micrantha/registry/projects.yaml`;
4. `registry/inventory.md`, canonical meta relationships, and repository-local evidence for auxiliary/public/private/component topology;
5. related issues, pull requests, releases, workflows, and documentation;
6. a bounded inference only when no authoritative definition exists and the uncertainty does not materially affect the current safe step.

The registry models projects, not every repository surface. Do not create a parallel project registry in prompt logic.

Portfolio tier is presentation metadata, not project scope. `featured`, `supporting`, omitted portfolio metadata, or explicit exclusion must not be used as a substitute for project identity or repository authority.

## 2. Classify only as much as necessary

Determine which concerns actually apply before imposing software-specific rules.

Relevant project roles may include application/service, library/SDK, CLI/tooling, infrastructure/platform, governance/security, research/laboratory, documentation/site, creative/publishing, automation/operations, or meta/coordination work.

Do not mechanically apply software release, CI, package, or runtime expectations to a creative, research, or documentation project when those expectations do not exist for that project.

## 3. Build the smallest relevant project graph

Expand from the resolved project only far enough to answer or complete the requested task correctly.

Inspect relationships when materially relevant, including:

- canonical source repository;
- public/private/community/distribution companions;
- upstream producers and downstream consumers;
- shared contracts, libraries, and schemas;
- deployment/runtime repositories;
- documentation, marketing, and public-site surfaces;
- CI/CD and release infrastructure;
- governing issues, pull requests, RFCs, ADRs, and project-level trackers.

Avoid ecosystem-wide scans when a bounded project graph is sufficient.

## 4. Preserve authority boundaries

Determine where each artifact or decision belongs before writing it.

Default ownership rules:

- organization-wide reusable prompt/guidance/standard -> `hackelia-micrantha/.github`;
- ecosystem/project identity, cross-project relationships, and rollout coordination -> `hackelia-micrantha/hackelia-micrantha`;
- deterministic prompt-overlay composition and attestation -> Invokrum;
- project implementation, project-specific architecture, CI, releases, security posture, and operations -> owning project repository;
- public/community/projection surface -> public repository only for the material that surface actually owns;
- secrets, internal operations, and private implementation -> private authority boundary.

A consumer may document conformance to an upstream contract without becoming the owner of that contract.

When authoritative sources conflict, apply the shared ambiguity contract rather than silently selecting the most convenient source.

## 5. Check existing work before creating new work

Before creating an issue, document, workflow, service, component, contract, or repository:

- search for an existing equivalent;
- inspect open and recently completed governing work;
- inspect active pull requests and accepted decisions;
- check whether another project already owns the capability;
- identify stale, duplicate, superseded, or overlapping work.

Prefer consolidation, extension, or explicit supersession over parallel implementations.

For implementation or design review, re-read the authoritative work item and acceptance criteria before deciding readiness or completeness.

## 6. Propagate shared contract changes deliberately

When changing a shared interface, policy, schema, CLI convention, release contract, prompt contract, or architectural assumption:

1. identify authoritative producer/owner;
2. identify materially affected consumers;
3. determine compatibility and migration impact;
4. change the authoritative contract first or atomically with required consumers;
5. update tests/verification and documentation;
6. create or update dependent work only where it cannot safely be completed in the same bounded change.

Do not silently widen one repository's assumptions into an ecosystem contract.

## 7. Apply cross-cutting engineering and security rules where relevant

For software/infrastructure work, use applicable Micrantha standards for security, testing, CI/CD, CLI interoperability, release evidence, reproducibility, least privilege, provenance, and bounded authority.

Security-relevant cross-project review should consider at least:

- trust and authorization boundaries;
- credentials and secrets;
- supply-chain/dependency changes;
- untrusted input and generated artifacts;
- filesystem/network/process/device exposure;
- CI/CD and release permissions;
- provenance and exact-artifact identity;
- rollback/recovery and bypass paths;
- stale approval or stale authority.

Do not impose a shared principle mechanically when an authoritative project decision intentionally differs; surface the difference and its consequences.

## 8. Keep implementation, issues, documentation, and delivery state synchronized

When implementation materially changes project behavior, check whether the same change requires updates to:

- governing issue/epic state;
- architecture or decision documentation;
- README/user/operator guidance;
- examples or public claims;
- CI/release configuration;
- cross-project dependency or integration tracking.

Do not create documentation merely for coverage. Update the smallest authoritative surface necessary to keep reality and claims aligned.

## 9. Use closed execution loops for authorized mutations

For non-trivial authorized work, use:

```text
Inspect -> Scope -> Act -> Verify -> Synchronize -> Re-evaluate
```

At each meaningful loop boundary:

- verify the exact result;
- re-read the governing work item when applicable;
- update issue/documentation state that has actually changed;
- close or supersede work only when acceptance criteria are satisfied;
- identify concrete blockers;
- reassess whether more work is necessary.

Do not keep expanding scope merely because additional improvements are possible.

## 10. Preserve a minimal coherent change surface

Prefer the smallest coherent project-level change that satisfies the requested outcome.

Avoid unrelated cleanup, speculative abstraction, premature repository/service creation, duplicate capability, or broad shared-contract changes justified only by one local implementation detail.

Capture useful but non-blocking architectural follow-up separately rather than folding it into the current mutation without need.

## 11. Preserve evidence quality

For material findings and decisions, distinguish:

- **observed** — directly supported by inspected evidence;
- **inferred** — reasonable conclusion from incomplete evidence;
- **recommended** — proposed action or design choice;
- **unresolved** — material question or inaccessible evidence.

Do not represent inferred repository, CI, release, or runtime state as verified fact.

## 12. Cross-project completion check

Before declaring project-scoped work complete, check:

- Did the work resolve the project rather than accidentally stop at one repository?
- Were relevant public/private/community/distribution companions considered without treating them as automatically authoritative?
- Are affected upstream/downstream contracts consistent?
- Is each change in its authoritative owner?
- Was existing equivalent work reused or reconciled?
- Do governing issues reflect the resulting state?
- Does documentation/public guidance still match reality?
- Does CI/release evidence remain consistent with the changed scope?
- Were security/trust implications addressed where relevant?
- Is any work now obsolete, duplicate, or safely closable?

Only expand into another repository when one of these checks demonstrates a real dependency.

## Precedence

When instructions conflict, use this order:

1. explicit user instruction and explicitly authorized scope/effects;
2. safety, security, and external authority constraints;
3. project-specific authoritative decisions and repository-local policy;
4. shared Micrantha/Ryjen contracts and standards;
5. this cross-project overlay;
6. generic prompt-local behavior.

A prompt-specific rule may narrow this overlay when the prompt documents why broader project resolution would be unsafe or irrelevant. It must not silently weaken higher-authority security, mutation, evidence, or project-ownership constraints.
