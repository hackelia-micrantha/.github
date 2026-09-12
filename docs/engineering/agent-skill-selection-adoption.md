# Project adoption of automatic skill selection

The shared selector is canonical organization guidance, but repository agents only receive it automatically when their instruction-loading mechanism can see or import it.

For repositories using `AGENTS.md`, adopt the following minimal contract at the repository root or compose it into an existing file:

```markdown
## Micrantha shared skill selection

Use the Micrantha organization skill-selection contract from
`hackelia-micrantha/.github/docs/engineering/agent-skill-selection.md`.

When operator intent matches `proceed in loops`, `continue until blocked`,
`run this to completion`, or an active non-trivial run followed by `proceed`
or `continue`, select the shared `long-running-execution` contract.

Skill selection does not grant merge, release, deployment, publication,
destructive, permission, credential, external-communication, or other
consequential-effect authority.
```

A repository may copy the effective selector rather than depend on remote lookup, provided the source contract and revision are recorded so drift can be reviewed deliberately.

Prefer project automation that verifies the local selector against the organization contract over relying on manual synchronization.
