---
name: implementation-plan
description: Convert accepted intent, a groomed issue, RFC, ADR, or epic into ordered, independently verifiable implementation slices.
---

# Implementation plan

## Trigger

Use for `make a plan`, `proceed`, `break this down`, or when accepted work is too broad to implement safely in one change.

## Inputs

- authoritative issue/spec/RFC/ADR or equivalent accepted intent;
- current implementation and dependency graph;
- release, compatibility, security, and migration constraints.

## Workflow

1. Reconfirm the accepted outcome and separate unresolved decisions from implementation work.
2. Identify contracts/boundaries that must remain stable while work is in progress.
3. Slice vertically where possible so each step produces independently reviewable evidence.
4. Order slices by dependency and risk: establish contracts/invariants first, then implementation, integration, migration, and cleanup.
5. Include tests, static analysis, documentation, packaging, migration, rollback, and operational changes in the slice that creates the obligation rather than deferring them to a generic cleanup phase.
6. Identify parallel-safe work and work that must remain serialized.
7. Define per-slice acceptance evidence and the condition for moving to the next slice.
8. Route newly discovered architectural alternatives back to `qart-analysis` rather than burying a decision in implementation detail.

## Evidence

The plan should map each slice to an accepted requirement, decision, risk, or dependency and name the validation that proves it complete.

## Completion

Complete when the first slice can start immediately, later slices have explicit dependency edges, and the overall plan reaches the accepted outcome without relying on an undefined final integration step.

## References

- `docs/prompts/planning/classify-and-route.md`
- `docs/prompts/planning/next-executable-slice.md`
- `docs/prompts/pull-requests/large-change-decomposition.md`
- `docs/engineering/work-items.md`
