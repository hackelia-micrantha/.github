from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import repository_health


class RegistryValidationTests(unittest.TestCase):
    def valid_registry(self) -> dict[str, object]:
        return {
            "$schema": "./repositories.schema.json",
            "schemaVersion": 1,
            "organization": "hackelia-micrantha",
            "repositories": [
                {
                    "repository": "hackelia-micrantha/example",
                    "classification": "service",
                    "maturity": "active",
                    "visibility": "public",
                    "defaultBranch": "main",
                    "archived": False,
                    "monitor": True,
                    "authority": ["example service"],
                    "requiredFiles": ["README.md"],
                }
            ],
        }

    def test_valid_registry_has_no_errors(self) -> None:
        self.assertEqual(repository_health.validate_registry(self.valid_registry()), [])

    def test_duplicate_repository_and_archived_maturity_are_rejected(self) -> None:
        registry = self.valid_registry()
        first = registry["repositories"][0]  # type: ignore[index]
        duplicate = dict(first)  # type: ignore[arg-type]
        duplicate["maturity"] = "archived"
        duplicate["archived"] = False
        registry["repositories"].append(duplicate)  # type: ignore[union-attr]

        errors = repository_health.validate_registry(registry)

        self.assertTrue(any("duplicates" in error for error in errors))
        self.assertTrue(
            any("archived maturity but archived is not true" in error for error in errors)
        )

    def test_unsafe_required_file_path_is_rejected(self) -> None:
        registry = self.valid_registry()
        registry["repositories"][0]["requiredFiles"] = ["../secret"]  # type: ignore[index]

        errors = repository_health.validate_registry(registry)

        self.assertTrue(any("unsafe path" in error for error in errors))


class WorkflowTemplateValidationTests(unittest.TestCase):
    def test_matching_workflow_and_properties_are_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            templates = root / "workflow-templates"
            templates.mkdir()
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/reusable-mise-ci.yml").write_text(
                "name: reusable\n", encoding="utf-8"
            )
            (templates / "mise-ci.yml").write_text(
                "uses: .github/workflows/reusable-mise-ci.yml\n", encoding="utf-8"
            )
            (templates / "mise-ci.properties.json").write_text(
                json.dumps({"name": "Mise CI", "description": "Run CI"}),
                encoding="utf-8",
            )

            self.assertEqual(repository_health.validate_workflow_templates(root), [])

    def test_missing_properties_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            templates = root / "workflow-templates"
            templates.mkdir()
            (templates / "mise-ci.yml").write_text("name: CI\n", encoding="utf-8")

            errors = repository_health.validate_workflow_templates(root)

            self.assertTrue(any("no matching" in error for error in errors))


class RepositoryHealthTests(unittest.TestCase):
    def entry(self, visibility: str = "public") -> dict[str, object]:
        return {
            "repository": "hackelia-micrantha/example",
            "classification": "service",
            "maturity": "active",
            "visibility": visibility,
            "defaultBranch": "main",
            "archived": False,
            "monitor": True,
            "authority": ["example service"],
            "requiredFiles": ["README.md"],
        }

    @patch("tools.repository_health.github_request")
    def test_inaccessible_private_repository_is_unknown(self, request) -> None:
        request.return_value = (404, None, "Not Found")

        result = repository_health.check_repository(
            self.entry("private"), "https://api.github.test", "token"
        )

        self.assertEqual(result["status"], "unknown")
        self.assertIn("inaccessible", result["findings"][0]["message"])

    @patch("tools.repository_health.github_request")
    def test_public_missing_required_file_is_error(self, request) -> None:
        request.side_effect = [
            (
                200,
                {
                    "visibility": "public",
                    "default_branch": "main",
                    "archived": False,
                },
                None,
            ),
            (404, None, "Not Found"),
        ]

        result = repository_health.check_repository(
            self.entry(), "https://api.github.test", None
        )

        self.assertEqual(result["status"], "error")
        self.assertIn("required file missing", result["findings"][0]["message"])

    @patch("tools.repository_health.github_request")
    def test_matching_repository_is_ok(self, request) -> None:
        request.side_effect = [
            (
                200,
                {
                    "visibility": "public",
                    "default_branch": "main",
                    "archived": False,
                },
                None,
            ),
            (200, {}, None),
        ]

        result = repository_health.check_repository(
            self.entry(), "https://api.github.test", None
        )

        self.assertEqual(result["status"], "ok")

    def test_failure_thresholds(self) -> None:
        summary = {"ok": 1, "skipped": 0, "unknown": 1, "warning": 1, "error": 0}

        self.assertFalse(repository_health.should_fail(summary, "none"))
        self.assertFalse(repository_health.should_fail(summary, "error"))
        self.assertTrue(repository_health.should_fail(summary, "warning"))


if __name__ == "__main__":
    unittest.main()
