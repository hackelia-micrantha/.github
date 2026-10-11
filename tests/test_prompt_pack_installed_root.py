"""Unit checks for the deterministic local Invokrum bundle candidate builder."""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.verify_prompt_pack_installed_root import (
    SOURCES, make_candidate, publisher_identity, validate_installed_root,
    verified_publisher_result,
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
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            key = root / "publisher.pub"
            sig = root / "subject.sig"
            key.write_bytes(bytes(range(32)))
            sig.write_bytes(bytes(range(64)))
            fingerprint = hashlib.sha256(key.read_bytes()).hexdigest()
            self.assertIsNone(publisher_identity(None, None, None))
            self.assertEqual(fingerprint, publisher_identity(key, sig, fingerprint))
            with self.assertRaises(ValueError):
                publisher_identity(key, None, fingerprint)
            with self.assertRaises(ValueError):
                publisher_identity(key, sig, "0" * 64)
            with self.assertRaises(ValueError):
                publisher_identity(key, sig, "A" * 64)
            with self.assertRaises(ValueError):
                publisher_identity(key, sig, fingerprint + "0")
            sig.write_bytes(b"x" * 63)
            with self.assertRaises(ValueError):
                publisher_identity(key, sig, fingerprint)

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
