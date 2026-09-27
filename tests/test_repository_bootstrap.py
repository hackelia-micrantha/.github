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
BOOLEAN_KEYS = {
    "interface.cli",
    "interface.service",
    "interface.library",
    "interface.website",
    "interface.mobile",
}
STRING_KEYS = {
    "repository.name",
    "repository.purpose",
    "project.identity",
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
    "delivery.ciProvider",
    "delivery.releaseModel",
    "delivery.distribution",
    "security.profile",
}


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
                errors.append(f"{prefix} resolved decision requires value")
            else:
                value = decision.get("value")
                if key == "repository.visibility" and (not isinstance(value, str) or value not in {"public", "private", "internal"}):
                    errors.append(f"{prefix} repository.visibility has invalid value")
                elif key == "repository.defaultBranch":
                    if not isinstance(value, str) or not value.strip() or any(ch.isspace() for ch in value):
                        errors.append(f"{prefix} repository.defaultBranch requires non-empty token")
                elif key in BOOLEAN_KEYS and not isinstance(value, bool):
                    errors.append(f"{prefix} {key} requires boolean value")
                elif key in STRING_KEYS and (not isinstance(value, str) or not value.strip()):
                    errors.append(f"{prefix} {key} requires non-empty string value")
                elif key not in BOOLEAN_KEYS | STRING_KEYS | {"repository.visibility", "repository.defaultBranch"}:
                    errors.append(f"{prefix} resolved extension key lacks v1 value semantics")
            provenance = decision.get("provenance")
            if not isinstance(provenance, dict):
                errors.append(f"{prefix} resolved decision requires provenance")
            else:
                if provenance.get("authority") not in AUTHORITIES:
                    errors.append(f"{prefix} has invalid provenance authority")
                subject = provenance.get("subject")
                if not isinstance(subject, str) or not subject.strip():
                    errors.append(f"{prefix} provenance requires subject")
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
            else:
                if provenance.get("authority") not in AUTHORITIES:
                    errors.append(f"{prefix} has invalid provenance authority")
                subject = provenance.get("subject")
                if not isinstance(subject, str) or not subject.strip():
                    errors.append(f"{prefix} provenance requires subject")

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

    def test_example_resolves_only_explicit_fixture_and_org_policy(self) -> None:
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

    def test_semantic_validation_rejects_duplicate_decision_keys(self) -> None:
        manifest = json.loads(json.dumps(self.example))
        manifest["decisions"].append(
            {"key": "repository.visibility", "state": "unresolved"}
        )
        errors = validate_manifest(manifest)
        self.assertTrue(any("duplicates repository.visibility" in error for error in errors))

    def test_semantic_validation_rejects_unverifiable_provenance_shape(self) -> None:
        manifest = json.loads(json.dumps(self.example))
        manifest["decisions"][0]["provenance"].pop("subject", None)
        errors = validate_manifest(manifest)
        self.assertTrue(any("provenance requires subject" in error for error in errors))

    def test_semantic_validation_rejects_invalid_known_resolved_values(self) -> None:
        manifest = json.loads(json.dumps(self.example))
        visibility = next(d for d in manifest["decisions"] if d["key"] == "repository.visibility")
        visibility.update(
            {
                "state": "resolved",
                "value": {},
                "provenance": {
                    "authority": "human",
                    "subject": "repository-owner",
                    "reference": "test",
                },
            }
        )
        visibility.pop("question", None)
        errors = validate_manifest(manifest)
        self.assertTrue(any("repository.visibility has invalid value" in error for error in errors))

    def test_schema_marks_semantic_validation_as_required(self) -> None:
        self.assertIn(
            "semantic validation",
            self.schema["properties"]["decisions"]["description"].lower(),
        )
        self.assertIn(
            "authorized",
            self.schema["$defs"]["provenance"]["description"].lower(),
        )
        semantic = self.schema["x-micrantha-semantic-validation"]
        self.assertTrue(semantic["uniqueDecisionKeys"])
        self.assertTrue(semantic["verifyProvenanceAuthorityExternally"])
        self.assertTrue(semantic["revalidateAuthorityInputsBeforeApply"])


if __name__ == "__main__":
    unittest.main()
