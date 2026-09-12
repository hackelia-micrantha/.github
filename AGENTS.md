# Micrantha shared agent guidance

This file defines the default agent-selection behavior for work performed in this repository. Other Micrantha repositories do not automatically inherit this file; they should adopt or reference these organization defaults explicitly and may tighten them with repository-local policy.

## Intent-based skill selection

Select the most specific applicable skill from [`skills/`](skills/) from operator intent and current authoritative repository state. Do not require the operator to name a skill when the intent clearly matches one.

For a non-trivial engineering task, automatically load and apply [`skills/long-running-execution/SKILL.md`](skills/long-running-execution/SKILL.md) when the operator says or clearly means any of the following:

- `proceed in loops`;
- `continue until blocked`;
- `run this to completion`;
- `review -> fix -> validate -> re-review`;
- `fix loop to proceed`;
- `proceed` or `continue` when an existing non-trivial run is already active and repeated continuation prompts would otherwise be required.

Do not activate `long-running-execution` for a trivial one-step task merely because the word `proceed` appears.

Once selected, continue through safe, reversible, already-authorized transitions without asking for generic continuation confirmation. Preserve the skill's retry budgets, exact-candidate evidence requirements, re-review discipline, and stop/escalation conditions.

## Authority is not selected from intent

Skill selection does not grant new authority. In particular, `proceed`, `continue`, or selection of `long-running-execution` does not by itself authorize merge, release, tag, publication, deployment, destructive deletion, permission or credential changes, external communication, or other consequential effects.

Apply the authority and evidence boundaries in:

- [`docs/engineering/agent-execution-contract.md`](docs/engineering/agent-execution-contract.md);
- [`docs/engineering/ai-assisted-sdlc.md`](docs/engineering/ai-assisted-sdlc.md);
- the selected skill;
- repository-local policy and accepted decisions.

When multiple skills apply, compose them and preserve the strictest authority, security, evidence, retry, and completion requirements.
