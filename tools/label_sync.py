#!/usr/bin/env python3
"""Report-only planner for Micrantha label synchronization."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

NAME_RE = re.compile(r"^[a-z][a-z0-9-]*:[A-Za-z0-9][A-Za-z0-9.-]*$")
COLOR_RE = re.compile(r"^[0-9a-fA-F]{6}$")
PREFIXES = ("priority:", "status:", "type:", "area:", "maturity:")


def load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from None


def documented(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    found = set(re.findall(r"`([A-Za-z0-9-]+:[A-Za-z0-9.-]+)`", text))
    return {name for name in found if name.startswith(PREFIXES)}


def validate(manifest: Any, registry: Any, standards: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict) or not isinstance(registry, dict):
        return ["manifest and registry roots must be objects"]
    if manifest.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    org = manifest.get("organization")
    if org != registry.get("organization"):
        errors.append("manifest organization must match repository registry")

    labels = manifest.get("labels")
    if not isinstance(labels, list) or not labels:
        return errors + ["labels must be a non-empty array"]

    canonical_names: dict[str, str] = {}
    aliases: dict[str, tuple[str, str]] = {}
    for i, item in enumerate(labels):
        p = f"labels[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{p} must be an object")
            continue
        name, color, desc = item.get("name"), item.get("color"), item.get("description")
        valid_name = isinstance(name, str) and bool(NAME_RE.fullmatch(name))
        if not valid_name:
            errors.append(f"{p}.name must use dimension:value syntax")
        else:
            folded = name.casefold()
            previous = canonical_names.get(folded)
            if previous is not None:
                errors.append(f"{p}.name duplicates canonical label {previous!r}")
            else:
                canonical_names[folded] = name
        if not isinstance(color, str) or not COLOR_RE.fullmatch(color):
            errors.append(f"{p}.color must be six hex digits without #")
        if not isinstance(desc, str) or not desc.strip() or len(desc) > 100:
            errors.append(f"{p}.description must contain 1-100 characters")
        raw_aliases = item.get("aliases", [])
        if not isinstance(raw_aliases, list) or any(
            not isinstance(alias, str) or not alias for alias in raw_aliases
        ):
            errors.append(f"{p}.aliases must be a string array")
            continue
        if len({alias.casefold() for alias in raw_aliases}) != len(raw_aliases):
            errors.append(f"{p}.aliases must not contain case-insensitive duplicates")
        if not valid_name:
            continue
        for alias in raw_aliases:
            folded_alias = alias.casefold()
            previous = aliases.get(folded_alias)
            if folded_alias == name.casefold():
                errors.append(f"{p} has alias {alias!r} equal to its canonical label")
                continue
            if previous and previous[1] != name:
                errors.append(
                    f"{p} has alias {alias!r} already owned by {previous[1]!r}"
                )
                continue
            aliases[folded_alias] = (alias, name)

    names = set(canonical_names.values())
    for folded_alias, (alias, owner) in aliases.items():
        canonical = canonical_names.get(folded_alias)
        if canonical is not None:
            errors.append(
                f"alias {alias!r} for {owner!r} collides with canonical label {canonical!r}"
            )

    docs = documented(standards)
    missing, extra = sorted(docs - names), sorted(names - docs)
    if missing:
        errors.append("manifest is missing documented labels: " + ", ".join(missing))
    if extra:
        errors.append("manifest has undocumented labels: " + ", ".join(extra))

    registered = {
        item.get("repository")
        for item in registry.get("repositories", [])
        if isinstance(item, dict)
    }
    repos = manifest.get("repositories")
    if not isinstance(repos, list) or not repos:
        return errors + ["repositories must be a non-empty allowlist"]
    seen: set[str] = set()
    for i, item in enumerate(repos):
        p = f"repositories[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{p} must be an object")
            continue
        repo = item.get("repository")
        if not isinstance(repo, str) or "/" not in repo:
            errors.append(f"{p}.repository must be owner/name")
        else:
            if repo in seen:
                errors.append(f"{p}.repository duplicates {repo}")
            seen.add(repo)
            if repo not in registered:
                errors.append(f"{p}.repository is not in metadata/repositories.json")
            if org and not repo.startswith(f"{org}/"):
                errors.append(f"{p}.repository is outside {org}")
        if item.get("mode") != "report-only":
            errors.append(f"{p}.mode must be report-only; apply is not implemented")
        selected = item.get("labels")
        if not isinstance(selected, list) or not selected:
            errors.append(f"{p}.labels must be a non-empty array")
        elif len(selected) != len(set(selected)):
            errors.append(f"{p}.labels must not contain duplicates")
        elif any(name not in names for name in selected):
            errors.append(f"{p}.labels contains an unknown canonical label")
    return errors


def snapshot(name: str, value: dict[str, Any]) -> dict[str, str]:
    return {
        "name": name,
        "color": str(value.get("color", "")).lstrip("#").lower(),
        "description": str(value.get("description") or ""),
    }


def plan(
    manifest: dict[str, Any], repo: str, current: list[dict[str, Any]]
) -> dict[str, Any]:
    adoption = next(
        (item for item in manifest["repositories"] if item["repository"] == repo),
        None,
    )
    if not adoption:
        raise ValueError(f"repository is not allowlisted for label sync: {repo}")

    catalog = {item["name"]: item for item in manifest["labels"]}
    existing = {
        str(item["name"]): snapshot(str(item["name"]), item)
        for item in current
        if isinstance(item, dict) and item.get("name")
    }
    lower = {name.lower(): name for name in existing}
    considered_existing: set[str] = set()
    actions: list[dict[str, Any]] = []

    for name in adoption["labels"]:
        wanted = catalog[name]
        desired = snapshot(name, wanted)
        aliases = wanted.get("aliases", [])
        alias_hits = [alias for alias in aliases if alias in existing]
        case_hit = lower.get(name.lower())
        canonical = existing.get(name)

        existing_names: list[str] = []
        if canonical:
            existing_names.append(name)
        if case_hit and case_hit != name and case_hit not in existing_names:
            existing_names.append(case_hit)
        for alias in alias_hits:
            if alias not in existing_names:
                existing_names.append(alias)
        considered_existing.update(existing_names)
        before = [existing[value] for value in existing_names]

        if canonical:
            if alias_hits or (case_hit and case_hit != name):
                action, reason = (
                    "collision",
                    "canonical label coexists with alias/case conflict",
                )
            elif (
                canonical["color"] == desired["color"]
                and canonical["description"] == desired["description"]
            ):
                action, reason = "no-op", "metadata matches"
            else:
                action, reason = "update", "canonical label metadata differs"
        elif case_hit and case_hit != name:
            action, reason = "collision", f"case-conflicting label {case_hit!r} exists"
        elif len(alias_hits) == 1:
            action, reason = "migration", f"known alias {alias_hits[0]!r} exists"
        elif len(alias_hits) > 1:
            action, reason = "collision", "multiple known aliases exist"
        else:
            action, reason = "create", "canonical label is absent"

        actions.append(
            {
                "label": name,
                "action": action,
                "existing": before,
                "desired": desired,
                "reason": reason,
            }
        )

    preserved = sorted(name for name in existing if name not in considered_existing)
    summary: dict[str, int] = {}
    for item in actions:
        summary[item["action"]] = summary.get(item["action"], 0) + 1
    return {
        "repository": repo,
        "mode": "report-only",
        "mutates": False,
        "summary": summary,
        "actions": actions,
        "preservedRepositoryLabels": preserved,
    }


def request(url: str, token: str | None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "micrantha-label-sync-report/1",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with urllib.request.urlopen(
            urllib.request.Request(url, headers=headers), timeout=30
        ) as response:
            return json.loads(response.read())
    except (urllib.error.HTTPError, urllib.error.URLError) as exc:
        raise ValueError(f"GitHub label inventory request failed: {exc}") from None


def fetch_labels(repo: str) -> list[dict[str, Any]]:
    owner, name = (urllib.parse.quote(value, safe="") for value in repo.split("/", 1))
    api = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")
    token = os.environ.get("GITHUB_TOKEN") or None
    values: list[dict[str, Any]] = []
    page = 1
    while True:
        batch = request(
            f"{api}/repos/{owner}/{name}/labels?per_page=100&page={page}", token
        )
        if not isinstance(batch, list):
            raise ValueError("GitHub label inventory response is not an array")
        values.extend(value for value in batch if isinstance(value, dict))
        if len(batch) < 100:
            return values
        page += 1


def escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def format_existing(values: list[dict[str, str]]) -> str:
    if not values:
        return "—"
    return "<br>".join(
        f"`{escape(value['name'])}` `#{value['color']}` — {escape(value['description']) or '_(empty)_'}"
        for value in values
    )


def format_desired(value: dict[str, str]) -> str:
    return f"`#{value['color']}` — {escape(value['description'])}"


def render(value: dict[str, Any]) -> str:
    lines = [
        "# Micrantha label synchronization plan",
        "",
        f"Repository: `{value['repository']}`",
        "Mode: `report-only`",
        "Mutation: **disabled**",
        "",
        "| Label | Action | Existing | Desired | Reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    lines += [
        (
            f"| `{item['label']}` | {item['action']} | "
            f"{format_existing(item['existing'])} | {format_desired(item['desired'])} | "
            f"{escape(item['reason'])} |"
        )
        for item in value["actions"]
    ]
    preserved = value["preservedRepositoryLabels"]
    lines += ["", f"Out-of-scope repository labels preserved: **{len(preserved)}**"]
    if preserved:
        lines += ["", ", ".join(f"`{name}`" for name in preserved)]
    lines += ["", "Evidence only: no apply, rename, or delete operation exists.", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path("metadata/labels.json"))
    parser.add_argument("--registry", type=Path, default=Path("metadata/repositories.json"))
    parser.add_argument(
        "--standards", type=Path, default=Path("docs/standards/labels.md")
    )
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("validate")
    planner = sub.add_parser("plan")
    planner.add_argument("--repository", required=True)
    planner.add_argument("--current-labels", type=Path)
    planner.add_argument("--output-json", type=Path)
    planner.add_argument("--output-markdown", type=Path)
    args = parser.parse_args()

    try:
        manifest, registry = load(args.manifest), load(args.registry)
        errors = validate(manifest, registry, args.standards)
    except (ValueError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if args.command == "validate":
        print("Label sync metadata is valid and consistent with docs/standards/labels.md")
        return 0
    if args.command != "plan":
        parser.print_help(sys.stderr)
        return 2

    try:
        current = (
            load(args.current_labels)
            if args.current_labels
            else fetch_labels(args.repository)
        )
        if not isinstance(current, list):
            raise ValueError("current labels must be a JSON array")
        result = plan(manifest, args.repository, current)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    text = render(result)
    print(text)
    if args.output_json:
        args.output_json.write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
    if args.output_markdown:
        args.output_markdown.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
