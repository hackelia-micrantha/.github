"""Regression tests for redacted, local-only, history publication checks."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import publication_history_preflight as audit  # noqa: E402


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=True)


class PublicationHistoryPreflightTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.name", "Test User")
        git(self.root, "config", "user.email", "test@example.invalid")

    def tearDown(self):
        self.temporary.cleanup()

    def commit(self, path: str, data: str | bytes):
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data if isinstance(data, bytes) else data.encode())
        git(self.root, "add", "--", path)
        git(self.root, "commit", "-qm", "test fixture")

    def report(self, max_blob_bytes=2_000_000):
        return audit.audit(self.root, 500, max_blob_bytes, 5_000_000)

    def test_deleted_secret_remains_reported_without_exposing_bytes(self):
        marker = "SENSITIVE-EXAMPLE-DO-NOT-PUBLISH"
        self.commit(".env", "LNBITS_API_KEY=" + marker + "\n")
        git(self.root, "rm", "-q", ".env")
        (self.root / "README.md").write_text("safe public tip\n")
        git(self.root, "add", "README.md")
        git(self.root, "commit", "-qm", "remove old config")
        report = self.report()
        rules = {entry["rule"] for entry in report["findings"]}
        self.assertIn("committed-runtime-environment", rules)
        self.assertIn("hardcoded-secret-assignment", rules)
        self.assertNotIn(marker, json.dumps(report))
        self.assertEqual(report["status"], "review-required")

    def test_path_only_rule_not_applied_to_alias_with_same_blob(self):
        self.commit(".env", "generic-safe-content")
        (self.root / "README.md").write_text("generic-safe-content")
        git(self.root, "add", "README.md")
        git(self.root, "commit", "-qm", "same blob different name")
        report = self.report()
        self.assertTrue(any(x["path"] == ".env" and
                            x["rule"] == "committed-runtime-environment"
                            for x in report["findings"]))
        self.assertFalse(any(x["path"] == "README.md" and
                             x["rule"] == "committed-runtime-environment"
                             for x in report["findings"]))

    def test_historical_filename_persists_across_rename(self):
        self.commit("README.md", "safe text")
        git(self.root, "mv", "README.md", "old-identity.pem")
        git(self.root, "commit", "-qm", "rename to security-sensitive path")
        git(self.root, "mv", "old-identity.pem", "README.md")
        git(self.root, "commit", "-qm", "restore harmless path")
        report = self.report()
        self.assertTrue(any(
            x["path"] == "old-identity.pem"
            and x["rule"] == "key-or-credential-file"
            for x in report["findings"]
        ))

    def test_private_key_report_does_not_contain_key_body(self):
        marker = "SENSITIVE-EXAMPLE-PEM-CONTENT"
        self.commit("config.txt", "-----BEGIN PRIVATE KEY-----\n"
                    + marker + "\n-----END PRIVATE KEY-----\n")
        report = self.report()
        self.assertIn("private-key-pem",
                      {x["rule"] for x in report["findings"]})
        self.assertNotIn(marker, json.dumps(report))

    def test_database_review_is_distinct_from_block(self):
        self.commit("data/old.db", b"SQLite format 3\x00example")
        report = self.report()
        self.assertEqual(report["counts"]["block"], 0)
        self.assertEqual(report["counts"]["review"], 1)

    def test_big_blob_is_indeterminate_not_clean(self):
        self.commit("big.bin", b"Z" * 4096)
        report = self.report(max_blob_bytes=1024)
        self.assertEqual(report["status"], "indeterminate")
        self.assertFalse(report["history_scan_complete"])
        self.assertEqual(report["blobs_uninspected"], 1)

    def test_safe_repository_has_no_pattern_findings(self):
        self.commit(".env.example", "LNBITS_API_KEY=replace-with-value\n")
        self.assertEqual(self.report()["status"], "no-pattern-findings")

    def test_no_refs_is_indeterminate(self):
        with tempfile.TemporaryDirectory() as path:
            git(Path(path), "init", "-q")
            with self.assertRaises(audit.Incomplete):
                audit.audit(Path(path), 10, 1000, 10000)


if __name__ == "__main__":
    unittest.main()
