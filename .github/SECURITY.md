# Security policy

Micrantha takes security seriously. For a repository-specific security policy, see its local `SECURITY.md`. This document defines the organization-wide defaults.

## Supported versions

Security updates are applied to the latest release or active development branch of each repository. Experimental and prototype repositories may not receive dedicated security patches — their maturity is disclosed in the [repository catalogue](docs/architecture/repository-catalogue.md).

## Reporting a vulnerability

**Do not report security vulnerabilities through public issues.**

To report a vulnerability in a Micrantha repository:

1. **Prefer private reporting.** If the repository has enabled [GitHub private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability), use that mechanism.
2. **Otherwise, email.** Send details to the repository steward or organization owner. Contact information is listed in the repository's local `SECURITY.md` or `GOVERNANCE.md`.
3. **Include enough to reproduce.** Describe the affected component, version, the nature of the vulnerability, and a minimal reproduction or impact scenario. Do not include exploit payloads, credentials, or sensitive data in public forums.

## What to expect

- **Acknowledgment** within a reasonable period.
- **Triage** against the organization [security engineering standard](docs/standards/security.md) and the affected repository's maturity and risk model.
- **Coordination** on disclosure timeline, affected versions, and remediation or mitigation.
- **Credit** where appropriate and agreed.

## Scope

Security reports are material when they affect:

- authentication, authorization, delegation, or identity;
- trust boundaries among users, services, agents, tools, runners, devices, or repositories;
- secrets, keys, tokens, signing identities, or sensitive configuration;
- personal, regulated, customer, or security-sensitive data;
- executable content, plugins, package installation, build systems, or supply-chain inputs;
- network exposure, tenancy, isolation, or resource limits;
- policy enforcement, audit evidence, provenance, or bypass paths.

Issues outside these boundaries may still be valid but are handled as ordinary defects or hardening work.

## Security exceptions

Accepted residual risk follows the [security exception](docs/standards/security.md#security-exceptions) format: scoped, time-bounded, attributable to a human decision owner, and reviewed before expiry.
