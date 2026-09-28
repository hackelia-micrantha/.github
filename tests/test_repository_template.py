import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs" / "standards" / "templates" / "thin-repository"
PROPOSAL = TEMPLATE / ".repora" / "bootstrap.proposed.json"


class ThinRepositoryTemplateTests(unittest.TestCase):
    def test_reference_tree_is_deliberately_minimal(self) -> None:
        files = sorted(
            str(path.relative_to(TEMPLATE))
            for path in TEMPLATE.rglob("*")
            if path.is_file()
        )
        self.assertEqual(
            files,
            [".repora/bootstrap.proposed.json", "README.md"],
        )

    def test_template_does_not_embed_architecture_defaults(self) -> None:
        forbidden = {
            "LICENSE",
            "LICENSE.md",
            "LICENSE.txt",
            "flake.nix",
            "flake.lock",
            "CODEOWNERS",
            ".gitignore",
        }
        files = {
            str(path.relative_to(TEMPLATE))
            for path in TEMPLATE.rglob("*")
            if path.is_file()
        }
        self.assertTrue(forbidden.isdisjoint(files))
        self.assertFalse(
            any(path.startswith(".github/workflows/") for path in files)
        )

    def test_bootstrap_proposal_is_assumption_free(self) -> None:
        proposal = json.loads(PROPOSAL.read_text())
        self.assertEqual(proposal["schemaVersion"], 1)
        self.assertEqual(proposal["kind"], "micrantha.repository-bootstrap")
        self.assertIn(
            "/af0ec6581e7593b4e5cb8a5ada4294cde86115e8/"
            "metadata/repository-bootstrap.schema.json",
            proposal["$schema"],
        )

        resolved = [d for d in proposal["decisions"] if d["state"] == "resolved"]
        self.assertEqual(len(resolved), 1)
        self.assertEqual(resolved[0]["key"], "repository.defaultBranch")
        self.assertEqual(resolved[0]["value"], "main")
        self.assertEqual(
            resolved[0]["provenance"]["authority"],
            "organization-policy",
        )

        unresolved = {
            d["key"] for d in proposal["decisions"] if d["state"] == "unresolved"
        }
        for key in {
            "repository.name",
            "repository.visibility",
            "repository.license",
            "implementation.language",
            "implementation.runtime",
            "implementation.buildSystem",
            "implementation.packageManager",
            "delivery.ciProvider",
            "delivery.releaseModel",
            "delivery.distribution",
            "interface.cli",
            "interface.service",
            "interface.library",
            "interface.website",
            "interface.mobile",
        }:
            self.assertIn(key, unresolved)

    def test_template_readme_does_not_claim_policy_authority(self) -> None:
        text = (TEMPLATE / "README.md").read_text().lower()
        self.assertIn("assumption-free", text)
        self.assertIn("not ongoing policy authority", text)
        self.assertNotIn("recommended stack", text)
        self.assertNotIn("default license", text)


if __name__ == "__main__":
    unittest.main()
