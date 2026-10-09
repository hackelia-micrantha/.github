#!/usr/bin/env python3
"""Exercise exact digest-pinned, offline installed-root composition for Micrantha."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ENTRY_POINT = "micrantha-prompt-pack.yaml"
SOURCES = (
    ENTRY_POINT,
    "docs/prompts/README.md",
    "docs/prompts/overlays/cross-project-execution.md",
    "docs/prompts/planning/classify-and-route.md",
    "docs/prompts/issues/issue-grooming.md",
    "docs/prompts/reviews/engineering-artifact-review.md",
)
PROFILES = ("classify-and-route", "issue-grooming", "engineering-artifact-review")


def make_candidate(source_root: Path, candidate_root: Path) -> tuple[bytes, str]:
    records = []
    for path in sorted(SOURCES):
        src = source_root / path
        if src.is_symlink() or any(part.is_symlink() for part in src.parents if part != source_root.parent):
            raise ValueError(f"refusing linked source: {path}")
        if not src.is_file():
            raise ValueError(f"missing regular source: {path}")
        payload = src.read_bytes()
        dest = candidate_root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(payload)
        records.append({
            "path": path,
            "byte_length": len(payload),
            "digest": hashlib.sha256(payload).hexdigest(),
        })
    manifest = {
        "format": "invokrum.pack-bundle/v1",
        "digest_algorithm": "sha256",
        "entry_point": ENTRY_POINT,
        "files": records,
    }
    canonical = json.dumps(manifest, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return canonical, hashlib.sha256(canonical).hexdigest()


def invoke(invokrum: Path, *args: str, success: bool = True) -> subprocess.CompletedProcess[bytes]:
    process = subprocess.run([str(invokrum), *args], capture_output=True, check=False)
    if success and process.returncode != 0:
        raise RuntimeError(f"Invokrum failed: {list(args)}; {process.stderr.decode(errors='replace')}")
    return process


def prove(invokrum: Path, source_root: Path) -> dict:
    with tempfile.TemporaryDirectory(prefix="micrantha-installed-proof-") as tmp:
        scratch = Path(tmp)
        candidate = scratch / "candidate"
        canonical, digest = make_candidate(source_root, candidate)
        manifest = scratch / "bundle-manifest.json"
        manifest.write_bytes(canonical)
        subject = f"sha256:{digest}"
        store = scratch / "store"
        install_args = (
            "install", str(candidate), "--candidate-format", "directory",
            "--bundle-manifest", str(manifest), "--subject", subject,
            "--store", str(store), "--format", "json",
        )
        first = json.loads(invoke(invokrum, *install_args).stdout)
        second = json.loads(invoke(invokrum, *install_args).stdout)
        if not (
            first.get("format") == second.get("format") == "invokrum.cli/v1"
            and first.get("command") == second.get("command") == "install"
            and first.get("installation_format") == second.get("installation_format") == "invokrum.installation/v1"
            and first.get("publisher_authentication") == second.get("publisher_authentication") == "not-provided"
            and first.get("subject") == second.get("subject") == subject
            and first.get("root") == second.get("root")
            and first.get("reused") is False and second.get("reused") is True
        ):
            raise RuntimeError("installed subject, reuse, or digest-only identity mismatch")

        installed_root = Path(first["root"])
        if not installed_root.is_dir() or not installed_root.is_relative_to(store.resolve()):
            raise RuntimeError("installer returned a root outside the selected private store")

        outputs = {}
        for profile in PROFILES:
            original = invoke(invokrum, "compose", "--pack", str(source_root / ENTRY_POINT), "--profile", profile).stdout
            resolved = invoke(invokrum, "compose", "--pack", str(installed_root / ENTRY_POINT), "--profile", profile).stdout
            if original != resolved:
                raise RuntimeError(f"installed composition bytes differ for {profile}")
            lock_path = scratch / f"{profile}.lock"
            lock_path.write_bytes(invoke(invokrum, "lock", "--pack", str(installed_root / ENTRY_POINT), "--profile", profile).stdout)
            verified = json.loads(invoke(
                invokrum, "verify", "--lock", str(lock_path),
                "--pack", str(installed_root / ENTRY_POINT),
                "--profile", profile, "--format", "json",
            ).stdout)
            if verified.get("verified") is not True:
                raise RuntimeError(f"installed lock verification failed for {profile}")
            outputs[profile] = hashlib.sha256(resolved).hexdigest()

        changed = scratch / "changed"
        shutil.copytree(candidate, changed)
        with (changed / "docs/prompts/issues/issue-grooming.md").open("ab") as stream:
            stream.write(b"\n<!-- intentional bundle mutation -->\n")
        tampered_args = list(install_args)
        tampered_args[1] = str(changed)
        if invoke(invokrum, *tampered_args, success=False).returncode == 0:
            raise RuntimeError("modified candidate passed original subject/manifest verification")

        # Installation verification must remain valid after a rejected candidate.
        control = invoke(
            invokrum, "compose", "--pack", str(installed_root / ENTRY_POINT),
            "--profile", "issue-grooming",
        ).stdout
        if hashlib.sha256(control).hexdigest() != outputs["issue-grooming"]:
            raise RuntimeError("rejected candidate affected installed content")

        return {
            "format": "micrantha.installed-prompt-pack-proof/v1",
            "subject": subject,
            "mode": "digest-pinned-only",
            "publisher_authentication": "not-provided",
            "installation_reuse_verified": True,
            "source_mutation_rejected": True,
            "offline_profile_sha256": outputs,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--invokrum", type=Path, required=True)
    parser.add_argument("--pack-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence = prove(args.invokrum.resolve(), args.pack_root.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Installed-root composition, reuse, and mutation rejection verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
