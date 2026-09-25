"""Tests for deterministic independent-review bundle construction."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from tools.review_bundle import (
    DEFAULT_PROMPT,
    PROMPT_PROFILE,
    build_bundle,
    canonical_bytes,
    main,
    verify_patch_range,
)


class ReviewBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.patch = self.root / "candidate.patch"
        self.patch.write_text("diff --git a/a b/a\n+safe change\n", encoding="utf-8")
        self.verify_patcher = mock.patch("tools.review_bundle.verify_patch_range")
        self.verify_mock = self.verify_patcher.start()
        self.addCleanup(self.verify_patcher.stop)

    def args(self, **overrides: object) -> argparse.Namespace:
        values: dict[str, object] = {
            "repository": "hackelia-micrantha/.github",
            "subject": "pull_request:123",
            "repository_root": self.root,
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
        self.assertEqual(PROMPT_PROFILE, first["review"]["prompt_profile"])
        self.assertEqual(DEFAULT_PROMPT, first["review"]["prompt"])
        self.assertIsNone(first["review"]["prompt_context"])
        self.assertTrue(first["constraints"]["read_only"])
        self.assertFalse(first["constraints"]["mutation_tools_allowed"])
        self.verify_mock.assert_called()

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
        self.assertEqual(DEFAULT_PROMPT, bundle["review"]["prompt"])
        self.assertEqual(PROMPT_PROFILE, bundle["review"]["prompt_profile"])
        self.assertEqual(
            "Focus on schema compatibility.",
            bundle["review"]["prompt_context"],
        )

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

    def test_verifies_patch_against_exact_git_range(self) -> None:
        repo = self.root / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.email", "review@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.name", "Review Fixture"], check=True)
        tracked = repo / "file.txt"
        tracked.write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "file.txt"], check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "base"], check=True)
        base = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
        tracked.write_text("candidate\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "commit", "-q", "-am", "candidate"], check=True)
        head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
        canonical = subprocess.check_output(
            [
                "git", "-C", str(repo), "diff", "--binary", "--full-index",
                "--no-color", "--no-ext-diff", "--no-textconv", "--no-renames",
                "--src-prefix=a/", "--dst-prefix=b/", base, head, "--",
            ]
        )
        exact_patch = self.root / "exact.patch"
        exact_patch.write_bytes(canonical)
        verify_patch_range(repo, base, head, canonical)
        with self.assertRaisesRegex(ValueError, "does not match"):
            verify_patch_range(repo, base, head, canonical + b"\n# stale")

    def test_output_path_cannot_overwrite_patch(self) -> None:
        exit_code = main(
            [
                "--repository", "hackelia-micrantha/.github",
                "--subject", "pull_request:123",
                "--repository-root", str(self.root),
                "--patch-base-sha", "b" * 40,
                "--reviewed-sha", "a" * 40,
                "--patch", str(self.patch),
                "--source-exposure", "public",
                "--scope", "review evidence boundary",
                "--authority-ref", "docs/governance/independent-review.md",
                "--output", str(self.patch),
            ]
        )
        self.assertEqual(2, exit_code)
        self.assertTrue(self.patch.read_text(encoding="utf-8").startswith("diff --git"))

    def test_schema_encodes_subject_transfer_and_prompt_invariants(self) -> None:
        schema_path = (
            Path(__file__).resolve().parents[1]
            / "metadata"
            / "independent-review-bundle.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        subject = schema["properties"]["candidate"]["properties"]["subject"]
        self.assertEqual(["kind", "number"], subject["required"])

        review = schema["properties"]["review"]
        self.assertEqual(PROMPT_PROFILE, review["properties"]["prompt_profile"]["const"])
        self.assertEqual(DEFAULT_PROMPT, review["properties"]["prompt"]["const"])

        transfer = review["properties"]["external_source_transfer"]
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
        self.assertTrue(
            any(
                rule.get("if", {})
                .get("properties", {})
                .get("source_exposure", {})
                .get("const")
                == "public"
                for rule in review["allOf"]
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
