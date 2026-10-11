---
name: security-review
description: Review a Micrantha change, capability, or system for assets, trust boundaries, abuse paths, privileges, untrusted input, secret exposure, supply-chain risk, and safe failure.
---

# Security review

## Trigger

Use for `security review`, `threat review`, `review this boundary`, or whenever a change affects authentication, authorization, secrets, external input, execution, agents/tools, release pipelines, or cross-repository trust.

## Inputs

- architecture/data-flow and affected trust boundaries;
- actor identities, capabilities, credentials, and authority sources;
- untrusted inputs, external dependencies, execution environments, and persistence;
- relevant security requirements and project-local threat model/evidence.

## Workflow

1. Identify assets, actors, trust boundaries, entry points, and authoritative security properties.
2. Trace untrusted data and control flow across parsing, storage, network, process, plugin/tool, and repository/release boundaries.
3. Review authentication, authorization, least privilege, ambient authority, capability delegation, revocation, stale authority, and approval semantics.
4. Check secret handling and process/environment inheritance; require bounded environments where subprocesses do not need ambient credentials.
5. Review injection, path/file handling, unsafe deserialization, race/state transitions, replay/idempotency, denial behavior, and error information exposure where relevant.
6. Review dependency, build, provenance, artifact, and publication trust for supply-chain changes.
7. For agentic systems, inspect tool identity, policy enforcement, approval/evidence/provenance, bypass resistance, and distinction between advisory memory/context and effect authority.
8. Require tests of protected invariants and denial paths, not only successful authorization.
9. Rank findings by exploitability/impact and identify the weakest durable control that prevents recurrence.

## Mutation boundary

Do not reproduce secret values. Report location/type/exposure path and remediation. Read-only unless fixes are explicitly authorized.

## Completion

Complete when material trust boundaries and abuse paths are accounted for, residual risks are explicit, and each actionable finding has a concrete control and validation expectation.

## References

- `docs/standards/security.md`
- `docs/standards/ci-cd.md`
- `docs/standards/source-exposure-and-distribution.md`
- `docs/prompts/security/agentic-workflow-security-review.md`
- `docs/prompts/reviews/compound-review.md`
