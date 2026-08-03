# Micrantha engineering standards

These standards define organization-wide defaults for engineering evidence, security, delivery, documentation, and work-item taxonomy. They complement [`GOVERNANCE.md`](../../GOVERNANCE.md), the [repository lifecycle](../governance/repository-lifecycle.md), and repository-local requirements.

## Standards

- [Testing and validation](testing.md)
- [CI/CD](ci-cd.md)
- [Security engineering](security.md)
- [Releases and versioning](releases.md)
- [Documentation](documentation.md)
- [Labels and work-item taxonomy](labels.md)

## Application

Apply requirements according to the repository's classification, maturity, risk, supported surface, and deployment model. A small experimental library does not need the same controls as a stable release pipeline or an authorization service, but it must state its limitations honestly.

Repository-local standards may be stricter. A local exception should identify:

- the organization default being changed;
- why the default does not fit;
- the replacement control or evidence;
- affected security, compatibility, release, or support claims;
- the accountable owner and review date.

Exceptions do not authorize misleading maturity claims, weakened security boundaries without risk acceptance, or bypass of required release and validation gates.

## Shared principles

1. Validate outcomes and contracts, not only implementation details.
2. Treat failure, migration, rollback, and security paths as first-class behavior.
3. Keep CI least-privileged, deterministic, observable, and resistant to untrusted input.
4. Do not describe planned, experimental, or partially integrated behavior as fully delivered.
5. Preserve traceability from decisions and issues to code, validation, release evidence, and documentation.
6. Prefer small, bounded, independently reviewable changes.
7. Record limitations and residual risks instead of hiding them behind generic checklists.

## Maturity relationship

The [repository lifecycle](../governance/repository-lifecycle.md) defines when stronger evidence becomes necessary. Experimental repositories may use reduced ceremony, while Incubating, Active, Stable, and Maintenance repositories progressively require stronger validation, compatibility, release, operational, and support evidence.
