from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools import label_sync


class LabelSyncTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.manifest = label_sync.load(cls.root / "metadata/labels.json")
        cls.registry = label_sync.load(cls.root / "metadata/repositories.json")
        cls.standard = cls.root / "docs/standards/labels.md"

    def test_manifest_matches_documented_taxonomy_and_registry(self) -> None:
        self.assertEqual(
            label_sync.validate(self.manifest, self.registry, self.standard), []
        )

    def test_mutating_mode_is_rejected(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["repositories"][0]["mode"] = "apply"
        errors = label_sync.validate(manifest, self.registry, self.standard)
        self.assertTrue(any("apply is not implemented" in error for error in errors))

    def test_plan_distinguishes_outcomes_and_preserves_out_of_scope_labels(self) -> None:
        manifest = {
            "labels": [
                {"name": "status:ready", "color": "0e8a16", "description": "Ready."},
                {"name": "status:deferred", "color": "c5def5", "description": "Deferred."},
                {"name": "priority:P1", "color": "d93f0b", "description": "Next up."},
                {
                    "name": "type:bug",
                    "color": "d73a4a",
                    "description": "Bug.",
                    "aliases": ["bug"],
                },
                {"name": "area:ci", "color": "0052cc", "description": "CI."},
                {
                    "name": "type:feature",
                    "color": "a2eeef",
                    "description": "Feature.",
                    "aliases": ["enhancement"],
                },
            ],
            "repositories": [
                {
                    "repository": "hackelia-micrantha/example",
                    "mode": "report-only",
                    "labels": [
                        "status:ready",
                        "priority:P1",
                        "type:bug",
                        "area:ci",
                        "type:feature",
                    ],
                }
            ],
        }
        current = [
            {"name": "status:ready", "color": "0e8a16", "description": "Ready."},
            {"name": "status:deferred", "color": "c5def5", "description": "Deferred."},
            {"name": "priority:P1", "color": "ffffff", "description": "Old."},
            {"name": "bug", "color": "d73a4a", "description": "Bug."},
            {"name": "type:feature", "color": "a2eeef", "description": "Feature."},
            {"name": "enhancement", "color": "a2eeef", "description": "Feature."},
            {"name": "workflow", "color": "ededed", "description": ""},
        ]

        result = label_sync.plan(manifest, "hackelia-micrantha/example", current)
        actions = {item["label"]: item for item in result["actions"]}

        self.assertEqual(actions["status:ready"]["action"], "no-op")
        self.assertEqual(actions["priority:P1"]["action"], "update")
        self.assertEqual(actions["priority:P1"]["existing"][0]["color"], "ffffff")
        self.assertEqual(actions["priority:P1"]["desired"]["color"], "d93f0b")
        self.assertEqual(actions["priority:P1"]["existing"][0]["description"], "Old.")
        self.assertEqual(actions["priority:P1"]["desired"]["description"], "Next up.")
        self.assertEqual(actions["type:bug"]["action"], "migration")
        self.assertEqual(actions["type:bug"]["existing"][0]["name"], "bug")
        self.assertEqual(actions["area:ci"]["action"], "create")
        self.assertEqual(actions["area:ci"]["existing"], [])
        self.assertEqual(actions["type:feature"]["action"], "collision")
        self.assertEqual(
            {item["name"] for item in actions["type:feature"]["existing"]},
            {"type:feature", "enhancement"},
        )
        self.assertEqual(
            result["preservedRepositoryLabels"], ["status:deferred", "workflow"]
        )
        self.assertFalse(result["mutates"])

    def test_render_includes_exact_existing_and_desired_metadata(self) -> None:
        value = {
            "repository": "hackelia-micrantha/example",
            "mode": "report-only",
            "mutates": False,
            "actions": [
                {
                    "label": "priority:P1",
                    "action": "update",
                    "existing": [
                        {"name": "priority:P1", "color": "ffffff", "description": "Old."}
                    ],
                    "desired": {
                        "name": "priority:P1",
                        "color": "d93f0b",
                        "description": "Next up.",
                    },
                    "reason": "canonical label metadata differs",
                }
            ],
            "preservedRepositoryLabels": [],
        }
        text = label_sync.render(value)
        self.assertIn("`#ffffff` — Old.", text)
        self.assertIn("`#d93f0b` — Next up.", text)
        self.assertIn("Mutation: **disabled**", text)

    def test_unallowlisted_repository_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "not allowlisted"):
            label_sync.plan(
                {"labels": [], "repositories": []},
                "hackelia-micrantha/example",
                [],
            )


if __name__ == "__main__":
    unittest.main()
