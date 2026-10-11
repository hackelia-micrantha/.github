from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "metadata" / "posture-policy-profiles" / "active-code-v1.json"


class ActiveCodePosturePolicyTests(unittest.TestCase):
    def load_profile(self) -> dict[str, object]:
        return json.loads(PROFILE.read_text(encoding="utf-8"))

    def test_profile_contract_and_scope_are_stable(self) -> None:
        profile = self.load_profile()

        self.assertEqual(profile["kind"], "repora.posture-policy-profile")
        self.assertEqual(profile["version"], 1)
        self.assertEqual(profile["id"], "micrantha-active-code-v1")
        self.assertEqual(profile["exceptions"], [])

    def test_profile_uses_only_stable_hygiene_facts(self) -> None:
        profile = self.load_profile()
        rules = {rule["id"]: rule for rule in profile["rules"]}

        expected = {
            "default-branch-protected": {
                "fact": "repository.default_branch_protected",
                "operator": "equals",
                "expected": True,
            },
            "immutable-third-party-actions": {
                "fact": "ci.mutable_third_party_action_count",
                "operator": "at_most",
                "expected": 0,
            },
            "workflow-permissions-declared": {
                "fact": "ci.workflows_without_declared_permissions_count",
                "operator": "at_most",
                "expected": 0,
            },
        }

        self.assertEqual(set(rules), set(expected))
        for rule_id, contract in expected.items():
            with self.subTest(rule=rule_id):
                rule = rules[rule_id]
                self.assertEqual(rule["area"], "repository-hygiene")
                self.assertEqual(rule["severity"], "high")
                self.assertEqual(rule["fact"], contract["fact"])
                self.assertEqual(rule["operator"], contract["operator"])
                self.assertEqual(rule["expected"], contract["expected"])
                self.assertTrue(rule["title"].strip())
                self.assertTrue(rule["remediation"])


if __name__ == "__main__":
    unittest.main()
