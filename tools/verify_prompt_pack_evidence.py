#!/usr/bin/env python3
"""Verify generated Invokrum prompt-pack evidence against committed goldens."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify(golden_path: Path, evidence_root: Path) -> list[str]:
    golden = load_json(golden_path)
    errors: list[str] = []

    if golden.get("format") != "micrantha.prompt-pack-golden/v1":
        return ["unsupported golden fixture format"]

    profiles = golden.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        return ["golden fixture contains no profiles"]

    actual_profiles = {path.name for path in evidence_root.iterdir() if path.is_dir()}
    expected_profiles = set(profiles)
    if actual_profiles != expected_profiles:
        errors.append(
            f"profile set mismatch: expected {sorted(expected_profiles)}, "
            f"got {sorted(actual_profiles)}"
        )

    for profile in sorted(expected_profiles):
        expected = profiles[profile]
        profile_dir = evidence_root / profile
        if not profile_dir.is_dir():
            continue

        context_path = profile_dir / "context.md"
        inspect_path = profile_dir / "inspect.json"
        lock_path = profile_dir / "invokrum.lock"
        verify_path = profile_dir / "verify.json"
        required = (context_path, inspect_path, lock_path, verify_path)

        missing = [path.name for path in required if not path.is_file()]
        if missing:
            errors.append(f"{profile}: missing evidence files {missing}")
            continue

        context_digest = sha256(context_path)
        if context_digest != expected.get("context_sha256"):
            errors.append(
                f"{profile}: context digest drift: expected "
                f"{expected.get('context_sha256')}, got {context_digest}"
            )

        if load_json(inspect_path) != expected.get("inspect"):
            errors.append(f"{profile}: inspect evidence drift")

        actual_lock = load_json(lock_path)
        if actual_lock != expected.get("lock"):
            errors.append(f"{profile}: lock evidence drift")

        lock_output_digest = (
            actual_lock.get("manifest", {}).get("output", {}).get("digest")
            if isinstance(actual_lock, dict)
            else None
        )
        if lock_output_digest != context_digest:
            errors.append(f"{profile}: lock output digest does not bind rendered context")

        verification = load_json(verify_path)
        if verification.get("verified") is not True:
            errors.append(f"{profile}: Invokrum verification did not report verified=true")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("golden", type=Path)
    parser.add_argument("evidence_root", type=Path)
    args = parser.parse_args()

    errors = verify(args.golden, args.evidence_root)
    if errors:
        for error in errors:
            print(error)
        return 1

    print("Micrantha prompt-pack evidence matches committed goldens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
