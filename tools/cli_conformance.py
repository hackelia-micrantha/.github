#!/usr/bin/env python3
"""Read-only black-box smoke probes for an explicitly declared installed CLI.

This is a preliminary CLI contract probe, not a replacement for project-owned
domain, security, packaging, release-readiness, or Testule verification.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def validate_manifest(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("manifest must be a JSON object")
    for key in ("executable", "read_only_command", "machine_format_args", "install_root", "man_page"):
        if key not in data:
            raise ValueError(f"missing required manifest field: {key}")
    for key in ("executable", "read_only_command", "machine_format_args", "help_args", "version_args"):
        value = data.get(key, [] if key != "executable" else None)
        if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
            raise ValueError(f"{key} must be an array of nonempty argument strings")
    if not data["executable"]:
        raise ValueError("executable must contain an absolute installed executable path")
    executable = Path(data["executable"][0])
    if not executable.is_absolute():
        raise ValueError("executable[0] must be an absolute path")
    if not data["read_only_command"]:
        raise ValueError("read_only_command is required (no implicit effectful probe)")
    for key in ("install_root", "man_page"):
        if not isinstance(data[key], str) or not data[key]:
            raise ValueError(f"{key} must be a nonempty string")
    root = Path(data["install_root"])
    if not root.is_absolute():
        raise ValueError("install_root must be an absolute path")
    resolved_root = root.resolve()
    resolved_executable = executable.resolve()
    if not resolved_executable.is_relative_to(resolved_root):
        raise ValueError("executable[0] must resolve within install_root")
    man = Path(data["man_page"])
    if man.is_absolute() or ".." in man.parts or not man.as_posix().startswith("share/man/man1/") or man.suffix != ".1":
        raise ValueError("man_page must be a relative share/man/man1/<tool>.1 path")
    if "expected_version" in data and (not isinstance(data["expected_version"], str) or not data["expected_version"]):
        raise ValueError("expected_version must be a nonempty string")
    return data


def probe(data: dict[str, Any], timeout: float) -> dict[str, Any]:
    env = dict(os.environ)
    env.update({"CI": "true", "NO_COLOR": "1", "TERM": "dumb"})
    results: list[dict[str, Any]] = []

    def run(label: str, args: list[str], *, machine: bool = False, version: bool = False) -> None:
        try:
            completed = subprocess.run(
                data["executable"] + args,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                errors="replace",
                env=env,
                timeout=timeout,
                check=False,
            )
            output = completed.stdout
            reasons: list[str] = []
            if completed.returncode != 0:
                reasons.append(f"exit status {completed.returncode}, expected 0")
            if ANSI.search(output):
                reasons.append("ANSI escape codes on redirected stdout with NO_COLOR")
            if not output.strip() and (machine or version):
                reasons.append("missing required stdout result")
            if machine and output:
                try:
                    json.loads(
                        output,
                        parse_constant=lambda value: (_ for _ in ()).throw(
                            ValueError(f"nonstandard JSON constant: {value}")
                        ),
                    )
                except (ValueError, TypeError) as exc:
                    reasons.append(f"stdout is not one valid JSON document: {exc}")
            if version and data.get("expected_version") and data["expected_version"] not in output:
                reasons.append("version output does not include expected_version")
            if label == "help" and not (output.strip() or completed.stderr.strip()):
                reasons.append("help response is empty")
            results.append({"probe": label, "passed": not reasons, "reasons": reasons})
        except (OSError, subprocess.TimeoutExpired) as exc:
            results.append({"probe": label, "passed": False, "reasons": [type(exc).__name__]})

    run("help", data.get("help_args", ["--help"]))
    run("version", data.get("version_args", ["--version"]), version=True)
    run("json", data["read_only_command"] + data["machine_format_args"], machine=True)

    root = Path(data["install_root"]).resolve()
    executable = Path(data["executable"][0])
    resolved_executable = executable.resolve()
    executable_bound = (
        resolved_executable.is_relative_to(root)
        and executable.is_file()
        and os.access(executable, os.X_OK)
    )
    results.append({
        "probe": "installed_executable",
        "passed": executable_bound,
        "reasons": [] if executable_bound else [
            "candidate executable missing, not executable, or outside install_root"
        ],
    })

    page = root / data["man_page"]
    within_root = page.resolve().is_relative_to(root)
    valid = within_root and page.is_file() and page.stat().st_size > 0
    results.append({
        "probe": "installed_man_page",
        "passed": valid,
        "reasons": [] if valid else ["installed section-1 man page missing, empty, or outside install_root"],
    })
    return {"passed": all(item["passed"] for item in results), "results": results}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="JSON profile of an installed CLI and one explicitly read-only command")
    parser.add_argument("--timeout", type=float, default=10, help="per-command timeout in seconds")
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    try:
        data = validate_manifest(json.loads(args.manifest.read_text(encoding="utf-8")))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}))
        return 2
    result = probe(data, args.timeout)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
