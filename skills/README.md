# Micrantha engineering skills

Micrantha skills are reusable, bounded orchestration contracts for recurring engineering work. A skill defines **when to run**, **what evidence to inspect**, **which existing prompts and standards govern the work**, **what mutations are permitted**, and **what completion means**.

Skills do not replace prompts, standards, templates, or project-local authority. They compose those sources into an executable workflow.

## Ownership and adoption

**Operational skills are project-local by default.** A project repository owns the skills that encode its actual workflows, tools, architecture, maturity, release path, security boundaries, and completion rules.

The skills in this repository are **organization-wide defaults and reusable reference contracts**. They provide common vocabulary and a starting point for repeated engineering workflows, but they are not implicitly installed, enabled, or mandatory in every Micrantha project.

A project may:

- adopt a shared skill unchanged when it accurately represents the project;
- specialize a shared skill with project-local inputs, tooling, evidence, or tighter invariants;
- compose several shared skills into a project-specific workflow;
- define a project-only skill when the workflow is not meaningfully reusable elsewhere;
- omit a shared skill that does not apply to the project's maturity, architecture, or operating model.

Project-local skills must not silently weaken organization security, governance, release, or compatibility standards that apply to the project. Conversely, organization defaults must not override repository-local implementation truth or invent project requirements.

When a local skill derives materially from a shared default, prefer recording the source skill and revision/version so drift can be reviewed deliberately rather than inherited accidentally.

The Micrantha meta repository may catalogue shared and project-local skills and compose ecosystem workflows. That catalog is coordination metadata, not the source of truth for a project's operational behavior.

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

## Model selection

A skill should describe the **reasoning capability and evidence required**, not assume that a frontier model is always necessary.

Use the least expensive/smallest model path that can reliably perform the bounded task under the project's verification and authority controls. In particular, experimental, exploratory, low-consequence, or easily reversible work may intentionally use local or smaller models when their limitations are acceptable and deterministic validation provides the required evidence.

Escalate to a stronger or frontier model when the task materially benefits from it, for example because of:

- broad or difficult repository/system synthesis;
- consequential architectural or security reasoning;
- material ambiguity that a weaker model repeatedly fails to resolve;
- repeated implementation/review failure without progress;
- semantic verification that cannot be decided adequately by deterministic checks;
- project policy that explicitly requires a stronger model class for the affected boundary.

Model class is not a security boundary, source of authority, or proof of correctness. A frontier model does not replace deterministic verification, independent evidence, human disposition where required, or least-privilege execution. A smaller/local model does not justify weakening those controls either.

Project-local skills may declare a justified model capability/profile or escalation rule when useful, but should avoid hard-coding a vendor/model name unless interoperability with that exact model is itself under test.

## Initial shared defaults

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

The shared execution, ambiguity, validation, and priority contracts in [`docs/prompts/README.md`](../docs/prompts/README.md) apply to every shared skill unless a skill explicitly tightens them. A project-local skill should reference the organization standards that remain applicable and document intentional project-specific differences.

Prefer durable mechanical controls over adding more prompt prose. When a recurring lesson can be enforced by a test, schema, type, CI gate, packaging check, capability boundary, or safer tool behavior, create or recommend that mechanism rather than relying on operator memory.
