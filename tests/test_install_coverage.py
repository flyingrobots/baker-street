"""Keep installation coverage obligations independent with fixed proof inputs."""

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import TypedDict

from verification.check_install_coverage import (
    CHECKER_FILE,
    INSTALL_FILES,
    check_report,
    main,
)


class FileProof(TypedDict):
    """Keep deliberately invalid summary values as objects until admission."""

    summary: dict[str, object]
    excluded_lines: list[int]


def proof() -> dict[str, object]:
    """Supply four exact 95/100 records, independent of any producer's percentages."""
    return {
        "meta": {"branch_coverage": True},
        "files": {
            name: {
                "summary": {
                    "num_statements": 100,
                    "covered_lines": 95,
                    "num_branches": 100,
                    "covered_branches": 95,
                    "excluded_lines": 0,
                },
                "excluded_lines": [],
            }
            for name in INSTALL_FILES | {CHECKER_FILE}
        },
    }


class InstallCoverageTests(unittest.TestCase):
    """Require each floor, inventory, count and the bounded public admission route."""

    def test_independent_dimensions_inventory_and_count_admission(self) -> None:
        """A strong other component or dimension cannot excuse a deficient result."""
        expected = {
            "installation": {
                "statements": 300,
                "covered_statements": 285,
                "branches": 300,
                "covered_branches": 285,
            },
            "checker": {
                "statements": 100,
                "covered_statements": 95,
                "branches": 100,
                "covered_branches": 95,
            },
        }
        self.assertEqual(check_report(proof()), expected)
        for name in ("scripts/install.py", CHECKER_FILE):
            for key, value in (
                ("covered_lines", 94 if name == CHECKER_FILE else 90),
                ("covered_branches", 94 if name == CHECKER_FILE else 90),
                ("num_statements", 0),
                ("covered_lines", 101),
                ("num_branches", -1),
                ("covered_branches", 101),
                ("excluded_lines", 1),
                ("covered_lines", True),
                ("covered_lines", "95"),
            ):
                document = proof()
                files: dict[str, FileProof] = {
                    path: {
                        "summary": {
                            "num_statements": 100,
                            "covered_lines": 95,
                            "num_branches": 100,
                            "covered_branches": 95,
                            "excluded_lines": 0,
                        },
                        "excluded_lines": [],
                    }
                    for path in INSTALL_FILES | {CHECKER_FILE}
                }
                files[name]["summary"][key] = value
                document["files"] = files
                with (
                    self.subTest(name=name, key=key, value=value),
                    self.assertRaises(ValueError),
                ):
                    check_report(document)
        invalid_documents: list[object] = [
            None,
            {},
            {**proof(), "meta": {}},
            {**proof(), "files": {}},
            {**proof(), "files": {"unexpected": {}}},
        ]
        for document in invalid_documents:
            with self.subTest(document=document), self.assertRaises(ValueError):
                check_report(document)

    def test_actual_admission_command_reports_success_and_bounded_refusals(
        self,
    ) -> None:
        """Retain exact counts on success; failed or oversized proofs emit no success."""
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "coverage.json"
            path.write_text(json.dumps(proof()), encoding="utf-8")
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                self.assertEqual(main([str(path)]), 0)
            self.assertEqual(json.loads(stdout.getvalue()), check_report(proof()))
            self.assertEqual(stderr.getvalue(), "")
            for content in (b"invalid", b"{}", b" " * 1048577):
                path.write_bytes(content)
                stdout, stderr = io.StringIO(), io.StringIO()
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    self.assertEqual(main([str(path)]), 2)
                self.assertEqual(stdout.getvalue(), "")
                self.assertIn("refused", stderr.getvalue())
            path.unlink()
            with redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(path)]), 2)

    def test_zero_branches_and_explicit_excluded_lines_are_refused(self) -> None:
        """An empty branch dimension or hidden exclusion is no coverage proof."""
        for excluded, branches, hits in (([1], 100, 95), ([], 0, 0)):
            files: dict[str, FileProof] = {
                name: {
                    "summary": {
                        "num_statements": 100,
                        "covered_lines": 95,
                        "num_branches": branches,
                        "covered_branches": hits,
                        "excluded_lines": 0,
                    },
                    "excluded_lines": excluded,
                }
                for name in INSTALL_FILES | {CHECKER_FILE}
            }
            with (
                self.subTest(excluded=excluded, branches=branches),
                self.assertRaises(ValueError),
            ):
                check_report({"meta": {"branch_coverage": True}, "files": files})

    def test_nonregular_coverage_proof_is_refused_without_waiting(self) -> None:
        """An owned FIFO is not a report and must not block the command."""
        with tempfile.TemporaryDirectory() as temporary:
            fifo = Path(temporary) / "fifo"
            os.mkfifo(fifo)
            with redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(fifo)]), 2)
