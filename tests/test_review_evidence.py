"""Tests for durable independent-review evidence disposition."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import tempfile
import unittest

from tools.review_bundle import build_bundle
from tools.review_evidence import EVIDENCE_SCHEMA, canonical_digest, validate_evidence
from tools.review_result import RESULT_SCHEMA


class ReviewEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.patch = self.root / "candidate.patch"
        self.patch.write_text("diff --git a/a b/a\n+candidate\n", encoding="utf-8")

    def bundle(self) -> dict:
        return build_bundle(
            argparse.Namespace(
                repository="hackelia-micrantha/.github",
                subject="pull_request:130",
                patch_base_sha="a" * 40,
            reviewed_sha="c" * 40,
                patch=self.patch,
                patch_ref="https://example.invalid/immutable/c.patch",
                scope=["governance boundary"],
                authority_ref=["docs/governance/independent-review.md"],
                acceptance_ref=["issue:123"],
                validation_ref=["Meta validation: success"],
                source_exposure="public",
                external_transfer_authorization_ref=None,
                prompt_context_file=None,
                output=None,
            )
        )

    def result(self, bundle: dict, *, state: str = "clean", findings=None) -> dict:
        return {
            "schema": RESULT_SCHEMA,
            "review_bundle_sha256": bundle["bundle_sha256"],
            "reviewed_sha": bundle["candidate"]["reviewed_sha"],
            "review_prompt_sha256": hashlib.sha256(
                bundle["review"]["prompt"].encode("utf-8")
            ).hexdigest(),
            "reviewer": {
                "kind": "human",
                "identity": "reviewer@example",
                "provider": None,
                "model": None,
                "execution_location": "local",
                "independence_basis": "independent non-author review",
                "non_author": True,
                "separate_review_context": True,
                "repository_write_credentials_available": False,
                "mutation_tools_available": False,
            },
            "scope": list(bundle["review"]["scope"]),
            "result": state,
            "findings": [] if findings is None else findings,
            "blocked_reasons": ["review unavailable"] if state == "blocked" else [],
            "limitations": [],
        }

    def finding(self, finding_id: str = "R1") -> dict:
        return {
            "id": finding_id,
            "severity": "medium",
            "title": "Review finding",
            "description": "A material finding.",
            "evidence_refs": ["candidate.patch:L1-L2"],
        }

    def evidence(self, bundle: dict, result: dict, *, dispositions=None, state="complete") -> dict:
        reviewer = result["reviewer"]
        return {
            "schema": EVIDENCE_SCHEMA,
            "review_bundle_sha256": bundle["bundle_sha256"],
            "review_result_sha256": canonical_digest(result),
            "reviewed_sha": result["reviewed_sha"],
            "review_prompt_sha256": result["review_prompt_sha256"],
            "reviewer": {
                key: reviewer[key]
                for key in ("kind", "identity", "provider", "model", "independence_basis")
            },
            "scope": list(result["scope"]),
            "result": result["result"],
            "finding_dispositions": [] if dispositions is None else dispositions,
            "accountable_owner": "ryjen",
            "disposition_state": state,
            "evidence_ref": "pr-comment:12345",
            "notes": [],
            "constraints": {
                "evidence_not_authority": True,
                "merge_authorized": False,
                "release_authorized": False,
                "mutation_authorized": False,
            },
        }

    def test_clean_review_can_complete_without_findings(self) -> None:
        bundle = self.bundle()
        result = self.result(bundle)
        evidence = self.evidence(bundle, result)
        self.assertEqual([], validate_evidence(bundle, result, evidence))

    def test_findings_require_exact_accountable_disposition(self) -> None:
        bundle = self.bundle()
        result = self.result(bundle, state="findings", findings=[self.finding()])
        resolved = self.evidence(
            bundle,
            result,
            dispositions=[
                {
                    "finding_id": "R1",
                    "state": "resolved",
                    "reference": "commit:deadbeef",
                }
            ],
        )
        self.assertEqual([], validate_evidence(bundle, result, resolved))

        missing = self.evidence(bundle, result)
        self.assertIn(
            "finding dispositions must cover exactly the review result findings",
            validate_evidence(bundle, result, missing),
        )

    def test_accepted_finding_requires_reference(self) -> None:
        bundle = self.bundle()
        result = self.result(bundle, state="findings", findings=[self.finding()])
        evidence = self.evidence(
            bundle,
            result,
            dispositions=[
                {"finding_id": "R1", "state": "accepted", "reference": None}
            ],
        )
        self.assertTrue(
            any(
                "accepted state requires a reference" in error
                for error in validate_evidence(bundle, result, evidence)
            )
        )

    def test_blocked_finding_forces_blocked_disposition(self) -> None:
        bundle = self.bundle()
        result = self.result(bundle, state="findings", findings=[self.finding()])
        evidence = self.evidence(
            bundle,
            result,
            dispositions=[
                {"finding_id": "R1", "state": "blocked", "reference": None}
            ],
            state="complete",
        )
        self.assertIn(
            "findings disposition_state must be blocked for its finding dispositions",
            validate_evidence(bundle, result, evidence),
        )

    def test_blocked_review_result_cannot_be_dispositioned_complete(self) -> None:
        bundle = self.bundle()
        result = self.result(bundle, state="blocked")
        evidence = self.evidence(bundle, result, state="complete")
        self.assertIn(
            "blocked review result cannot have complete disposition",
            validate_evidence(bundle, result, evidence),
        )

    def test_evidence_must_bind_exact_result_digest(self) -> None:
        bundle = self.bundle()
        result = self.result(bundle)
        evidence = self.evidence(bundle, result)
        evidence["review_result_sha256"] = "d" * 64
        self.assertIn(
            "review evidence is not bound to this review result",
            validate_evidence(bundle, result, evidence),
        )

    def test_reviewer_summary_must_match_result(self) -> None:
        bundle = self.bundle()
        result = self.result(bundle)
        evidence = self.evidence(bundle, result)
        evidence["reviewer"]["identity"] = "other-reviewer"
        self.assertIn(
            "review evidence reviewer summary does not match review result",
            validate_evidence(bundle, result, evidence),
        )

    def test_authority_flags_cannot_be_promoted_by_evidence_record(self) -> None:
        bundle = self.bundle()
        result = self.result(bundle)
        evidence = self.evidence(bundle, result)
        evidence["constraints"]["merge_authorized"] = True
        self.assertIn(
            "review evidence authority constraints are invalid",
            validate_evidence(bundle, result, evidence),
        )


if __name__ == "__main__":
    unittest.main()
