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

Privileged automation changes that alter write authority, credentials, protected approval, release authority, destructive behavior, or security boundaries must also follow [independent review for privileged changes](../governance/independent-review.md). Passing CI, CODEOWNERS routing, or self-merge does not replace a required non-author review. When a hosted reviewer is unavailable, a separately run external or local model may provide read-only review evidence using an exact-SHA review bundle; no repository mutation credential is required for that fallback.

## Mutation boundary

Automation that changes repository state must be least privileged, explicitly authorized, exact-plan-bound, stale-safe and independently reviewed where material. Separate read-only evidence from effect credentials, recheck protected preconditions immediately before effects, and retain terminal evidence without granting the evidence collector mutation authority. Unknown outcomes require reconciliation rather than blind retry.

## Third-party actions

Third-party actions are pinned to reviewed commit SHAs. Version comments are informational; the SHA is the executed identity. Updates require reviewing release notes, runtime changes, permissions, and supported runner versions.

## Private operational reporting

Credentials must be scoped to the minimum reviewed resources and actions. Do not place private inventory, status, error details or artifact contents in public logs, reports or workflows. An inaccessible repository is unknown, not absent or healthy.

## Reporting vulnerabilities

Follow the organization security policy. Do not include credentials, private repository contents, exploit payloads, or sensitive runner details in public issues or health artifacts.
