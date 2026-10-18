# Local workspace setup and cleanup

Use this prompt when starting an engineering task on a local host or reconciling stale checkouts.

**Apply:** [Local Git workspace and concurrency standard](../../standards/local-git-workspaces.md), the branching/integration standard, and repository-local authority and security policy.

## Instruction to execution agent

> Discover the exact repository identity and canonical primary checkout before acting. Default to one canonical Git object store per repository, with task-owned linked worktrees under `<primary>/.worktrees/<task-id>`. Preserve concurrent work: one writer per branch/worktree, separate review and integration worktrees, and task-scoped mutable build/test state. Share only verified concurrency-safe, content-addressed caches. Prefer repo flake environments, not duplicate clones or per-task base images.
>
> **Start:** inventory `git worktree list --porcelain`, local refs, branch/upstream/merge evidence, uncommitted/untracked/ignored changes, locks, active processes, and available disk. Reuse an existing worktree only when its ownership and exact task match; otherwise create a dedicated linked worktree with a unique branch. Never mutate a checkout being edited by another actor.
>
> **Finish:** classify candidates as active / safe-to-retire / protected / indeterminate. A clean checkout is not necessarily disposable. Verify unique commits, refs, tags, stash/reflog state and non-Git artifacts before removing an independent clone; preserve unique history in a namespaced ref or verified bundle. Do not equate squash-merged PRs with Git ancestor reachability. Use Git-native worktree operations; use only non-forced branch pruning when permitted. Never delete remote branches, caches, or files through broad recursive cleanup without separate authority.
>
> **Report:** canonical layout and exceptions; count of active, protected, retired and unresolved worktrees; unique history preserved; actual allocated disk space reclaimed; tool/evidence failures; and the smallest next safe action. Fail closed on uncertainty and prioritize avoiding concurrent-agent interference over marginal disk savings.

## Required output

1. **Baseline:** canonical checkout map, candidate inventory, active owner and working-tree evidence.
2. **Proposed mutations:** exact source/destination, affected branch/objects, deletion versus reversible relocation, authority and risk.
3. **Execution verification:** Git metadata, HEAD and dirty-state parity, candidate integrity, and space delta.
4. **Residual:** protected work, uncertain refs, ongoing agents, unproven cleanup, and follow-up checks.

Do not create a new policy engine, cleanup daemon, or second repository registry to implement this prompt. Reuse Git, the existing repository inventory and current execution/evidence contracts.
