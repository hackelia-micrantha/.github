# Testing and validation standard

Testing exists to provide evidence that a declared outcome, contract, or safety property is true. Test count and coverage percentages are supporting signals, not substitutes for risk-based validation.

Micrantha uses a **risk-shaped test pyramid**: prefer the lowest layer that can faithfully validate a property, keep fast deterministic validation broad, and add progressively narrower higher-level validation where real boundaries or supported user/operator paths require it.

The organization does not mandate a universal unit/integration/end-to-end percentage. A repository should be able to explain why each material boundary is validated at the layer where failures can actually be observed.

## Required validation model

For each material change, identify:

- the behavior or property being validated;
- the authoritative contract or acceptance criterion;
- the relevant primary, failure, edge, migration, rollback, and security paths;
- the smallest test layer that provides trustworthy evidence;
- any higher-level boundary whose behavior cannot be established from lower-level tests;
- any behavior that remains unverified and why.

Do not add every test type mechanically. Use the combination required by the risk and integration boundary.

## Test pyramid

The default economic shape is:

```text
                  release / operational
                 install / upgrade / smoke
                    system / end-to-end
                     integration
                  contract / component
        unit / property / model / fuzz where useful

        cross-cutting: negative, security, compatibility,
        migration, resilience, concurrency, performance
```

Interpret the pyramid as a cost and feedback model, not a quota.

- **Unit/component** validation should carry most local behavioral coverage because it is fast, deterministic, and cheap to diagnose.
- **Contract** tests validate externally observable boundaries without requiring a complete deployed system.
- **Integration** tests validate real infrastructure and component interaction where fakes would hide material failure modes.
- **System/end-to-end** tests validate a small set of supported user/operator outcomes that cannot be established faithfully below that layer.
- **Release/operational** validation proves properties of the artifact and supported lifecycle, not merely the source tree.

Push a property downward only while the lower layer remains trustworthy. Do not replace a real database migration test with a mocked repository test, a packaged CLI test with a direct library test, or an authorization boundary test with an implementation-detail assertion.

## Test layers

| Layer | Purpose | Typical evidence |
| --- | --- | --- |
| Unit or component | Local logic, state transitions, parsing, policy, and error handling | Fast deterministic tests isolated from external systems |
| Contract | Public API, schema, command, event, file format, exit code, or provider boundary | Producer/consumer compatibility and stable error semantics |
| Integration | Real interaction among owned components or infrastructure | Database, filesystem, network, runner, package, or service behavior |
| System or end-to-end | Supported user or operator outcome across the deployed path | Install, execute, approve, release, recover, or migrate workflow |
| Release or operational | Built/package artifact and supported lifecycle | Package inspection, install/upgrade/rollback, smoke, recovery, runbook or failure exercise |

The following are **cross-cutting validation dimensions**, not separate pyramid levels. Apply them at the lowest trustworthy layer and at affected boundaries where needed:

| Dimension | Examples |
| --- | --- |
| Negative and boundary | malformed input, empty/maximal values, invalid state transitions, dependency failure |
| Security and adversarial | authorization denial, isolation, replay/substitution, path escape, secret handling, fail-closed behavior |
| Property/model/fuzz | invariants, generated inputs, state machines, parsers, protocol and serialization boundaries |
| Migration and compatibility | upgrade, downgrade where supported, rollback, mixed versions, schema/config compatibility |
| Resilience and concurrency | retries, cancellation, partial failure, races, restart, resource exhaustion |
| Performance and capacity | declared latency, throughput, memory/CPU/storage or scale limits |

## Planning hierarchy

Testing intent should be explicit before CI configuration becomes the de facto specification.

Use three conceptual plan levels:

1. **Micrantha baseline** — organization-wide invariants such as risk-based layering, deterministic evidence, regression coverage, required-gap visibility, security-negative validation, and exact revision binding.
2. **Project archetype** — reusable expectations for a CLI, library, service, web application, mobile application, infrastructure component, or security-sensitive system.
3. **Repository plan** — concrete properties, boundaries, environments, adapters, exceptions, and release requirements for the repository.

A repository may implement this hierarchy directly in documentation and native tooling while Testule adoption is incomplete. Once represented as Testule resources, composition must remain explicit and deterministic; inherited defaults must not hide conflicting or unsupported requirements.

## Testule integration

