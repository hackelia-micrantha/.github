# Automation security boundaries

Shared automation is a convenience and policy surface, not a new source of repository authority.

## Trust model

- Caller repositories control their workflow triggers, inputs, task definitions, and required-check configuration.
- Reusable workflows run with the caller's event context and effective permission ceiling.
- The shared CI workflows request only read access to repository contents and do not declare secrets.
- Caller-supplied runner labels, commands, or task names are repository-controlled configuration and must not be populated directly from untrusted issue, pull-request, branch, commit, or dispatch text.
- Untrusted fork code must not run on persistent privileged self-hosted runners.

## Inputs

Inputs are intended for reviewed workflow configuration. Do not pass untrusted event fields directly into:

- runner selection;
- working directories;
- mise task names;
- Nix commands or configuration;
- artifact names or paths;
- deployment or publication targets.

A repository that needs dynamic behavior should validate it against a fixed allowlist before calling a shared workflow.

## Secrets and permissions

The initial reusable workflows do not accept or inherit caller secrets. Adding secrets or write permissions requires a dedicated design and security review covering:

- authority and least privilege;
- event and fork behavior;
- protected environments;
- credential exposure paths;
- evidence and approval;
- rollback and incident response;
- current callers and migration.

## Label mutation boundary

The current label-sync implementation is report-only and has no write credential or `apply` path.

The separately reviewed [label mutation authority contract](label-mutation-authority.md) defines the required boundary before mutation can be implemented. The first `.github`-only pilot separates read-only preflight from the only write-authorized job. The apply job may use the ephemeral repository-scoped `GITHUB_TOKEN` with only `contents: read` and `issues: write`; no broader repository or organization permission is required for repository label creation.

Mutation must be manual-dispatch only, default-branch only, exact-plan-bound, stale-safe, collision-safe, and restricted to the reviewed repository/label allowlist. After approval, the write-authorized job must verify that the **live** default-branch tip still equals the approved control-plane revision, then re-read live label state. Pull requests, forks, pushes, schedules, issue comments, and repository dispatches must not obtain label-write authority.

A later cross-repository rollout must mint a short-lived GitHub App installation token scoped to the exact reviewed repository set and repository `Issues: write`. Broad personal tokens, classic PATs, and organization-admin authority are not acceptable substitutes.

The first mutation implementation is **create-only**. Metadata update is deferred because the label update API has no documented compare-and-swap/conditional write contract, leaving a residual read/write overwrite race. Alias migration/rename requires a separate reviewed decision; delete is unsupported initially. Every create must re-check its exact precondition immediately before the API request and stop on conflict rather than reinterpret changed state.

## Third-party actions

Third-party actions are pinned to reviewed commit SHAs. Version comments are informational; the SHA is the executed identity. Updates require reviewing release notes, runtime changes, permissions, and supported runner versions.

## Health-report token

`ORG_REPOSITORY_READ_TOKEN` is optional and should be a fine-grained token or GitHub App token limited to read-only metadata and contents for the registered repositories.

The health script does not print the token or API response bodies. It reports inaccessible private repositories as unknown rather than proving absence.

## Reporting vulnerabilities

Follow the organization security policy. Do not include credentials, private repository contents, exploit payloads, or sensitive runner details in public issues or health artifacts.
