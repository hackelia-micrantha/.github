#!/usr/bin/env python3
"""Read-only publication preflight for Git-tracked current-tree files.

This is not a credential-history scan, human disclosure review, or proof of safety.
Only rule identifiers and paths are emitted; candidate values are never printed.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

MAX_TEXT_BYTES = 2 * 1024 * 1024
EXAMPLE_NAMES = {".env.example", ".env.sample", ".env.template"}
PRIVATE_KEY_HEADER = re.compile(
    rb"(?m)^-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----\r?$"
)
TOKEN_PATTERNS = (
    re.compile(rb"\bghp_[A-Za-z0-9]{30,}\b"),
    re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(rb"\bsk_live_[A-Za-z0-9]{16,}\b"),
)
ASSIGNMENT = re.compile(
    rb"(?mi)^[ \t]*(?:export[ \t]+)?"
    rb"(?:LNBITS_API_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY|GEMINI_API_KEY|"
    rb"SECRET_KEY|API_SECRET|ADMIN_PASSWORD|GITHUB_TOKEN)[ \t]*=[ \t]*"
    rb"([^\r\n#]+)"
)
PLACEHOLDER = re.compile(
    rb"(?i)^(?:\$\{[^}]+\}|\$[A-Z_]+|<[^>]+>|"
    rb"replace[-_ ].*|change[-_ ]?me.*|your[-_ ].*|example.*|"
    rb"sample.*|placeholder.*|dummy.*|none|null|unset|todo|x{3,}|\.{3,})$"
)
KEY_FILE_NAMES = {
    "id_rsa", "id_ed25519", "id_ecdsa", "credentials.json",
    "google-services.json", "googleservice-info.plist", ".npmrc",
    ".netrc", ".pypirc", ".git-credentials",
}
KEY_SUFFIXES = (".pem", ".key", ".p12", ".pfx", ".jks", ".keystore", ".tfstate")
DATABASE_SUFFIXES = (".db", ".sqlite", ".sqlite3")
BACKUP_SUFFIXES = (".bak", ".backup", ".orig")
TEXT_SUFFIXES = {
    ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".go", ".rs",
    ".sh", ".bash", ".zsh", ".yaml", ".yml", ".json", ".toml", ".nix",
    ".md", ".txt", ".env", ".example", ".conf", ".ini", ".tf", ".tfvars",
    ".xml", ".properties", ".gradle", ".rb", ".ex", ".exs", ".sql",
    ".html", ".css", ".swift", ".kt", ".java", ".c", ".h", ".cpp",
}


def classify_path(relative: str) -> list[tuple[str, str]]:
    p = Path(relative)
    name = p.name.lower()
    suffix = p.suffix.lower()
    results: list[tuple[str, str]] = []
    if (name == ".env" or name.startswith(".env.")) and name not in EXAMPLE_NAMES:
        results.append(("block", "runtime-env"))
    if name in KEY_FILE_NAMES or suffix in KEY_SUFFIXES:
        results.append(("block", "credential-or-key-file"))
    if suffix in DATABASE_SUFFIXES:
        results.append(("review", "database-may-contain-personal-data"))
    if suffix in BACKUP_SUFFIXES:
        results.append(("review", "backup-or-retired-artifact"))
    if "resume" in name and suffix in {".pdf", ".doc", ".docx", ".html"}:
        results.append(("review", "public-personal-profile"))
    return results


def tracked_files(root: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--cached"],
        capture_output=True, check=True,
    )
    return sorted({p.decode("utf-8", "surrogateescape") for p in
                   completed.stdout.split(b"\0") if p})


def scan(root: Path) -> list[dict[str, str]]:
    root = root.resolve(strict=True)
    findings: list[dict[str, str]] = []
    for relative in tracked_files(root):
        path = root / relative

        def emit(severity: str, rule: str) -> None:
            findings.append({"path": relative, "severity": severity, "rule": rule})

        for severity, rule in classify_path(relative):
            emit(severity, rule)
        if path.is_symlink():
            if not path.resolve().is_relative_to(root):
                emit("block", "symlink-escapes-root")
            else:
                emit("review", "tracked-symlink")
            continue
        if not path.is_file():
            emit("review", "missing-tracked-file")
            continue
        if path.stat().st_size > MAX_TEXT_BYTES:
            if path.suffix.lower() in TEXT_SUFFIXES:
                emit("review", "oversize-text-not-inspected")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {
            ".env", ".envrc", ".npmrc", ".netrc", ".pypirc",
        }:
            continue
        data = path.read_bytes()
        if b"\0" in data:
            emit("review", "binary-in-text-file")
            continue
        if PRIVATE_KEY_HEADER.search(data):
            emit("block", "pem-private-key")
        if any(p.search(data) for p in TOKEN_PATTERNS):
            emit("block", "recognized-token-shape")
        for match in ASSIGNMENT.finditer(data):
            value = match.group(1).strip().strip(b"'\"").strip()
            if value and not PLACEHOLDER.fullmatch(value):
                emit("block", "hardcoded-credential-assignment")
                break
    return sorted(findings, key=lambda x: (x["path"], x["rule"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--strict", action="store_true",
                        help="Also fail on human-review findings")
    args = parser.parse_args()
    try:
        findings = scan(args.root)
    except (OSError, subprocess.CalledProcessError) as error:
        print(json.dumps({"status": "indeterminate", "error_type": type(error).__name__}))
        return 2
    blocking = sum(f["severity"] == "block" for f in findings)
    review = sum(f["severity"] == "review" for f in findings)
    print(json.dumps({
        "status": "blocked" if blocking or (args.strict and review) else "ok",
        "scope": "git-tracked-current-tree-only",
        "blocking_count": blocking,
        "review_count": review,
        "findings": findings,
    }, indent=2))
    return 1 if blocking or (args.strict and review) else 0


if __name__ == "__main__":
    raise SystemExit(main())
