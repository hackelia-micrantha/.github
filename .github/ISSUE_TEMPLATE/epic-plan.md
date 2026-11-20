---
name: Epic or plan
about: Coordinate a larger outcome and its next executable delivery slice
title: "[epic]: "
labels: ""
assignees: ""
---

## Explain it to a human

In 1–3 plain-language sentences, explain the larger problem, why it matters, and what success looks like.

## What needs to change

Describe the larger observable result, essential architectural and safety boundaries, and non-goals. Link authoritative design/decisions rather than repeating them. An epic coordinates **vertical outcomes**, not tickets for each technical layer; it is not itself executable.

## Done when

- [ ] [Measurable system or user outcome is achieved]
- [ ] [Applicable safety, integration, migration, or adoption evidence is verified]

## Tracking

- **Priority:** P0 / P1 / P2 / P3 — one-sentence repository-global rationale.
- **Status:** Draft / Ready / In progress / Blocked / Complete.
- **Blocked by:** [Decision or dependent issue + unblock condition, if relevant]
- **Child outcomes:** [Links to existing issues, grouped only if useful]
- **Next executable slice:** [One ready issue / concrete bounded outcome]
- **Evidence and decisions:** [PR / CI / QART / RFC / ADR / spec links]
- **Not included:** [Material scope boundary, if relevant]

Update this issue only when coordination state materially changes. Do not duplicate child-issue progress reports, technical specs, or PR logs.
