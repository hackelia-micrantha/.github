#!/usr/bin/env python3
"""Validate a reviewer result against an exact independent-review bundle.

This tool validates evidence linkage and fail-closed result semantics. It does
not prove reviewer independence, authorize external source transfer, accept
findings, merge, release, deploy, or mutate a repository.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

from tools.review_bundle import canonical_bytes, reject_json_constant

BUNDLE_SCHEMA = "micrantha.independent-review-bundle/v1"
RESULT_SCHEMA = "micrantha.independent-review-result/v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def load_strict_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=reject_json_constant,
    )
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def bundle_digest(bundle: dict[str, Any]) -> str:
    claimed = bundle.get("bundle_sha256")
    if not isinstance(claimed, str) or not SHA256.fullmatch(claimed):
        raise ValueError("bundle_sha256 is missing or invalid")
    unsigned = dict(bundle)
    unsigned.pop("bundle_sha256", None)
    actual = hashlib.sha256(canonical_bytes(unsigned)).hexdigest()
    if actual != claimed:
        raise ValueError("bundle_sha256 does not match canonical bundle content")
    return actual


def prompt_digest(bundle: dict[str, Any]) -> str:
    review = bundle.get("review")
    if not isinstance(review, dict):
        raise ValueError("bundle review object is missing")
    prompt = review.get("prompt")
    if not isinstance(prompt, str) or not prompt:
        raise ValueError("bundle review prompt is missing")
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def candidate_sha(bundle: dict[str, Any]) -> str:
    candidate = bundle.get("candidate")
    if not isinstance(candidate, dict):
        raise ValueError("bundle candidate object is missing")
    value = candidate.get("reviewed_sha")
    if not isinstance(value, str) or not SHA40.fullmatch(value):
        raise ValueError("bundle reviewed_sha is missing or invalid")
    return value


def bundle_scope(bundle: dict[str, Any]) -> list[str]:
    review = bundle.get("review")
    if not isinstance(review, dict):
        raise ValueError("bundle review object is missing")
    scope = review.get("scope")
    if (
        not isinstance(scope, list)
        or not scope
        or not all(isinstance(item, str) and item for item in scope)
    ):
        raise ValueError("bundle review scope is missing or invalid")
    if len(scope) != len(set(scope)):
        raise ValueError("bundle review scope contains duplicates")
    return scope


def transfer_state(bundle: dict[str, Any]) -> str:
    review = bundle.get("review")
    if not isinstance(review, dict):
        raise ValueError("bundle review object is missing")
    transfer = review.get("external_source_transfer")
    if not isinstance(transfer, dict):
        raise ValueError("bundle external_source_transfer is missing")
    state = transfer.get("state")
    if state not in {"public-source", "prohibited", "explicitly-authorized"}:
        raise ValueError("bundle external source-transfer state is invalid")
    return state


def validate_finding(value: Any, index: int, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"findings[{index}] must be an object")
        return
    expected = {"id", "severity", "title", "description", "evidence_refs"}
    extra = set(value) - expected
    missing = expected - set(value)
    if extra:
        errors.append(f"findings[{index}] has unexpected fields: {sorted(extra)}")
    if missing:
        errors.append(f"findings[{index}] is missing fields: {sorted(missing)}")

    for key in ("id", "title", "description"):
        item = value.get(key)
        if not isinstance(item, str) or not item.strip():
            errors.append(f"findings[{index}].{key} must be a nonempty string")

    if value.get("severity") not in {"critical", "high", "medium", "low", "info"}:
        errors.append(f"findings[{index}].severity is invalid")

    refs = value.get("evidence_refs")
    if not isinstance(refs, list) or not all(
        isinstance(item, str) and item.strip() for item in refs
    ):
        errors.append(f"findings[{index}].evidence_refs must be an array of nonempty strings")
    elif len(refs) != len(set(refs)):
        errors.append(f"findings[{index}].evidence_refs contains duplicates")


def validate_result(bundle: dict[str, Any], result: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    try:
        if bundle.get("schema") != BUNDLE_SCHEMA:
            errors.append("unsupported review bundle schema")
        expected_bundle_digest = bundle_digest(bundle)
        expected_sha = candidate_sha(bundle)
        expected_prompt_digest = prompt_digest(bundle)
        expected_scope = bundle_scope(bundle)
        source_transfer_state = transfer_state(bundle)
    except ValueError as exc:
        return [str(exc)]

    if result.get("schema") != RESULT_SCHEMA:
        errors.append("unsupported review result schema")

    if result.get("review_bundle_sha256") != expected_bundle_digest:
        errors.append("review result is not bound to this review bundle")

    if result.get("reviewed_sha") != expected_sha:
        errors.append("review result reviewed_sha does not match the bundle candidate")

    if result.get("review_prompt_sha256") != expected_prompt_digest:
        errors.append("review result prompt digest does not match the bundle prompt")

    scope = result.get("scope")
    if not isinstance(scope, list) or not all(
        isinstance(item, str) and item.strip() for item in scope
    ):
        errors.append("review result scope must be a nonempty array of strings")
    elif sorted(scope) != sorted(expected_scope):
        errors.append("review result scope does not exactly match the bundle scope")

    reviewer = result.get("reviewer")
    if not isinstance(reviewer, dict):
        errors.append("reviewer must be an object")
        reviewer = {}

    expected_reviewer_fields = {
        "kind",
        "identity",
        "provider",
        "model",
        "execution_location",
        "independence_basis",
        "non_author",
        "separate_review_context",
        "repository_write_credentials_available",
        "mutation_tools_available",
    }
    missing_reviewer = expected_reviewer_fields - set(reviewer)
    extra_reviewer = set(reviewer) - expected_reviewer_fields
    if missing_reviewer:
        errors.append(f"reviewer is missing fields: {sorted(missing_reviewer)}")
    if extra_reviewer:
        errors.append(f"reviewer has unexpected fields: {sorted(extra_reviewer)}")

    if reviewer.get("kind") not in {
        "human",
        "automated-service",
        "external-model",
        "local-model",
    }:
        errors.append("reviewer kind is invalid")

    for key in ("identity", "independence_basis"):
        value = reviewer.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"reviewer {key} must be a nonempty string")

    for key in ("provider", "model"):
        value = reviewer.get(key)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            errors.append(f"reviewer {key} must be null or a nonempty string")

    location = reviewer.get("execution_location")
    if location not in {"local", "external", "unknown"}:
        errors.append("reviewer execution_location is invalid")

    if reviewer.get("non_author") is not True:
        errors.append("reviewer must attest non_author=true")
    if reviewer.get("separate_review_context") is not True:
        errors.append("reviewer must attest separate_review_context=true")
    if reviewer.get("repository_write_credentials_available") is not False:
        errors.append("review context must not have repository write credentials")
    if reviewer.get("mutation_tools_available") is not False:
        errors.append("review context must not have mutation tools")

    if source_transfer_state == "prohibited" and location != "local":
        errors.append(
            "private/restricted source with prohibited external transfer requires local execution"
        )

    findings = result.get("findings")
    if not isinstance(findings, list):
        errors.append("findings must be an array")
        findings = []
    else:
        for index, finding in enumerate(findings):
            validate_finding(finding, index, errors)

    blocked_reasons = result.get("blocked_reasons")
    if not isinstance(blocked_reasons, list) or not all(
        isinstance(item, str) and item.strip() for item in blocked_reasons
    ):
        errors.append("blocked_reasons must be an array of nonempty strings")
        blocked_reasons = []
    elif len(blocked_reasons) != len(set(blocked_reasons)):
        errors.append("blocked_reasons contains duplicates")

    limitations = result.get("limitations")
    if not isinstance(limitations, list) or not all(
        isinstance(item, str) and item.strip() for item in limitations
    ):
        errors.append("limitations must be an array of nonempty strings")
    elif len(limitations) != len(set(limitations)):
        errors.append("limitations contains duplicates")

    state = result.get("result")
    if state not in {"clean", "findings", "blocked"}:
        errors.append("review result state is invalid")
    elif state == "clean":
        if findings:
            errors.append("clean review cannot contain findings")
        if blocked_reasons:
            errors.append("clean review cannot contain blocked_reasons")
    elif state == "findings":
        if not findings:
            errors.append("findings result must contain at least one finding")
        if blocked_reasons:
            errors.append("findings result cannot contain blocked_reasons")
    elif state == "blocked" and not blocked_reasons:
        errors.append("blocked result must contain at least one blocked reason")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("result", type=Path)
    args = parser.parse_args(argv)

    try:
        bundle = load_strict_json(args.bundle)
        result = load_strict_json(args.result)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"passed": False, "errors": [str(exc)]}, sort_keys=True))
        return 2

    errors = validate_result(bundle, result)
    report = {"passed": not errors, "errors": errors}
    print(json.dumps(report, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
