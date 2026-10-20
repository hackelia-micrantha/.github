from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "micrantha-prompt-pack.yaml"
PROMPTS = ROOT / "docs" / "prompts"
MANIFEST = PROMPTS / "manifest.yaml"

EXPECTED_SOURCES = {
    "docs/prompts/README.md",
    "docs/prompts/overlays/cross-project-execution.md",
    "docs/prompts/planning/classify-and-route.md",
    "docs/prompts/issues/issue-grooming.md",
    "docs/prompts/reviews/engineering-artifact-review.md",
    "docs/prompts/pull-requests/merge-gate-review.md",
    "docs/prompts/decisions/qart-analysis.md",
}
EXPECTED_PROFILES = {
    "classify-and-route",
    "issue-grooming",
    "engineering-artifact-review",
    "merge-gate-review",
    "qart-analysis",
    "qats-analysis",
}


class PromptPackTests(unittest.TestCase):
    def _text(self) -> str:
        return PACK.read_text(encoding="utf-8")

    def _section(self, name: str, next_name: str) -> str:
        text = self._text()
        start = text.index(f"{name}:\n") + len(name) + 2
        end = text.index(f"\n{next_name}:", start)
        return text[start:end]

    def test_pack_uses_invokrum_v1_and_stable_id(self) -> None:
        text = self._text()
        self.assertIn("schema: invokrum.dev/v1\n", text)
        self.assertIn("id: micrantha-meta-prompts\n", text)

    def test_pack_sources_are_canonical_repository_files(self) -> None:
        overlay_section = self._section("overlays", "profiles")
        sources = set(re.findall(r"^    source: ([^\n]+)$", overlay_section, re.MULTILINE))
        self.assertEqual(EXPECTED_SOURCES, sources)
        missing = [source for source in sorted(sources) if not (ROOT / source).is_file()]
        self.assertEqual([], missing, f"pack references missing canonical sources: {missing}")

    def test_installed_root_candidate_covers_pack_profiles_and_sources(self) -> None:
        from tools.verify_prompt_pack_installed_root import ENTRY_POINT, PROFILES, SOURCES

        overlays = self._section("overlays", "profiles")
        sources = set(re.findall(r"^    source: ([^\n]+)$", overlays, re.MULTILINE))
        profile_section = self._section("profiles", "variables")
        profiles = set(re.findall(r"^  - id: ([a-z0-9-]+)$", profile_section, re.MULTILINE))
        self.assertEqual(sources | {ENTRY_POINT}, set(SOURCES))
        self.assertEqual(profiles, set(PROFILES))

    def test_required_foundation_scope_and_workflow_classes_are_exactly_one(self) -> None:
        classes = self._section("classes", "overlays")
        for class_id, order in (("foundation", 10), ("scope", 20), ("workflow", 30)):
            block = (
                f"  - id: {class_id}\n"
                f"    order: {order}\n"
                "    minimum: 1\n"
                "    maximum: 1\n"
            )
            self.assertIn(block, classes)

    def test_initial_profiles_select_shared_scope_and_one_workflow(self) -> None:
        profiles = self._section("profiles", "variables")
        profile_ids = set(re.findall(r"^  - id: ([a-z0-9-]+)$", profiles, re.MULTILINE))
        self.assertEqual(EXPECTED_PROFILES, profile_ids)

        workflow_by_profile = {profile: profile for profile in EXPECTED_PROFILES}
        workflow_by_profile["qats-analysis"] = "qart-analysis"
        for profile_id in sorted(EXPECTED_PROFILES):
            pattern = re.compile(
                rf"  - id: {re.escape(profile_id)}\n"
                r"    selections:\n"
                r"      foundation:\n"
                r"        - shared-engineering-contracts\n"
                r"      scope:\n"
                r"        - cross-project-execution\n"
                r"      workflow:\n"
                rf"        - {re.escape(workflow_by_profile[profile_id])}(?:\n|$)"
            )
            self.assertRegex(profiles, pattern)

    def test_qats_reuses_qart_workflow_without_a_second_source(self) -> None:
        overlays = self._section("overlays", "profiles")
        profiles = self._section("profiles", "variables")
        self.assertEqual(1, overlays.count("    source: docs/prompts/decisions/qart-analysis.md\n"))
        for profile in ("qart-analysis", "qats-analysis"):
            start = profiles.index(f"  - id: {profile}\n")
            next_profile = profiles.find("\n  - id: ", start + 1)
            block = profiles[start:] if next_profile == -1 else profiles[start:next_profile]
            self.assertIn("      workflow:\n        - qart-analysis\n", block)

    def test_workflow_sources_remain_registered_in_prompt_manifest(self) -> None:
        manifest = MANIFEST.read_text(encoding="utf-8")
        expected = {
            "classify-and-route": "planning/classify-and-route.md",
            "issue-grooming": "issues/issue-grooming.md",
            "engineering-artifact-review": "reviews/engineering-artifact-review.md",
            "merge-gate-review": "pull-requests/merge-gate-review.md",
            "qart-analysis": "decisions/qart-analysis.md",
        }
        for prompt_id, relative_path in expected.items():
            entry = (
                f"  - id: {prompt_id}\n"
                f"    name:"
            )
            self.assertIn(entry, manifest)
            prompt_start = manifest.index(f"  - id: {prompt_id}\n")
            next_entry = manifest.find("\n  - id: ", prompt_start + 1)
            prompt_block = manifest[prompt_start:] if next_entry == -1 else manifest[prompt_start:next_entry]
            self.assertIn(f"    file: {relative_path}\n", prompt_block)


if __name__ == "__main__":
    unittest.main()
