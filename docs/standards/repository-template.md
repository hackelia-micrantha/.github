# Thin repository template

Status: Proposed reference transport for the repository-bootstrap standard.

The Micrantha generic GitHub repository template is an **optional creation transport**, not a policy source, starter kit, or golden implementation repository.

## Authority

The authoritative bootstrap semantics remain in [Repository bootstrap](repository-bootstrap.md). The reference skeleton in `templates/thin-repository/` is intentionally pinned to the accepted bootstrap v1 schema revision and exists so the eventual GitHub template repository can be created and audited without inventing defaults.

Template contents copied into a generated repository become ordinary repository-local materialized state. They do not inherit future template changes and do not override current organization/project policy.

## Required tree

The generic template contains exactly:

```text
README.md
.repora/
  bootstrap.proposed.json
```

The proposal path is `.repora/bootstrap.proposed.json`, matching `repoctl bootstrap init`.

The default proposal leaves every project/repository design decision unresolved except `repository.defaultBranch=main`, which is resolved from organization policy.

## Forbidden generic contents

Do not add any of the following merely because a repository is created:

- LICENSE or license selection;
- implementation language/runtime scaffold;
- package manager or build-system files;
- language-specific `.gitignore`;
- `flake.nix`, `flake.lock`, or executable CI merely as placeholders;
- CI, release, deployment, or environment workflows;
- project-specific CODEOWNERS;
- CLI/service/library/web/mobile implementation scaffolds;
- copies of community-health files already inherited from the public organization `.github` repository.

Executable CI applicability remains an explicit decision. When it is applicable, the repository must converge on the organization flake-first CI standard rather than treating template presence as compliance.

## GitHub provider creation contract

Template-based repository creation is allowed only after the provider-required decisions are explicit.

A reviewed creation plan must:

1. bind the exact template repository plus immutable commit/tree identity;
2. pass repository visibility explicitly; omission must not fall through to GitHub's public/private default;
3. pass `include_all_branches=false`;
4. create only the organization-authorized `main` branch unless another branch requirement is explicitly resolved;
5. preserve the resolved repository name and other provider-required values exactly;
6. run the generated repository through normal `repoctl bootstrap inspect -> plan -> apply` verification;
7. fall back to another reviewed provisioning path if the template-generation API cannot represent a resolved decision without coercion.

Template freshness alone is not a compliance requirement.

## Repository identity decisions

Before the actual GitHub template repository is created, these provider-level choices remain explicit human decisions:

- final template repository name;
- template repository visibility.

The repository-local bootstrap manifest path is resolved by the implemented Repora contract as `.repora/bootstrap.proposed.json`.

## Validation

Organization tests enforce the reference tree and reject common architectural defaults in the generic skeleton. The eventual GitHub template repository should be compared against this reference tree and pinned revision before it is treated as an approved creation transport.
