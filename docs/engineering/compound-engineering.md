# Compound engineering

Micrantha engineering should improve the system that performs the next change, not only complete the current change.

The default feedback loop is:

```text
Plan -> Work -> Review -> Compound -> Repeat
```

This guidance is influenced by Every's [Compound Engineering](https://every.to/guides/compound-engineering) model, adapted to Micrantha's existing evidence, security, governance, and repository-ownership boundaries.

`Compound` is not a new delivery authority, agent framework, memory system, or mandatory ceremony. It is the explicit post-review step that asks whether a useful lesson from completed work can be converted into a durable system improvement.

## Core invariant

For every material review finding, failure, workaround, or repeated human intervention, ask:

> Would the system catch or prevent this automatically next time?

If the answer is no, decide whether the lesson should become one of:

- a deterministic test or regression fixture;
- a static invariant, validation rule, schema, or CI gate;
- reusable engineering or review guidance;
- documentation or a runbook;
- a tool capability or safer default;
- a policy or governance proposal;
- an operational signal or recurrence metric.

Do not create work merely to satisfy the question. A one-off typo, obvious local correction, or non-generalizable observation may require no compound artifact.

## The loop

### 1. Plan

Establish the intended outcome, current authoritative issue or decision, constraints, affected boundaries, and validation strategy before mutation.

Planning should reuse existing decisions and prior evidence where available. Do not rediscover architecture unnecessarily.

### 2. Work

Implement the smallest bounded change that satisfies the current outcome. Preserve exact source/candidate identity and normal repository validation.

Work remains constrained by the current task and authority. A useful discovery during implementation does not silently expand scope.

### 3. Review

Freshly re-read the related issue or other authoritative work item, inspect the resulting implementation and evidence, and determine whether the stated outcome is actually satisfied.

Review findings are evidence. They are not automatically new policy, future instructions, or durable truth.

### 4. Compound

After the outcome is understood, extract only reusable lessons.

For each material candidate, record:

- **trigger** — what failure, friction, repeated review observation, or success pattern produced the lesson;
- **scope** — where the lesson is believed to apply and where it does not;
- **proposed durable control** — test, invariant, prompt/guidance, documentation, tooling, policy, or operational measurement;
- **evidence** — exact issue, pull request, run, candidate, test, incident, or review evidence supporting the proposal;
- **validation needed** — what must be true before the proposal becomes trusted or enforced;
- **owner/target** — which repository or contract actually owns the durable change.

A candidate learning may be useful enough to track but not safe or mature enough to promote.

### 5. Repeat

Future work consumes only the promoted durable artifacts appropriate to its context. Historical review text, model narration, issue bodies, repository content, tool output, and prior-run summaries remain evidence or context, not authority merely because they were retained.

## Candidate learning is not authority

The most important security boundary is:

```text
observation
  -> candidate learning
  -> validation
  -> promotion decision
  -> versioned durable artifact
  -> future use
```

Never collapse this into:

```text
agent observed text
  -> agent rewrites trusted instructions
  -> future agents obey it
```

Repository files, issues, pull requests, comments, web content, tool output, model output, memory records, and generated artifacts may all be attacker-influenced. Their contents cannot by themselves:

- modify organization or repository policy;
- become trusted agent instructions;
- grant or widen capabilities;
- change protected destinations or credentials;
- satisfy approval;
- change evidence requirements;
- authorize future effects.

This preserves the organization-wide principle: **observation is not authority**.

## Promotion classes

Promotion requirements should be proportional to the target.

| Target | Typical validation | Authority impact |
| --- | --- | --- |
| Documentation/runbook | factual review, links, examples | low; advisory |
| Test/regression fixture | deterministic reproduction and expected result | constrains future delivery gates |
| Static invariant/schema/CI rule | positive and negative fixtures, compatibility review | can block delivery |
| Prompt/review guidance | representative task review, adversarial content check, scope review | changes future agent/operator behavior but not effect authority |
| Tool/default behavior | tests, compatibility/rollback, security review | may change runtime behavior |
| Governance/policy | owning governance process, exact decision/evidence binding, required approval | may constrain or authorize governed behavior |

