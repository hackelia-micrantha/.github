# Local Git workspace and concurrency standard

Status: Proposed organization default. Repository-local constraints take precedence.

## Purpose and model

Minimize duplicated on-disk checkout and build state while keeping parallel humans, agents, reviews, and validation isolated. **One primary checkout and Git object store per repository per host/workspace** is the default. The primary checkout is a stable anchor, not a shared scratch surface. All additional working trees belong at `<primary>/.worktrees/<task-id>` and use `git worktree`, not repeated `git clone`.

The policy controls local directory hygiene; it does **not** authorize publishing, merging, deleting remote refs, bypassing Git review, or running system-wide garbage collection. It composes with the branching, agent-execution, and security standards.

## Identity, location, and ownership

1. Discover the canonical checkout using repository identity and Git's `--git-common-dir` (normalize SSH/HTTPS remote URLs; distinguish forks and unrelated remotes). Preserve nested groupings such as `Projects/career/data` and `Projects/micrantha/<repo>`. Do not move repositories based only on directory names.
2. The primary checkout is `main` (or a documented project-specific default), preferably clean. Avoid using it for concurrent modifications, detached reviews, or integration experiments.
3. Create a distinct short-lived branch and worktree for **each active task/actor**. Name the directory with a stable issue/PR identifier plus an optional short owner or purpose suffix, e.g. `.worktrees/issue-123-review`. No two actors modify one worktree or branch concurrently; handoff requires explicit ownership transfer.
4. Put `/.worktrees/` in the primary checkout's local `.git/info/exclude` or equivalent repository ignore policy. Do not recursively recurse through nested worktrees when auditing, formatting, or packaging the primary checkout.
5. Use `git worktree add`, `git worktree move`, `git worktree remove`, and `git worktree list --porcelain` to manage linked worktrees. Never raw-move a linked checkout or edit Git administrative pointers directly. Fetching a second full clone is exceptional and must record why sharing the object store is unsuitable.
6. One active writer per branch. A review agent is read-only in the target worktree or uses its own detached/independent review worktree. Integration work uses a separate `integration/<initiative>` worktree, not the primary checkout.
7. A task-owned writable worktree retains its **unique named branch** across clone-to-worktree migration; read-only review snapshots may intentionally remain detached. When several old clones use the same branch name at different SHAs, preserve those revisions as detached review snapshots and archived refs rather than stealing or forcing branch ownership.
8. Worktrees share the same Git refs, config, hooks, object store and maintenance state. Serialize cooperative worktree allocation, branch/ref updates and destructive Git maintenance by the resolved Git common directory (for example, a short-lived local `flock` on a common-dir lock file). This lock only coordinates participants using the convention; it does not intercept arbitrary Git commands. Keep independently untrusted actors in separate trust boundaries rather than sharing an administrative store.

## Isolation versus space

- **Share immutable or content-addressed inputs** where safe: one Git object store, the Nix store/binary cache, downloaded package caches, and compiler caches with established concurrency and hash-key semantics.
- **Isolate mutable state** that can collide: each worktree's index, generated outputs, `.direnv`, `node_modules`, test DB, containers/volumes, sockets, ports, emulator state, and deployment/preview credentials. Do not symlink build or test directories across independent agents merely to save space.
- Use repo-owned flakes as project toolchains; prefer `nix develop` with shared Nix store over full per-task container images. Derivations/caches are keyed by exact inputs; avoid creating redundant per-worktree environments when the flake lock is identical.
- Use dedicated task-scoped `TMPDIR` and test resources. Where a tool offers a concurrency-safe shared artifact cache (e.g. `sccache`), use it; do not assume arbitrary build directories are concurrency-safe. Put cache growth under a documented disk budget and use tooling-native cache eviction.
- Default to **one primary checkout plus only the worktrees needed for active, isolated tasks**. Worktree count is not an artificial cap: parallel agents can fan out when their cost and ownership are justified. Prefer keeping no unused build artifacts over imposing a global worktree maximum.

## Build, test, and clean task contract

Repositories performing local builds or tests **must provide a repository-owned, idempotent `mise clean` task**, using the canonical Mise task names `build`, `test`, and `clean` where those stages apply. The portable invocation is `mise run build`, `mise run test`, `mise run clean` (or equivalent short task invocation on supported Mise versions). Do not introduce fake build/test stages solely to satisfy naming when a repository has no such stage; document any task that cannot yet be migrated and treat a missing `clean` task as an adoption gap, not a successful cleanup.

