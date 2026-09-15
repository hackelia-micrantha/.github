# Repository hygiene posture policy

Status: Current

## Purpose

Micrantha uses Repora to observe repository and CI posture and to evaluate explicit policy without giving the policy layer provider-mutation authority. The organization-owned profile at `metadata/posture-policy-profiles/active-code-v1.json` defines the initial baseline for actively maintained code repositories.

The profile complements `metadata/repositories.json`, the repository census, and repository-local CI. It does not replace project identity, lifecycle, source/release authority, or repository-specific security policy.

## Scope

Apply `micrantha-active-code-v1` deliberately to repositories whose current role is active code development, including appropriate incubating, active, or stable implementation repositories.

Do not apply it mechanically to archived repositories, empty placeholders, pure mirrors/projections, historical surfaces, documentation-only repositories, or community surfaces whose reviewed contract differs. Repository maturity and topology remain explicit inputs to policy selection.

## Initial rules

The v1 profile requires:

- a protected default branch when provider evidence is available;
- zero mutable third-party GitHub Action references;
- explicit workflow-level GitHub token permissions in every observed workflow.

Third-party Action mutability is evaluated from Repora's stable `ci.mutable_third_party_action_count` aggregate. Full commit SHAs and immutable digests are accepted; repository-local actions are not counted as third-party dependencies.

## Evidence semantics

Repora preserves `observed`, `unknown`, and `unavailable` evidence. Unknown or unavailable facts do not become policy passes and must remain visible in the report.

This matters for provider or plan limitations. For example, if branch-protection state for a private repository cannot be observed with the available provider capability, the result is unavailable evidence rather than an inferred configuration failure or pass.

## pull_request_target review

The first active-code profile does not make `pull_request_target` usage a universal hard failure. Target-context workflows require a trust-boundary review because legitimate metadata-only workflows and explicitly governed private-repository exceptions have different semantics.

Repora still records detailed workflow evidence and `ci.pull_request_target_workflow_count`. Review each use against the Micrantha CI standard: candidate-controlled code must not gain privileged execution merely because a workflow runs in base-repository context. Any retained executable exception must be explicit and tested.

## Read-only evaluation flow

Capture immutable repository facts, converge them offline, then evaluate the organization-owned policy profile:

```sh
repoctl posture inventory OWNER/REPO > inventory.json
repoctl posture converge \
  --inventory inventory.json \
  > posture-facts.json
repoctl posture report \
  --profile metadata/posture-policy-profiles/active-code-v1.json \
  --facts posture-facts.json \
  --as-of YYYY-MM-DD \
  --format markdown
```

The profile is external policy data. `posture inventory` performs GET-only observation and `posture converge` / `posture report` are offline. This flow does not change branch rules, workflows, repository files, releases, or any other provider state.

## Rollout

Use the profile as a reporting and triage baseline before making it a required merge gate across repositories. Review each failure against repository classification and trust boundaries, record justified exceptions explicitly, and route concrete remediation to the owning repository.

A future profile revision may add dependency maintenance, release evidence, or stronger branch requirements once the corresponding stable facts and repository-type applicability are defined. Avoid embedding dynamic workflow/action names or hidden whole-repository scoring into organization policy.
