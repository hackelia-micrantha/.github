from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "metadata" / "repository-bootstrap.schema.json"
EXAMPLE = ROOT / "docs" / "standards" / "templates" / "repository-bootstrap.json"

AUTHORITIES = {"human", "organization-policy", "project-policy"}
STATES = {"resolved", "unresolved", "not-applicable"}


def validate_manifest(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest root must be an object"]
    if data.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if data.get("kind") != "micrantha.repository-bootstrap":
        errors.append("kind must be micrantha.repository-bootstrap")

    decisions = data.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        return errors + ["decisions must be a non-empty array"]

    seen: set[str] = set()
    for index, decision in enumerate(decisions):
        prefix = f"decisions[{index}]"
        if not isinstance(decision, dict):
            errors.append(f"{prefix} must be an object")
            continue

        key = decision.get("key")
        if not isinstance(key, str) or "." not in key:
            errors.append(f"{prefix}.key must be a dotted decision key")
        elif key in seen:
            errors.append(f"{prefix}.key duplicates {key}")
        else:
            seen.add(key)

        state = decision.get("state")
        if state not in STATES:
            errors.append(f"{prefix}.state must be one of {sorted(STATES)}")
            continue

        if state == "resolved":
            if "value" not in decision or decision.get("value") is None:
                errors.append(f"{prefix} resolved decision requires non-null value")
            provenance = decision.get("provenance")
            if not isinstance(provenance, dict):
                errors.append(f"{prefix} resolved decision requires provenance")
            else:
                if provenance.get("authority") not in AUTHORITIES:
                    errors.append(f"{prefix} has invalid provenance authority")
                reference = provenance.get("reference")
                if not isinstance(reference, str) or not reference.strip():
                    errors.append(f"{prefix} provenance requires reference")
            if "question" in decision or "reason" in decision:
                errors.append(f"{prefix} resolved decision carries unresolved fields")

        elif state == "unresolved":
            if "value" in decision:
                errors.append(f"{prefix} unresolved decision must not carry value")
            if "provenance" in decision:
                errors.append(f"{prefix} unresolved decision must not carry decision provenance")
            if "reason" in decision:
                errors.append(f"{prefix} unresolved decision must not carry reason")

        elif state == "not-applicable":
            if "value" in decision:
                errors.append(f"{prefix} not-applicable decision must not carry value")
            reason = decision.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"{prefix} not-applicable decision requires reason")
            provenance = decision.get("provenance")
            if not isinstance(provenance, dict):
                errors.append(f"{prefix} not-applicable decision requires provenance")
            elif provenance.get("authority") not in AUTHORITIES:
                errors.append(f"{prefix} has invalid provenance authority")

    return errors


class RepositoryBootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.example = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_schema_and_example_are_valid_json_objects(self) -> None:
        self.assertIsInstance(self.schema, dict)
        self.assertIsInstance(self.example, dict)

    def test_schema_contains_no_default_keyword(self) -> None:
        found: list[str] = []

        def visit(value: Any, path: str = "$") -> None:
            if isinstance(value, dict):
                for key, child in value.items():
                    child_path = f"{path}.{key}"
                    if key == "default":
                        found.append(child_path)
                    visit(child, child_path)
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    visit(child, f"{path}[{index}]")

        visit(self.schema)
        self.assertEqual([], found, f"bootstrap schema must not define defaults: {found}")

    def test_example_satisfies_reference_semantics(self) -> None:
        self.assertEqual([], validate_manifest(self.example))

    def test_example_resolves_only_explicit_fixture_identity(self) -> None:
        resolved = [
            decision["key"]
            for decision in self.example["decisions"]
            if decision["state"] == "resolved"
        ]
        self.assertEqual(["repository.name", "repository.defaultBranch"], resolved)

    def test_unresolved_values_are_not_disguised_defaults(self) -> None:
        for decision in self.example["decisions"]:
            if decision["state"] != "unresolved":
                continue
            self.assertNotIn("value", decision)
            self.assertNotIn("provenance", decision)

    def test_example_keeps_material_creation_choices_explicit(self) -> None:
        decisions = {decision["key"]: decision for decision in self.example["decisions"]}
        required = {
            "repository.purpose",
            "project.identity",
            "repository.visibility",
            "repository.classification",
            "repository.maturity",
            "repository.license",
            "repository.sourceExposure",
            "repository.role",
            "repository.distributionMode",
            "repository.topology",
            "implementation.language",
            "implementation.runtime",
            "implementation.buildSystem",
            "implementation.packageManager",
            "interface.cli",
            "delivery.ciProvider",
            "delivery.releaseModel",
            "delivery.distribution",
            "security.profile",
        }
        self.assertEqual([], sorted(required - decisions.keys()))
        self.assertTrue(
            all(decisions[key]["state"] == "unresolved" for key in required),
            "material creation choices in the minimal example must remain unresolved",
        )

    def test_schema_does_not_allow_observation_as_decision_authority(self) -> None:
        provenance = self.schema["$defs"]["provenance"]
        authorities = provenance["properties"]["authority"]["enum"]
        self.assertEqual(["human", "organization-policy", "project-policy"], authorities)
        self.assertNotIn("observation", authorities)
        self.assertNotIn("repository-evidence", authorities)

    def test_decision_variants_are_explicit(self) -> None:
        definitions = self.schema["$defs"]
        self.assertEqual("resolved", definitions["resolvedDecision"]["properties"]["state"]["const"])
        self.assertEqual("unresolved", definitions["unresolvedDecision"]["properties"]["state"]["const"])
        self.assertEqual("not-applicable", definitions["notApplicableDecision"]["properties"]["state"]["const"])


if __name__ == "__main__":
    unittest.main()
