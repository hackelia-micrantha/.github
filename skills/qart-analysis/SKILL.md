---
name: qart-analysis
description: Resolve one bounded decision through Questions, Alternatives, Recommendation, and Trade-offs before promoting the decision to an ADR or broader RFC.
---

# QART analysis

## Trigger

Use when a consequential choice has real alternatives, unresolved assumptions, or trade-offs that should be explicit before implementation.

## Inputs

- one bounded decision question;
- constraints, non-goals, current architecture, and affected contracts;
- available implementation/research evidence and decision owner where known.

## Workflow

1. Frame one decision narrowly enough that a recommendation can actually be made.
2. Enumerate material questions and unknowns; resolve cheap factual questions before comparing alternatives.
3. Identify viable alternatives including status quo when it is genuinely viable.
4. Compare alternatives against explicit criteria: correctness, security, maintainability, operability, compatibility, cost, reversibility, complexity, and project-specific concerns.
5. Recommend an option only when evidence supports it; otherwise state what evidence is required next.
6. Record trade-offs, rejected alternatives, migration/rollback implications, and residual uncertainty.
7. Promote to an ADR when the decision is accepted; use an RFC first when broad review or cross-boundary coordination remains necessary.

## Evidence

Distinguish measured/verified constraints from assumptions and preferences. Link material evidence rather than restating it as fact without provenance.

## Completion

Complete when the bounded question has either an evidence-backed recommendation ready for disposition or a precisely defined investigation that blocks the decision.

## References

- `docs/prompts/decisions/qart-analysis.md`
- `docs/prompts/decisions/qart-to-adr.md`
- `docs/prompts/decisions/rfc-development.md`
- `docs/engineering/templates/qart.md`
