"""Unit checks for the deterministic local Invokrum bundle candidate builder."""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.verify_prompt_pack_installed_root import SOURCES, make_candidate


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