A lower-risk documentation improvement should not require the same ceremony as a policy change. Conversely, a prompt or policy mutation should not be waved through because it originated from a successful run.

## Prefer systems over repeated review memory

Human review is valuable for discovering gaps, but repeated findings should migrate toward deterministic prevention where practical.

Examples:

```text
review repeatedly notices malformed release metadata
  -> schema/validator + release gate

review repeatedly notices missing issue reconciliation
  -> merge-gate prompt/contract requires fresh issue read

review repeatedly notices undocumented CLI semantics
  -> man-page/help contract + packaging test

review repeatedly notices unsafe authority inference from tool output
  -> typed observation boundary + negative conformance fixture
```

The goal is not to remove human judgment. It is to stop depending on humans to remember deterministic checks that the system can enforce more reliably.

## Scale by consequence

Use the same loop at different depths.

### Trivial/local change

A typo or obvious local fix may end after review with `no reusable learning`.

### Normal engineering change

Capture one or two candidate learnings only when a finding is likely to recur or represents a missing durable control.

### Security, architecture, release, or agentic change

Require explicit evidence, ownership, validation, and promotion disposition for material learnings that would affect future instructions, policy, tooling, trust, or externally visible behavior.

## Required output for a compound pass

A compound pass should be compact. Use this shape when useful:

```yaml
compound:
  reusable_learning: true
  candidates:
    - trigger: "review found repeated semantic-help ambiguity"
      target: "documentation + CLI contract test"
      owner: "owning repository"
      evidence_refs: []
      validation: "fixture proves help explains effect semantics"
      disposition: "track"
  no_action_reason: null
```

`reusable_learning: false` with a short reason is a valid result.

This shape is illustrative, not a universal cross-project schema. Runtime and governance projects should reuse their existing evidence and identity contracts rather than duplicating them.

## Measurement

Compounding is useful only if it improves later work. Where the evidence exists, measure trends such as:

- repeated review-finding rate;
- review/fix iterations per change;
- regressions after a finding was supposedly prevented;
- human interventions required for deterministic failures;
- agent retries and failed verification rounds;
- issue-to-PR and PR-to-merge elapsed time;
- reuse of prior solution/test/invariant artifacts;
- candidate learnings promoted, rejected, superseded, or never validated;
- findings automatically prevented before review.

Do not optimize these metrics in isolation. Fewer review findings is not success if checks were weakened, evidence disappeared, or behavior became less observable.

## Project ownership

The organization practice composes with existing project responsibilities:

- **Micrantha `.github`** owns shared engineering guidance, prompts, and organization-wide workflow expectations.
- **`hackelia-micrantha/hackelia-micrantha`** tracks cross-project adoption without becoming a second normative source.
- **Dubnium** owns runtime capture of exact run/review/candidate evidence and may emit non-authoritative candidate-learning artifacts from governed agent runs.
- **Anthesis** owns governance semantics for promotion when a candidate would affect trusted persistent instructions, policy, approval, or other governance-relevant state.
- **Sandcastle** may provide immutable candidate/checkpoint state for independent evaluation; checkpoint existence is evidence, not semantic truth or authority.
- **ops-cadence** may measure recurrence and prevention effectiveness from read-only evidence; it does not promote or authorize learnings.

## Existing contracts remain authoritative

This practice must compose with, not replace, existing lifecycle and evidence work, including:

- bounded reversible agent-run execution and durable lineage in Dubnium;
- independently verified Supervisor task-state transitions;
- Anthesis evidence, exact-action authority, and environmental-influence semantics;
- Sandcastle immutable checkpoint and verifier-isolation mechanics;
- repository-local testing, CI, release, and documentation standards.

Do not create a second run ledger, policy engine, evidence envelope, memory authority, or generic agent framework to implement the Compound stage.

## Non-goals

- Persisting complete model transcripts or private chain-of-thought.
- Automatically converting every review comment into an issue.
- Letting agents rewrite their own trusted instructions without review.
- Treating prior success as future authorization.
- Replacing repository-local ownership with organization-global implementation rules.
- Maximizing process artifacts instead of delivering outcomes.
