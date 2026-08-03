#!/usr/bin/env python3
"""Validate Micrantha repository metadata and produce a read-only health report."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable

CLASSIFICATIONS = {
    "organization-meta",
    "public-website",
    "solution",
    "distribution",
    "service",
    "library-sdk",
    "adapter",
    "laboratory",
    "community-surface",
    "infrastructure",
    "repository-tool",
}
MATURITIES = {
    "proposed",
    "experimental",
    "incubating",
    "active",
    "stable",
    "maintenance",
    "superseded",
    "archived",
}
VISIBILITIES = {"public", "private", "internal"}
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SEVERITY_ORDER = {"ok": 0, "skipped": 0, "unknown": 1, "warning": 2, "error": 3}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"file does not exist: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from None


def validate_registry(data: Any, expected_org: str = "hackelia-micrantha") -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["registry root must be an object"]

    if data.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if data.get("organization") != expected_org:
        errors.append(f"organization must be {expected_org!r}")

    repositories = data.get("repositories")
    if not isinstance(repositories, list):
        errors.append("repositories must be an array")
        return errors

    seen: set[str] = set()
    for index, item in enumerate(repositories):
        prefix = f"repositories[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue

        required = {
            "repository",
            "classification",
            "maturity",
            "visibility",
            "defaultBranch",
            "archived",
            "monitor",
            "authority",
            "requiredFiles",
        }
        missing = sorted(required - item.keys())
        if missing:
            errors.append(f"{prefix} missing required fields: {', '.join(missing)}")

        repository = item.get("repository")
        if not isinstance(repository, str) or not REPOSITORY_RE.fullmatch(repository):
            errors.append(f"{prefix}.repository must be an owner/name slug")
        elif repository in seen:
            errors.append(f"{prefix}.repository duplicates {repository}")
        else:
            seen.add(repository)
            if not repository.startswith(f"{expected_org}/"):
                errors.append(
                    f"{prefix}.repository must belong to {expected_org}: {repository}"
                )

        if item.get("classification") not in CLASSIFICATIONS:
            errors.append(
                f"{prefix}.classification must be one of {sorted(CLASSIFICATIONS)}"
            )
        if item.get("maturity") not in MATURITIES:
            errors.append(f"{prefix}.maturity must be one of {sorted(MATURITIES)}")
        if item.get("visibility") not in VISIBILITIES:
            errors.append(f"{prefix}.visibility must be one of {sorted(VISIBILITIES)}")

        default_branch = item.get("defaultBranch")
        if not isinstance(default_branch, str) or not default_branch.strip():
            errors.append(f"{prefix}.defaultBranch must be a non-empty string")

        for field in ("archived", "monitor"):
            if not isinstance(item.get(field), bool):
                errors.append(f"{prefix}.{field} must be a boolean")

        authority = item.get("authority")
        if (
            not isinstance(authority, list)
            or not authority
            or any(not isinstance(value, str) or not value.strip() for value in authority)
        ):
            errors.append(f"{prefix}.authority must be a non-empty string array")
        elif len(authority) != len(set(authority)):
            errors.append(f"{prefix}.authority must not contain duplicates")

        required_files = item.get("requiredFiles")
        if not isinstance(required_files, list) or any(
            not isinstance(value, str) or not value.strip() for value in required_files
        ):
            errors.append(f"{prefix}.requiredFiles must be a string array")
        else:
            if len(required_files) != len(set(required_files)):
                errors.append(f"{prefix}.requiredFiles must not contain duplicates")
            for value in required_files:
                path = Path(value)
                if path.is_absolute() or ".." in path.parts:
                    errors.append(
                        f"{prefix}.requiredFiles contains unsafe path: {value!r}"
                    )

        maturity = item.get("maturity")
        archived = item.get("archived")
        if maturity == "archived" and archived is not True:
            errors.append(f"{prefix} has archived maturity but archived is not true")
        if archived is True and maturity != "archived":
            errors.append(f"{prefix} is archived but maturity is not archived")

        notes = item.get("notes")
        if notes is not None and not isinstance(notes, str):
            errors.append(f"{prefix}.notes must be a string when present")

    return errors


def validate_workflow_templates(root: Path) -> list[str]:
    errors: list[str] = []
    directory = root / "workflow-templates"
    if not directory.exists():
        return ["workflow-templates directory does not exist"]

    workflows = {
        path.stem: path
        for path in directory.iterdir()
        if path.is_file() and path.suffix in {".yml", ".yaml"}
    }
    properties = {
        path.name.removesuffix(".properties.json"): path
        for path in directory.iterdir()
        if path.is_file() and path.name.endswith(".properties.json")
    }

    for name, workflow in sorted(workflows.items()):
        metadata = properties.get(name)
        if metadata is None:
            errors.append(f"{workflow} has no matching {name}.properties.json")
            continue
        try:
            value = load_json(metadata)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not isinstance(value, dict):
            errors.append(f"{metadata} must contain a JSON object")
            continue
        for field in ("name", "description"):
            if not isinstance(value.get(field), str) or not value[field].strip():
                errors.append(f"{metadata} requires a non-empty {field}")
        references = [
            ".github/workflows/reusable-mise-ci.yml",
            ".github/workflows/reusable-nix-ci.yml",
        ]
        text = workflow.read_text(encoding="utf-8")
        for reference in references:
            if reference in text and not (root / reference).exists():
                errors.append(f"{workflow} references missing reusable workflow {reference}")

    for name, metadata in sorted(properties.items()):
        if name not in workflows:
            errors.append(f"{metadata} has no matching workflow YAML")

    return errors


def validate_all(registry_path: Path, root: Path) -> list[str]:
    try:
        registry = load_json(registry_path)
    except ValueError as exc:
        return [str(exc)]

    errors = validate_registry(registry)
    schema_path = registry_path.with_name("repositories.schema.json")
    try:
        load_json(schema_path)
    except ValueError as exc:
        errors.append(str(exc))
    errors.extend(validate_workflow_templates(root))
    return errors


def github_request(url: str, token: str | None) -> tuple[int, Any | None, str | None]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "micrantha-repository-health/1",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
            value = json.loads(body) if body else None
            return response.status, value, None
    except urllib.error.HTTPError as exc:
        return exc.code, None, exc.reason
    except urllib.error.URLError as exc:
        return 0, None, str(exc.reason)


def highest_status(findings: Iterable[dict[str, str]], default: str = "ok") -> str:
    status = default
    for finding in findings:
        candidate = finding["status"]
        if SEVERITY_ORDER[candidate] > SEVERITY_ORDER[status]:
            status = candidate
    return status


def check_repository(
    entry: dict[str, Any], api_url: str, token: str | None
) -> dict[str, Any]:
    slug = entry["repository"]
    if not entry["monitor"]:
        return {
            "repository": slug,
            "status": "skipped",
            "findings": [
                {"status": "skipped", "message": "monitoring disabled in registry"}
            ],
        }

    findings: list[dict[str, str]] = []
    repo_url = f"{api_url.rstrip('/')}/repos/{slug}"
    status, repository, error = github_request(repo_url, token)

    if status != 200 or not isinstance(repository, dict):
        if status == 404 and entry["visibility"] != "public":
            message = (
                "private/internal repository is missing or inaccessible to the configured token"
            )
            finding_status = "unknown"
        elif status == 404:
            message = "public repository was not found"
            finding_status = "error"
        else:
            message = f"repository metadata request failed ({status or 'network'}: {error})"
            finding_status = "unknown"
        return {
            "repository": slug,
            "status": finding_status,
            "findings": [{"status": finding_status, "message": message}],
        }

    actual_visibility = repository.get("visibility")
    if actual_visibility != entry["visibility"]:
        findings.append(
            {
                "status": "warning",
                "message": (
                    f"visibility drift: registry={entry['visibility']}, "
                    f"github={actual_visibility}"
                ),
            }
        )

    actual_branch = repository.get("default_branch")
    if actual_branch != entry["defaultBranch"]:
        findings.append(
            {
                "status": "warning",
                "message": (
                    f"default branch drift: registry={entry['defaultBranch']}, "
                    f"github={actual_branch}"
                ),
            }
        )

    actual_archived = bool(repository.get("archived"))
    if actual_archived != entry["archived"]:
        findings.append(
            {
                "status": "warning",
                "message": (
                    f"archived-state drift: registry={entry['archived']}, "
                    f"github={actual_archived}"
                ),
            }
        )

    for required_file in entry["requiredFiles"]:
        encoded = urllib.parse.quote(required_file, safe="/")
        file_url = f"{repo_url}/contents/{encoded}"
        file_status, _, file_error = github_request(file_url, token)
        if file_status == 200:
            continue
        if file_status == 404:
            findings.append(
                {
                    "status": "error",
                    "message": f"required file missing: {required_file}",
                }
            )
        else:
            findings.append(
                {
                    "status": "unknown",
                    "message": (
                        f"could not verify {required_file} "
                        f"({file_status or 'network'}: {file_error})"
                    ),
                }
            )

    if not findings:
        findings.append(
            {"status": "ok", "message": "registry metadata and required files match"}
        )

    return {
        "repository": slug,
        "status": highest_status(findings),
        "findings": findings,
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, int]:
    summary = {key: 0 for key in SEVERITY_ORDER}
    for result in results:
        summary[result["status"]] += 1
    return summary


def markdown_report(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Micrantha repository health",
        "",
        f"Generated: `{report['generatedAt']}`",
        "",
        (
            f"**Summary:** {summary['ok']} ok · {summary['warning']} warning · "
            f"{summary['error']} error · {summary['unknown']} unknown · "
            f"{summary['skipped']} skipped"
        ),
        "",
        "| Repository | Status | Findings |",
        "| --- | --- | --- |",
    ]
    icons = {
        "ok": "✅",
        "warning": "⚠️",
        "error": "❌",
        "unknown": "❔",
        "skipped": "⏭️",
    }
    for result in report["repositories"]:
        findings = "<br>".join(
            finding["message"].replace("|", "\\|") for finding in result["findings"]
        )
        status = result["status"]
        lines.append(
            f"| `{result['repository']}` | {icons[status]} {status} | {findings} |"
        )
    lines.extend(
        [
            "",
            (
                "Unknown private-repository results usually mean the configured token "
                "lacks access; they do not prove that a repository is missing."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def should_fail(summary: dict[str, int], threshold: str) -> bool:
    if threshold == "none":
        return False
    if threshold == "error":
        return summary["error"] > 0
    if threshold == "warning":
        return summary["error"] > 0 or summary["warning"] > 0
    raise ValueError(f"unsupported threshold: {threshold}")


def command_validate(args: argparse.Namespace) -> int:
    errors = validate_all(args.registry, args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"Validated {args.registry} and workflow templates under "
        f"{args.root / 'workflow-templates'}"
    )
    return 0


def command_health(args: argparse.Namespace) -> int:
    errors = validate_all(args.registry, args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

    registry = load_json(args.registry)
    token = os.environ.get("GITHUB_TOKEN") or None
    api_url = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    results = [
        check_repository(entry, api_url, token) for entry in registry["repositories"]
    ]
    report = {
        "generatedAt": dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat(),
        "organization": registry["organization"],
        "summary": summarize(results),
        "repositories": results,
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    markdown = markdown_report(report)
    args.output_markdown.write_text(markdown, encoding="utf-8")
    print(markdown)

    return 1 if should_fail(report["summary"], args.fail_on) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser(
        "validate", help="validate the registry and workflow-template layout"
    )
    validate_parser.add_argument(
        "--registry",
        type=Path,
        default=Path("metadata/repositories.json"),
    )
    validate_parser.add_argument("--root", type=Path, default=Path("."))
    validate_parser.set_defaults(func=command_validate)

    health_parser = subparsers.add_parser(
        "health", help="produce a read-only repository-health report"
    )
    health_parser.add_argument(
        "--registry",
        type=Path,
        default=Path("metadata/repositories.json"),
    )
    health_parser.add_argument("--root", type=Path, default=Path("."))
    health_parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("artifacts/repository-health.json"),
    )
    health_parser.add_argument(
        "--output-markdown",
        type=Path,
        default=Path("artifacts/repository-health.md"),
    )
    health_parser.add_argument(
        "--fail-on",
        choices=("none", "error", "warning"),
        default="none",
    )
    health_parser.set_defaults(func=command_health)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.func is None:
        parser.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
