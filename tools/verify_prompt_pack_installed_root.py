#!/usr/bin/env python3
"""Exercise exact digest-pinned, offline installed-root composition for Micrantha."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
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
    "docs/prompts/pull-requests/merge-gate-review.md",
)
PROFILES = ("classify-and-route", "issue-grooming", "engineering-artifact-review", "merge-gate-review")


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


def validate_installed_root(installed_root: Path, store: Path) -> None:
    """Require a real directory rooted inside the selected local store."""
    if installed_root.is_symlink() or not installed_root.is_dir():
        raise RuntimeError("installer returned a linked or missing installed root")
    try:
        resolved_root = installed_root.resolve(strict=True)
        resolved_store = store.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise RuntimeError("installer root/store could not be resolved") from error
    if (
        not installed_root.is_relative_to(store)
        or resolved_root == resolved_store
        or not resolved_root.is_relative_to(resolved_store)
    ):
        raise RuntimeError("installer returned a root outside the selected private store")


def validate_publisher_inputs(
    public_key: Path | None, signature: Path | None, trusted_key: str | None,
) -> str | None:
    """Require complete caller-owned inputs; Invokrum validates the key and signature."""
    supplied = (public_key is not None, signature is not None, trusted_key is not None)
    if not any(supplied):
        return None
    if not all(supplied):
        raise ValueError("publisher key, signature, and trusted fingerprint must be supplied together")
    assert trusted_key is not None
    if len(trusted_key) != 64 or any(char not in "0123456789abcdef" for char in trusted_key):
        raise ValueError("trusted fingerprint must be exactly 64 lowercase hex digits")
    return trusted_key


def verify_source_commit(
    source_root: Path, source_commit: str, staged_root: Path | None = None,
) -> str:
    """Bind each canonical pack source to an explicit clean 40-hex Git revision."""
    if len(source_commit) != 40 or any(ch not in "0123456789abcdef" for ch in source_commit):
        raise ValueError("source commit must be a full lowercase 40-hex Git SHA")
    root = source_root.resolve(strict=True)

    def git(*args: str) -> bytes:
        # Git refs/replace and inherited GIT_* variables must not redefine
        # what the pinned commit SHA means during trusted-source verification.
        clean_env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        clean_env["GIT_NO_REPLACE_OBJECTS"] = "1"
        clean_env["GIT_CONFIG_NOSYSTEM"] = "1"
        clean_env["GIT_CONFIG_GLOBAL"] = os.devnull
        command = subprocess.run(
            ["git", "--no-replace-objects", "-C", str(root), *args],
            env=clean_env, capture_output=True, check=False, timeout=20,
        )
        if command.returncode != 0:
            raise ValueError(f"source Git verification failed: {args[0]}")
        return command.stdout

    top = Path(git("rev-parse", "--show-toplevel").decode("utf-8").strip()).resolve(strict=True)
    if top != root:
        raise ValueError("pack source root must be the selected Git worktree root")
    if git("rev-parse", "--verify", "HEAD").decode("ascii").strip() != source_commit:
        raise ValueError("source checkout HEAD does not match the expected commit")
    if git("status", "--porcelain", "--untracked-files=normal").strip():
        raise ValueError("source checkout has uncommitted or untracked changes")
    for source in SOURCES:
        # git show returns raw blob bytes; do not normalize whitespace or line endings.
        pinned_bytes = git("show", f"{source_commit}:{source}")
        if (root / source).read_bytes() != pinned_bytes:
            raise ValueError(f"canonical source differs from the selected commit: {source}")
        if staged_root is not None and (staged_root / source).read_bytes() != pinned_bytes:
            raise ValueError(f"staged source differs from the selected commit: {source}")
    return source_commit



def snapshot_publisher_inputs(public_key: Path, signature: Path, private_root: Path) -> tuple[Path, Path]:
    """Copy immutable evidence bytes for both accepted install and replay checks."""
    key_copy = private_root / "publisher.ed25519.pub"
    signature_copy = private_root / "publisher.ed25519.sig"
    key_copy.write_bytes(public_key.read_bytes())
    signature_copy.write_bytes(signature.read_bytes())
    return key_copy, signature_copy


def verified_publisher_result(result: dict, subject: str, trusted_key: str) -> bool:
    """Check the installer output shape; cryptographic proof remains Invokrum's responsibility."""
    return (
        result.get("installation_format") == "invokrum.installation/v2"
        and isinstance(result.get("publisher_authentication"), dict)
        and result["publisher_authentication"] == {
            "status": "verified-and-authorized",
            "mechanism": "ed25519-subject-v1",
            "subject": subject.removeprefix("sha256:"),
            "identity": {"key.sha256": trusted_key},
        }
    )


