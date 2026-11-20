# Shared automation principles

Public specifications and starter workflows define reusable interfaces and security constraints; repository-local owners remain accountable for task execution, verification, runner trust and release authority. No shared automation may silently inherit privileges, use private data for a public report or imply approval from a successful check.

- [Automation security](SECURITY.md)
- [Shared automation versioning](versioning.md)
- [CI/CD standard](../standards/ci-cd.md)
- [Publication preflight principles](publication-preflight.md)
- [Historical audit principles](publication-history-preflight.md)
- [Label taxonomy](../standards/labels.md)

Public starter templates and reusable CI entry points retain their reviewed interface; callers pin accepted revisions and supply their own tested tasks. Private operational inventories and evidence are not public documentation.
