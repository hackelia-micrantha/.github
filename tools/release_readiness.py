#!/usr/bin/env python3
"""Validate normalized release evidence against Micrantha repository posture.

The checker is deliberately repository-neutral. Project-owned release tooling produces a
small evidence document after building/inspecting its real package or artifact; this
module compares that evidence with the organization repository registry. It does not
fetch caller-selected URLs, build packages, sign artifacts, or reinterpret project
package-manager semantics.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from tools import source_posture

SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
PUBLIC_DISTRIBUTION_MODES = {"source", "binary", "package", "closure"}


def _repository_index(registry: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(registry, dict) or not isinstance(registry.get("repositories"), list):
        return {}
    return {
        item["repository"]: item
        for item in registry["repositories"]
        if isinstance(item, dict) and isinstance(item.get("repository"), str)
    }


def _require_bool(container: Any, field: str, expected: bool, errors: list[str], check: str) -> None:
    if not isinstance(container, dict) or container.get(field) is not expected:
        errors.append(f"[{check}] {field} must be {str(expected).lower()}")


def _artifact_by_path(evidence: dict[str, Any]) -> dict[str, dict[str, Any]]:
    artifacts = evidence.get("artifacts")
    if not isinstance(artifacts, list):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for artifact in artifacts:
        if isinstance(artifact, dict) and isinstance(artifact.get("path"), str):
            result[artifact["path"]] = artifact
    return result


def validate_release_evidence(registry: Any, evidence: Any) -> list[str]:
    """Return release-readiness errors for one normalized evidence document."""

    errors: list[str] = []

    posture_errors = source_posture.validate_registry_posture(registry)
    if posture_errors:
        return [f"[registry.posture] {error}" for error in posture_errors]

    if not isinstance(evidence, dict):
        return ["[evidence.shape] release evidence root must be an object"]
    if evidence.get("schemaVersion") != 1:
        errors.append("[evidence.schema] schemaVersion must be 1")

    repository = evidence.get("repository")
    if not isinstance(repository, str):
        errors.append("[evidence.repository] repository must be an owner/name string")
        return errors

    registered = _repository_index(registry)
    posture = registered.get(repository)
    if posture is None:
        errors.append(f"[evidence.repository] repository is not registered: {repository}")
        return errors
    if not source_posture.PRIMARY_FIELDS.issubset(posture):
        errors.append(
            f"[registry.unclassified] repository posture is not classified: {repository}"
        )
        return errors

    distribution_mode = posture.get("distributionMode")
    source_exposure = posture.get("sourceExposure")
    visibility = posture.get("visibility")

    release = evidence.get("release")
    if not isinstance(release, dict):
        errors.append("[release.shape] release must be an object")
        release = {}

    declared_release_authority = posture.get("releaseAuthority")
    if isinstance(declared_release_authority, str):
        if release.get("releaseAuthority") != declared_release_authority:
            errors.append(
                "[release.authority] evidence releaseAuthority must equal registry releaseAuthority "
                f"{declared_release_authority}"
            )

    canonical_identity = release.get("canonicalIdentity")
    if not isinstance(canonical_identity, str) or not canonical_identity:
        errors.append("[release.identity] release.canonicalIdentity must be a non-empty string")
    identity_claims = release.get("identityClaims", {})
    if not isinstance(identity_claims, dict):
        errors.append("[release.identity] release.identityClaims must be an object")
    elif isinstance(canonical_identity, str) and canonical_identity:
        for surface, value in sorted(identity_claims.items()):
            if not isinstance(value, str) or value != canonical_identity:
                errors.append(
                    f"[release.identity] identity claim {surface!r} must equal canonical identity {canonical_identity!r}"
                )

    acquisition = evidence.get("acquisition")
    if not isinstance(acquisition, dict):
        errors.append("[acquisition.shape] acquisition must be an object")
        acquisition = {}

    acquisition_mode = acquisition.get("mode")
    if distribution_mode in PUBLIC_DISTRIBUTION_MODES and acquisition_mode != distribution_mode:
        errors.append(
            f"[acquisition.mode] acquisition mode {acquisition_mode!r} contradicts registry distributionMode {distribution_mode!r}"
        )

    is_public_consumer_surface = visibility == "public" and distribution_mode in PUBLIC_DISTRIBUTION_MODES
    if is_public_consumer_surface:
        _require_bool(
            acquisition,
            "requiresPrivateCredentials",
            False,
            errors,
            "acquisition.credentials",
        )
        _require_bool(acquisition, "immutable", True, errors, "acquisition.immutable")

        clean_consumer = evidence.get("cleanConsumer")
        _require_bool(clean_consumer, "tested", True, errors, "consumer.clean")
        _require_bool(clean_consumer, "cacheMiss", True, errors, "consumer.clean")
        _require_bool(
            clean_consumer,
            "privateCredentialsAvailable",
            False,
            errors,
            "consumer.clean",
        )
        _require_bool(clean_consumer, "passed", True, errors, "consumer.clean")

    if distribution_mode == "binary":
        _require_bool(acquisition, "sourceBuild", False, errors, "binary.no-source-build")
        pins = acquisition.get("cryptographicPins")
        if not isinstance(pins, list) or not pins:
            errors.append("[binary.pin] public binary acquisition requires at least one cryptographic pin")
        elif any(not isinstance(pin, str) or not SHA256_RE.fullmatch(pin) for pin in pins):
            errors.append("[binary.pin] cryptographicPins must contain canonical sha256:<64 lowercase hex> values")
        if source_exposure == "public":
            errors.append(
                "[binary.exposure] binary distribution should not declare public implementation source exposure on the same surface"
            )

    if distribution_mode == "source":
        _require_bool(acquisition, "sourceBuild", True, errors, "source.build")
        if source_exposure != "public":
            errors.append("[source.exposure] source distribution requires public source exposure")

    inspection = evidence.get("inspection")
    if not isinstance(inspection, dict):
        errors.append("[artifact.inspection] inspection must be an object")
        inspection = {}

    for field, check in (
        ("credentialsPresent", "artifact.credentials"),
        ("signingKeysPresent", "artifact.signing-keys"),
        ("privateSecurityCorpusPresent", "artifact.private-security-corpus"),
        ("developmentOnlyMaterialPresent", "artifact.development-only"),
    ):
        _require_bool(inspection, field, False, errors, check)
    if distribution_mode == "binary":
        _require_bool(
            inspection,
            "privateImplementationSourcePresent",
            False,
            errors,
            "binary.private-source",
        )

    cli = evidence.get("cli")
    if cli is not None:
        if not isinstance(cli, dict):
            errors.append("[cli.shape] cli must be an object when present")
        else:
            artifacts = _artifact_by_path(evidence)
            executable_path = cli.get("executablePath")
            man_page_path = cli.get("manPagePath")
            if not isinstance(executable_path, str) or executable_path not in artifacts:
                errors.append("[cli.executable] cli executablePath must reference an inspected artifact")
            elif artifacts[executable_path].get("executable") is not True:
                errors.append("[cli.executable] CLI executable artifact must be executable")
            if not isinstance(man_page_path, str) or man_page_path not in artifacts:
                errors.append("[cli.man] cli manPagePath must reference an inspected artifact")
            elif not man_page_path.startswith("share/man/man1/") or not man_page_path.endswith(".1"):
                errors.append("[cli.man] section-1 man page must use share/man/man1/<name>.1")
            _require_bool(cli, "smokePassed", True, errors, "cli.smoke")
            _require_bool(cli, "operatorDocsPresent", True, errors, "cli.docs")

    return errors


def _read_json(path: Path, label: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: {label} does not exist: {path}", file=sys.stderr)
        raise SystemExit(2) from None
    except json.JSONDecodeError as exc:
        print(
            f"ERROR: invalid JSON in {label} {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}",
            file=sys.stderr,
        )
        raise SystemExit(2) from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path, help="normalized release-readiness evidence JSON")
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("metadata/repositories.json"),
        help="organization repository registry",
    )
    args = parser.parse_args()

    registry = _read_json(args.registry, "registry")
    evidence = _read_json(args.evidence, "release evidence")
    errors = validate_release_evidence(registry, evidence)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Release readiness evidence matches declared posture for {evidence['repository']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
