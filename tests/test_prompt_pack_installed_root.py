"""Unit checks for the deterministic local Invokrum bundle candidate builder."""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.verify_prompt_pack_installed_root import (
    SOURCES, make_candidate, validate_publisher_inputs, validate_installed_root,
    snapshot_publisher_inputs, verified_publisher_result, verify_source_commit,
)


class CandidateTest(unittest.TestCase):
    def test_generated_manifest_is_canonical_and_binds_original_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            source = root / "source"
            candidate = root / "candidate"
            for name in SOURCES:
                file = source / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(("sample " + name + "\n").encode("utf-8"))
            manifest, subject = make_candidate(source, candidate)
            document = json.loads(manifest)
            self.assertEqual(document["format"], "invokrum.pack-bundle/v1")
            self.assertEqual(document["entry_point"], "micrantha-prompt-pack.yaml")
            self.assertEqual([entry["path"] for entry in document["files"]], sorted(SOURCES))
            self.assertEqual(manifest, json.dumps(document, separators=(",", ":"), ensure_ascii=False).encode())
            self.assertEqual(subject, hashlib.sha256(manifest).hexdigest())
            for entry in document["files"]:
                payload = (candidate / entry["path"]).read_bytes()
                self.assertEqual(entry["digest"], hashlib.sha256(payload).hexdigest())
                self.assertEqual(entry["byte_length"], len(payload))

    def test_publisher_inputs_are_complete_and_host_pinned(self) -> None:
        # These are only CLI input checks, not cryptographic verification.
        key = Path("caller-owned-public-key")
        signature = Path("caller-owned-signature")
        fingerprint = "a" * 64
        self.assertIsNone(validate_publisher_inputs(None, None, None))
        self.assertEqual(fingerprint, validate_publisher_inputs(key, signature, fingerprint))
        with self.assertRaises(ValueError):
            validate_publisher_inputs(key, None, fingerprint)
        with self.assertRaises(ValueError):
            validate_publisher_inputs(None, signature, fingerprint)
        with self.assertRaises(ValueError):
            validate_publisher_inputs(key, signature, None)
        for invalid in ("", "0" * 63, "A" * 64, "0" * 65, "sha256:" + "a" * 64):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    validate_publisher_inputs(key, signature, invalid)

    def test_publisher_input_snapshot_survives_source_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            supplied_key = root / "external.pub"
            supplied_signature = root / "external.sig"
            supplied_key.write_bytes(bytes(range(32)))
            supplied_signature.write_bytes(bytes(range(64)))
            private = root / "private"
            private.mkdir()
            key_copy, sig_copy = snapshot_publisher_inputs(
                supplied_key, supplied_signature, private,
            )
            supplied_key.write_bytes(b"replacement public key")
            supplied_signature.write_bytes(b"replacement signature")
            self.assertEqual(key_copy.read_bytes(), bytes(range(32)))
            self.assertEqual(sig_copy.read_bytes(), bytes(range(64)))
            self.assertNotEqual(sig_copy.read_bytes(), supplied_signature.read_bytes())

    def test_source_commit_requires_clean_exact_git_tree(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch) / "source"
            root.mkdir()
            def git(*args: str) -> str:
                return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()
            git("init", "-q")
            for source in SOURCES:
                file = root / source
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(("source " + source + "\\n").encode())
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                "commit", "-qm", "pin canonical sources")
            sha = git("rev-parse", "HEAD")
            self.assertEqual(sha, verify_source_commit(root, sha))
            # A replacement ref must not redefine the tree behind a trusted SHA.
            fixture_source = root / SOURCES[-1]
            fixture_source.write_bytes(fixture_source.read_bytes() + b"malicious replacement")
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                "commit", "-qm", "replacement tree")
            replacement = git("rev-parse", "HEAD")
            git("replace", sha, replacement)
            git("reset", "--hard", sha)
            self.assertEqual(sha, git("rev-parse", "HEAD"))
            with self.assertRaises(ValueError):
                verify_source_commit(root, sha)
            git("replace", "-d", sha)
            git("reset", "--hard", sha)
            self.assertEqual(sha, verify_source_commit(root, sha))
            with self.assertRaises(ValueError):
                verify_source_commit(root, "0" * 40)
            with self.assertRaises(ValueError):
                verify_source_commit(root, sha[:12])
            changed = root / SOURCES[-1]
            original = changed.read_bytes()
            changed.write_bytes(original + b"intentional drift")
            with self.assertRaises(ValueError):
                verify_source_commit(root, sha)
            changed.write_bytes(original)
            untracked = root / "untracked.tmp"
            untracked.write_text("untracked", encoding="utf-8")
            with self.assertRaises(ValueError):
                verify_source_commit(root, sha)
            untracked.unlink()
            self.assertEqual(sha, verify_source_commit(root, sha))
            staged = Path(scratch) / "staged"
            make_candidate(root, staged)
            self.assertEqual(sha, verify_source_commit(root, sha, staged))
            staged_file = staged / SOURCES[-1]
            staged_file.write_bytes(staged_file.read_bytes() + b"late stage mutation")
            with self.assertRaisesRegex(ValueError, "staged source differs"):
                verify_source_commit(root, sha, staged)
            child = root / "docs"
            with self.assertRaises(ValueError):
                verify_source_commit(child, sha)

    def test_changed_bundle_has_separately_consistent_subject(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            source = root / "source"
            for path in SOURCES:
                file = source / path
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(("source " + path + "\\n").encode())
            original_manifest, original_digest = make_candidate(source, root / "original")
            altered = source / SOURCES[-1]
            altered.write_bytes(altered.read_bytes() + b"changed source")
            second_manifest, second_digest = make_candidate(source, root / "changed")
            self.assertNotEqual(original_digest, second_digest)
            self.assertNotEqual(original_manifest, second_manifest)
            self.assertEqual(hashlib.sha256(second_manifest).hexdigest(), second_digest)
            second = json.loads(second_manifest)
            self.assertEqual(second["format"], "invokrum.pack-bundle/v1")

    def test_authenticated_proof_requires_explicit_commit(self) -> None:
        from tools.verify_prompt_pack_installed_root import prove
        with self.assertRaisesRegex(ValueError, "source commit"):
            prove(Path("/nonexistent/invokrum"), Path("."), Path("pub"), Path("sig"), "a" * 64)

    def test_authenticated_result_rejects_unsigned_and_identity_mismatch(self) -> None:
        subject = "sha256:" + "a" * 64
        key = "b" * 64
        good = {
            "installation_format": "invokrum.installation/v2",
            "publisher_authentication": {
                "status": "verified-and-authorized",
                "mechanism": "ed25519-subject-v1",
                "subject": subject.removeprefix("sha256:"),
                "identity": {"key.sha256": key},
            },
        }
        self.assertTrue(verified_publisher_result(good, subject, key))
        self.assertFalse(verified_publisher_result(
            {"installation_format": "invokrum.installation/v1",
             "publisher_authentication": "not-provided"}, subject, key))
        for wrong in (
            {"status": "not-provided"},
            {**good["publisher_authentication"], "subject": "sha256:" + "c" * 64},
            {**good["publisher_authentication"], "identity": {"key.sha256": "c" * 64}},
            {**good["publisher_authentication"], "mechanism": "some-other-mechanism"},
        ):
            self.assertFalse(verified_publisher_result(
                {**good, "publisher_authentication": wrong}, subject, key))

    def test_installed_root_accepts_real_private_directory(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            store = Path(scratch) / "store"
            root = store / "sha256" / "subject"
            root.mkdir(parents=True)
            validate_installed_root(root, store)

    def test_installed_root_rejects_direct_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            base = Path(scratch)
            store = base / "store"
            outside = base / "outside"
            outside.mkdir()
            store.mkdir()
            linked = store / "subject"
            linked.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(RuntimeError):
                validate_installed_root(linked, store)

    def test_installed_root_rejects_symlinked_parent_escape(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            base = Path(scratch)
            store = base / "store"
            outside = base / "outside"
            (outside / "subject").mkdir(parents=True)
            store.mkdir()
            (store / "sha256").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(RuntimeError):
                validate_installed_root(store / "sha256" / "subject", store)

    def test_missing_canonical_source_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            source = root / "source"
            file = source / SOURCES[0]
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(b"pack")
            with self.assertRaises(ValueError):
                make_candidate(source, root / "candidate")

    def test_source_symlink_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            source = root / "source"
            for name in SOURCES:
                file = source / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(b"test")
            path = source / SOURCES[0]
            path.unlink()
            path.symlink_to(source / SOURCES[1])
            with self.assertRaises(ValueError):
                make_candidate(source, root / "candidate")


if __name__ == "__main__":
    unittest.main()
