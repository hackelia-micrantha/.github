# Automatic skill selection

Use the Micrantha shared skill-selection contract at `docs/engineering/agent-skill-selection.md`.

Interpret operator intent rather than requiring an explicit skill name. In particular, for a non-trivial active engineering run, phrases such as `proceed in loops`, `continue until blocked`, `run this to completion`, `fix loop to proceed`, and a subsequent bare `proceed` or `continue` should select `skills/long-running-execution/SKILL.md` automatically.

Compose specialized skills as required by the current transition. Skill selection never widens mutation or consequential-effect authority.
