"""Construct independent coverage counts and owned exception-source trees."""

import json
from datetime import date
from pathlib import Path
from typing import TypedDict

from verification.preference_coverage import CHECKER_FILES, RUNTIME_FILES

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
    for name in RUNTIME_FILES | CHECKER_FILES:
        files[name] = {
            "summary": {
                "num_statements": 100,
                "covered_lines": checker_hits
                if name in CHECKER_FILES
                else runtime_hits,
                "num_branches": 100,
                "covered_branches": checker_arcs
                if name in CHECKER_FILES
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
    for name in RUNTIME_FILES | CHECKER_FILES:
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
