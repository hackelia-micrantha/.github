# Agent skill selection

Micrantha agents should select reusable skills from operator intent and current authoritative state rather than require operators to remember skill names.

## Decision

When an available shared or project-local skill clearly matches the requested work, select it automatically unless repository-local policy requires an explicit selection step.

Skill selection chooses an execution contract. It does **not** grant additional mutation or effect authority.

## Long-running execution selector

Automatically select [`long-running-execution`](../../skills/long-running-execution/SKILL.md) for a non-trivial engineering run when operator intent includes or clearly means:

- `proceed in loops`;
- `continue until blocked`;
- `run this to completion`;
- `review -> fix -> validate -> re-review`;
- `fix loop to proceed`;
- `proceed` or `continue` when a non-trivial run is already active and the next safe transition can be derived from authoritative state.

Do not select it for a trivial one-step task solely because the operator used `proceed` or `continue`.

After selection, the agent should continue through reversible, low-risk, already-authorized transitions without repeatedly asking for continuation. The agent still stops or escalates for the conditions defined by the skill and the [agent execution contract](./agent-execution-contract.md).

## Consequential effects remain separately gated

Intent-based selection must not infer authority for:

- merge;
- release or tag creation;
- publication or deployment;
- destructive deletion;
- permission, credential, or secret mutation;
- external communication;
- consequential acceptance closure;
- any other effect separately governed by project or organization policy.

A phrase such as `proceed in loops` means "continue the governed run", not "grant every future effect required to finish it".

## Composition

When more than one skill applies, compose the specialized skill with the execution skill. Examples:

```text
proceed in loops on this PR
  -> long-running-execution
  -> pr-review
  -> merge-readiness when the graph reaches the merge gate

apply the Micrantha release strategy and proceed
  -> long-running-execution
  -> release-integration

fix this failing security change until blocked
  -> long-running-execution
  -> security-review
  -> applicable project-local validation skills
```

Composition preserves the strictest authority, evidence, security, retry, and completion rules among all selected skills.

## Repository adoption

The organization `.github` repository is the normative source for shared Micrantha skill-selection guidance, but GitHub does not automatically propagate arbitrary `AGENTS.md` files into every repository.

Therefore:

1. organization guidance defines the canonical selector;
2. repositories that use agent instruction files should adopt or reference the selector in their root `AGENTS.md` or equivalent agent configuration;
3. repository-local guidance may add triggers, specialize workflows, or tighten gates;
4. local guidance must not silently weaken applicable organization security, release, compatibility, or effect-authority requirements;
5. adoption should eventually be checked mechanically so drift is visible rather than dependent on operator memory.

The shared [`AGENTS.md`](../../AGENTS.md) is the executable reference for this repository and a template for project-local adoption.

## Related contracts

- [Long-running agent execution](./agent-execution-contract.md)
- [AI-assisted SDLC phase discipline](./ai-assisted-sdlc.md)
- [`long-running-execution` skill](../../skills/long-running-execution/SKILL.md)
- [Shared skills](../../skills/README.md)
