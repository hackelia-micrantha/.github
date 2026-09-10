#!/usr/bin/env python3
"""Validate Micrantha source-exposure and repository-distribution posture.

This validator is intentionally incremental: repositories without posture metadata are
accepted while the organization rollout proceeds. Once any primary posture field is
present, the complete primary triple is required and mechanically contradictory
combinations fail closed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SOURCE_EXPOSURES = {"public", "private", "none"}
REPOSITORY_ROLES = {"canonical", "distribution", "projection", "mirror", "internal", "meta"}
DISTRIBUTION_MODES = {"source", "binary", "package", "closure", "internal", "none"}
PRIMARY_FIELDS = {"sourceExposure", "repositoryRole", "distributionMode"}
REFERENCE_FIELDS = {
    "implementationAuthority",
    "releaseAuthority",
    "canonicalRepository",
    "publicDistributionRepository",
}
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def _prefix(index: int, repository: object) -> str:
    if isinstance(repository, str):
        return f"repositories[{index}] ({repository})"
    return f"repositories[{index}]"


def validate_repository_posture(
    item: dict[str, Any],
    *,
    index: int,
    registered: dict[str, dict[str, Any]],
) -> list[str]:
    """Return semantic posture errors for one registry entry."""

    errors: list[str] = []
    repository = item.get("repository")
    prefix = _prefix(index, repository)

    present_primary = PRIMARY_FIELDS.intersection(item)
    if not present_primary:
        # Migration mode: legacy entries remain valid until deliberately classified.
        return errors

    missing_primary = sorted(PRIMARY_FIELDS - item.keys())
    if missing_primary:
        errors.append(
            f"{prefix} posture is partial; missing: {', '.join(missing_primary)}"
        )
        return errors

    source_exposure = item.get("sourceExposure")
    repository_role = item.get("repositoryRole")
    distribution_mode = item.get("distributionMode")
    visibility = item.get("visibility")

    if source_exposure not in SOURCE_EXPOSURES:
        errors.append(
            f"{prefix}.sourceExposure must be one of {sorted(SOURCE_EXPOSURES)}"
        )
    if repository_role not in REPOSITORY_ROLES:
        errors.append(
            f"{prefix}.repositoryRole must be one of {sorted(REPOSITORY_ROLES)}"
        )
    if distribution_mode not in DISTRIBUTION_MODES:
        errors.append(
            f"{prefix}.distributionMode must be one of {sorted(DISTRIBUTION_MODES)}"
        )

    if source_exposure == "public" and visibility in {"private", "internal"}:
        errors.append(
            f"{prefix} declares public source exposure but repository visibility is {visibility}"
        )
    if source_exposure == "private" and visibility == "public":
        errors.append(
            f"{prefix} is public but declares private source exposure; use 'none' for a public artifact-only surface or 'public' for an intentional source projection"
        )
    if distribution_mode == "source" and source_exposure != "public":
        errors.append(
            f"{prefix} distributes source but sourceExposure is {source_exposure!r}"
        )
    if repository_role == "distribution" and distribution_mode == "none":
        errors.append(
            f"{prefix} has repositoryRole 'distribution' but distributionMode 'none'"
        )

    for field in sorted(REFERENCE_FIELDS):
        value = item.get(field)
        if value is None:
            continue
        if not isinstance(value, str) or not REPOSITORY_RE.fullmatch(value):
            errors.append(f"{prefix}.{field} must be an owner/name repository reference or null")
            continue
        target = registered.get(value)
        if target is None:
            errors.append(f"{prefix}.{field} references unregistered repository {value}")
            continue
        if field == "publicDistributionRepository" and target.get("visibility") != "public":
            errors.append(
                f"{prefix}.publicDistributionRepository must reference a public repository: {value}"
            )

    if isinstance(repository, str):
        canonical = item.get("canonicalRepository")
        if repository_role == "canonical" and canonical not in {None, repository}:
            errors.append(
                f"{prefix} is canonical but canonicalRepository points to {canonical}"
            )
        if repository_role in {"distribution", "projection", "mirror"} and canonical == repository:
            errors.append(
                f"{prefix} cannot point canonicalRepository at itself while acting as {repository_role}"
            )
        public_distribution = item.get("publicDistributionRepository")
        if public_distribution == repository:
            errors.append(f"{prefix}.publicDistributionRepository must not point to itself")

    return errors


def validate_registry_posture(data: Any) -> list[str]:
    """Validate posture metadata for every repository in a registry object."""

    if not isinstance(data, dict):
        return ["registry root must be an object"]
    repositories = data.get("repositories")
    if not isinstance(repositories, list):
        return ["repositories must be an array"]

    registered: dict[str, dict[str, Any]] = {}
    for item in repositories:
        if not isinstance(item, dict):
            continue
        repository = item.get("repository")
        if isinstance(repository, str):
            registered[repository] = item

    errors: list[str] = []
    for index, item in enumerate(repositories):
        if not isinstance(item, dict):
            continue
        errors.extend(
            validate_repository_posture(item, index=index, registered=registered)
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "registry",
        nargs="?",
        type=Path,
        default=Path("metadata/repositories.json"),
    )
    args = parser.parse_args()

    try:
        data = json.loads(args.registry.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file does not exist: {args.registry}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(
            f"ERROR: invalid JSON in {args.registry}: line {exc.lineno}, column {exc.colno}: {exc.msg}",
            file=sys.stderr,
        )
        return 2

    errors = validate_registry_posture(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    classified = sum(
        1
        for item in data.get("repositories", [])
        if isinstance(item, dict) and PRIMARY_FIELDS.intersection(item)
    )
    print(
        f"Validated source/distribution posture for {classified} classified repositories; unclassified entries remain permitted during rollout"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
