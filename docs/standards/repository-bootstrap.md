# Repository bootstrap

Micrantha repository bootstrap is **policy-driven, explicit, and fail-closed**.

The bootstrap contract exists to make new repositories consistent without turning missing information into architecture or product decisions. It is an organization standard owned by `.github`; tools such as Repora may consume and enforce it, but they do not acquire authority to invent organization defaults.

The central rule is:

> Unknown is a valid state. Missing information must not become a design decision.

This standard tracks [#121](https://github.com/hackelia-micrantha/.github/issues/121).

## Scope

This contract covers creation-time and early-bootstrap decisions whose accidental selection can become durable repository architecture, including:

- repository purpose, visibility, classification, maturity, and default branch;
- source exposure, repository topology/role, and distribution mode;
- license;
- implementation language, runtime, build system, and package manager;
- supported interfaces such as CLI, service, library, web, or mobile surfaces;
- CI provider/shape;
- release and distribution model;
- security posture/profile where a project-specific choice is required.

The list is not exhaustive. New decision keys may be introduced without treating unrecognized keys as optional defaults.

## Decision states

Every material bootstrap decision is represented explicitly as one of three states.

### `resolved`

A value is authorized and records provenance.

A resolved decision requires:

- a concrete non-null value;
- an authority class;
- a durable reference identifying the human decision or applicable policy.

Accepted authority classes in v1 are:

- `human`;
- `organization-policy`;
- `project-policy`.

Repository observations are deliberately **not** an authority class.

### `unresolved`

No authorized value currently exists.

An unresolved decision:

- has no value;
- has no decision provenance;
- may include the question that must be answered;
- remains visible in planning output.

Automation must not substitute a conventional value, neighboring-repository value, detected-tool value, or tool default.

### `not-applicable`

The decision has been considered and is explicitly inapplicable.

This is an affirmative decision, not omission. It therefore requires:

- a reason;
- decision provenance.

For example, a repository may explicitly declare a package-manager decision not applicable after a human or applicable policy establishes that no package manager is used.

## Resolution order

For a decision required by a planned action, resolution order is:

1. an explicit project/human decision;
2. an explicitly applicable project policy;
3. an explicitly applicable organization policy;
4. `unresolved`.

There is no heuristic fallback.

A lower-precedence source must not overwrite a higher-precedence explicit decision without a separately reviewed change.

## What does not count as a decision

Inspection can produce evidence, but evidence is not authority.

The following may be observations:

- a repository name ending in `ctl`;
- existing `.go`, `.rs`, `.ts`, or other source files;
- a detected package-manager lock file;
- GitHub visibility;
- a neighboring project's conventions;
- a workflow already present in the repository;
- historical organization frequency;
- an LLM recommendation;
- a template's internal default.

None of those observations may silently resolve a bootstrap decision.

Examples:

- `fooctl` does not imply that the project is a CLI.
- Go source does not prove Go is the intended long-term implementation language.
- public GitHub visibility does not select a license.
- private visibility does not select a public/private repository topology.
- a Node project does not select npm, pnpm, Yarn, or Bun.
- an existing GitHub Actions workflow does not by itself authorize GitHub Actions as the desired CI model.

An operator or applicable policy may review an observation and create a new resolved decision. That promotion is a distinct, attributable transition.

## Manifest

The v1 machine-readable contract is:

- schema: [`metadata/repository-bootstrap.schema.json`](../../metadata/repository-bootstrap.schema.json);
- minimal example: [`templates/repository-bootstrap.json`](templates/repository-bootstrap.json).

A manifest is a list of keyed decisions rather than a structure in which omitted properties acquire defaults.

Example decision:

```json
{
  "key": "repository.visibility",
  "state": "unresolved",
  "question": "Should this repository be public, private, or internal?"
}
```

A resolved decision carries authority:

```json
{
  "key": "repository.visibility",
  "state": "resolved",
  "value": "private",
  "provenance": {
    "authority": "human",
    "reference": "approved bootstrap request"
  }
}
```

The schema intentionally contains no JSON Schema `default` keywords.

## Missing keys

A missing decision key means only that the manifest does not contain that decision.

It does **not** mean:

- false;
- empty;
- disabled;
- the organization default;
- the tool default;
- not applicable.

If an action needs a missing decision key, the planner must report that requirement as unresolved/missing before the action can become executable.

This lets the manifest evolve without converting schema growth into silent behavior changes.

## Automatic bootstrap lifecycle

The intended automation lifecycle is:

```text
bootstrap trigger
  -> initialize decision manifest
  -> inspect current state
  -> resolve only explicit/applicable policy decisions
  -> plan exact changes + decision dependencies
  -> review
  -> apply exact reviewed plan
  -> verify resulting state
```

A bootstrap trigger may come from a local command, a newly detected repository, or future reviewed provider provisioning.

### Initialize

Initialization creates a manifest skeleton without overwrite.

Initialization must not choose material values merely to make the file complete.

### Inspect

Inspection is read-only.

It may record repository facts and evidence, but it must keep those observations separate from authorized decisions.

### Plan

Planning must:

- be deterministic for the same manifest, policy inputs, and observed state;
- list actions that are ready;
- list actions blocked by unresolved or missing decision keys;
- identify the decision dependencies of each action;
- avoid rendering unresolved values into output files;
- produce machine-readable output suitable for review and composition.

Unresolved decisions block only the actions that depend on them. They do not prevent an unrelated action whose complete authority and inputs are already established.

### Apply

Apply must consume an exact reviewed plan rather than re-deciding values during execution.

Apply must:

- fail stale when relevant observed state changed;
- never ask a renderer, framework, provider, or API to fill missing semantic values;
- preserve partial-result honesty;
- emit durable result/evidence appropriate to the effect;
- remain within the mutation authority of the invoked tool.

Provider repository creation is outside the v1 organization contract until a consuming implementation defines and reviews that capability separately.

## Template behavior

A repository bootstrap template is a **question and policy carrier**, not a bag of preferred technology defaults.

Template and schema authors must not:

- use JSON Schema defaults for material decisions;
- use empty string, `null`, false, or omission as a disguised default;
- branch on repository names to choose architecture;
- detect source files and silently select a language/runtime contract;
- copy licenses automatically;
- install a CI/release stack solely because it is common elsewhere;
- infer source-exposure topology from provider visibility;
- infer release authority from repository location.

Assumption-free files may be applied automatically only when their applicability is established by explicit policy or an explicit project decision.

## Provenance and later migration

Decision provenance is retained so later tooling can distinguish:

- a human/project-specific choice that must not be overwritten casually;
- an organization-policy decision that may become a migration candidate when that policy changes.

Policy evolution must not reinterpret an old human decision as inherited merely because the current organization policy now matches it.

## Authority boundaries

- **`.github`** owns organization bootstrap semantics, schemas, and shared standards.
- **Project repositories** own project-specific decisions and tighter local policy.
- **Repora/repoctl** may validate, inspect, plan, apply, and record evidence within its reviewed implementation boundary.
- **Anthesis** may evaluate approval/policy/evidence where an enforced governance runtime is used.
- Repository/provider provisioning requires its own reviewed capability and authority.

A consuming tool must not become a governance source merely because it implements this contract.

## Relationship to existing standards

Bootstrap resolves *which* standards and capabilities apply; it does not duplicate those standards.

Use the existing organization guidance for the resulting repository:

- [Repository topology and trust domains](../architecture/repository-topology-and-trust-domains.md)
- [Source exposure topologies](../architecture/source-exposure-topologies.md)
- [Source exposure and distribution](source-exposure-and-distribution.md)
- [CLI interoperability](cli-interoperability.md)
- [CLI design and UX](cli-design-and-ux.md)
- [CI/CD](ci-cd.md)
- [Testing and validation](testing.md)
- [Security engineering](security.md)
- [Documentation](documentation.md)
- [Releases and versioning](releases.md)

## Initial Repora integration

Repora implementation is tracked separately in [repora#193](https://github.com/hackelia-micrantha/repora/issues/193).

The intended command surface is namespaced so repository bootstrap does not collide with existing Repora mirror plan/apply semantics:

```text
repoctl bootstrap init
repoctl bootstrap inspect
repoctl bootstrap plan
repoctl bootstrap apply
```

The exact CLI is owned by Repora and remains subject to the Micrantha CLI standards. The organization contract defines semantics, not implementation architecture.
