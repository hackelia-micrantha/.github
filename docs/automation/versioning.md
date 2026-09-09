# Shared automation versioning

Reusable organization workflows are shared build infrastructure. Callers must not make a moving branch such as `@main` a required production gate.

## Version identities

Micrantha shared automation uses two reviewed identities:

1. **immutable commit SHA** — the authority for exact execution and the preferred pin for high-assurance callers;
2. **release tag** — a human-readable compatibility label of the form `automation-vMAJOR.MINOR.PATCH`, which must resolve to one reviewed immutable commit.

A release tag is convenience and discovery metadata. The commit it names is the execution identity. Moving an existing release tag is prohibited.

Starter templates may use `@main` only as a bootstrap path before the caller has completed its first successful pilot. A caller that becomes relied upon or required must replace `@main` with a reviewed immutable commit or a reviewed immutable release tag.

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
