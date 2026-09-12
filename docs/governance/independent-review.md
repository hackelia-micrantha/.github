# Independent review for privileged changes

This document defines what counts as **independent review** for privileged automation, security-boundary, release-authority, credential, governance, and other high-impact changes in the Micrantha organization.

It complements [organization governance](../../GOVERNANCE.md). Review produces evidence and challenge; it does not itself grant decision, risk-acceptance, merge, release, or mutation authority.

## Purpose

Micrantha is often maintained by a single human steward. Requiring a second repository maintainer for every privileged change would make the rule unusable, while allowing the author to self-attest would make it meaningless.

The policy therefore separates:

- **author/implementer** — creates or materially changes the candidate;
- **independent reviewer** — challenges the candidate without having authored that candidate and without mutation authority in the review process;
- **decision/merge/release owner** — exercises the authority assigned by governance after considering review evidence.

One human may remain the repository steward and merge owner. The independent-review requirement is satisfied by an independent review producer/process, not by adding unnecessary repository administration rights.

## When independent review is required

Independent review is required before merging or exercising a change that materially alters any of these boundaries:

- repository, organization, or cross-repository write authority;
- credentials, secrets, signing keys, token scope, or identity binding;
- protected environments, approval gates, branch/ruleset enforcement, or bypass behavior;
- release, publication, signing, promotion, or deployment authority;
- destructive or difficult-to-reverse automation;
- security controls, trust boundaries, residual-risk acceptance mechanisms, or incident-evidence integrity;
- organization governance that defines who or what may authorize privileged effects;
- an existing policy or workflow that explicitly names independent review as an acceptance gate.

Ordinary documentation, local reversible implementation, tests, and read-only reporting do not acquire this requirement merely because they live in `.github`. A repository or issue may impose a stricter gate.

## Independence requirements

A review counts as independent only when all of the following are true:

1. **Non-author** — the reviewer did not author or materially generate the candidate revision being accepted.
2. **Read-only review context** — the reviewer does not need write credentials or mutation capability to perform the review.
3. **Exact evidence** — the review identifies the exact commit SHA reviewed, or qualifies under the bounded-follow-up rule below.
4. **Challenge, not confirmation** — the reviewer is asked to find defects, unsafe assumptions, authority escalation, stale-state/TOCTOU gaps, rollback/evidence failures, and contradictions rather than merely approve the proposal.
5. **Attribution** — the evidence identifies the reviewer mechanism sufficiently to distinguish it from the authoring process.
6. **Disposition** — material findings are resolved, explicitly accepted by the accountable authority, or leave the change blocked.

A merge performed by the author, a CODEOWNERS match, passing CI, lack of objections, or a second self-review does **not** satisfy independence by itself.

## Accepted reviewer mechanisms

Use the narrowest available mechanism that provides credible independent challenge.

### 1. Independent human reviewer

A human who did not author/materially implement the candidate may review the exact revision. They do not need repository administration rights merely to provide review evidence.

When a trusted maintainer/reviewer team exists, GitHub review is the preferred human record.

### 2. Independent automated/model reviewer

A configured review service or model may satisfy the gate when:

- it did not generate/materially author the candidate revision;
- it reviews the exact diff/revision in a separate review context;
- the review path is read-only with respect to the repository;
- its identity/provider/tool is recorded;
- findings and dispositions are retained in the PR or linked durable evidence.

Examples include a dedicated PR-review bot, security-review service, or a separate model review workflow. A provider/model quota failure is an unavailable reviewer, not a clean review.

### 3. Manual external/local model fallback

For a solo-maintainer repository, an external or local model may be used without granting it repository write access.

The maintainer prepares a **review bundle** containing:

- repository and pull request/issue identifier;
- exact candidate commit SHA;
- exact diff or immutable patch reference;
- relevant authority/security contract and acceptance criteria;
- a review prompt that asks for adversarial findings and explicitly forbids assuming approval;
- any validation evidence needed to assess the boundary.

Run that bundle in a separate model/provider/context that did not materially author the candidate. Preserve the reviewer identity/provider/model when known, the exact reviewed SHA, the prompt or prompt digest, and the complete findings/disposition as a PR comment, attached artifact, issue, ADR, or other durable repository evidence.

Local models are acceptable when the same evidence and separation requirements are met. This gives the organization a fallback that does not depend on a hosted reviewer quota or on granting another service mutation authority.

## Reviewer diversity and provider independence

No single reviewer provider, model, subscription quota, or bot is a mandatory dependency for the organization.