def prove(
    invokrum: Path, source_root: Path,
    publisher_public_key: Path | None = None,
    publisher_signature: Path | None = None,
    trusted_key_sha256: str | None = None,
    source_commit: str | None = None,
) -> dict:
    trusted_key = validate_publisher_inputs(publisher_public_key, publisher_signature, trusted_key_sha256)
    if trusted_key is not None and source_commit is None:
        raise ValueError("authenticated proof requires an explicit source commit")
    if source_commit is not None:
        verify_source_commit(source_root, source_commit)
    with tempfile.TemporaryDirectory(prefix="micrantha-installed-proof-") as tmp:
        scratch = Path(tmp)
        candidate = scratch / "candidate"
        canonical, digest = make_candidate(source_root, candidate)
        if source_commit is not None:
            verify_source_commit(source_root, source_commit, candidate)
        manifest = scratch / "bundle-manifest.json"
        manifest.write_bytes(canonical)
        subject = f"sha256:{digest}"
        store = scratch / "store"
        install_args = (
            "install", str(candidate), "--candidate-format", "directory",
            "--bundle-manifest", str(manifest), "--subject", subject,
            "--store", str(store), "--format", "json",
        )
        if trusted_key is not None:
            assert publisher_public_key is not None and publisher_signature is not None
            key_copy, signature_copy = snapshot_publisher_inputs(
                publisher_public_key, publisher_signature, scratch,
            )
            install_args += (
                "--publisher-public-key", str(key_copy),
                "--publisher-signature", str(signature_copy),
                "--trusted-key-sha256", trusted_key,
            )
        first = json.loads(invoke(invokrum, *install_args).stdout)
        second = json.loads(invoke(invokrum, *install_args).stdout)
        if not (
            first.get("format") == second.get("format") == "invokrum.cli/v1"
            and first.get("command") == second.get("command") == "install"
            and (
                (trusted_key is None
                 and first.get("installation_format") == second.get("installation_format") == "invokrum.installation/v1"
                 and first.get("publisher_authentication") == second.get("publisher_authentication") == "not-provided")
                or
                (trusted_key is not None
                 and verified_publisher_result(first, subject, trusted_key)
                 and verified_publisher_result(second, subject, trusted_key))
            )
            and first.get("subject") == second.get("subject") == subject
            and first.get("root") == second.get("root")
            and first.get("reused") is False and second.get("reused") is True
        ):
            raise RuntimeError("installed subject, reuse, or publisher identity mismatch")

        installed_root = Path(first["root"])
        validate_installed_root(installed_root, store)

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

        if trusted_key is not None:
            assert publisher_signature is not None
            # Bad proof must fail without poisoning the verified installed root.
            invalid_signature = scratch / "invalid.sig"
            invalid_signature.write_bytes(bytes(64))
            rejected = list(install_args)
            rejected[rejected.index("--publisher-signature") + 1] = str(invalid_signature)
            if invoke(invokrum, *rejected, success=False).returncode == 0:
                raise RuntimeError("invalid publisher signature was accepted")

            denied = list(install_args)
            fingerprint_index = denied.index("--trusted-key-sha256") + 1
            denied[fingerprint_index] = (
                ("0" if trusted_key[0] != "0" else "1") + trusted_key[1:]
            )
            if invoke(invokrum, *denied, success=False).returncode == 0:
                raise RuntimeError("unauthorized publisher identity was accepted")

        wrong_subject = list(install_args)
        subject_index = wrong_subject.index("--subject") + 1
        wrong_subject[subject_index] = "sha256:" + (
            ("0" if digest[0] != "0" else "1") + digest[1:]
        )
        if invoke(invokrum, *wrong_subject, success=False).returncode == 0:
            raise RuntimeError("bundle subject substitution was accepted")

        changed = scratch / "changed"
        shutil.copytree(candidate, changed)
        with (changed / "docs/prompts/issues/issue-grooming.md").open("ab") as stream:
            stream.write(b"\n<!-- intentional bundle mutation -->\n")
        tampered_args = list(install_args)
        tampered_args[1] = str(changed)
        if invoke(invokrum, *tampered_args, success=False).returncode == 0:
            raise RuntimeError("modified candidate passed original subject/manifest verification")

        if trusted_key is not None:
            # An internally consistent *different* candidate/manifest/subject must
            # reject the valid original signature, independent of bundle digest checks.
            alternate = scratch / "alternate-candidate"
            alternate_manifest, alternate_digest = make_candidate(changed, alternate)
            altered_manifest_path = scratch / "alternate.bundle.json"
            altered_manifest_path.write_bytes(alternate_manifest)
            alternate_args = list(install_args)
            alternate_args[1] = str(alternate)
            alternate_args[alternate_args.index("--bundle-manifest") + 1] = str(altered_manifest_path)
            alternate_args[alternate_args.index("--subject") + 1] = f"sha256:{alternate_digest}"
            if invoke(invokrum, *alternate_args, success=False).returncode == 0:
                raise RuntimeError("publisher signature was accepted for a different valid subject")

        missing = scratch / "missing"
        shutil.copytree(candidate, missing)
        (missing / "docs/prompts/overlays/cross-project-execution.md").unlink()
        missing_args = list(install_args)
        missing_args[1] = str(missing)
        if invoke(invokrum, *missing_args, success=False).returncode == 0:
            raise RuntimeError("candidate missing a required overlay was installed")

        invalid = invoke(
            invokrum, "validate", "--pack", str(installed_root / ENTRY_POINT),
            "--profile", "unregistered-profile", "--format", "json", success=False,
        )
        if invalid.returncode == 0:
            raise RuntimeError("unregistered profile was accepted")

        # Installation verification must remain valid after rejected candidates.
        control = invoke(
            invokrum, "compose", "--pack", str(installed_root / ENTRY_POINT),
            "--profile", "issue-grooming",
        ).stdout
        if hashlib.sha256(control).hexdigest() != outputs["issue-grooming"]:
            raise RuntimeError("rejected candidate affected installed content")

        evidence = {
            "format": "micrantha.installed-prompt-pack-proof/v1",
            "subject": subject,
            "mode": "authenticated-local" if trusted_key is not None else "digest-pinned-only",
            "publisher_authentication": (
                first["publisher_authentication"] if trusted_key is not None else "not-provided"
            ),
            "installation_reuse_verified": True,
            "source_mutation_rejected": True,
            "subject_mismatch_rejected": True,
            "missing_overlay_rejected": True,
            "bad_signature_rejected": True if trusted_key is not None else None,
            "untrusted_publisher_rejected": True if trusted_key is not None else None,
            "signature_subject_mismatch_rejected": True if trusted_key is not None else None,
            "unknown_profile_rejected": True,
            "offline_profile_sha256": outputs,
        }
        if source_commit is not None:
            evidence["source_commit"] = source_commit
        return evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--invokrum", type=Path, required=True)
    parser.add_argument("--pack-root", type=Path, default=Path("."))
    parser.add_argument("--publisher-public-key", type=Path)
    parser.add_argument("--publisher-signature", type=Path)
    parser.add_argument("--trusted-key-sha256")
    parser.add_argument("--source-commit", help="Exact 40-hex Git source commit (required with publisher)")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence = prove(
        args.invokrum.resolve(), args.pack_root.resolve(),
        args.publisher_public_key, args.publisher_signature, args.trusted_key_sha256,
        args.source_commit,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Installed-root composition, reuse, and mutation rejection verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
