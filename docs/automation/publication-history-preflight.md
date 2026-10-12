# Historical Git publication audit

Status: opt-in, read-only evidence collection.

`tools/publication_history_preflight.py` complements the existing current-tree
publication preflight. Run it locally against a **full Git clone** with the relevant
branches and tags fetched. It examines all blobs reachable through local refs,
including files removed in later commits, and writes an access-controlled JSON report.

```sh
python tools/publication_history_preflight.py \
  --repo /path/to/full-clone \
  --output /secure/path/publication-history-report.json
```

A local report is created with mode `0600` and never overwritten. Standard output
contains only summary counts. Finding entries record the rule, path, and example
object identifier, **not** matching secret values.

Exit status:
- `0`: all reachable blobs within limits inspected and no blocking pattern found;
  human-review findings may still exist, and this is not publication approval.
- `1`: blocking credential patterns or risky committed paths found.
- `2`: indeterminate scan or an uninspected oversized blob. Never treat as green.

Limits are bounded by `--max-objects`, `--max-blob-bytes`, and
`--max-total-bytes`. Increase them intentionally where oversized artifacts
would otherwise make completeness indeterminate.

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

This is not enabled as a broad GitHub CI job: it must not upload private
findings or spend runner budget on entire repository histories. Follow the
Micrantha security standard, private incident process, and the repository's
publication owner.
