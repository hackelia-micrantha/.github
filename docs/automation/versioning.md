# Shared automation versioning

Reusable organization workflows are shared build infrastructure. Callers must not make a moving branch such as `@main` a required production gate.

## Version identities

Micrantha shared automation uses two reviewed identities:

1. **immutable commit SHA** — the authority for exact execution and the preferred pin for high-assurance callers;
2. **release tag** — a human-readable compatibility label of the form `automation-vMAJOR.MINOR.PATCH`, which must resolve to one reviewed immutable commit.

A release tag is convenience and discovery metadata. The commit it names is the execution identity. Moving an existing release tag is prohibited.

New starter templates are pinned to the reviewed automation-v1 candidate commit `c0016c206607f6f101b8e6b70340ad7d4ab52837`. Callers must review that pin and may advance it only through a reviewed shared-automation version change.

## Current automation-v1 candidate

Candidate execution identity:

`c0016c206607f6f101b8e6b70340ad7d4ab52837`

This revision contains the reusable Mise and Nix workflows with read-only permissions, reviewed third-party action pins, caller-selected runners, and delegated-job timeout inputs.

Pilot evidence:

- **Repora / Nix** — the shared Nix workflow passed on PR #163 and again on `main` after merge, using the same immutable shared-workflow revision. The pilot also exposed and repaired a repository-local workflow-policy assumption: caller jobs that delegate via top-level `uses:` cannot own `timeout-minutes`; the called reusable workflow must own the runtime bound.
- **Anthesis / Mise** — the shared Mise workflow passed on PR #235 on the existing `runner-anthesis` self-hosted boundary, with direct fork execution rejected and a 15-minute delegated timeout. Default-branch repeat evidence is required after merge before the Mise pilot is considered complete.

Publication of the convenience tag `automation-v1.0.0` remains a separate final release action. Until that tag exists, callers should continue using the immutable candidate SHA.

## Compatibility policy

- **PATCH** — fixes that preserve workflow inputs, permission expectations, job/check names, and normal caller behavior.
- **MINOR** — backward-compatible inputs or capabilities; existing pinned callers continue to work without changes.
- **MAJOR** — removes or changes inputs, permissions, runner assumptions, job/check names, or other caller-visible contracts.

Changes are classified by caller impact, not by implementation size.

## Release evidence

Before publishing an automation version:

1. meta validation is green on the exact candidate commit;
2. third-party actions remain pinned to reviewed commits;
3. permissions and secret requirements are reviewed;
4. at least one representative caller exercises each reusable workflow family included in the release;
5. caller workflows pin the exact candidate commit during the pilot;
6. fork/self-hosted-runner behavior is recorded;
7. stable job/check names and rollback are documented.

The release tag is published only after the candidate commit is reviewed. A caller may use the immutable candidate SHA before the convenience tag exists.

## Pilot and promotion

Pilots are additive. They must not replace repository-owned build/test logic until repeated success shows that the shared wrapper preserves the repository contract.

A successful pilot proves only the wrapper/caller integration it actually exercises. It does not prove that another repository, runner, secret model, or task is compatible.

After at least one pull-request run and one default-branch run succeed for the same pinned shared-workflow revision, the caller may choose to adopt the wrapper more broadly. Making the check required remains a repository-local decision.

## Fork and runner boundaries

Reusable workflows do not weaken the caller's trust boundary.

- Private or self-hosted callers must preserve their existing fork rejection or trusted-import policy.
- The caller selects the runner explicitly when the default hosted runner is inappropriate.
- A reusable workflow does not gain secrets or permissions merely because another caller has them.
- Repository-scoped credentials, deployment authority, and mutation remain outside the initial shared CI workflows.

## Rollback

Rollback is deterministic: change the caller's `uses:` reference back to the last known-good immutable commit or release tag and re-run the caller's normal validation. No shared branch force-push or tag movement is required.

If the failure is in repository-owned task logic rather than the shared wrapper, fix the owning repository instead of rolling shared automation backward.
