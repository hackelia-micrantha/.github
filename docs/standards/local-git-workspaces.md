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

## Build, test, and cleanup lifecycle

**Every local build or test sequence must have a defined follow-up cleanup action**, regardless of which command runner, language, build system, or CI orchestrator was used. The contract is **build → test → cleanup** when both build and test are needed, or **build → cleanup / test → cleanup** for a single stage. The *lifecycle* is the standard, **not a particular tool or task name**. An action that generates no task-local files may have an explicitly documented no-op cleanup.

- **Tool-neutral implementation:** use the repository's native entry points—Mise, Make, Just, npm scripts, Cargo, Nix, a shell script, CI job finalizer, or equivalent. For example, `mise run build; mise run test; mise run clean` expresses the sequence in a Mise-based repository; `make build; make test; make clean` expresses it for Make. These are examples, **not mandatory interfaces**; adopt existing repository-specific clean tasks before adding new commands.
- **Follow-through on failure:** attempt cleanup in a `finally` / `EXIT` / CI `always()` step **even when build or tests fail**. Capture incomplete cleanup as a follow-up if interrupted, killed, or blocked by an active user of the output. Do not imply SIGKILL cleanup can be guaranteed.
- **Ownership and scope:** cleanup must be safe to repeat, target only generated outputs and resources owned by the invoking task/worktree, and not mutate another agent's work. Never substitute `git clean -fdx`, broad recursive deletion, global Nix garbage collection, or eviction of shared compiler/package caches.
- **Evidence before cleanup:** export original command exit status, exact revision, test reports, logs, coverage, and reproduction data outside cleanup targets first. Keep published/release artifacts and required review evidence until their consumers finish; if cleanup is deliberately deferred, record the owner, retained outputs, and next eligible cleanup point.
- **Independent outcomes:** preserve the original build/test failure code and record cleanup success or failure independently. A successful cleanup must never turn a failed test green. If cleanup fails after otherwise successful work, the overall operation fails; if both fail, the original build/test status remains visible alongside the cleanup failure.
- **Document repository behavior:** the project-native build/test/cleanup commands and precisely owned output locations must be discoverable in the repository. A missing clean path is an **adoption gap**, not permission to invent an unsafe replacement. Where `nix build --no-link` produces only immutable store results, cleanup can explicitly be a no-op for those outputs; it must not evict shared Nix store objects.
- **Parallel work:** prefer per-task output locations and scoped resource ownership. Cleanup runs in the producing task's context only once no other running task depends on those outputs.

A failure-safe shell pattern with **illustrative Mise adapters** (substitute the repository's own commands or an equivalent CI finalizer):

```bash
build_step()   { mise run build; }  # example, not required
test_step()    { mise run test; }
cleanup_step() { mise run clean; }

set -euo pipefail
finish() {
  result=$?
  trap - EXIT
  cleanup_result=0
  cleanup_step || cleanup_result=$?
  if [ "$cleanup_result" -ne 0 ]; then
    echo "cleanup failed: $cleanup_result (build/test exit: $result)" >&2
    if [ "$result" -eq 0 ]; then exit "$cleanup_result"; fi
  fi
  exit "$result"
}
trap finish EXIT
build_step
test_step
```

This performs cleanup after the *sequence*, not between a build and a test that requires its output. A test-only or build-only operation uses the same finalizer with just that stage. Cleanup of generated resources is distinct from retiring a Git worktree, which requires the separate lifecycle checks below.

## Audit and incremental adoption

Use `python3 tools/check_cleanup_finalizers.py --json /path/to/repository` to **flag possible** missing or premature CI cleanup finalizers without installing Mise. The scanner uses only Python’s standard library and recognizes Make, Cargo, Go, Gradle, npm, Yarn, Mise, and Nix-style commands. It is an **advisory static heuristic**, not a YAML interpreter or a substitute for artifact, ownership, and failure-path review. Use `--strict` only on a deliberately qualified repository; CI jobs that use `nix build --no-link` and create no local output may document an explicit `# cleanup: no-local-outputs` exception. Each finding must be confirmed before changing a workflow or deleting files.

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
