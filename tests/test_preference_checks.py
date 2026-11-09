"""Exercise complete coverage inventories and independent coverage floors."""

import json
import tempfile
import unittest
from pathlib import Path

from preference_proof_fixtures import fixture, proof

from verification.preference_coverage import (
    CHECKER_FILE,
    CHECKER_FILES,
    check_coverage,
    check_source_inventory,
)
from verification.preference_proofs import PreferenceCheckError


class PreferenceCheckTests(unittest.TestCase):
    """Examine the named admission obligations with fixed independent inputs."""

    def test_real_producer_projection_preserves_the_coverage_schema(self) -> None:
        """Retained real producer keys catch a mistaken hand-built count field."""
        path = (
            Path(__file__).resolve().parents[1]
            / "verification/fixtures/coverage-7.11.json"
        )
        report: object = json.loads(path.read_text(encoding="utf-8"))
        result = check_coverage(report)
        self.assertEqual(
            result["runtime"],
            {
                "statements": 344,
                "covered_statements": 329,
                "branches": 112,
                "covered_branches": 108,
            },
        )
        self.assertEqual(
            result["checker"],
            {
                "statements": 263,
                "covered_statements": 260,
                "branches": 112,
                "covered_branches": 110,
            },
        )

    def test_exact_floors_have_independent_counts(self) -> None:
        """Each of two separate five-module groups has an exact 95/100 boundary."""
        result = check_coverage(proof())
        self.assertEqual(
            result["runtime"],
            {
                "statements": 500,
                "covered_statements": 475,
                "branches": 500,
                "covered_branches": 475,
            },
        )
        self.assertEqual(
            result["checker"],
            {
                "statements": 100 * len(CHECKER_FILES),
                "covered_statements": 95 * len(CHECKER_FILES),
                "branches": 100 * len(CHECKER_FILES),
                "covered_branches": 95 * len(CHECKER_FILES),
            },
        )

    def test_one_dimension_or_scope_cannot_excuse_another(self) -> None:
        """A passing other dimension and scope must not disguise 94 percent."""
        cases = (
            (
                proof(runtime_hits=94, runtime_arcs=100, checker_hits=100),
                "statement_floor",
            ),
            (
                proof(runtime_hits=100, runtime_arcs=94, checker_arcs=100),
                "branch_floor",
            ),
            (proof(runtime_hits=100, checker_hits=94), "statement_floor"),
            (proof(runtime_arcs=100, checker_arcs=94), "branch_floor"),
        )
        for value, reason in cases:
            with (
                self.subTest(reason=reason),
                self.assertRaisesRegex(PreferenceCheckError, reason),
            ):
                check_coverage(value)

    def test_coverage_requires_branch_measurement_and_exact_inventory(self) -> None:
        """A missing, extra or empty module is not a measured complete scope."""
        value = proof()
        bad_values: list[object] = [
            {},
            {**value, "meta": {}},
            {**value, "meta": {"branch_coverage": False}},
            {**value, "files": {}},
            {
                **value,
                "files": {
                    name: record
                    for name, record in value["files"].items()
                    if name != CHECKER_FILE
                },
            },
            {**value, "files": {**value["files"], "unexpected.py": {}}},
            {**value, "files": {**value["files"], CHECKER_FILE: None}},
        ]
        for altered in bad_values:
            with self.subTest(value=altered), self.assertRaises(PreferenceCheckError):
                check_coverage(altered)

    def test_coverage_rejects_bad_counts_and_exclusions(self) -> None:
        """Counts are exact integers; neither exclusions nor impossible hits pass."""
        value = proof()
        record = value["files"][CHECKER_FILE]
        for field, bad in (
            ("num_statements", 0),
            ("covered_lines", 101),
            ("num_branches", -1),
            ("covered_branches", 101),
            ("excluded_lines", 1),
            ("covered_lines", "95"),
            ("num_branches", True),
            ("covered_branches", None),
        ):
            altered = {**record, "summary": {**record["summary"], field: bad}}
            with (
                self.subTest(field=field, bad=bad),
                self.assertRaises(PreferenceCheckError),
            ):
                check_coverage(
                    {**value, "files": {**value["files"], CHECKER_FILE: altered}}
                )
        altered = {**record, "excluded_lines": [1]}
        with self.assertRaisesRegex(PreferenceCheckError, "coverage_exclusion"):
            check_coverage(
                {**value, "files": {**value["files"], CHECKER_FILE: altered}}
            )
        for name in value["files"]:
            value["files"][name]["summary"]["num_branches"] = 0
            value["files"][name]["summary"]["covered_branches"] = 0
        with self.assertRaisesRegex(PreferenceCheckError, "branch_evidence_empty"):
            check_coverage(value)

    def test_source_inventory_refuses_missing_and_added_modules(self) -> None:
        """A plausible report cannot excuse an absent or newly unmeasured module."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture(root)
            check_source_inventory(root)
            for name in ("scripts/prepare_header.py", *sorted(CHECKER_FILES)):
                path = root / name
                path.unlink()
                with (
                    self.subTest(name=name),
                    self.assertRaisesRegex(
                        PreferenceCheckError, "source_inventory_mismatch"
                    ),
                ):
                    check_source_inventory(root)
                path.write_text("pass\n", encoding="utf-8")
            (root / "scripts/preference_unexpected.py").write_text(
                "pass\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(
                PreferenceCheckError, "source_inventory_mismatch"
            ):
                check_source_inventory(root)

    def test_checker_inventory_refuses_an_unmeasured_added_module(self) -> None:
        """A newly added examination module must enter the measured inventory."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture(root)
            (root / "verification/preference_unexpected.py").write_text(
                "pass\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(
                PreferenceCheckError, "source_inventory_mismatch"
            ):
                check_source_inventory(root)
