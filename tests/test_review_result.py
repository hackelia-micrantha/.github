"""Tests for independent-review result validation."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from tools.review_bundle import build_bundle
from tools.review_result import (
    RESULT_SCHEMA,
    load_strict_json,
    validate_result,
)


class ReviewResultTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.patch = self.root / "candidate.patch"
        self.patch.write_text("diff --git a/a b/a\n+candidate\n", encoding="utf-8")

    def bundle(self, *, source_exposure: str = "public") -> dict:
        args = argparse.Namespace(
            repository="hackelia-micrantha/.github",
            subject="pull_request:129",
            patch_base_sha="a" * 40,
            reviewed_sha="b" * 40,
            patch=self.patch,
            patch_ref="https://example.invalid/immutable/b.patch",
            scope=["security boundary", "evidence contract"],
            authority_ref=["docs/governance/independent-review.md"],
            acceptance_ref=["issue:123"],
            validation_ref=["Meta validation: success"],
            source_exposure=source_exposure,
            external_transfer_authorization_ref=None,
            prompt_context_file=None,
            output=None,
        )
        return build_bundle(args)

    def result(
        self,
        bundle: dict,
        *,
        state: str = "clean",
        execution_location: str = "local",
        findings: list[dict] | None = None,
        blocked_reasons: list[str] | None = None,
    ) -> dict:
        return {
            "schema": RESULT_SCHEMA,
            "review_bundle_sha256": bundle["bundle_sha256"],
            "reviewed_sha": bundle["candidate"]["reviewed_sha"],
            "review_prompt_sha256": hashlib.sha256(
                bundle["review"]["prompt"].encode("utf-8")
            ).hexdigest(),
            "reviewer": {
                "kind": "local-model",
                "identity": "anthesis-verifier:test",
                "provider": "dubnium-local",
                "model": "reviewer-fixture",
                "execution_location": execution_location,
                "independence_basis": "fresh read-only verifier fixture",
                "non_author": True,
                "separate_review_context": True,
                "repository_write_credentials_available": False,
                "mutation_tools_available": False,
            },
            "scope": list(bundle["review"]["scope"]),
            "result": state,
            "findings": [] if findings is None else findings,
            "blocked_reasons": [] if blocked_reasons is None else blocked_reasons,
            "limitations": [],
        }

    def finding(self) -> dict:
        return {
            "id": "R1",
            "severity": "medium",
            "title": "Example finding",
            "description": "A bounded reviewer finding.",
            "evidence_refs": ["candidate.patch:L1-L2"],
        }

    def test_clean_result_is_exactly_bound_to_bundle(self) -> None:
        bundle = self.bundle()
        result = self.result(bundle)
        self.assertEqual([], validate_result(bundle, result))

    def test_findings_result_requires_findings(self) -> None:
        bundle = self.bundle()
        valid = self.result(bundle, state="findings", findings=[self.finding()])
        self.assertEqual([], validate_result(bundle, valid))

        invalid = self.result(bundle, state="findings")
        errors = validate_result(bundle, invalid)
        self.assertIn("findings result must contain at least one finding", errors)

    def test_blocked_result_requires_reason_but_may_preserve_partial_findings(self) -> None:
        bundle = self.bundle()
        valid = self.result(
            bundle,
            state="blocked",
            findings=[self.finding()],
            blocked_reasons=["reviewer timeout after partial analysis"],
        )
        self.assertEqual([], validate_result(bundle, valid))

        invalid = self.result(bundle, state="blocked")
        self.assertIn(
            "blocked result must contain at least one blocked reason",
            validate_result(bundle, invalid),
        )

    def test_clean_result_cannot_hide_findings_or_blocked_state(self) -> None:
        bundle = self.bundle()
        result = self.result(
            bundle,
            findings=[self.finding()],
            blocked_reasons=["quota exhausted"],
        )
        errors = validate_result(bundle, result)
        self.assertIn("clean review cannot contain findings", errors)
        self.assertIn("clean review cannot contain blocked_reasons", errors)

    def test_rejects_stale_or_mismatched_evidence_binding(self) -> None:
        bundle = self.bundle()
        cases = [
            ("review_bundle_sha256", "c" * 64, "not bound to this review bundle"),
            ("reviewed_sha", "c" * 40, "reviewed_sha does not match"),
            ("review_prompt_sha256", "c" * 64, "prompt digest does not match"),
        ]
        for field, value, expected in cases:
            with self.subTest(field=field):
                result = self.result(bundle)
                result[field] = value
                self.assertTrue(
                    any(expected in error for error in validate_result(bundle, result))
                )

    def test_rejects_bundle_tampering(self) -> None:
        bundle = self.bundle()
        result = self.result(bundle)
        bundle["review"]["scope"].append("tampered")
        errors = validate_result(bundle, result)
        self.assertIn(
            "bundle_sha256 does not match canonical bundle content",
            errors,
        )

    def test_private_source_with_prohibited_transfer_requires_local_execution(self) -> None:
        bundle = self.bundle(source_exposure="private")
        local = self.result(bundle, execution_location="local")
        self.assertEqual([], validate_result(bundle, local))

        external = self.result(bundle, execution_location="external")
        self.assertIn(
            "private/restricted source with prohibited external transfer requires local execution",
            validate_result(bundle, external),
        )

        unknown = self.result(bundle, execution_location="unknown")
        self.assertIn(
            "private/restricted source with prohibited external transfer requires local execution",
            validate_result(bundle, unknown),
        )

    def test_rejects_author_or_mutation_capable_review_context(self) -> None:
        bundle = self.bundle()
        result = self.result(bundle)
        result["reviewer"]["non_author"] = False
        result["reviewer"]["repository_write_credentials_available"] = True
        result["reviewer"]["mutation_tools_available"] = True
        errors = validate_result(bundle, result)
        self.assertIn("reviewer must attest non_author=true", errors)
        self.assertIn(
            "review context must not have repository write credentials",
            errors,
        )
        self.assertIn("review context must not have mutation tools", errors)

    def test_rejects_unknown_top_level_fields_and_duplicate_finding_ids(self) -> None:
        bundle = self.bundle()
        result = self.result(
            bundle,
            state="findings",
            findings=[self.finding(), self.finding()],
        )
        result["unexpected"] = True
        errors = validate_result(bundle, result)
        self.assertTrue(any("unexpected fields" in error for error in errors))
        self.assertIn("finding ids must be unique", errors)

    def test_scope_must_cover_exact_bundle_scope(self) -> None:
        bundle = self.bundle()
        result = self.result(bundle)
        result["scope"] = ["security boundary"]
        self.assertIn(
            "review result scope does not exactly match the bundle scope",
            validate_result(bundle, result),
        )

    def test_strict_json_loader_rejects_nonstandard_constants(self) -> None:
        path = self.root / "result.json"
        path.write_text('{"value": NaN}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "nonstandard JSON constant"):
            load_strict_json(path)

    def test_result_schema_matches_contract_identifier(self) -> None:
        schema_path = (
            Path(__file__).resolve().parents[1]
            / "metadata"
            / "independent-review-result.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(
            RESULT_SCHEMA,
            schema["properties"]["schema"]["const"],
        )
        reviewer = schema["properties"]["reviewer"]["properties"]
        self.assertTrue(reviewer["non_author"]["const"])
        self.assertFalse(reviewer["mutation_tools_available"]["const"])


if __name__ == "__main__":
    unittest.main()
