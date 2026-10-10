"""Fail-closed shared CI adoption contracts (no third-party YAML parser needed)."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SHARED = [
    ROOT / ".github/workflows/reusable-nix-ci.yml",
    ROOT / ".github/workflows/reusable-mise-ci.yml",
]
STARTERS = [
    ROOT / "workflow-templates/nix-ci.yml",
    ROOT / "workflow-templates/mise-ci.yml",
    ROOT / "workflow-templates/docs-ci.yml",
]
UNCONFIGURED = "runner-REPLACE_WITH_APPROVED_KEY"


class RunnerPlacementContracts(unittest.TestCase):
    def test_shared_ci_requires_an_explicit_runner(self) -> None:
        for path in SHARED:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                inputs = text.split("  workflow_call:\n", maxsplit=1)[1]
                runner = inputs.split("      runner:\n", maxsplit=1)[1].split(
                    "      working-directory:\n", maxsplit=1
                )[0]
                self.assertIn("        required: true\n", runner)
                self.assertIn("        type: string\n", runner)
                self.assertNotIn("default:", runner)
                self.assertNotIn("ubuntu-", runner)

    def test_shared_nix_reuses_jit_nix_substrate(self) -> None:
        text = SHARED[0].read_text(encoding="utf-8")
        self.assertIn("if: ${{ startsWith(inputs.runner, 'runner-') }}", text)
        self.assertIn("command -v nix", text)
        self.assertIn("nix --version", text)
        self.assertIn("if: ${{ !startsWith(inputs.runner, 'runner-') }}", text)
        self.assertIn("uses: cachix/install-nix-action@", text)

    def test_starters_are_unconfigured_and_push_only(self) -> None:
        for path in STARTERS:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                trigger = text.split("\npermissions:\n", maxsplit=1)[0]
                self.assertIn("  push:\n", trigger)
                self.assertIn("    branches: [$default-branch]", trigger)
                self.assertNotIn("  pull_request:\n", trigger)
                self.assertNotIn("  pull_request_target:\n", trigger)
                self.assertIn(f"      runner: {UNCONFIGURED}\n", text)
                self.assertNotIn("runner: ubuntu-", text)


if __name__ == "__main__":
    unittest.main()
