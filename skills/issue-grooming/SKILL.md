---
name: issue-grooming
description: Turn a finding, request, or rough issue into a bounded engineering work item with observable outcome, scope, acceptance criteria, dependencies, and validation.
---

# Issue grooming

## Trigger

Use for `groom this issue`, `make an issue`, `update issues`, or whenever an executable backlog item lacks a falsifiable outcome or clear verification.

## Inputs

- problem/finding and affected repository boundary;
- authoritative requirements or design evidence;
- known dependencies/blockers and current implementation evidence.

## Workflow

1. Verify that an issue is the right artifact; route unresolved alternatives to QART, broad proposals to RFC, unknown feasibility to a spike, and accepted decisions to ADR where appropriate.
2. Begin the issue body with the exact heading **Explain it to a human** and one to three accurate plain-language sentences; state the user/operator/system outcome rather than implementation activity alone.
3. Bound in-scope and out-of-scope work. Use INVEST as a heuristic for executable vertical slices, not a required field checklist or a reason to split issues by technical layer.
4. Add acceptance criteria that can be objectively verified.
5. Identify dependencies, blockers, compatibility/security implications, and required docs. Name affected interface, application, domain/policy, adapter, and cross-cutting boundaries only when material.
6. Reference `docs/standards/testing.md`; choose the lowest faithful test-pyramid layers, real integration/operational boundaries, and exact evidence expected. Separate issue-specific acceptance from shared Definition of Done checks.
7. Assign priority from current impact and dependency value rather than age.
8. Use the compact **What needs to change / Done when / Tracking** format in `CONTRIBUTING.md`; link authoritative details instead of duplicating technical design, logs, decisions, and CI histories. Prefer in-place status edits over routine progress comments, without losing human discussion or historical evidence.
9. Avoid combining unrelated outcomes merely to reduce issue count; avoid one issue per observation when one coherent outcome covers them.

## Evidence

The issue should link or name the evidence that motivated it and identify assumptions that remain unverified.

## Completion

Complete when an implementer can start the issue without rediscovering intent, scope, authority, dependencies, or the definition of done.

## References

- `docs/prompts/issues/issue-grooming.md`
- `docs/prompts/planning/classify-and-route.md`
- `docs/engineering/work-items.md`
- `.github/ISSUE_TEMPLATE/delivery-slice.md`
