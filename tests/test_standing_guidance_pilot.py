"""Bounded regression tests for the #139 pilot; no network or live model needed."""
import importlib.util
import json
import sys
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
                    "choices": [{
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
            self.assertEqual(evidence["negative_case_status"], "not_run_not_enforced")
            with mock.patch.object(sys, "argv", args), \
                 mock.patch.object(module, "treatment_context", return_value=(b"treated", "invokrum 0.2.1")), \
                 mock.patch.object(module, "request_json", side_effect=fake_request):
                with self.assertRaises(FileExistsError):
                    module.main()

    def test_bad_fixture_fails_closed(self):
        fixture = json.loads(module.FIXTURE.read_text())
        fixture["cases"][0]["gold"]["finding_sections"] = ["NO_SUCH_SECTION"]
        with self.assertRaises(AssertionError):
            module.verify_fixture(fixture)


if __name__ == "__main__":
    unittest.main()
