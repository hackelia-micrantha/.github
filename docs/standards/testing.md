# Testing and validation standard

Testing exists to provide evidence that a declared outcome, contract, or safety property is true. Test count and coverage percentages are supporting signals, not substitutes for risk-based validation.

## Required validation model

For each material change, identify:

- the behavior or property being validated;
- the authoritative contract or acceptance criterion;
- the relevant primary, failure, edge, migration, rollback, and security paths;
- the smallest test layer that provides trustworthy evidence;
- any behavior that remains unverified and why.

Do not add every test type mechanically. Use the combination required by the risk and integration boundary.

## Test layers

| Layer | Purpose | Typical evidence |
| --- | --- | --- |
| Unit or component | Local logic, state transitions, parsing, policy, and error handling | Fast deterministic tests isolated from external systems |
| Contract | Public API, schema, command, event, file format, exit code, or provider boundary | Producer/consumer compatibility and stable error semantics |
| Integration | Real interaction among owned components or infrastructure | Database, filesystem, network, runner, package, or service behavior |
| End-to-end | Supported user or operator outcome across the deployed path | Install, execute, approve, release, recover, or migrate workflow |
| Security and negative path | Authorization, validation, isolation, abuse resistance, and safe failure | Denial, redaction, least privilege, replay resistance, boundary enforcement |
| Migration and compatibility | Existing consumers, data, configuration, and mixed versions | Upgrade, downgrade where supported, rollback, and deprecation behavior |
| Performance and capacity | Declared latency, throughput, resource, or scale limits | Reproducible benchmark with environment and threshold |
| Operational exercise | Detection, diagnosis, recovery, and ownership | Alert, runbook, failure injection, restore, or incident simulation |

## Expectations by change

### Bug fixes

A bug fix should include a regression test at the lowest trustworthy layer. When the defect crossed a boundary or escaped existing validation, add or strengthen the boundary-level test that should have detected it.

### New capabilities

Validate the primary outcome, relevant failure behavior, authorization and data boundaries, compatibility commitments, and an integrated supported path. Merged local slices do not prove capability completeness by themselves.

### Refactoring

Preserve observable behavior with focused tests. Add characterization tests when behavior is poorly specified, but do not freeze accidental defects or internal structure without justification.

### Security changes

Test the protected invariant and denial behavior, not only the successful path. Evidence should show that unauthorized, malformed, stale, replayed, or untrusted input cannot cross the affected boundary where those cases are material.

### Releases and migrations

Validate artifact installation or consumption, version identity, upgrade behavior, compatibility claims, release metadata, and rollback or recovery where promised.

## Determinism and isolation

Tests should be reproducible and independent of execution order. Control time, randomness, external services, environment, locale, filesystem state, and network access where they affect results.

A test may intentionally exercise real external infrastructure when that boundary is the subject of validation. Mark such tests clearly, make prerequisites explicit, and prevent them from silently becoming unreliable required gates.

## Fixtures and test data

- Use synthetic or properly authorized data.
- Do not commit production secrets, tokens, personal data, or sensitive incident material.
- Keep fixtures small enough to understand and version.
- Record the generator or provenance of complex fixtures.
- Validate generated fixtures when malformed data would weaken the test.

## Flaky tests

A flaky required test is a broken gate, not normal noise.

When flakiness is detected:

1. preserve failure evidence;
2. identify whether the cause is product behavior, test design, infrastructure, or an external dependency;
3. fix promptly or quarantine with an owner, issue, rationale, and expiry;
4. do not convert a required test into a non-blocking check merely to make CI green;
5. remove quarantine only after repeated evidence of stability.

Retries may collect diagnostic evidence but must not conceal a consistently unreliable result.

## Coverage

Coverage tools may identify untested code, but organization policy does not mandate a universal percentage. Repositories may define thresholds when they are meaningful and resistant to gaming.

Prioritize coverage of:

- public and cross-repository contracts;
- security and authorization decisions;
- state transitions and recovery;
- parsing and untrusted input;
- compatibility and migration logic;
- failure behavior with material operational impact.

## Test evidence in pull requests

A pull request should report:

- exact commands or workflows run;
- relevant environment or platform matrix;
- results and artifacts;
- skipped validation and rationale;
- failures, flakiness, or limitations discovered;
- follow-up required before release or capability completion.

Do not use “tests pass” when only a subset ran or when the result came from a stale commit.

## Completion

An issue or capability is complete when its acceptance criteria and declared properties are evidenced at the appropriate layers. Passing unit tests alone does not establish integration, release, migration, security, or operational readiness unless those boundaries are genuinely absent.
