# RFC: <proposal title>

## Metadata

- **Status:** Draft | In review | Accepted | Rejected | Withdrawn | Superseded
- **Authors:**
- **Decision owners:**
- **Created:** YYYY-MM-DD
- **Target decision date:**
- **Related QART analyses:**
- **Resulting ADRs:**
- **Related epics or issues:**

## Summary

Describe the proposal, the problem it addresses, and the recommended direction. This section should stand on its own.

## Motivation

Explain the current limitation or opportunity, affected users and operators, security or governance concern, strategic value, and why broader review is warranted now.

## Goals

- Required outcome
- Required system property

## Non-goals

- Adjacent work intentionally excluded
- Implementation detail intentionally left open

## Background and current state

Describe the existing architecture, workflows, components, contracts, data and control flow, trust boundaries, limitations, evidence, and relevant prior decisions.

## Proposal

Describe applicable:

- major components and responsibilities;
- interfaces, schemas, protocols, commands, configuration, and versioning;
- state ownership, consistency, idempotency, and concurrency;
- data and control flow;
- integration and deployment model;
- failure handling and recovery;
- security, privacy, authorization, and governance boundaries;
- evidence, observability, support, and ownership.

## Architecture

Include diagrams only when they clarify responsibilities, boundaries, or flow. Explain material trust and failure boundaries in prose.

## Decision summary

| Question | Alternatives | Recommendation | Key trade-off | QART / ADR |
| --- | --- | --- | --- | --- |
| Bounded decision question | Credible options | Recommendation or pending | Accepted cost | Link or pending |

Keep substantial alternatives analysis in separate QART documents.

## Detailed design

### Components and responsibilities

| Component | Responsibility | Owner |
| --- | --- | --- |
| Component | Durable responsibility | Owner |

### Interfaces and contracts

Document normative APIs, events, commands, configuration, file formats, schemas, error semantics, exit codes, compatibility, and versioning guarantees.

### State and consistency

Describe persistent and transient state, ownership, concurrency, consistency, retry, idempotency, and recovery behavior.

### Failure model

Describe invalid input, dependency failure, timeout, partial completion, retries, degraded operation, recovery, and fail-open versus fail-closed behavior.

## Security, privacy, and governance

- Assets and sensitive data:
- Threat and misuse scenarios:
- Trust and authorization boundaries:
- Required controls and approvals:
- Secret management and least privilege:
- Evidence, provenance, audit, and retention:
- Privacy, residency, deletion, and telemetry constraints:
- Residual risk and acceptance owner:

## Operational design

Describe deployment, configuration, feature flags, health, metrics, logs, traces, alerts, capacity, cost, backup, recovery, incident response, troubleshooting, and ownership.

## Compatibility, migration, and rollout

Describe existing consumers, backward and forward compatibility, mixed-version behavior, data and configuration migration, staged rollout, rollback, deprecation, and removal.

## Alternatives considered

### Alternative: Name

- **Benefits:**
- **Costs and risks:**
- **Reason not selected:**
- **Reconsider when:**

## Delivery plan

### Phase 1: Foundation or contract

- **Outcome:**
- **Scope:**
- **Validation:**
- **Rollback:**

### Phase 2: Integration or adoption

Repeat only for meaningful phases. Link bounded delivery issues rather than turning the RFC into an implementation backlog.

## Validation and success measures

- Required prototype, benchmark, or evidence:
- Contract and integration validation:
- Failure, security, migration, and compatibility validation:
- Operational exercise or demonstration:
- Observable success measure or threshold:

## Risks

| Risk | Impact | Mitigation or contingency | Owner |
| --- | --- | --- | --- |
| Material risk | Low / Medium / High | Mitigation | Owner |

## Unresolved questions

Include only questions that materially affect approval. For each, state alternatives, current recommendation, evidence needed, decision owner, and deadline.

## Decision and disposition

Complete after review.

- **Disposition:** Accepted / Rejected / Withdrawn / Superseded
- **Decision date:**
- **Conditions of acceptance:**
- **Required ADRs:**
- **Required specifications:**
- **Next executable slice:**
