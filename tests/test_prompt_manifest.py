from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "docs" / "prompts"
MANIFEST = PROMPTS / "manifest.yaml"
README = PROMPTS / "README.md"


class PromptManifestTests(unittest.TestCase):
    def _entries(self) -> list[tuple[str, str]]:
        text = MANIFEST.read_text(encoding="utf-8")
        ids = re.findall(r"^  - id: ([a-z0-9-]+)$", text, flags=re.MULTILINE)
        files = re.findall(r"^    file: ([^\n]+)$", text, flags=re.MULTILINE)
        self.assertEqual(
            len(ids),
            len(files),
            "each manifest prompt entry must contain exactly one id and file",
        )
        return list(zip(ids, files, strict=True))

    def test_prompt_ids_are_unique(self) -> None:
        ids = [prompt_id for prompt_id, _ in self._entries()]
        self.assertEqual(len(ids), len(set(ids)), "prompt ids must be unique")

    def test_manifest_prompt_files_exist(self) -> None:
        missing = [
            f"{prompt_id}: {relative}"
            for prompt_id, relative in self._entries()
            if not (PROMPTS / relative).is_file()
        ]
        self.assertEqual([], missing, f"manifest references missing prompt files: {missing}")

    def test_human_index_links_manifest_prompts(self) -> None:
        readme = README.read_text(encoding="utf-8")
        missing = [
            f"{prompt_id}: {relative}"
            for prompt_id, relative in self._entries()
            if f"]({relative})" not in readme
        ]
        self.assertEqual([], missing, f"README does not link manifest prompts: {missing}")

    def test_compound_review_is_registered(self) -> None:
        entries = dict(self._entries())
        self.assertEqual("reviews/compound-review.md", entries.get("compound-review"))


if __name__ == "__main__":
    unittest.main()