- **Follow-through:** after each local build and/or test *sequence*, run `mise run clean` as the final stage, **including when build/test failed**. Arrange cleanup in a shell `EXIT` trap, `finally` block, or equivalent so short-circuiting validation does not skip it. If interrupted or force-killed before cleanup, record a pending cleanup and reconcile after active use ends; no process can guarantee cleanup after SIGKILL.
- **Ownership and scope:** `clean` removes only the current task/worktree's known generated build outputs, temporary test artifacts, and task-owned resources once they are no longer in use. It is safe to repeat and must not touch other agents' worktrees or shared mutable resources. Never substitute `git clean -fdx`, a broad recursive deletion, global Nix garbage collection, or shared compiler/package-cache eviction.
- **Preserve evidence first:** export build/test exit status, exact revision, required test reports, logs, coverage, and reproducibility metadata to durable evidence outside cleanup targets before `clean`. Preserve published/release artifacts and evidence required by CI or reviewers until they are safely consumed or explicitly retained.
- **Report both outcomes:** preserve the original build/test result independently from cleanup status; do not let successful cleanup hide a failing test, or a failed cleanup masquerade as a passing run. Treat cleanup failure as a separate actionable finding.
- **Repository-specific contract:** implement `clean` alongside `build`/`test` in the repository's `mise.toml` or `.mise.toml`. The task must declare precisely which paths/resources it owns. If build outputs live entirely in an immutable shared Nix store (e.g. `nix build --no-link`), `clean` may have no local outputs to remove; document that explicitly rather than evicting shared store objects.
- **No cross-agent cleanup:** do not run cleanup while another task or process depends on the same mutable outputs. Prefer task-scoped output locations or allocation locks over guessing whether a directory is unused.

A failure-safe local sequence, assuming the repository provides all three tasks:

```bash
set -euo pipefail
finish() {
  result=$?
  trap - EXIT
  if ! mise run clean; then
    echo "cleanup failed (original build/test exit: $result)" >&2
    exit 1
  fi
  exit "$result"
}
trap finish EXIT
mise run build
mise run test
```

Run `mise run clean` in the **same task worktree** that produced the outputs. A `test`-only operation uses the same cleanup wrapper without the build step. Cleanup is distinct from *retiring a completed Git worktree*, which remains governed by the lifecycle checks below.

## Lifecycle and retention

1. **Acquire:** resolve canonical repo and primary, check existing task worktree/branch, allocate unique task/actor identity, ensure the base commit is recorded, then `git worktree add`. Do not reuse an unrelated previous task's worktree.
2. **Work:** record owner, task, branch, base SHA, worktree path, last activity, and any non-Git artifacts that must be retained. Treat running processes, open files, locks, and in-flight operations as active.
3. **Handoff/review:** leave the exact commit and dirty-state evidence; do not share the writer's index with another agent. Revalidate the exact candidate after integration when warranted.
4. **Close:** confirm PR/issue disposition and local changes, untracked/ignored files, stash, submodules, local-only refs, and commits against the designated authoritative base. Reconcile squash-merged branches by PR/evidence, **not** by Git ancestry alone.
5. **Clean:** only with explicit cleanup authority, remove a completed clean worktree via `git worktree remove`, then remove the unused branch via `git branch -d` when proven integrated. Do not use `-D`, `--force`, `git clean -fdx`, `git reset --hard`, or provider ref deletion in routine hygiene.
6. **Defer:** dirty, locked, uncertain, in-progress, detached, unique-history, or unobservably busy workspaces remain protected. Record a specific blocker and next verification; avoid age-based automatic deletion. Stale age merely triggers review (suggested: 14 days since use).
7. **Duplicates:** reconcile each independent clone's HEAD, all refs/tags/stashes, reflog-only commits, ignored and untracked data, and alternate/additional worktrees. Preserve unique commits in namespaced refs or a verified Git bundle before retiring a clone. Quarantine alone does **not** recover space; actual deletion is a separately gated transition with a tested recovery path and retention policy.
8. **Reconcile:** rerun inventory after every batch. Report paths, branch/ref changes, retained work, bytes genuinely reclaimed (same filesystem/allocated blocks), and rollback/recovery mappings. Do not report moved bytes as reclaimed.

## Safety boundaries

- Never guess unused status from branch naming, absence of upstream, age, or remote UI alone. Protected branches, source-of-truth branches, release branches, and active worktree branches are excluded.
- A checkout that is clean can still contain unique local commits, tags, stashes, reflog history, ignored files, or valuable CI evidence.
- No cleanup while a target worktree is in use, locked, under rebase/merge/cherry-pick/bisect, or has status probes that timed out. Probe before and after each operation; fail closed on ambiguous results.
- Conversion from independent clone to linked worktree requires explicit restoration or intentional-detachment disposition for branch ownership; verify the result against the original HEAD, refs and worktree status. A shallow clone with missing ancestry must be retained until the boundary is reconciled without rewriting another checkout's history.
- Keep exceptions explicit for large, independent trust boundaries, destructive testing, separate identities/forks, or tool incompatibility; document extra disk cost and cleanup date.
- No automated cleanup of the Nix store, language caches, container images, or volumes merely because Git worktrees were retired. Such eviction needs separate ownership, resource checks, and authorization.

## Example

```sh
repo="$HOME/Projects/dubnium"
git -C "$repo" worktree list --porcelain
git -C "$repo" worktree add -b "fix/1234" "$repo/.worktrees/issue-1234" origin/main
# ... task-scoped validation and integration ...
git -C "$repo" worktree remove "$repo/.worktrees/issue-1234" # clean + closed only
git -C "$repo" merge-base --is-ancestor "fix/1234" "origin/main" && git -C "$repo" branch -d "fix/1234" # only for ancestry-integrated branches
```

Use the [local-workspace hygiene prompt](../prompts/planning/local-workspace-hygiene.md) for an evidence-first cleanup or agent bootstrap.
