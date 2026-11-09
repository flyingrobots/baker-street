"""Exercise coverage dimensions and exception custody with fixed proof fixtures."""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from pathlib import Path
from typing import TypedDict

from verification.check_preferences import (
    CHECKER_FILE,
    PROOF_BYTES,
    RUNTIME_FILES,
    PreferenceCheckError,
    check_coverage,
    check_exceptions,
    check_source_inventory,
    definitions,
    load_json,
    main,
    read_text,
    source_exceptions,
)

TODAY = date(2026, 11, 8)
SOURCE = (
    "import subprocess\n\n"
    "def inquire():\n"
    "    # policy-exception: PREF-EXAMPLE -- Fixed inquiry.\n"
    "    subprocess.run(arguments)  # noqa: S603\n"
)


class Summary(TypedDict):
    """Known counts in an independently constructed coverage fixture."""

    num_statements: int
    covered_lines: int
    num_branches: int
    covered_branches: int
    excluded_lines: int


class FileProof(TypedDict):
    """One known module in the fixture inventory."""

    summary: Summary
    excluded_lines: list[int]


class CoverageProof(TypedDict):
    """A fixture whose deliberate alterations remain ordinary object inputs."""

    meta: dict[str, bool]
    files: dict[str, FileProof]


def proof(
    *,
    runtime_hits: int = 95,
    runtime_arcs: int = 95,
    checker_hits: int = 95,
    checker_arcs: int = 95,
) -> CoverageProof:
    """Supply exactly 100 statements and branches per module, at the boundary."""
    files: dict[str, FileProof] = {}
    for name in RUNTIME_FILES | {CHECKER_FILE}:
        files[name] = {
            "summary": {
                "num_statements": 100,
                "covered_lines": checker_hits if name == CHECKER_FILE else runtime_hits,
                "num_branches": 100,
                "covered_branches": checker_arcs
                if name == CHECKER_FILE
                else runtime_arcs,
                "excluded_lines": 0,
            },
            "excluded_lines": [],
        }
    return {"meta": {"branch_coverage": True}, "files": files}


def exception() -> dict[str, object]:
    """Describe the sole source waiver in the owned fixture."""
    return {
        "id": "PREF-EXAMPLE",
        "rule": "PY-EXCEPTIONS",
        "diagnostic": "S603",
        "path": "scripts/preference_roots.py",
        "symbols": ["inquire"],
        "reason": "Fixed inquiry.",
        "risk": "An unrelated caller could be added.",
        "compensating_check": "Examine the fixed argument vector.",
        "approver": "fixture examination only",
    }


def registry(entry: dict[str, object] | None = None) -> dict[str, object]:
    """Use parent defaults whose expiry is fixed independently of the host clock."""
    return {
        "schema_version": 1,
        "owner": "fixture owner",
        "tracking": "fixture card",
        "review_condition": "Remove with the call.",
        "expires": "2100-01-01",
        "entries": [exception() if entry is None else entry],
    }


def fixture(root: Path) -> Path:
    """Write a small owned source tree; no fixture source is executed."""
    (root / "scripts").mkdir()
    (root / "verification").mkdir()
    for name in RUNTIME_FILES | {CHECKER_FILE}:
        (root / name).write_text("pass\n", encoding="utf-8")
    (root / "scripts/preference_roots.py").write_text(SOURCE, encoding="utf-8")
    (root / "verification/ruff.toml").write_text(
        "[lint]\n[lint.per-file-ignores]\n", encoding="utf-8"
    )
    (root / "verification/exceptions.json").write_text(
        json.dumps(registry()), encoding="utf-8"
    )
    coverage = root / "coverage.json"
    coverage.write_text(json.dumps(proof()), encoding="utf-8")
    return coverage


