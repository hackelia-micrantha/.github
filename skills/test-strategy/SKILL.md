---
name: test-strategy
description: Design a risk-based layered validation strategy for a Micrantha project or capability, including Testule where it strengthens deterministic execution and evidence.
---

# Test strategy

## Trigger

Use for `define the test strategy`, `review test gaps`, `prepare tests before implementation/release`, or when a project has ad-hoc tests without an explicit validation model.

## Inputs

- project/capability contracts and supported user/operator outcomes;
- architecture and integration boundaries;
- material security, migration, compatibility, performance, and operational risks;
- current test suites, tooling, CI gates, and Testule capability where applicable.

## Workflow

1. Map requirements and safety properties to failure modes and observable evidence.
2. Build a project-appropriate test pyramid/layer model rather than mechanically requiring every layer.
3. Put deterministic local behavior at unit/component level; protect public schemas/commands/formats with contract tests; exercise owned real boundaries with integration tests; keep end-to-end coverage focused on critical supported paths.
4. Add negative/security, migration/rollback, compatibility, performance/capacity, and operational exercises only where concrete risk warrants them.
5. Identify escaped-defect and boundary gaps; require bug fixes to add regression coverage at the lowest trustworthy layer and strengthen the layer that should have caught the escape.
6. Define fixtures, isolation, determinism, external-dependency policy, flake handling, and test-data security.
7. Integrate Testule where it can provide reusable test orchestration, fixtures, conformance, evidence capture, or failure injection without making projects depend on unnecessary central runtime authority.
8. Ensure local canonical commands and CI gates exercise equivalent validation; distinguish required gates from advisory diagnostics.
9. Define release validation against the packaged/installed artifact, not only the source tree.

## Evidence

Produce a requirements/risk-to-test map, layer ownership, canonical commands/gates, known gaps, and explicit rationale for omitted layers.

## Completion

Complete when material requirements and risks have a named trustworthy validation mechanism, gaps are explicit and prioritized, and CI/release evidence can prove what actually ran.

## References

- `docs/standards/testing.md`
- `docs/standards/ci-cd.md`
- `docs/prompts/README.md` shared validation contract
- Testule project-local contracts and documentation when integration is proposed
