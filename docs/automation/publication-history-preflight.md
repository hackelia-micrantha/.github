# Historical Git publication audit

Status: opt-in, read-only evidence collection.

Historical publication assessment complements current-tree review. Inspect all relevant reachable branch, tag and other authorized ref objects within deliberate resource limits, from a verified complete clone. Retain structured findings, coverage, and indeterminate results in a private permissioned report with no matching secrets. A report with review findings is not clearance; absent refs, unreadable objects and oversized uninspected blobs block qualification.

## Required safeguards

1. Use a deliberately authorized repository checkout. This command never
   fetches, pushes, revokes, changes visibility, or modifies Git refs.
2. Keep findings on an encrypted or permissioned local/private surface.
   Do not upload reports to GitHub Actions artifacts, open issues, public
   CI logs, or model transcripts.
3. Rotate or revoke exposed credentials at their issuers. Cleaning current
   tree tips and rewriting Git history do not invalidate copied credentials.
4. Determine the status of every branch and tag, including stale feature
   branches and archives. External forks, clones, private PR refs, GitHub caches,
   releases, rendered sites, and unreachable objects remain outside this tool.
5. A path-only or pattern-only match may be harmless test data; conversely,
   a clean pattern scan does not demonstrate that personal data, proprietary
   architecture, access control, or unpublished material is absent.
6. Require explicit human classification for database files, backups,
   personal documents, and any other publication-boundary findings.

The local `git rev-list --objects --all` path is representative and may not
enumerate every filename used for the same blob across history. Use commit/path
analysis to reconstruct all affected references before rewriting.

Do not expose private findings through public CI, or run unbounded repository history scanning. Follow the
Micrantha security standard, private incident process, and the repository's
publication owner.
