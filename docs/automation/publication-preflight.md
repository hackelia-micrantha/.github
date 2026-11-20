# Public repository publication preflight

Status: proposed / rollout-by-review

Current-tree publication preflight inspects tracked files for recognizable credential patterns, restricted key/configuration formats and review-worthy material. A blocking finding prevents publication; ambiguous findings require accountable classification. Unreadable or uninspected content is indeterminate rather than clean. Emit only bounded findings and never matching secret values. The preflight complements, rather than replaces, reviewed exact output paths, semantic disclosure classification and independently qualified publication authority.

## Non-goals and trust boundaries

A clean current tree does **not** prove that a repository is safe to publish.
This check does not inspect prior commits, unreachable objects, forks, release
attachments, Actions artifacts, pull-request discussions, deployed websites,
external caches, or non-pattern-sensitive proprietary information.

Conduct a separate **full-history** secret and private-data review before first
publication or after suspected exposure, with findings delivered to private,
access-controlled evidence storage. Do not send discovered secrets into public
issues, CI logs, artifacts, model transcripts, or PR descriptions.

Removing a tracked credential from `HEAD` never substitutes for
**issuer-side revocation or rotation**. For historical leak cleanup, coordinate
the credential lifecycle, disclosure scope, branch/tag/fork references, and
history rewrite under an explicit recovery plan.

Treat public/private publication as a trust boundary: classify proposed material
against the owner repository's publication policy, licensing rights, personal
data obligations, attack-surface disclosure and intellectual-property boundary.
A matching filename or `git ls-files` check cannot make these decisions.

## CI and rollout

Before
making the check mandatory for project release or promotion, integrate it into
a **reviewed** candidate pipeline, verify coverage and false-positive behavior,
and classify the target repository as public code, community contract, static
site, fork, archived historical project, or other deliberate publication profile.

Avoid a universal `--strict` gate without an exception and review mechanism:
some legitimate projects intentionally distribute public test databases, sample
debug signing keys, PDFs, and historical documentation. Such exceptions must
be exact, justified, and attributable; do not silently disable the rule globally.

This tool complements (and does not replace) Repora source/CI posture observation,
the Micrantha security standard, repository-specific publishing gates, and
GitHub native secret-scanning alerts.
