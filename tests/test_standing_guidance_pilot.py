"""Bounded regression tests for the #139 pilot; no network or live model needed."""
import importlib.util
import json
import sys
import io
import urllib.error
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "standing_guidance_pilot", ROOT / "tools/standing_guidance_pilot.py"
)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class PilotTests(unittest.TestCase):
    def test_frozen_fixture(self):
        fixture = json.loads(module.FIXTURE.read_text())
        module.verify_fixture(fixture)
        self.assertEqual(
            [c["id"] for c in fixture["cases"]],
            ["rfc-authz", "adr-outbox", "plan-healthz"],
        )

    def test_loopback_only(self):
        for good in ("http://127.0.0.1:8000/v1", "http://localhost:11434"):
            self.assertTrue(module.endpoint_url(good).endswith("/v1"))
        for bad in (
            "https://127.0.0.1:8000/v1", "http://example.com/v1",
            "http://127.0.0.1.evil.test:8000/v1",
            "http://127.0.0.1:8000/v1?token=x",
            "http://user:secret@127.0.0.1:8000/v1",
        ):
            with self.subTest(url=bad), self.assertRaises(ValueError):
                module.endpoint_url(bad)

    def test_parsing_and_section_screen(self):
        artifact = json.loads(module.FIXTURE.read_text())["cases"][0]
        parsed = module.parse_answer(
            '{"decision":"fix","findings":['
            '{"section":"R2","severity":"blocker","reason":"No proof or authorization"}]}'
        )
        self.assertTrue(module.score(artifact, parsed)["decision_matches_key"])
        self.assertEqual(module.score(artifact, parsed)["required_section_hits"], 1)
        self.assertIsNone(module.parse_answer("unstructured prose"))
        self.assertIsNone(module.score(artifact, None))
        clean = json.loads(module.FIXTURE.read_text())["cases"][2]
        self.assertEqual(module.score(clean, {
            "decision": "ready", "findings": [],
        })["unkeyed_material_sections"], [])

    def test_missing_or_invalid_reasons_do_not_count_as_valid_findings(self):
        template = '{"decision":"fix","findings":[{"section":"R2","severity":"blocker",%s}]}'
        invalid = ('"extra":"no reason"', '"reason":42', '"reason":null',
                   '"reason":""', '"reason":"  "')
        for field in invalid:
            with self.subTest(field=field):
                self.assertIsNone(module.parse_answer(template % field))
        self.assertIsNotNone(module.parse_answer(
            template % '"reason":"Unauthenticated header is trusted"'
        ))

    def test_malformed_completion_keeps_partial_failure_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "partial.json"
            args = ["pilot", "--run", "--output", str(out)]
            for malformed in ({"choices": []}, {"choices": [{}]},
                              {"choices": [{"message": {}}]},
                              {"choices": [{"message": {"content": 42}}]}):
                if out.exists():
                    out.unlink()
                def fake_request(url, payload=None):
                    if url.endswith("/models"):
                        return {"data": [{"id": "fake-model"}]}
                    return malformed
                with self.subTest(result=malformed), \
                     mock.patch.object(sys, "argv", args), \
                     mock.patch.object(module, "treatment_context", return_value=(b"treatment", "invokrum 0.2.1")), \
                     mock.patch.object(module, "request_json", side_effect=fake_request):
                    with self.assertRaises(ValueError):
                        module.main()
                evidence = json.loads(out.read_text())
                self.assertEqual(evidence["runs"], [])
                self.assertEqual(evidence["error"]["case_id"], "rfc-authz")
                self.assertEqual(evidence["error"]["failure_type"], "ValueError")
                self.assertEqual(evidence["error"]["condition"], "baseline")

    def test_malformed_models_response_keeps_partial_failure_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "models-error.json"
            args = ["pilot", "--run", "--output", str(out)]
            bad_responses = (
                [], {"data": None}, {"data": []}, {"data": [None]},
                {"data": [{}]}, {"data": [{"id": 32}]},
                {"data": [{"id": ""}]}, {"data": [{"id": "  "}]},
            )
            for response in bad_responses:
                if out.exists():
                    out.unlink()
                with self.subTest(response=response), \
                     mock.patch.object(sys, "argv", args), \
                     mock.patch.object(module, "treatment_context", return_value=(b"treated", "invokrum 0.2.1")), \
                     mock.patch.object(module, "request_json", return_value=response):
                    with self.assertRaises(ValueError):
                        module.main()
                evidence = json.loads(out.read_text())
                self.assertEqual(evidence["runs"], [])
                self.assertEqual(evidence["error"]["stage"], "model_discovery")
                self.assertEqual(evidence["error"]["failure_type"], "ValueError")

    def test_eighteen_calls_and_persisted_evidence_with_mock_transport(self):
        # This is synthetic harness validation, NOT actual model evaluation.
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "evidence.json"
            requests = []

            def fake_request(url, payload=None):
                if url.endswith("/models"):
                    return {"data": [{"id": "fake-model", "owned_by": "test"}]}
                requests.append(payload)
                return {
                    "id": f"mock-completion-{len(requests)}",
                    "model": "fake-model",
                    "system_fingerprint": "mock-build-sha",
                    "choices": [{
                        "finish_reason": "stop",
                        "message": {"content": '{"decision":"ready","findings":[]}'}
                    }],
                    "usage": {"prompt_tokens": 5, "completion_tokens": 8},
                }

            args = [
                "pilot", "--run", "--endpoint", "http://127.0.0.1:8000/v1",
                "--output", str(out),
            ]
            with mock.patch.object(sys, "argv", args), \
                 mock.patch.object(module, "treatment_context", return_value=(b"treated", "invokrum 0.2.1")), \
                 mock.patch.object(module, "request_json", side_effect=fake_request):
                self.assertEqual(module.main(), 0)
            evidence = json.loads(out.read_text())
            self.assertEqual(len(requests), 18)
            self.assertEqual(len(evidence["runs"]), 18)
            self.assertEqual(
                {r["condition"] for r in evidence["runs"]},
                {"baseline", "treatment"},
            )
            self.assertEqual(evidence["model"], "fake-model")
            self.assertTrue(all(
                r["response_metadata"]["served_model"] == "fake-model"
                and r["response_metadata"]["finish_reason"] == "stop"
                and r["response_metadata"]["system_fingerprint"] == "mock-build-sha"
                for r in evidence["runs"]
            ))
            self.assertEqual(evidence["negative_case_status"], "not_run_not_enforced")
            with mock.patch.object(sys, "argv", args), \
                 mock.patch.object(module, "treatment_context", return_value=(b"treated", "invokrum 0.2.1")), \
                 mock.patch.object(module, "request_json", side_effect=fake_request):
                with self.assertRaises(FileExistsError):
                    module.main()

    def test_completion_model_identity_and_finish_reason_are_required(self):
        good = {
            "id": "run-1", "model": "test-model", "system_fingerprint": "fp1",
            "choices": [{"finish_reason": "stop",
                         "message": {"content": '{"decision":"ready","findings":[]}'}}],
        }
        self.assertEqual(module.completion_content(good, "test-model")[0],
                         '{"decision":"ready","findings":[]}')
        for change in (
            {"model": "other-model"}, {"model": None}, {"model": ""},
            {"choices": [{"finish_reason": "length", "message": {"content": "{}"}}]},
            {"choices": [{"finish_reason": "content_filter", "message": {"content": "{}"}}]},
            {"choices": [{"message": {"content": "{}"}}]},
        ):
            altered = {**good, **change}
            with self.subTest(change=change), self.assertRaises(ValueError):
                module.completion_content(altered, "test-model")

    def test_bounded_response_rejects_large_and_non_json_body(self):
        with mock.patch.object(module.urllib.request, "build_opener") as builder:
            response = io.BytesIO(b" " * (module.MAX_RESPONSE_BYTES + 1))
            builder.return_value.open.return_value.__enter__.return_value = response
            with self.assertRaises(ValueError):
                module.request_json("http://127.0.0.1:8000/v1/models")
        with mock.patch.object(module.urllib.request, "build_opener") as builder:
            response = io.BytesIO(b"{bad json")
            builder.return_value.open.return_value.__enter__.return_value = response
            with self.assertRaises(ValueError):
                module.request_json("http://127.0.0.1:8000/v1/models")

    def test_http_error_is_bounded_diagnostic_and_partial_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = Path(tmp) / "failed.json"
            args = ["pilot", "--run", "--output", str(result)]
            def fake_request(url, payload=None):
                if url.endswith("/models"):
                    return {"data": [{"id": "fake-model"}]}
                raise urllib.error.HTTPError(
                    url, 400, "Bad Request", {},
                    io.BytesIO(b'{"error":{"message":"Unsupported parameter: seed"}}'),
                )
            with mock.patch.object(sys, "argv", args), \
                 mock.patch.object(module, "treatment_context",
                                   return_value=(b"treated", "invokrum 0.2.1")), \
                 mock.patch.object(module, "request_json", side_effect=fake_request):
                with self.assertRaises(urllib.error.HTTPError):
                    module.main()
            recorded = json.loads(result.read_text())
            self.assertEqual(recorded["runs"], [])
            self.assertEqual(recorded["error"]["http_status"], 400)
            self.assertEqual(recorded["error"]["http_reason"], "Bad Request")
            self.assertEqual(recorded["error"]["parameter_hints"], ["seed"])
            self.assertLessEqual(len(recorded["error"]["http_reason"]), 128)

    def test_bad_fixture_fails_closed(self):
        fixture = json.loads(module.FIXTURE.read_text())
        fixture["cases"][0]["gold"]["finding_sections"] = ["NO_SUCH_SECTION"]
        with self.assertRaises(AssertionError):
            module.verify_fixture(fixture)


if __name__ == "__main__":
    unittest.main()
