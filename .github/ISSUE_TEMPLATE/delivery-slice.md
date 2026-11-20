---
name: Engineering delivery slice
about: Deliver a bounded integration, migration, infrastructure, or implementation outcome
title: "[delivery]: "
labels: ""
assignees: ""
---

## Explain it to a human

In 1–3 plain-language sentences: what's wrong, why it matters, and what will be better?

## What needs to change

State one observable vertical outcome and only essential scope, constraints, or non-goals. When material, summarize the **behavioral contract**, **affected architectural interfaces/trust boundaries**, and **verification strategy** (lowest faithful test-pyramid layers and real-boundary evidence). Link existing designs rather than copying them.

## Done when

- [ ] [Observable result, including relevant failure or security behavior]
- [ ] [Required compatibility, migration, or recovery property if applicable]
- [ ] [Applicable unit/contract/integration/system or release evidence proves the outcome; omit irrelevant layers]

## Tracking

- **Priority:** P0 / P1 / P2 / P3 — one-sentence repository-global rationale.
- **Status:** Ready / Blocked / In progress / Review.
- **Blocked by:** [Link + unblock condition, if relevant]
- **Not included:** [Material non-goal, if relevant]
- **Evidence:** [PR / CI / issue / decision / spec links]

Keep only applicable fields. Follow [the shared issue standard](../../CONTRIBUTING.md#issue-simplicity-and-update-discipline); update current state here, not through routine progress comments.
