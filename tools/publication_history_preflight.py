#!/usr/bin/env python3
"""Offline redacted audit of objects reachable from local Git refs.

No network operations, no mutation, and no credential values in reports.
This is evidence collection, NOT a comprehensive confidentiality guarantee.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

OID = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
PEM = re.compile(rb"(?m)^-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----\r?$")
TOKEN_SHAPES = (
    re.compile(rb"\bghp_[A-Za-z0-9]{30,}\b"),
    re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    re.compile(rb"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(rb"\bsk_live_[A-Za-z0-9]{16,}\b"),
)
SECRET_LINE = re.compile(
    rb"(?mi)^[ \t]*(?:export[ \t]+)?"
    rb"(?:LNBITS_API_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY|"
    rb"GEMINI_API_KEY|GITHUB_TOKEN|API_SECRET|ADMIN_PASSWORD|SECRET_KEY)"
    rb"[ \t]*=[ \t]*([^\r\n#]+)"
)
PLACEHOLDER = re.compile(
    rb"(?i)^(?:\$\{[^}]+\}|\$[A-Z_]+|<[^>]+>|"
    rb"replace[-_ ].*|change[-_ ]?me.*|your[-_ ].*|"
    rb"example.*|sample.*|placeholder.*|dummy.*|"
    rb"none|null|unset|todo|x{3,}|\.{3,})$"
)
TEXT_EXTENSIONS = {
    ".py", ".sh", ".js", ".mjs", ".cjs", ".json", ".yaml", ".yml",
    ".toml", ".md", ".nix", ".ts", ".tsx", ".go", ".rs", ".txt",
    ".html", ".xml", ".env", ".example", ".ini", ".conf", ".properties",
    ".tf", ".tfvars", ".rb", ".ex", ".exs", ".kt", ".swift",
}
KEY_FILES = {
    "id_rsa", "id_ed25519", "id_ecdsa", "credentials.json",
    "google-services.json", "googleservice-info.plist",
    ".npmrc", ".netrc", ".pypirc", ".git-credentials",
}
KEY_EXTENSIONS = {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore", ".tfstate"}
DATA_EXTENSIONS = {".db", ".sqlite", ".sqlite3"}
REVIEW_EXTENSIONS = {".bak", ".backup", ".orig"}
EXAMPLE_ENV = {".env.example", ".env.sample", ".env.template"}


class Incomplete(RuntimeError):
    """Fail closed if objects or bytes could not be inspected."""


def git(repo: Path, *args: str, data: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], input=data, capture_output=True, check=False
    )
    if result.returncode:
        raise Incomplete(f"git {args[0]} returned {result.returncode}")
    return result.stdout


def reachable(repo: Path, limit: int) -> tuple[list[str], dict[str, set[str]]]:
    refs = git(repo, "for-each-ref", "--format=%(objectname)")
    if not refs.strip():
        raise Incomplete("repository has no refs")
    objects: list[str] = []
    paths: dict[str, set[str]] = {}
    for raw in git(repo, "rev-list", "--objects", "--all").splitlines():
        oid, _, name = raw.partition(b" ")
        key = oid.decode("ascii", "strict")
        if not OID.fullmatch(key):
            raise Incomplete("unexpected object identifier")
        if key not in paths:
            objects.append(key)
            paths[key] = set()
            if len(objects) > limit:
                raise Incomplete("object limit exceeded")
        if name:
            paths[key].add(name.decode("utf-8", "surrogateescape"))
    if not objects:
        raise Incomplete("no reachable objects")
    return objects, paths


def historical_filenames(repo: Path, max_paths: int) -> set[str]:
    # A rev-list object ID gets only one representative path. Recover the
    # complete set of changed filenames independently to avoid path-rule gaps.
    raw = git(repo, "log", "--all", "--format=", "--name-only", "-z")
    names = {
        item.decode("utf-8", "surrogateescape")
        for item in raw.split(b"\0") if item.strip()
    }
    if len(names) > max_paths:
        raise Incomplete("historical filename limit exceeded")
    return names


def blob_inventory(repo: Path, objects: list[str]) -> list[tuple[str, int]]:
    out: list[tuple[str, int]] = []
    for i in range(0, len(objects), 4096):
        batch = objects[i:i + 4096]
        data = git(
            repo, "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)",
            data=("\n".join(batch) + "\n").encode("ascii"),
        )
        lines = data.splitlines()
        if len(lines) != len(batch):
            raise Incomplete("truncated object inventory")
        for wanted, line in zip(batch, lines):
            parts = line.decode("ascii", "strict").split()
            if len(parts) != 3 or parts[0] != wanted:
                raise Incomplete("object unavailable or malformed")
            if parts[1] == "blob":
                out.append((wanted, int(parts[2])))
    return out


def batched_blobs(repo: Path, ids: list[str]):
    data = git(repo, "cat-file", "--batch", data=("\n".join(ids) + "\n").encode("ascii"))
    offset = 0
    for wanted in ids:
        end = data.find(b"\n", offset)
        if end < 0:
            raise Incomplete("truncated batch header")
        header = data[offset:end].decode("ascii", "strict").split()
        if len(header) != 3 or header[:2] != [wanted, "blob"]:
            raise Incomplete("invalid blob header")
        size = int(header[2])
        offset = end + 1
        stop = offset + size
        if data[stop:stop + 1] != b"\n":
            raise Incomplete("truncated blob bytes")
        yield wanted, data[offset:stop]
        offset = stop + 1
    if offset != len(data):
        raise Incomplete("unexpected trailing blob bytes")


def path_rules(path: str):
    name = Path(path).name.lower()
    ext = Path(path).suffix.lower()
    if (name == ".env" or name.startswith(".env.")) and name not in EXAMPLE_ENV:
        yield "block", "committed-runtime-environment"
    if name in KEY_FILES or ext in KEY_EXTENSIONS:
        yield "block", "key-or-credential-file"
    if ext in DATA_EXTENSIONS:
        yield "review", "database-may-contain-personal-data"
    if ext in REVIEW_EXTENSIONS:
        yield "review", "backup-or-retired-artifact"
    if "resume" in name and ext in {".pdf", ".doc", ".docx", ".html"}:
        yield "review", "public-personal-document"


def content_rules(data: bytes):
    if PEM.search(data):
        yield "block", "private-key-pem"
    if any(pattern.search(data) for pattern in TOKEN_SHAPES):
        yield "block", "credential-token-shape"
    for match in SECRET_LINE.finditer(data):
        value = match.group(1).strip().strip(b"'\"").strip()
        if value and not PLACEHOLDER.fullmatch(value):
            yield "block", "hardcoded-secret-assignment"
            break


def audit(repo: Path, max_objects: int, max_blob_bytes: int, max_total_bytes: int):
    objects, paths = reachable(repo, max_objects)
    all_names = historical_filenames(repo, max_objects)
    inventory = blob_inventory(repo, objects)
    seen_bytes = 0
    pending: list[str] = []
    findings: dict[tuple[str, str, str], dict] = {}
    incomplete_blobs = 0

    def record(oid: str, severity: str, rule: str, specified_path: str | None = None):
        for path in sorted([specified_path] if specified_path is not None
                           else paths[oid] or {"[unattributed blob]"}):
            key = (path, severity, rule)
            if key not in findings:
                findings[key] = {"path": path, "severity": severity, "rule": rule,
                                 "example_blob_oid": oid, "matched_blob_versions": 0}
            findings[key]["matched_blob_versions"] += 1

    for oid, size in inventory:
        for path in paths[oid] or {"[unattributed blob]"}:
            for severity, rule in path_rules(path):
                record(oid, severity, rule, path)
        if size > max_blob_bytes:
            incomplete_blobs += 1
            record(oid, "review", "uninspected-oversize-blob")
            continue
        seen_bytes += size
        if seen_bytes > max_total_bytes:
            raise Incomplete("total scanned byte budget exceeded")
        pending.append(oid)

    for start in range(0, len(pending), 16):
        for oid, data in batched_blobs(repo, pending[start:start + 16]):
            for severity, rule in content_rules(data):
                record(oid, severity, rule)

    # Report historical risk-bearing names even when Git assigned their
    # shared blob an unrelated representative path.
    for path in sorted(all_names):
        for severity, rule in path_rules(path):
            key = (path, severity, rule)
            if key not in findings:
                findings[key] = {
                    "path": path, "severity": severity, "rule": rule,
                    "example_blob_oid": None, "matched_blob_versions": 0,
                    "attribution": "historical-path-only",
                }

    counts = Counter(f["severity"] for f in findings.values())
    return {
        "scope": "objects-reachable-from-local-refs",
        "status": "indeterminate" if incomplete_blobs else "review-required"
                  if counts["block"] or counts["review"] else "no-pattern-findings",
        "history_scan_complete": incomplete_blobs == 0,
        "objects_seen": len(objects),
        "blobs_seen": len(inventory),
        "bytes_inspected": seen_bytes,
        "blobs_uninspected": incomplete_blobs,
        "counts": {"block": counts["block"], "review": counts["review"]},
        "findings": sorted(findings.values(), key=lambda x: (x["path"], x["rule"])),
        "limitations": [
            "Only local refs; external forks, reflogs, PR-only refs and caches not scanned",
            "Blob-to-path attribution is representative; changed filename coverage also uses git log",
            "No live credential validation, proprietary-IP review or runtime testing",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-objects", type=int, default=250000)
    parser.add_argument("--max-blob-bytes", type=int, default=2 * 1024 * 1024)
    parser.add_argument("--max-total-bytes", type=int, default=1024 * 1024 * 1024)
    args = parser.parse_args()
    if args.output.exists():
        print("Output already exists; refusing overwrite", file=sys.stderr)
        return 2
    try:
        result = audit(args.repo, args.max_objects, args.max_blob_bytes,
                       args.max_total_bytes)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
    except (Incomplete, OSError, ValueError) as exc:
        print(f"INDETERMINATE: {type(exc).__name__}", file=sys.stderr)
        return 2
    print(json.dumps({
        "status": result["status"],
        "blobs_seen": result["blobs_seen"],
        "blobs_uninspected": result["blobs_uninspected"],
        "counts": result["counts"],
    }))
    if result["status"] == "indeterminate":
        return 2
    return 1 if result["counts"]["block"] else 0


if __name__ == "__main__":
    sys.exit(main())