[Testule](https://github.com/hackelia-micrantha/testule) is Micrantha's portable **test-plan, testability-contract, adapter, normalized-evidence, and gap-analysis layer**. It does not replace ecosystem-native test frameworks or CI/CD.

The intended boundary is:

```text
Micrantha testing policy / repository requirements
                  |
                  v
            Testule TestPlan
                  |
          native/tool adapters
          /       |        \
     cargo test  go test   pytest / Vitest / Playwright / ...
          \       |        /
                  v
          normalized Evidence
                  |
                  v
             testule gaps
                  |
            CI / release gate
```

Rules:

- native tools remain authoritative for execution semantics;
- Testule represents what must be verified, what ran, what evidence exists, and what gaps remain;
- Testule Evidence must bind the exact subject revision and applicable plan identity before it satisfies a requirement;
- a required `missing`, `unsupported`, `skipped`, failed, stale, or mismatched requirement does not become satisfied because aggregate CI is green;
- Testule is not a runtime dependency of the product merely because it validates the product;
- Testule integration must not grant agents, adapters, CI, or test processes ambient filesystem, network, secret, process, or mutation authority;
- repositories may adopt Testule incrementally as required adapters/resources become available, but declared required validation must remain visible during migration rather than silently disappearing.

Organization-owned baseline/archetype plans belong with Micrantha engineering policy. Generic composition/resource/evidence semantics belong in Testule. Project-specific correctness remains repository-owned.

## Execution profiles

Repositories should map their applicable validation into three execution profiles. Exact workflow names and scheduling remain repository-owned.

### Pull request / fast feedback

Prefer bounded, deterministic checks that keep change feedback inexpensive:

- compile/type validation, formatting, linting, and applicable static/security analysis;
- unit/component tests;
- contract tests;
- property/fuzz smoke campaigns where useful;
- affected or bounded integration tests;
- Testule plan validation and gap evaluation where adopted.

A PR profile may intentionally omit expensive exhaustive validation only when later required gates are explicit.

### Main / comprehensive

Validate broader repository behavior after integration:

- full applicable integration suites;
- broader system paths;
- compatibility/migration matrices;
- longer bounded fuzz/property campaigns;
- concurrency/resilience/security-negative suites;
- package/build checks where a repository produces consumable artifacts.

Main-branch success should produce evidence tied to the exact integrated revision, not reuse stale PR evidence after the subject changed.

### Release

Release validation is against the **candidate artifact and exact release identity**, not merely the source checkout.

Where applicable validate:

- reproducible build/package construction;
- package/archive contents and provenance;
- install/uninstall or consumption through the supported distribution path;
- `--help`, `--version`, man pages, machine-output and exit-code contracts for CLI products;
- upgrade/migration and rollback/recovery commitments;
- critical end-to-end smoke paths;
- required security/adversarial, compatibility, performance, or operational properties;
- Testule gaps for release-required properties using evidence bound to the candidate revision/artifact.

A release is justified by evidence for declared requirements, not by the statement that "CI is green."

## Expectations by change

### Bug fixes

A bug fix should include a regression test at the lowest trustworthy layer. When the defect crossed a boundary or escaped existing validation, add or strengthen the boundary-level test that should have detected it.

A reproduced fuzz/property failure should be promoted into a durable regression case when the concrete failing input or invariant is useful and stable.

### New capabilities

Validate the primary outcome, relevant failure behavior, authorization and data boundaries, compatibility commitments, and an integrated supported path. Merged local slices do not prove capability completeness by themselves.

### Refactoring

Preserve observable behavior with focused tests. Add characterization tests when behavior is poorly specified, but do not freeze accidental defects or internal structure without justification.

### Security changes

Test the protected invariant and denial behavior, not only the successful path. Evidence should show that unauthorized, malformed, stale, replayed, substituted, or untrusted input cannot cross the affected boundary where those cases are material.

### Releases and migrations

Validate artifact installation or consumption, version identity, upgrade behavior, compatibility claims, release metadata, and rollback or recovery where promised.

## Determinism and isolation

Tests should be reproducible and independent of execution order. Control time, randomness, external services, environment, locale, filesystem state, and network access where they affect results.

A test may intentionally exercise real external infrastructure when that boundary is the subject of validation. Mark such tests clearly, make prerequisites explicit, and prevent them from silently becoming unreliable required gates.

Generated data, environment configuration, clocks, randomness, service state, resource limits, and fault injection should be treated as explicit test inputs when they materially affect reproducibility.

## Fixtures and test data

- Use synthetic or properly authorized data.
- Do not commit production secrets, tokens, personal data, or sensitive incident material.
- Keep fixtures small enough to understand and version.
- Record the generator, seed, or provenance of complex fixtures where available.
- Preserve minimized reproducers for useful fuzz/property failures.
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

Coverage, mutation score, test count, and benchmark totals are supporting observations. None replace evidence that the declared behavior, failure mode, or invariant was actually exercised.

## Test evidence in pull requests

A pull request should report:

- exact commands or workflows run;
- exact subject/head revision for the evidence;
- relevant environment or platform matrix;
- results and artifacts;
- skipped, unsupported, or unavailable validation and rationale;
- failures, flakiness, or limitations discovered;
- follow-up required before release or capability completion.

Do not use “tests pass” when only a subset ran or when the result came from a stale commit.

## Completion

An issue or capability is complete when its acceptance criteria and declared properties are evidenced at the appropriate layers. Passing unit tests alone does not establish integration, release, migration, security, or operational readiness unless those boundaries are genuinely absent.

Where a Testule plan is authoritative for the validation scope, completion additionally requires that mandatory requirements are satisfied by evidence bound to the applicable plan and exact subject revision, or that an explicit repository/organization decision changes the requirement itself.
