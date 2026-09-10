# Micrantha engineering skills

Micrantha skills are reusable, bounded orchestration contracts for recurring engineering work. A skill defines **when to run**, **what evidence to inspect**, **which existing prompts and standards govern the work**, **what mutations are permitted**, and **what completion means**.

Skills do not replace prompts, standards, templates, or project-local authority. They compose those sources into an executable workflow.

## Contract

Each skill uses `SKILL.md` and should define:

- **Trigger** — recognizable operator intent and situations where the skill applies;
- **Inputs** — minimum context and authority required;
- **Workflow** — ordered evidence-backed actions;
- **Evidence** — what must be inspected or produced;
- **Mutation boundary** — read-only by default unless the invocation authorizes writes;
- **Completion** — a falsifiable stop condition;
- **References** — canonical Micrantha prompts, standards, templates, or project-local sources.

A skill may invoke another skill. Composition must preserve the stricter authority, security, evidence, and completion requirements of every invoked skill.

## Initial skill set

| Skill | Purpose |
| --- | --- |
| [`project-review`](project-review/SKILL.md) | Broad repository/project reconciliation |
| [`project-triage`](project-triage/SKILL.md) | Convert reviewed state into a prioritized executable queue |
| [`issue-grooming`](issue-grooming/SKILL.md) | Produce bounded, verifiable work items |
| [`qart-analysis`](qart-analysis/SKILL.md) | Resolve a bounded decision through Questions, Alternatives, Recommendation, Trade-offs |
| [`implementation-plan`](implementation-plan/SKILL.md) | Turn accepted intent into ordered, independently verifiable slices |
| [`pr-review`](pr-review/SKILL.md) | Review a change set for correctness, risk, scope, and evidence |
| [`merge-readiness`](merge-readiness/SKILL.md) | Decide merge/fix/block/close from exact-head evidence |
| [`test-strategy`](test-strategy/SKILL.md) | Design risk-based layered validation and Testule integration |
| [`security-review`](security-review/SKILL.md) | Review trust boundaries, abuse paths, privileges, and safe failure |
| [`release-integration`](release-integration/SKILL.md) | Apply Micrantha release/distribution/integration strategy across repositories |

## Execution rules

The shared execution, ambiguity, validation, and priority contracts in [`docs/prompts/README.md`](../docs/prompts/README.md) apply to every skill unless a skill explicitly tightens them.

Prefer durable mechanical controls over adding more prompt prose. When a recurring lesson can be enforced by a test, schema, type, CI gate, packaging check, capability boundary, or safer tool behavior, create or recommend that mechanism rather than relying on operator memory.
