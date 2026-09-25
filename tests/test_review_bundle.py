"""Tests for deterministic independent-review bundle construction."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from tools.review_bundle import build_bundle, canonical_bytes


class ReviewBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.patch = self.root / "candidate.patch"
        self.patch.write_text("diff --git a/a b/a\n+safe change\n", encoding="utf-8")

    def args(self, **overrides: object) -> argparse.Namespace:
        values: dict[str, object] = {
            "repository": "hackelia-micrantha/.github",
            "subject": "pull_request:123",
            "patch_base_sha": "b" * 40,
            "reviewed_sha": "a" * 40,
            "patch": self.patch,
            "patch_ref": "https://example.invalid/immutable/a.patch",
            "scope": ["review evidence boundary"],
            "authority_ref": ["docs/governance/independent-review.md"],
            "acceptance_ref": ["issue:123"],
            "validation_ref": ["ci:green"],
            "source_exposure": "public",
            "external_transfer_authorization_ref": None,
            "prompt_context_file": None,
            "output": None,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def test_bundle_is_deterministic_and_digest_bound(self) -> None:
        first = build_bundle(self.args())
        second = build_bundle(self.args())
        self.assertEqual(first, second)
        self.assertNotIn("generated_at", first)

        expected = first["bundle_sha256"]
        unsigned = dict(first)
        unsigned.pop("bundle_sha256")
        self.assertEqual(expected, hashlib.sha256(canonical_bytes(unsigned)).hexdigest())

        self.assertEqual("b" * 40, first["candidate"]["patch_base_sha"])
        self.assertEqual("a" * 40, first["candidate"]["reviewed_sha"])
        self.assertEqual(
            hashlib.sha256(self.patch.read_bytes()).hexdigest(),
            first["candidate"]["patch"]["sha256"],
        )
        self.assertTrue(first["constraints"]["read_only"])
        self.assertFalse(first["constraints"]["mutation_tools_allowed"])
        self.assertIn("Do not mutate the repository", first["review"]["prompt"])

    def test_patch_change_changes_bundle_identity(self) -> None:
        before = build_bundle(self.args())
        self.patch.write_text("diff --git a/a b/a\n+different change\n", encoding="utf-8")
        after = build_bundle(self.args())
        self.assertNotEqual(
            before["candidate"]["patch"]["sha256"],
            after["candidate"]["patch"]["sha256"],
        )
        self.assertNotEqual(before["bundle_sha256"], after["bundle_sha256"])

    def test_private_source_defaults_to_external_prohibited(self) -> None:
        bundle = build_bundle(self.args(source_exposure="private"))
        self.assertEqual(
            {"state": "prohibited", "authorization_ref": None},
            bundle["review"]["external_source_transfer"],
        )

    def test_private_source_can_record_explicit_external_authorization(self) -> None:
        bundle = build_bundle(
            self.args(
                source_exposure="private",
                external_transfer_authorization_ref="approval:SEC-42",
            )
        )
        self.assertEqual(
            {
                "state": "explicitly-authorized",
                "authorization_ref": "approval:SEC-42",
            },
            bundle["review"]["external_source_transfer"],
        )

    def test_project_context_cannot_replace_mandatory_adversarial_prompt(self) -> None:
        context = self.root / "review-context.txt"
        context.write_text("Focus on schema compatibility.", encoding="utf-8")
        bundle = build_bundle(self.args(prompt_context_file=context))
        prompt = bundle["review"]["prompt"]
        self.assertIn("Do not assume the proposal is approved.", prompt)
        self.assertIn("Do not mutate the repository.", prompt)
        self.assertIn("Focus on schema compatibility.", prompt)
        self.assertIn("does not override the adversarial instructions", prompt)

    def test_public_source_rejects_unnecessary_transfer_override(self) -> None:
        with self.assertRaisesRegex(ValueError, "unnecessary for public source"):
            build_bundle(
                self.args(external_transfer_authorization_ref="approval:not-needed")
            )

    def test_requires_exact_lowercase_patch_base_sha(self) -> None:
        for value in ("abc", "B" * 40, "g" * 40, "b" * 39):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "patch_base_sha"):
                    build_bundle(self.args(patch_base_sha=value))

    def test_rejects_identical_patch_base_and_candidate(self) -> None:
        with self.assertRaisesRegex(ValueError, "different revisions"):
            build_bundle(self.args(patch_base_sha="a" * 40))

    def test_requires_exact_lowercase_commit_sha(self) -> None:
        for value in ("abc", "A" * 40, "g" * 40, "a" * 39):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "40-hex"):
                    build_bundle(self.args(reviewed_sha=value))

    def test_requires_number_for_pull_request_or_issue(self) -> None:
        for subject in ("pull_request", "issue:0", "pull_request:x"):
            with self.subTest(subject=subject):
                with self.assertRaisesRegex(ValueError, "subject must be"):
                    build_bundle(self.args(subject=subject))

    def test_commit_subject_has_no_number(self) -> None:
        bundle = build_bundle(self.args(subject="commit"))
        self.assertEqual(
            {"kind": "commit", "number": None},
            bundle["candidate"]["subject"],
        )

    def test_schema_encodes_subject_and_transfer_state_invariants(self) -> None:
        schema_path = (
            Path(__file__).resolve().parents[1]
            / "metadata"
            / "independent-review-bundle.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        subject = schema["properties"]["candidate"]["properties"]["subject"]
        self.assertEqual(["kind", "number"], subject["required"])
        self.assertTrue(
            any(
                rule.get("then", {})
                .get("properties", {})
                .get("number", {})
                .get("type")
                == "null"
                for rule in subject["allOf"]
            )
        )

        transfer = schema["properties"]["review"]["properties"][
            "external_source_transfer"
        ]
        self.assertTrue(
            any(
                rule.get("if", {})
                .get("properties", {})
                .get("state", {})
                .get("const")
                == "explicitly-authorized"
                and rule.get("then", {})
                .get("properties", {})
                .get("authorization_ref", {})
                .get("type")
                == "string"
                for rule in transfer["allOf"]
            )
        )

    def test_schema_file_matches_emitted_contract_version(self) -> None:
        schema_path = (
            Path(__file__).resolve().parents[1]
            / "metadata"
            / "independent-review-bundle.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(
            "micrantha.independent-review-bundle/v1",
            schema["properties"]["schema"]["const"],
        )
        self.assertFalse(
            schema["properties"]["constraints"]["properties"]["mutation_tools_allowed"][
                "const"
            ]
        )


if __name__ == "__main__":
    unittest.main()
