#!/usr/bin/env python3
"""Advisory static audit of native CI cleanup finalizers. No Mise dependency."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

JOB = re.compile(r"^  ([A-Za-z0-9_-]+):\s*$", re.M)
STEP = re.compile(r"^      - (?:name|run|uses):")
PRODUCER_NAME = re.compile(r"\b(build|builds|assemble|assembly|compile|compilation|test|tests|testing|render|rendering|fuzz|fuzzing|package|packaging|playwright)\b", re.I)
PRODUCER_RUN = re.compile(r"(?:\b(?:cargo|go)\s+(?:test|build|fuzz|package)\b|\./gradlew\s+:(?:\S+)|\b(?:npm|yarn|mise)\s+(?:run\s+)?(?:test|build|ci)\b|\bnix\s+(?:build|flake\s+check)\b|\bmake\s+(?:test|build|coverage|e2e|check)\b|\bplaywright\s+test\b)", re.I)
CLEAN = re.compile(r"\b(clean|cleanup|retire generated|remove (?:temporary|generated|build))\b", re.I)


def steps_for(body: str) -> list[str]:
    items, current = [], []
    for line in body.splitlines():
        if STEP.match(line):
            if current:
                items.append("\n".join(current))
            current = [line]
        elif current:
            current.append(line)
    if current:
        items.append("\n".join(current))
    return items


def evaluate_workflow(path: Path) -> list[dict]:
    contents = path.read_text(encoding="utf8")
    match = re.search(r"^jobs:\s*$", contents, re.M)
    if match is None:
        return []
    text = contents[match.end():]
    boundaries = list(JOB.finditer(text))
    findings = []
    for i, item in enumerate(boundaries):
        body = text[item.end():boundaries[i + 1].start() if i + 1 < len(boundaries) else len(text)]
        steps = steps_for(body)
        if not steps:
            continue
        producers, cleaners, uploads = [], [], []
        for index, step in enumerate(steps):
            header = step.split("\n", 1)[0]
            if "upload-artifact@" in step or "name: Upload " in header:
                uploads.append(index)
            if CLEAN.search(header) or re.search(r"\b(?:make|yarn|npm|mise)\s+(?:run\s+)?clean(?::\S+)?\b", step) or re.search(r"\b(?:cargo|gradlew)\s+clean\b", step):
                cleaners.append(index)
                continue
            if PRODUCER_NAME.search(header) or PRODUCER_RUN.search(step):
                producers.append(index)
        if not producers and not cleaners:
            continue
        status = "no_local_output_declared" if "# cleanup: no-local-outputs" in body else "no_build_or_test"
        notes = []
        if producers and status != "no_local_output_declared":
            if not cleaners:
                status = "missing_finalizer"
                notes.append("No native cleanup finalizer recognized")
            elif min(cleaners) <= max(producers):
                status = "premature_cleanup"
                notes.append("No cleanup after final build/test step")
            elif any(k > max(cleaners) for k in uploads):
                status = "premature_cleanup"
                notes.append("Artifact upload after cleanup")
            elif not any("always()" in steps[k] for k in cleaners if k > max(producers)):
                status = "conditional_cleanup"
                notes.append("No always() finalizer; verify deferred cleanup on failure")
            else:
                status = "finalizer_present"
        findings.append({"workflow": str(path), "job": item.group(1), "status": status,
                         "producer_steps": len(producers), "cleanup_steps": len(cleaners),
                         "upload_steps": len(uploads), "notes": notes})
    return findings


def audit(root: Path) -> list[dict]:
    directory = root / ".github" / "workflows"
    if not directory.is_dir():
        return [{"workflow": str(directory), "job": None, "status": "no_workflows", "notes": ["Inspect native build/test"]}]
    records = []
    for path in sorted([*directory.glob("*.yaml"), *directory.glob("*.yml")]):
        records.extend(evaluate_workflow(path))
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repositories", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true", dest="json_mode")
    parser.add_argument("--strict", action="store_true", help="Fail on suspected missing or premature finalizers")
    args = parser.parse_args()
    reports = [{"repository": str(repo.resolve()), "jobs": audit(repo)} for repo in args.repositories]
    if args.json_mode:
        print(json.dumps(reports, indent=2))
    else:
        for report in reports:
            print(report["repository"])
            for job in report["jobs"]:
                print("  ", job["status"], job["job"], job["workflow"])
    errors = {"missing_finalizer", "premature_cleanup"}
    return 1 if args.strict and any(job["status"] in errors for report in reports for job in report["jobs"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
