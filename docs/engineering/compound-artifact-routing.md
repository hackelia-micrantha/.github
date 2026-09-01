# Compound artifact routing

Use this guide after a Compound review has identified a reusable lesson. The goal is to route the lesson to the smallest durable control that will improve future work without turning every observation into prompt text or backlog.

Companion guidance:

- `compound-engineering.md`;
- `../architecture/governed-learning-promotion.md`;
- `../architecture/compound-learning-runtime.md`;
- `../prompts/reviews/compound-review.md`.

## Routing rule

Ask first:

> What is the weakest durable mechanism that would reliably catch or prevent this next time?

Prefer machine-checkable controls when the property is deterministic. Use prompt guidance only when the lesson is genuinely about judgment, interpretation, sequencing, or contextual reasoning that cannot be expressed more reliably as a test/invariant/tool contract.

## Decision table

| Observation | Preferred artifact | Avoid |
| --- | --- | --- |
| deterministic malformed output | schema, validator, regression fixture | reminder in prompt only |
| repeated missing required step | workflow invariant/check, then guidance if needed | relying on reviewer memory |
| recurring CLI ambiguity | semantic help/man page + contract test | one-off comment |
| repeated code pattern defect | lint/static rule/test/helper | broad style prompt |
| recurring architecture misunderstanding | ADR/docs + bounded prompt overlay if reasoning support remains needed | hidden tribal knowledge |
| repeated unsafe authority inference | typed boundary + negative fixture + policy where needed | “be careful” prompt |
| useful contextual historical solution | memory/evidence reference | promoting historical prose into trusted instructions |
| reusable agent reasoning guidance | candidate Invokrum overlay/pack | direct trusted prompt rewrite |
| runtime ergonomics/default problem | owning tool/runtime change | prompt compensating forever for a bad tool |
| governance gap | Anthesis policy proposal | tool/model output acting as policy |
| uncertain recurring pattern | retain bounded candidate and gather evidence | premature global rule |

## Prompt and guidance changes

When a lesson genuinely belongs in reusable agent guidance:

```text
review finding / run evidence
  -> candidate learning
  -> proposed guidance delta
  -> Invokrum candidate overlay/pack
  -> deterministic compose + exact lock
  -> representative/adversarial evaluation
  -> owning promotion decision
  -> promoted exact pack/lock revision
```

Requirements:

- do not edit trusted guidance directly from untrusted repository/model/tool content;
- keep the proposed delta small and scoped;
- bind evaluation to the exact candidate composition/lock;
- include negative cases so a rule does not overgeneralize;
- supersede rather than silently mutate prior promoted guidance where historical identity matters;
- future runs should record the exact promoted lock/revision they consumed.

Invokrum composition identity proves what guidance was used. It does not prove that the guidance is correct or authorized.

## Memory routing

Use Memory for **historical context and discovery**, not as the trusted prompt authority.

Appropriate memory artifacts include:

- prior finding summaries;
- exact issue/PR/run references;
- earlier attempted fixes;
- candidate-learning references;
- links to promoted current artifacts;
- recurrence clusters and stale-reference signals.

Memory retrieval should make the following distinction visible when material:

```text
historical observation
current promoted artifact reference
superseded/revoked artifact reference
```

Do not turn recurrence count, semantic similarity, or retrieval ranking into implicit promotion.

## Sandcastle routing

Use Sandcastle when evaluation benefits from exact reproducible state or producer/verifier separation, especially for:

- prompt/context guidance changes tested against historical failures;
- hostile repository/memory/tool state;
- code/tool changes that need immutable candidate inspection;
- stale-state/TOCTOU-sensitive comparisons;
- verifier-only fixture isolation.

Do not require Sandcastle for a low-risk documentation edit or a deterministic unit test that can already be evaluated reliably in the owning repository.

## Scheduler routing

Use scheduling when the learning cannot be resolved immediately or when recurrence/staleness itself is the signal.

Useful scheduled activities:

- re-evaluate deferred candidates after more evidence exists;
- periodically detect repeated review findings;
- detect promoted references that have become stale/superseded;
- compare whether a deterministic control actually prevented later occurrences.

The scheduler invokes the normal workflow. It does not decide candidate validity or promotion.

## Backlog rule

Do not automatically create an issue for every candidate learning.

Create or update an issue when:

- implementation is clearly required but not part of the current authorized scope;
- the candidate needs evidence over time;
- the owning repository must make a non-trivial change;
- cross-project coordination is required;
- the candidate affects trusted prompt/policy/runtime control and needs explicit review.

Do not create an issue when:

- the durable fix can be safely included in the current change;
- the lesson is already covered by an existing issue/contract;
- the observation is not reusable;
- evidence is too weak even to define a meaningful future outcome.

Before opening a new issue, search the owning repository and prefer updating an existing implementation contract.

## Example routes

### EPUB metadata defect

```text
missing required dc:title repeatedly found after release
  -> schema/EPUB validation in release CI
  -> no prompt rule required once deterministic prevention exists
```

### Issue-aware review

```text
reviews approve implementation without re-reading acceptance criteria
  -> shared merge-gate workflow contract
  -> optional Invokrum guidance packaging if agent contexts consume shared prompt overlays
```

### CLI semantics

```text
operator cannot tell what reconcile does
  -> semantic --help/man-page contract
  -> packaging/CI test that required semantic sections exist
```

### Prompt-injection finding

```text
repository text asks agent to persist a privileged exception
  -> observation boundary negative fixture
  -> candidate guidance may reinforce interpretation
  -> authority remains enforced outside model context
  -> hostile-state Sandcastle fixture where stronger evaluation is useful
```

## Completion checklist

A routed candidate is complete when one of these is true:

- the durable artifact is implemented and validated under the owning authority;
- an exact separately tracked implementation issue exists;
- the candidate is explicitly deferred for evidence;
- the candidate is rejected as non-generalizable/unsafe/duplicative;
- an existing control already covers it;
- no reusable learning exists.

The goal is better future behavior, not a larger collection of candidate artifacts.