For a normal privileged change, **one acceptable non-author independent review** is sufficient unless a stricter issue/repository gate applies.

For exceptionally broad effects—organization administration, broad cross-repository mutation, root/signing-key authority, destructive organization-wide operations, or bypass of existing approval boundaries—the decision owner should require either:

- an independent human reviewer; or
- two independent review mechanisms, preferably from different providers/model families, before accepting the change.

This additional diversity is a risk control, not a general requirement for every security-related edit.

## Exact-head rule

Independent review must normally bind to the exact revision that will be accepted when the change affects privileged semantics.

Exact-head review is required for changes to:

- permissions, credentials, workflow events, protected environments, mutation behavior, release authority, or security controls;
- normative governance or authority semantics;
- executable code implementing a privileged boundary;
- a prior finding's substantive remediation.

### Bounded follow-up exception

A new independent review is not required after an already reviewed revision only when every follow-up change is mechanically bounded and cannot change the reviewed authority/behavior. Examples:

- spelling or punctuation corrections;
- formatting-only changes;
- corrected links/references;
- generated indexes or metadata with deterministic validation;
- clean rebasing that preserves the reviewed file contents exactly.

The PR must record the reviewed ancestor SHA and evidence that the follow-up is mechanically bounded. Any normative wording change, executable change, permission/event change, or ambiguity about semantic effect invalidates this exception and requires exact-head review.

## Evidence record

The review evidence should record at least:

```text
reviewed_sha: <40-hex commit>
reviewer_kind: human | automated-service | external-model | local-model
reviewer_identity: <GitHub login, service, model/process identifier>
provider: <provider or local runtime when applicable>
independence_basis: <why reviewer did not author/materially generate candidate>
scope: <security/authority surfaces reviewed>
review_prompt_or_check: <text, stable reference, or digest>
result: clean | findings | blocked
findings: <links or identifiers>
disposition: <resolved/accepted/blocked with accountable owner>
evidence_ref: <PR review/comment/artifact/issue/ADR>
```

The record must not contain secrets, tokens, private keys, or unnecessary private repository content.

## Relationship to approval and authority

Independent review is **evidence**, not approval authority.

- A model or bot cannot accept residual risk merely by returning a clean review.
- A reviewer does not become a release owner or organization administrator by reviewing a change.
- The accountable human decision owner remains responsible for findings disposition and final authority.
- Protected-environment approval must still bind to the exact privileged effect when required by the implementation contract.

## CODEOWNERS and solo-maintainer repositories

`CODEOWNERS` records stewardship/review routing. It is not proof of independent review.

If the only CODEOWNER authored the change, their approval/merge can satisfy repository ownership but not a separate non-author review gate. Do not add broad collaborators or administrative permissions solely to manufacture independence. Use an accepted independent reviewer mechanism instead.

When additional trusted maintainers exist, a reviewer team may be added and used as the preferred independent human path.

## Failure and unavailable-reviewer behavior

Fail closed when a privileged change requires independent review and no acceptable reviewer is available.

- A bot/provider quota error is not a review.
- A syntactically accepted reviewer request with no resulting review evidence is not a review.
- A timed-out or partial review is not clean unless its evidence explicitly covers the required scope.
- Do not downgrade the change classification merely to avoid the gate.

Read-only preparation, tests, design work, and evidence gathering may continue while the gate is blocked, provided they do not merge or exercise the privileged capability being protected.

## Bootstrap and policy changes

This policy itself is organization governance. The organization owner may land the initial policy under the pre-existing governance model, but once landed, future material changes to this policy require the independent-review rules defined here.

A policy edit that merely fixes links, spelling, or formatting may use the bounded-follow-up rule.

## Practical review bundle prompt

A fallback reviewer should receive a prompt equivalent to:

> Review the exact candidate revision adversarially. Do not assume the proposal is approved. Look specifically for authority escalation, permission/event exposure, stale-state and TOCTOU errors, credential leakage, bypass paths, evidence/attribution gaps, rollback/quarantine failures, contradictions with repository governance, and claims stronger than the implementation can guarantee. Report actionable findings by severity and state explicitly if no material finding remains. Do not mutate the repository.

The repository may provide more specific project/security context, but it should not bias the reviewer toward approval.

## Reassessment

Revisit this policy when:

- the organization gains additional trusted maintainers;
- a stable multi-provider automated review workflow exists;
- Anthesis can record/verify reviewer evidence without becoming a bootstrap dependency;
- GitHub review/environment capabilities materially change;
- an incident shows that the independence or evidence rules are insufficient.
