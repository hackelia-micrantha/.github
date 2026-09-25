#!/usr/bin/env python3
"""Validate durable independent-review evidence and finding disposition.

This tool binds an accountable disposition record to an exact validated review
bundle/result pair. It does not grant merge, release, deployment, environment
approval, or mutation authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from tools.review_bundle import canonical_bytes
from tools.review_result import load_strict_json, validate_result

EVIDENCE_SCHEMA = "micrantha.independent-review-evidence/v1"


def canonical_digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def validate_evidence(
    bundle: dict[str, Any],
    result: dict[str, Any],
    evidence: dict[str, Any],
) -> list[str]:
    errors = validate_result(bundle, result)
    if errors:
        return [f"review result invalid: {error}" for error in errors]

    expected_top_level = {
        "schema",
        "review_bundle_sha256",
        "review_result_sha256",
        "reviewed_sha",
        "review_prompt_sha256",
        "reviewer",
        "scope",
        "result",
        "finding_dispositions",
        "accountable_owner",
        "disposition_state",
        "evidence_ref",
        "notes",
        "constraints",
    }
    missing = expected_top_level - set(evidence)
    extra = set(evidence) - expected_top_level
    if missing:
        errors.append(f"review evidence is missing fields: {sorted(missing)}")
    if extra:
        errors.append(f"review evidence has unexpected fields: {sorted(extra)}")

    if evidence.get("schema") != EVIDENCE_SCHEMA:
        errors.append("unsupported review evidence schema")

    if evidence.get("review_bundle_sha256") != bundle["bundle_sha256"]:
        errors.append("review evidence is not bound to this review bundle")

    expected_result_digest = canonical_digest(result)
    if evidence.get("review_result_sha256") != expected_result_digest:
        errors.append("review evidence is not bound to this review result")

    if evidence.get("reviewed_sha") != result["reviewed_sha"]:
        errors.append("review evidence reviewed_sha does not match review result")

    if evidence.get("review_prompt_sha256") != result["review_prompt_sha256"]:
        errors.append("review evidence prompt digest does not match review result")

    if evidence.get("scope") != result["scope"]:
        errors.append("review evidence scope does not match review result")

    if evidence.get("result") != result["result"]:
        errors.append("review evidence result state does not match review result")

    expected_reviewer = {
        key: result["reviewer"][key]
        for key in ("kind", "identity", "provider", "model", "independence_basis")
    }
    if evidence.get("reviewer") != expected_reviewer:
        errors.append("review evidence reviewer summary does not match review result")

    owner = evidence.get("accountable_owner")
    if not isinstance(owner, str) or not owner.strip():
        errors.append("accountable_owner must be a nonempty string")

    evidence_ref = evidence.get("evidence_ref")
    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
        errors.append("evidence_ref must be a nonempty string")

    notes = evidence.get("notes")
    if not isinstance(notes, list) or not all(
        isinstance(item, str) and item.strip() for item in notes
    ):
        errors.append("notes must be an array of nonempty strings")
    elif len(notes) != len(set(notes)):
        errors.append("notes contains duplicates")

    constraints = evidence.get("constraints")
    expected_constraints = {
        "evidence_not_authority": True,
        "merge_authorized": False,
        "release_authorized": False,
        "mutation_authorized": False,
    }
    if constraints != expected_constraints:
        errors.append("review evidence authority constraints are invalid")

    dispositions = evidence.get("finding_dispositions")
    if not isinstance(dispositions, list):
        errors.append("finding_dispositions must be an array")
        dispositions = []

    expected_finding_ids = [
        finding["id"]
        for finding in result["findings"]
        if isinstance(finding, dict) and isinstance(finding.get("id"), str)
    ]
    seen_ids: list[str] = []
    blocked_disposition = False

    for index, disposition in enumerate(dispositions):
        if not isinstance(disposition, dict):
            errors.append(f"finding_dispositions[{index}] must be an object")
            continue
        expected_fields = {"finding_id", "state", "reference"}
        missing_fields = expected_fields - set(disposition)
        extra_fields = set(disposition) - expected_fields
        if missing_fields:
            errors.append(
                f"finding_dispositions[{index}] is missing fields: {sorted(missing_fields)}"
            )
        if extra_fields:
            errors.append(
                f"finding_dispositions[{index}] has unexpected fields: {sorted(extra_fields)}"
            )

        finding_id = disposition.get("finding_id")
        if not isinstance(finding_id, str) or not finding_id.strip():
            errors.append(
                f"finding_dispositions[{index}].finding_id must be a nonempty string"
            )
        else:
            seen_ids.append(finding_id)

        state = disposition.get("state")
        if state not in {"resolved", "accepted", "blocked"}:
            errors.append(f"finding_dispositions[{index}].state is invalid")
        if state == "blocked":
            blocked_disposition = True

        reference = disposition.get("reference")
        if reference is not None and (
            not isinstance(reference, str) or not reference.strip()
        ):
            errors.append(
                f"finding_dispositions[{index}].reference must be null or a nonempty string"
            )
        if state in {"resolved", "accepted"} and not (
            isinstance(reference, str) and reference.strip()
        ):
            errors.append(
                f"finding_dispositions[{index}] {state} state requires a reference"
            )

    if len(seen_ids) != len(set(seen_ids)):
        errors.append("finding disposition ids must be unique")

    if sorted(seen_ids) != sorted(expected_finding_ids):
        errors.append("finding dispositions must cover exactly the review result findings")

    disposition_state = evidence.get("disposition_state")
    if disposition_state not in {"complete", "blocked"}:
        errors.append("disposition_state is invalid")
    elif result["result"] == "clean":
        if dispositions:
            errors.append("clean review evidence cannot contain finding dispositions")
        if disposition_state != "complete":
            errors.append("clean review evidence must be complete")
    elif result["result"] == "blocked":
        if disposition_state != "blocked":
            errors.append("blocked review result cannot have complete disposition")
    elif result["result"] == "findings":
        expected_state = "blocked" if blocked_disposition else "complete"
        if disposition_state != expected_state:
            errors.append(
                f"findings disposition_state must be {expected_state} for its finding dispositions"
            )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("result", type=Path)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args(argv)

    try:
        bundle = load_strict_json(args.bundle)
        result = load_strict_json(args.result)
        evidence = load_strict_json(args.evidence)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"passed": False, "errors": [str(exc)]}, sort_keys=True))
        return 2

    errors = validate_evidence(bundle, result, evidence)
    print(json.dumps({"passed": not errors, "errors": errors}, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