class PreferenceCheckTests(unittest.TestCase):
    """Reject each missing obligation independently of a passing combined figure."""

    def test_suppression_requires_the_prescribed_preceding_comment(self) -> None:
        """A factual reason uses the recorded grammar at the immediately prior line."""
        valid = (
            "def inquire():\n"
            "    # policy-exception: PREF-EXAMPLE -- Fixed inquiry.\n"
            "    subprocess.run(arguments)  # noqa: S603\n"
        )
        for source in (
            valid,
            valid.replace(
                "Fixed inquiry.", "Fixed inquiry; noqa names one diagnostic."
            ),
        ):
            with self.subTest(source=source):
                self.assertEqual(
                    source_exceptions({"example.py": source}),
                    {
                        "PREF-EXAMPLE": ("S603", "example.py", ("inquire",)),
                    },
                )

    def test_legacy_detached_and_multiple_diagnostic_annotations_are_refused(
        self,
    ) -> None:
        """The old trailing form and misplaced metadata cannot replace the protocol."""
        prefix = (
            "def inquire():\n    # policy-exception: PREF-EXAMPLE -- Fixed inquiry.\n"
        )
        invalid = (
            "def inquire():\n    subprocess.run(arguments)  # noqa: S603  # PREF-EXAMPLE: Fixed inquiry.\n",
            "def inquire():\n    subprocess.run(arguments)  # noqa: S603\n",
            prefix + "\n    subprocess.run(arguments)  # noqa: S603\n",
            prefix.replace("Fixed inquiry.", " ")
            + "    subprocess.run(arguments)  # noqa: S603\n",
            prefix + "    subprocess.run(arguments)  # noqa: S603, S602\n",
            "def inquire():\n    value = 1 # policy-exception: PREF-EXAMPLE -- Fixed inquiry.\n    subprocess.run(arguments)  # noqa: S603\n",
            "# policy-exception: PREF-EXAMPLE -- Fixed inquiry.\nsubprocess.run(arguments)  # noqa: S603\n",
            "# pragma: no branch\n",
        )
        for source in invalid:
            with self.subTest(source=source), self.assertRaises(PreferenceCheckError):
                source_exceptions({"example.py": source})

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
                "statements": 229,
                "covered_statements": 225,
                "branches": 106,
                "covered_branches": 102,
            },
        )

    def test_exact_floors_have_independent_counts(self) -> None:
        """The oracle is five times 95/100, and a separate checker at 95/100."""
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
                "statements": 100,
                "covered_statements": 95,
                "branches": 100,
                "covered_branches": 95,
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

    def test_current_registry_and_source_waiver_agree(self) -> None:
        """One identified source call has one justified, unexpired record."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture(root)
            self.assertEqual(check_exceptions(root, registry(), {"lint": {}}, TODAY), 1)

    def test_source_inventory_refuses_missing_and_added_modules(self) -> None:
        """A plausible report cannot excuse an absent or newly unmeasured module."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture(root)
            check_source_inventory(root)
            for name in ("scripts/prepare_header.py", CHECKER_FILE):
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

    def test_registry_requires_metadata_and_existing_symbols(self) -> None:
        """Missing metadata, malformed identities and absent symbols are refused."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture(root)
            cases: list[tuple[str, object]] = [
                ("id", "bad id"),
                ("diagnostic", "PT009,PT027"),
                ("path", "outside.py"),
                ("symbols", []),
                ("symbols", ["absent"]),
                ("symbols", ["inquire", "inquire"]),
                ("reason", ""),
                ("risk", None),
                ("approver", False),
                ("compensating_check", 17),
                ("rule", ""),
            ]
            for field, value in cases:
                with (
                    self.subTest(field=field, value=value),
                    self.assertRaises(PreferenceCheckError),
                ):
                    check_exceptions(
                        root,
                        registry({**exception(), field: value}),
                        {"lint": {}},
                        TODAY,
                    )
            for field in ("owner", "tracking", "review_condition", "expires"):
                document = registry()
                del document[field]
                with self.subTest(field=field), self.assertRaises(PreferenceCheckError):
                    check_exceptions(root, document, {"lint": {}}, TODAY)

    def test_registry_rejects_missing_orphaned_duplicate_and_expired_entries(
        self,
    ) -> None:
        """The observed suppression and registry must correspond in both directions."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture(root)
            bad_documents: list[object] = [
                {**registry(), "schema_version": True},
                {**registry(), "entries": None},
                {**registry(), "entries": [None]},
                {**registry(), "entries": []},
                {**registry(), "entries": [exception(), exception()]},
                {
                    **registry(),
                    "entries": [exception(), {**exception(), "id": "SECOND"}],
                },
                registry({**exception(), "id": "ORPHAN"}),
                registry({**exception(), "expires": "2026-11-07"}),
                registry({**exception(), "expires": "invalid"}),
            ]
            for document in bad_documents:
                with self.subTest(document=document), self.assertRaises(ValueError):
                    check_exceptions(root, document, {"lint": {}}, TODAY)
            self.assertEqual(
                check_exceptions(
                    root,
                    registry({**exception(), "expires": TODAY.isoformat()}),
                    {"lint": {}},
                    TODAY,
                ),
                1,
            )

    def test_source_suppression_must_be_exact_unique_and_inside_a_function(
        self,
    ) -> None:
        """A broad pragma, repeated identity or module-level exception is refused."""
        for source in (
            "# ruff: noqa\n",
            "# type: ignore\n",
            "# pragma: no cover\n",
            "# pyright: ignore\n",
            "# noqa: S603  # PREF-EXAMPLE: Outside a function.\n",
            SOURCE + SOURCE.replace("inquire", "another"),
        ):
            with self.subTest(source=source), self.assertRaises(PreferenceCheckError):
                source_exceptions({"example.py": source})
        self.assertEqual(
            source_exceptions({"empty.py": "# ordinary remark\npass\n"}), {}
        )
        nested = "class Outer:\n    async def query(self):\n        def inner():\n            pass\n"
        self.assertEqual(
            set(definitions(nested)), {"Outer", "Outer.query", "Outer.query.inner"}
        )
        with self.assertRaisesRegex(PreferenceCheckError, "ambiguous_symbol"):
            definitions("def repeated(): pass\ndef repeated(): pass\n")

    def test_configuration_cannot_add_a_broad_or_unregistered_waiver(self) -> None:
        """Configured exceptions must be permitted, registered and annotated."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture(root)
            for lint in (
                {"ignore": ["S603"]},
                {"extend-ignore": ["S603"]},
                {"extend-per-file-ignores": {"x.py": ["S603"]}},
                {"per-file-ignores": {"absent.py": ["PT009"]}},
                {"per-file-ignores": {"scripts/preference_roots.py": ["S603"]}},
                {"per-file-ignores": {"scripts/preference_roots.py": ["PT009"]}},
            ):
                with self.subTest(lint=lint), self.assertRaises(PreferenceCheckError):
                    check_exceptions(root, registry(), {"lint": lint}, TODAY)

    def test_framework_waiver_has_named_classes_and_an_adjacent_reason(self) -> None:
        """A configured framework exception cannot drift from its source classes."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture(root)
            (root / "tests").mkdir()
            path = "tests/test_preference_example.py"
            (root / path).write_text(
                "import unittest\nclass Example(unittest.TestCase):\n    pass\n",
                encoding="utf-8",
            )
            entry = {
                **exception(),
                "id": "PREF-EXAMPLE-PT009",
                "diagnostic": "PT009",
                "path": path,
                "symbols": ["Example"],
            }
            document = {**registry(), "entries": [exception(), entry]}
            config = {"lint": {"per-file-ignores": {path: ["PT009"]}}}
            with self.assertRaisesRegex(
                PreferenceCheckError, "configured_reason_required"
            ):
                check_exceptions(root, document, config, TODAY)
            (root / "verification/ruff.toml").write_text(
                f'[lint.per-file-ignores]\n"{path}" = ["PT009"] # PREF-EXAMPLE-PT009: unittest assertions.\n',
                encoding="utf-8",
            )
            self.assertEqual(check_exceptions(root, document, config, TODAY), 2)
            (root / path).write_text(
                "import unittest\nclass Example(unittest.TestCase):\n"
                "    def inquire(self):\n"
                "        # policy-exception: PREF-EXAMPLE-PT009 -- Conflicting identity.\n"
                "        subprocess.run(arguments)  # noqa: S603\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                PreferenceCheckError, "duplicate_suppression_identity"
            ):
                check_exceptions(root, document, config, TODAY)
            (root / path).write_text("class Example:\n    pass\n", encoding="utf-8")
            with self.assertRaisesRegex(
                PreferenceCheckError, "framework_scope_mismatch"
            ):
                check_exceptions(root, document, config, TODAY)

    def test_proof_read_is_bounded_regular_and_utf8(self) -> None:
        """No directory, symlink, oversized or undecodable proof is admitted."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "proof.json"
            path.write_text("{}", encoding="utf-8")
            self.assertEqual(read_text(path), "{}")
            link = root / "link"
            link.symlink_to(path)
            for bad in (root, link):
                with self.subTest(path=bad), self.assertRaises(PreferenceCheckError):
                    read_text(bad)
            path.write_bytes(b" " * (PROOF_BYTES + 1))
            with self.assertRaisesRegex(PreferenceCheckError, "proof_size_limit"):
                read_text(path)
            path.write_bytes(b"\xff")
            with self.assertRaises(UnicodeError):
                read_text(path)

    def test_json_proof_refuses_duplicates_nonfinite_values_and_long_integers(
        self,
    ) -> None:
        """Codec admission happens before numeric counts or registry records are used."""
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "proof.json"
            path.write_text('{"count":17}', encoding="utf-8")
            self.assertEqual(load_json(path), {"count": 17})
            for content, reason in (
                ('{"count":1,"count":2}', "duplicate_proof_key"),
                ('{"count":NaN}', "nonfinite_proof_constant"),
                ('{"count":12345678901234567}', "proof_integer_limit"),
            ):
                path.write_text(content, encoding="utf-8")
                with (
                    self.subTest(content=content),
                    self.assertRaisesRegex(PreferenceCheckError, reason),
                ):
                    load_json(path)

    def test_command_reports_admission_and_refusal_distinctly(self) -> None:
        """Supported tools report exact counts; older interpreters explicitly refuse."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            coverage = fixture(root)
            arguments = ["--root", str(root), "--coverage", str(coverage)]
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = main(arguments)
            if sys.version_info < (3, 13):
                self.assertEqual(result, 2)
                self.assertIn("require Python 3.13", stderr.getvalue())
                self.assertEqual(stdout.getvalue(), "")
                return
            self.assertEqual(result, 0, stderr.getvalue())
            self.assertEqual(stderr.getvalue(), "")
            self.assertEqual(
                json.loads(stdout.getvalue()),
                {"coverage": check_coverage(proof()), "exceptions": 1},
            )
            for content in ("not JSON", "[]", json.dumps({"files": {}})):
                coverage.write_text(content, encoding="utf-8")
                stdout, stderr = io.StringIO(), io.StringIO()
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    result = main(arguments)
                self.assertEqual(result, 2)
                self.assertEqual(stdout.getvalue(), "")
                self.assertIn("incomplete or invalid proof", stderr.getvalue())
            coverage.unlink()
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                self.assertEqual(main(arguments), 2)
            coverage.write_text(json.dumps(proof()), encoding="utf-8")
            (root / "scripts/preference_unexpected.py").write_text(
                "pass\n", encoding="utf-8"
            )
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(main(arguments), 2)
