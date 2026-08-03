# ADR-<number>: <decision title>

## Status

Proposed | Accepted | Deprecated | Superseded | Rejected

## Metadata

- **Date:** YYYY-MM-DD
- **Decision owners:**
- **Scope:** Repository / subsystem / contract / deployment / organization
- **Related RFC:**
- **Related QART analysis:**
- **Related issues or pull requests:**
- **Supersedes:**
- **Superseded by:**

## Context

Describe only the architectural context and forces needed to understand why a durable decision was required:

- current system and problem;
- decision drivers and constraints;
- relevant trust, compatibility, operational, or ownership boundaries;
- evidence and accepted assumptions.

## Decision

> We will <decision>.

State the selected approach directly and in present tense. Define where it applies, which boundaries or contracts it creates or preserves, and any explicit exclusions.

## Alternatives considered

### Alternative: Name

- **Benefits:**
- **Costs and limitations:**
- **Reason not selected:**

Link to the source QART or RFC for substantial analysis rather than duplicating it.

## Rationale

Explain why the decision best satisfies the drivers and why its accepted trade-offs are appropriate.

## Consequences

### Positive

- Benefit or capability enabled

### Negative and accepted costs

- Complexity, limitation, migration cost, or lost benefit accepted

### Security, privacy, and governance

- Trust-boundary or authorization implications:
- Sensitive-data or secret implications:
- Evidence, audit, approval, or retention obligations:
- Residual risk and acceptance owner:

### Operations and ownership

- Deployment, configuration, monitoring, recovery, support, or ownership obligation:

### Compatibility, migration, and rollback

- Existing consumers and mixed-version behavior:
- Migration and deprecation:
- Rollback or irreversibility:

## Implementation constraints

Record architectural constraints imposed by the decision, not a full implementation plan.

- Required boundary, contract, invariant, or prohibited coupling

## Validation

The decision is implemented correctly when:

- [ ] Observable architectural or contract property
- [ ] Security or authorization property
- [ ] Compatibility or migration condition
- [ ] Operational or recovery condition

## Reassessment triggers

Reconsider or supersede this decision when:

- scale, platform, dependency, security, cost, compatibility, or product assumption materially changes;
- a named risk becomes unacceptable;
- the owning boundary or contract changes.

## Implementation follow-up

- Bounded issue, migration, validation, or documentation link
