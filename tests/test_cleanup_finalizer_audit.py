from pathlib import Path
import tempfile
import unittest
from tools.check_cleanup_finalizers import audit, evaluate_workflow


class NativeCleanupWorkflowScanner(unittest.TestCase):
    def check(self, steps, expected):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "ci.yml"
            file.write_text("name: CI\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n" + steps)
            result = evaluate_workflow(file)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["status"], expected)
            return result[0]

    def test_make_cleanup_after_uploaded_artifact(self):
        self.check("      - name: Build binary\n        run: make build\n"
                   "      - name: Upload bundle\n        uses: actions/upload-artifact@sha\n"
                   "      - name: Clean generated binary\n        if: always()\n        run: make clean\n",
                   "finalizer_present")

    def test_npm_cleanup_without_mise(self):
        self.check("      - name: Test generated assets\n        run: npm run test\n"
                   "      - name: Cleanup after evidence\n        if: always()\n        run: yarn clean:build\n",
                   "finalizer_present")

    def test_missing_is_advisory(self):
        finding = self.check("      - name: Build\n        run: cargo build\n", "missing_finalizer")
        self.assertGreater(len(finding["notes"]), 0)

    def test_early_cleanup_before_artifact_is_flagged(self):
        self.check("      - name: Build\n        run: go build ./...\n"
                   "      - name: Clean\n        if: always()\n        run: make clean\n"
                   "      - name: Upload binary\n        uses: actions/upload-artifact@sha\n",
                   "premature_cleanup")

    def test_cleanup_not_on_failed_validation_flagged(self):
        self.check("      - name: Test\n        run: go test ./...\n"
                   "      - name: Clean\n        run: make clean\n",
                   "conditional_cleanup")

    def test_no_output_documented(self):
        self.check("    # cleanup: no-local-outputs\n"
                   "      - name: Build\n        run: nix build --no-link .#tool\n",
                   "no_local_output_declared")

    def test_non_build_job_is_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github/workflows"
            workflows.mkdir(parents=True)
            (workflows / "ci.yml").write_text(
                "name: CI\njobs:\n  policy:\n    runs-on: ubuntu-latest\n    steps:\n"
                "      - name: Validate workflow policy\n        run: python tools/check.py\n"
            )
            self.assertEqual(audit(root), [])


if __name__ == "__main__":
    unittest.main()
