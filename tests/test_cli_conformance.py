"""Smoke coverage of the shared installed-CLI contract probe."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

from tools.cli_conformance import probe, validate_manifest


class CliConformanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.exe = self.root / "fixture.py"
        self.exe.write_text(
            f"#!{sys.executable}\n"
            "import json, sys\n"
            "args = sys.argv[1:]\n"
            "if '--help' in args: print('usage: fixture [--help]'); sys.exit(0)\n"
            "if '--version' in args: print('fixture 1.2.3'); sys.exit(0)\n"
            "if args == ['list', '--format', 'json']: print(json.dumps({'data': [1]})); sys.exit(0)\n"
            "sys.exit(2)\n",
            encoding="utf-8",
        )
        self.exe.chmod(0o755)
        man = self.root / "share" / "man" / "man1" / "fixture.1"
        man.parent.mkdir(parents=True)
        man.write_text(".TH FIXTURE 1\n.SH NAME\nfixture\\-test\n", encoding="utf-8")
        self.profile = {
            "executable": [str(self.exe)],
            "help_args": ["--help"],
            "version_args": ["--version"],
            "read_only_command": ["list"],
            "machine_format_args": ["--format", "json"],
            "expected_version": "1.2.3",
            "install_root": str(self.root),
            "man_page": "share/man/man1/fixture.1",
        }

    def test_passing_package_probe(self) -> None:
        result = probe(validate_manifest(self.profile), 3)
        self.assertTrue(result["passed"], result)
        self.assertEqual(5, len(result["results"]))
        self.assertTrue(
            next(x for x in result["results"] if x["probe"] == "installed_executable")["passed"]
        )

    def test_rejects_machine_stdout_contamination(self) -> None:
        self.exe.write_text(
            self.exe.read_text(encoding="utf-8").replace(
                "print(json.dumps({'data': [1]}))",
                "print('progress'); print(json.dumps({'data': [1]}))",
            ),
            encoding="utf-8",
        )
        result = probe(validate_manifest(self.profile), 3)
        self.assertFalse(result["passed"])
        self.assertFalse(next(x for x in result["results"] if x["probe"] == "json")["passed"])

    def test_rejects_nonstandard_json_constants(self) -> None:
        self.exe.write_text(
            self.exe.read_text(encoding="utf-8").replace(
                "print(json.dumps({'data': [1]}))",
                "print('{\\"data\\": NaN}')",
            ),
            encoding="utf-8",
        )
        result = probe(validate_manifest(self.profile), 3)
        json_probe = next(x for x in result["results"] if x["probe"] == "json")
        self.assertFalse(json_probe["passed"])
        self.assertTrue(
            any("nonstandard JSON constant" in reason for reason in json_probe["reasons"])
        )

    def test_rejects_executable_outside_install_root(self) -> None:
        self.profile["executable"] = [sys.executable]
        with self.assertRaisesRegex(ValueError, "within install_root"):
            validate_manifest(self.profile)

    def test_rejects_executable_symlink_escape(self) -> None:
        symlink = self.root / "fixture-link"
        symlink.symlink_to(sys.executable)
        self.profile["executable"] = [str(symlink)]
        with self.assertRaisesRegex(ValueError, "within install_root"):
            validate_manifest(self.profile)

    def test_rejects_missing_man_page(self) -> None:
        self.profile["man_page"] = "share/man/man1/missing.1"
        result = probe(validate_manifest(self.profile), 3)
        self.assertFalse(next(x for x in result["results"] if x["probe"] == "installed_man_page")["passed"])

    def test_rejects_unsafe_man_path(self) -> None:
        self.profile["man_page"] = "../fixture.1"
        with self.assertRaises(ValueError):
            validate_manifest(self.profile)

    def test_requires_explicit_read_only_command(self) -> None:
        self.profile["read_only_command"] = []
        with self.assertRaises(ValueError):
            validate_manifest(self.profile)


if __name__ == "__main__":
    unittest.main()
