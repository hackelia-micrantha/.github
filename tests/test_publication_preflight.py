"""Publication preflight regression tests, including redacted output invariants."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import publication_preflight as preflight  # noqa: E402


class PublicationPreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def add(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "--", name], check=True)
        return path

    def scan(self):
        return preflight.scan(self.root)

    def test_example_configuration_is_not_a_secret(self):
        self.add(".env.example",
                 "LNBITS_API_KEY=replace-with-new-credential\n"
                 "ADMIN_PASSWORD=<set-at-deployment>\n")
        self.add("src/app.py", "print('hello')\n")
        self.assertEqual([], self.scan())

    def test_public_runtime_env_is_blocked_without_echoing_value(self):
        sensitive = "not-a-test-placeholder-123"
        self.add(".env", "LNBITS_API_KEY=" + sensitive + "\n")
        findings = self.scan()
        self.assertTrue(any(f["rule"] == "runtime-env" for f in findings))
        self.assertTrue(any(f["rule"] == "hardcoded-credential-assignment"
                            for f in findings))
        self.assertNotIn(sensitive, json.dumps(findings))

    def test_private_key_header_and_token_patterns(self):
        private_key = "-----BEGIN " + "PRIVATE KEY-----\n" + "example bytes" + "\n"
        self.add("notes.md", private_key)
        self.add("cli.py", "token = 'ghp_" + "A" * 36 + "'\n")
        findings = self.scan()
        self.assertIn("pem-private-key", {f["rule"] for f in findings})
        self.assertIn("recognized-token-shape", {f["rule"] for f in findings})
        self.assertNotIn("A" * 36, json.dumps(findings))

    def test_sensitive_file_types_and_human_review_items(self):
        self.add("tls/identity.p12", b"\x00")
        self.add("resources/users.db", b"SQLite format 3\x00")
        self.add("public/app.js.bak", "old implementation")
        self.add("docs/resume.pdf", b"%PDF-1.5")
        findings = self.scan()
        rules = {f["rule"] for f in findings}
        self.assertIn("credential-or-key-file", rules)
        self.assertIn("database-may-contain-personal-data", rules)
        self.assertIn("backup-or-retired-artifact", rules)
        self.assertIn("public-personal-profile", rules)

    def test_external_symlink_is_not_followed(self):
        target = self.root / "bad-link"
        target.symlink_to("../outside-private-file")
        subprocess.run(["git", "-C", str(self.root), "add", "bad-link"],
                       check=True)
        self.assertIn("symlink-escapes-root",
                      {f["rule"] for f in self.scan()})

    def test_tracked_only_and_no_git_history_claim(self):
        (self.root / ".env").write_text("LNBITS_API_KEY=secret\n")
        self.add("README.md", "# Public\n")
        self.assertEqual([], self.scan())


if __name__ == "__main__":
    unittest.main()
