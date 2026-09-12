# Long-running execution selector

This selector complements `SKILL.md` and is intended for agent-instruction surfaces that choose skills from operator intent.

Select `long-running-execution` automatically when a non-trivial engineering run is active and the operator says or clearly means:

- `proceed in loops`;
- `continue until blocked`;
- `run this to completion`;
- `review -> fix -> validate -> re-review`;
- `fix loop to proceed`;
- `proceed` or `continue` when the current run already has a resolvable next safe transition.

Do not select it for a trivial one-step task solely because `proceed` or `continue` appears.

Selection continues the governed execution graph; it never grants new merge, release, publication, deployment, deletion, permission, credential, external-communication, or other consequential-effect authority.

Canonical organization guidance: `docs/engineering/agent-skill-selection.md`.
