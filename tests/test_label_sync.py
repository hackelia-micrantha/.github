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

    def test_unknown_manifest_fields_are_rejected(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["unexpected"] = True
        manifest["labels"][0]["alias"] = ["legacy"]
        manifest["repositories"][0]["lables"] = []
        errors = label_sync.validate(manifest, self.registry, self.standard)
        self.assertTrue(any("manifest has unknown fields: unexpected" in error for error in errors))
        self.assertTrue(any("labels[0] has unknown fields: alias" in error for error in errors))
        self.assertTrue(
            any("repositories[0] has unknown fields: lables" in error for error in errors)
        )

    def test_alias_cannot_collide_with_a_canonical_label(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["labels"][0]["aliases"] = ["TYPE:BUG"]
        errors = label_sync.validate(manifest, self.registry, self.standard)
        self.assertTrue(
            any("collides with canonical label 'type:bug'" in error for error in errors)
        )

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
            {"name": "BUG", "color": "d73a4a", "description": "Bug."},
            {"name": "type:feature", "color": "a2eeef", "description": "Feature."},
            {"name": "enhancement", "color": "a2eeef", "description": "Feature."},
            {"name": "workflow", "color": "ededed", "description": ""},
        ]

        result = label_sync.plan(
            manifest,
            "hackelia-micrantha/example",
            current,
            control_revision="abc123",
        )
        actions = {item["label"]: item for item in result["actions"]}

        self.assertEqual(actions["status:ready"]["action"], "no-op")
        self.assertFalse(actions["status:ready"]["initialMutationEligible"])
        self.assertEqual(actions["priority:P1"]["action"], "update")
        self.assertTrue(actions["priority:P1"]["initialMutationEligible"])
        self.assertEqual(actions["priority:P1"]["existing"][0]["color"], "ffffff")
        self.assertEqual(actions["priority:P1"]["desired"]["color"], "d93f0b")
        self.assertEqual(actions["priority:P1"]["existing"][0]["description"], "Old.")
        self.assertEqual(actions["priority:P1"]["desired"]["description"], "Next up.")
        self.assertEqual(actions["type:bug"]["action"], "migration")
        self.assertFalse(actions["type:bug"]["initialMutationEligible"])
        self.assertEqual(actions["type:bug"]["existing"][0]["name"], "BUG")
        self.assertEqual(actions["area:ci"]["action"], "create")
        self.assertTrue(actions["area:ci"]["initialMutationEligible"])
        self.assertEqual(actions["area:ci"]["existing"], [])
        self.assertEqual(actions["type:feature"]["action"], "collision")
        self.assertFalse(actions["type:feature"]["initialMutationEligible"])
        self.assertEqual(
            {item["name"] for item in actions["type:feature"]["existing"]},
            {"type:feature", "enhancement"},
        )
        self.assertEqual(
            result["preservedRepositoryLabels"], ["status:deferred", "workflow"]
        )
        self.assertEqual(result["controlRevision"], "abc123")
        self.assertEqual(len(result["manifestSha256"]), 64)
        self.assertEqual(len(result["planSha256"]), 64)
        self.assertFalse(result["mutates"])

    def test_plan_digest_binds_relevant_state_and_ignores_preserved_labels(self) -> None:
        repo = "hackelia-micrantha/.github"
        revision = "a" * 40

        baseline = label_sync.plan(
            self.manifest,
            repo,
            [],
            control_revision=revision,
        )
        with_unrelated_local_label = label_sync.plan(
            self.manifest,
            repo,
            [{"name": "workflow", "color": "ededed", "description": "Local."}],
            control_revision=revision,
        )
        self.assertEqual(
            baseline["planSha256"], with_unrelated_local_label["planSha256"]
        )
        self.assertNotEqual(
            baseline["preservedRepositoryLabels"],
            with_unrelated_local_label["preservedRepositoryLabels"],
        )

        different_revision = label_sync.plan(
            self.manifest,
            repo,
            [],
            control_revision="b" * 40,
        )
        self.assertNotEqual(baseline["planSha256"], different_revision["planSha256"])

        first_label = self.manifest["labels"][0]
        selected_state_changed = label_sync.plan(
            self.manifest,
            repo,
            [first_label],
            control_revision=revision,
        )
        self.assertNotEqual(
            baseline["planSha256"], selected_state_changed["planSha256"]
        )

        changed_manifest = copy.deepcopy(self.manifest)
        changed_manifest["labels"][0]["description"] = "Changed desired state."
        manifest_changed = label_sync.plan(
            changed_manifest,
            repo,
            [],
            control_revision=revision,
        )
        self.assertNotEqual(
            baseline["manifestSha256"], manifest_changed["manifestSha256"]
        )
        self.assertNotEqual(baseline["planSha256"], manifest_changed["planSha256"])

    def test_canonical_json_is_key_order_independent(self) -> None:
        left = {"b": 2, "a": {"d": 4, "c": 3}}
        right = {"a": {"c": 3, "d": 4}, "b": 2}
        self.assertEqual(label_sync.canonical_json(left), label_sync.canonical_json(right))
        self.assertEqual(label_sync.sha256_json(left), label_sync.sha256_json(right))

    def test_render_includes_exact_identity_and_metadata(self) -> None:
        value = {
            "repository": "hackelia-micrantha/example",
            "controlRevision": "abc123",
            "manifestSha256": "1" * 64,
            "planSha256": "2" * 64,
            "mode": "report-only",
            "mutates": False,
            "actions": [
                {
                    "label": "priority:P1",
                    "action": "update",
                    "initialMutationEligible": True,
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
        self.assertIn("Control revision: `abc123`", text)
        self.assertIn(f"Manifest SHA-256: `{'1' * 64}`", text)
        self.assertIn(f"Plan SHA-256: `{'2' * 64}`", text)
        self.assertIn("`#ffffff` — Old.", text)
        self.assertIn("`#d93f0b` — Next up.", text)
        self.assertIn("Initial write candidate", text)
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
