---
name: Delivery issue
description: Implement a bounded feature, infrastructure change, security improvement, bug fix, or refactor
title: ""
labels: []
assignees: []
---

## Summary

Describe the problem, desired outcome, and why the work matters.

## Work-item type

Feature / Infrastructure / Security hardening / Bug / Refactor / Documentation

## Context

Include the current behaviour, relevant architecture, evidence, constraints, and related issues, PRs, RFCs, ADRs, or documentation.

## Problem

State the observable problem, impact, risk, or missing capability. Distinguish confirmed facts from suspected causes.

## Desired outcome

Describe what should be observably true when this issue is complete.

## Scope

### In scope

- <Required outcome or behaviour>

### Out of scope

- <Adjacent or follow-up work>

## Requirements

### Functional

- [ ] <Required behaviour>
- [ ] <Failure or fallback behaviour>

### Quality attributes and constraints

- Security:
- Reliability:
- Compatibility:
- Performance or capacity:
- Maintainability:
- Auditability or determinism:

Remove attributes that do not materially apply.

## Acceptance criteria

### Scenario: <primary behaviour>

**Given** <initial condition>  
**When** <action or event>  
**Then** <observable result>

### Scenario: <failure or edge case>

**Given** <invalid, unavailable, or adversarial condition>  
**When** <operation occurs>  
**Then** <safe and observable result>

## Security and governance

- Assets and trust boundaries:
- Authorization and approval requirements:
- Secret or sensitive-data handling:
- Fail-open, fail-closed, quarantine, or override posture:
- Required evidence or provenance:
- Residual risk:

## Operational considerations

- Observability and diagnostics:
- Deployment and configuration:
- Migration and compatibility:
- Rollout and rollback:
- Recovery and support:

## Validation strategy

- [ ] Unit or component tests
- [ ] Contract or integration tests
- [ ] End-to-end tests
- [ ] Security or adversarial tests
- [ ] Compatibility or migration tests
- [ ] Manual validation or demo

Remove checks that do not apply and state the concrete evidence expected.

## Delivery slices

1. <Foundation or contract>
2. <Core capability>
3. <Integration, hardening, or rollout>

Use independently reviewable and preferably independently mergeable slices.

## Dependencies

- **Blocked by:**
- **Blocks:**
- **Related:**

## Definition of done

- [ ] Acceptance criteria are satisfied
- [ ] Primary, failure, and relevant adversarial paths are tested
- [ ] Security and trust boundaries are preserved or strengthened
- [ ] Operational visibility is present where required
- [ ] Compatibility, migration, and rollback concerns are addressed
- [ ] Documentation is updated
- [ ] CI and required quality gates pass
- [ ] Remaining work is captured separately
