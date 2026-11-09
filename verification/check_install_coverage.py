"""Require separate statement and branch floors for installation and its checker."""

import argparse
import json
import os
import stat
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TypeGuard

INSTALL_FILES = frozenset(
    {"scripts/install.py", "scripts/install_paths.py", "scripts/release_payload.py"}
)
CHECKER_FILE = "verification/check_install_coverage.py"
COUNTS = {
    "statements": "num_statements",
    "covered_statements": "covered_lines",
    "branches": "num_branches",
    "covered_branches": "covered_branches",
}


class Arguments(argparse.Namespace):
    """Declare the measured report supplied to the repository-only command."""

    report: Path


def object_mapping(value: object) -> TypeGuard[dict[object, object]]:
    """Keep untrusted dictionary keys and values as objects."""
    return isinstance(value, dict)


def field(value: object, key: str) -> object:
    """Require an object before reading one of its fields."""
    if not object_mapping(value):
        message = "Coverage proof requires an object"
        raise ValueError(message)
    return value.get(key)


def count(value: object, key: str) -> int:
    """Admit exact nonnegative integer counts without coercion or rounding."""
    result = field(value, key)
    if type(result) is not int or result < 0:
        message = "Coverage proof requires exact nonnegative counts"
        raise ValueError(message)
    return result


def file_counts(record: object) -> dict[str, int]:
    """Refuse empty modules, exclusions and impossible coverage counts."""
    summary = field(record, "summary")
    result = {name: count(summary, source) for name, source in COUNTS.items()}
    if count(summary, "excluded_lines") or field(record, "excluded_lines") != []:
        message = "Excluded source is not admitted"
        raise ValueError(message)
    if (
        not result["statements"]
        or result["covered_statements"] > result["statements"]
        or result["covered_branches"] > result["branches"]
    ):
        message = "Coverage counts are inconsistent"
        raise ValueError(message)
    return result


def check_report(document: object) -> dict[str, dict[str, int]]:
    """Require the exact complete inventories and independent 95-percent floors."""
    files = field(document, "files")
    if (
        field(field(document, "meta"), "branch_coverage") is not True
        or not object_mapping(files)
        or frozenset(files) != INSTALL_FILES | {CHECKER_FILE}
    ):
        message = "Complete branch coverage inventory is required"
        raise ValueError(message)
    results: dict[str, dict[str, int]] = {}
    for scope, names in (("installation", INSTALL_FILES), ("checker", {CHECKER_FILE})):
        totals = dict.fromkeys(COUNTS, 0)
        for name in names:
            values = file_counts(files[name])
            for key in COUNTS:
                totals[key] += values[key]
        if (
            not totals["branches"]
            or totals["covered_statements"] * 100 < totals["statements"] * 95
            or totals["covered_branches"] * 100 < totals["branches"] * 95
        ):
            message = "Both separate coverage floors require 95 percent"
            raise ValueError(message)
        results[scope] = totals
    return results


def read_report(path: Path) -> object:
    """Read at most one MiB from an ordinary unsymlinked proof file."""
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    with os.fdopen(os.open(path, flags), "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            message = "A regular coverage proof is required"
            raise ValueError(message)
        content = stream.read(1048577)
    if len(content) > 1048576:
        message = "Coverage proof exceeds one MiB"
        raise ValueError(message)
    return json.loads(content)


def main(argv: Sequence[str] | None = None) -> int:
    """Read a bounded report and print admitted counts or refuse with status two."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    arguments = parser.parse_args(argv, namespace=Arguments())
    try:
        results = check_report(read_report(arguments.report))
    except (OSError, ValueError) as error:
        sys.stderr.write(f"Installation coverage refused: {error}\n")
        return 2
    sys.stdout.write(json.dumps(results) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
