#!/usr/bin/env python3
"""Bounded, read-only paired pilot for .github issue #139 (not a general eval framework)."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/standing-guidance-pilot.json"
PACK = ROOT / "micrantha-prompt-pack.yaml"
GOLDEN = ROOT / "tests/fixtures/micrantha-prompt-pack-golden.json"
PROFILE = "engineering-artifact-review"
BASELINE = (
    "Review the engineering artifact for decision readiness. "
    "Identify material defects; do not invent blockers. "
    "Reply only with the requested JSON."
)
ANSWER_FORMAT = (
    'Return ONLY a JSON object: {"decision":"ready" or "fix",'
    '"findings":[{"section":"section ID","severity":"blocker" or "material"'
    ' or "suggestion","reason":"short source-grounded reason"}]}. '
    "For a clean artifact, return decision ready and no findings. "
    "Only cite IDs that actually occur in the artifact."
)


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def verify_fixture(fixture: dict) -> None:
    assert fixture["schema"] == "micrantha.standing-guidance-pilot/v1"
    assert len(fixture["cases"]) == 3
    ids = [case["id"] for case in fixture["cases"]]
    assert len(set(ids)) == len(ids)
    for case in fixture["cases"]:
        assert case["gold"]["decision"] in {"ready", "fix"}
        assert all(s in case["artifact"] for s in case["gold"]["finding_sections"])
        assert (case["gold"]["decision"] == "ready") == (not case["gold"]["finding_sections"])
    assert "negative_case" in fixture


def treatment_context(invokrum: str) -> tuple[bytes, str]:
    proc = subprocess.run(
        [invokrum, "compose", "--pack", str(PACK), "--profile", PROFILE],
        cwd=ROOT, check=True, capture_output=True,
    )
    expected = json.loads(GOLDEN.read_text())["profiles"][PROFILE]["context_sha256"]
    actual = digest(proc.stdout)
    if actual != expected:
        raise ValueError(f"Invokrum exact profile mismatch: expected {expected}, got {actual}")
    version = subprocess.run(
        [invokrum, "--version"], check=True, capture_output=True, text=True,
    ).stdout.strip()
    if version != "invokrum 0.2.1":
        raise ValueError(f"Unexpected Invokrum version: {version}")
    return proc.stdout, version


def endpoint_url(base: str) -> str:
    url = urllib.parse.urlsplit(base)
    if url.scheme != "http" or url.hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("Pilot permits only a plain-HTTP loopback inference endpoint")
    if url.username or url.password or url.query or url.fragment:
        raise ValueError("Endpoint must not contain credentials or query parameters")
    if url.path.rstrip("/") not in {"", "/v1"}:
        raise ValueError("Use a loopback origin or /v1 endpoint")
    return base.rstrip("/") + ("" if url.path.rstrip("/") == "/v1" else "/v1")


class RejectRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Inference endpoint redirected; refusing network forwarding")


def request_json(url: str, payload: dict | None = None) -> dict:
    body = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"},
        method="GET" if body is None else "POST",
    )
    # Ignore proxy environment variables and refuse redirects to non-loopback hosts.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), RejectRedirect)
    with opener.open(req, timeout=90) as response:
        return json.load(response)


def parse_answer(content: str) -> dict | None:
    try:
        parsed = json.loads(content)
        if not isinstance(parsed, dict) or parsed.get("decision") not in {"ready", "fix"}:
            return None
        if not isinstance(parsed.get("findings"), list):
            return None
        if any(not isinstance(f, dict) or not isinstance(f.get("section"), str)
               or f.get("severity") not in {"blocker", "material", "suggestion"}
               for f in parsed["findings"]):
            return None
        return parsed
    except (json.JSONDecodeError, TypeError):
        return None


def score(case: dict, answer: dict | None) -> dict | None:
    """Deterministic section-ID screen, not independent semantic adjudication."""
    if answer is None:
        return None
    gold = set(case["gold"]["finding_sections"])
    reported = {
        f["section"] for f in answer["findings"]
        if f["severity"] in {"blocker", "material"}
    }
    return {
        "decision_matches_key": answer["decision"] == case["gold"]["decision"],
        "required_section_hits": len(gold & reported),
        "required_sections": len(gold),
        "unkeyed_material_sections": sorted(reported - gold),
        "note": "Unkeyed findings require blinded human review, not automatic dismissal.",
    }


def save_evidence(path: Path, data: dict) -> None:
    # Same-directory rename preserves the last completed iteration after a crash.
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent,
        prefix=f".{path.name}.", suffix=".tmp", delete=False,
    ) as stream:
        tmp = Path(stream.name)
        try:
            json.dump(data, stream, indent=2)
            stream.write("\n")
        except Exception:
            tmp.unlink(missing_ok=True)
            raise
    os.replace(tmp, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--invokrum", default="invokrum")
    parser.add_argument("--endpoint", default="http://127.0.0.1:8000/v1")
    parser.add_argument("--model", help="Exact model ID; default is first returned by /v1/models")
    parser.add_argument("--output", type=Path, help="New JSON evidence file (required with --run)")
    parser.add_argument("--run", action="store_true", help="Perform 18 paired model calls; default is preflight only")
    args = parser.parse_args()

    fixture_bytes = FIXTURE.read_bytes()
    fixture = json.loads(fixture_bytes)
    verify_fixture(fixture)
    context, cli_version = treatment_context(args.invokrum)
    endpoint = endpoint_url(args.endpoint)

    script_sha = digest(Path(__file__).read_bytes())
    evidence = {
        "harness_sha256": script_sha,
        "harness_revision": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
            capture_output=True, text=True,
        ).stdout.strip(),
        "mechanical_evaluator": "score(case, answer) in this harness",
        "schema": "micrantha.standing-guidance-pilot-result/v1",
        "fixture_sha256": digest(fixture_bytes),
        "source_commit": fixture["source_commit"],
        "treatment_context_sha256": digest(context),
        "baseline_sha256": digest(BASELINE.encode()),
        "invokrum_version": cli_version,
        "request_format_sha256": digest(ANSWER_FORMAT.encode()),
        "endpoint": endpoint,
        "model": None,
        "request_parameters": {"temperature": 0.3, "max_tokens": 600},
        "runs": [],
        "negative_case_status": "not_run_not_enforced",
        "semantic_grading": "not_done",
    }
    if not args.run:
        print(json.dumps({"status": "preflight_passed_no_inference", **{
            key: evidence[key] for key in (
                "fixture_sha256", "treatment_context_sha256", "baseline_sha256",
                "invokrum_version", "negative_case_status"
            )}}, indent=2))
        return 0
    if args.output is None:
        parser.error("--output is required with --run")
    models = request_json(endpoint + "/models").get("data", [])
    names = [m["id"] for m in models]
    if not names:
        raise ValueError("No models reported by endpoint")
    model = args.model or names[0]
    if model not in names:
        raise ValueError(f"Requested model {model!r} absent from endpoint")
    evidence["model"] = model
    evidence["model_advertised_metadata"] = next(m for m in models if m["id"] == model)

    # Exclusive creation avoids silent overwrites. Persist raw evidence after each call.
    with args.output.open("x", encoding="utf-8") as target:
        json.dump(evidence, target, indent=2)
    for case in fixture["cases"]:
        for repetition in range(3):
            for condition, system_text in (
                ("baseline", BASELINE), ("treatment", context.decode("utf-8"))
            ):
                prompt = (
                    f"Review this {case['shape']} as an engineering artifact.\n"
                    + ANSWER_FORMAT + "\n\n" + case["artifact"]
                )
                payload = {
                    "model": model,
                    "temperature": 0.3,
                    "max_tokens": 600,
                    "seed": 1900 + repetition,
                    "messages": [
                        {"role": "system", "content": system_text},
                        {"role": "user", "content": prompt},
                    ],
                }
                try:
                    result = request_json(endpoint + "/chat/completions", payload)
                except (OSError, ValueError, urllib.error.URLError) as exc:
                    evidence["error"] = {
                        "case_id": case["id"], "repetition": repetition,
                        "condition": condition, "failure_type": type(exc).__name__,
                    }
                    save_evidence(args.output, evidence)
                    raise
                raw = result["choices"][0]["message"]["content"]
                parsed = parse_answer(raw)
                evidence["runs"].append({
                    "case_id": case["id"], "repetition": repetition,
                    "condition": condition, "seed": payload["seed"],
                    "content": raw, "usage": result.get("usage"),
                    "parsed": parsed, "screen": score(case, parsed),
                })
                save_evidence(args.output, evidence)
    print(json.dumps({
        "output": str(args.output),
        "runs": len(evidence["runs"]),
        "semantic_grading": "requires_blinded_review",
        "negative_case": "not_run",
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError,
            urllib.error.URLError, KeyError, AssertionError) as exc:
        print(f"pilot error: {exc}", file=sys.stderr)
        sys.exit(1)
