"""Admit the complete source inventory and separate coverage dimensions."""

from pathlib import Path

from verification.preference_proofs import PreferenceCheckError, integer, mapping

RUNTIME_FILES = frozenset(
    f"scripts/{name}.py"
    for name in (
        "preference_schema",
        "preference_file",
        "preference_roots",
        "preference_header",
        "prepare_header",
    )
)
CHECKER_FILE = "verification/check_preferences.py"
CHECKER_FILES = frozenset({CHECKER_FILE}) | frozenset(
    f"verification/preference_{name}.py"
    for name in ("coverage", "proofs", "suppressions", "exceptions")
)


def check_coverage(document: object) -> dict[str, dict[str, int]]:
    """Require the complete inventory and separate exact 95-percent dimensions.

    Measure the five runtime modules together, and the new admission instrument
    separately. A strong result in one scope or dimension cannot excuse another.
    No excluded line, empty required module or absent branch evidence is admitted.
    """
    report = mapping(document)
    if mapping(report.get("meta")).get("branch_coverage") is not True:
        raise PreferenceCheckError("branch_measurement_required")
    files = mapping(report.get("files"))
    if frozenset(files) != RUNTIME_FILES | CHECKER_FILES:
        raise PreferenceCheckError("coverage_inventory_mismatch")
    results: dict[str, dict[str, int]] = {}
    for scope, names in (("runtime", RUNTIME_FILES), ("checker", CHECKER_FILES)):
        statements = covered = branches = branch_hits = 0
        for name in names:
            record = mapping(files[name])
            summary = mapping(record.get("summary"))
            count = integer(summary.get("num_statements"))
            hits = integer(summary.get("covered_lines"))
            arcs = integer(summary.get("num_branches"))
            arc_hits = integer(summary.get("covered_branches"))
            if count == 0 or hits > count or arc_hits > arcs:
                raise PreferenceCheckError("invalid_coverage_counts")
            if (
                integer(summary.get("excluded_lines")) != 0
                or record.get("excluded_lines") != []
            ):
                raise PreferenceCheckError("coverage_exclusion")
            statements += count
            covered += hits
            branches += arcs
            branch_hits += arc_hits
        if branches == 0:
            raise PreferenceCheckError("branch_evidence_empty")
        if covered * 100 < statements * 95:
            raise PreferenceCheckError("statement_floor")
        if branch_hits * 100 < branches * 95:
            raise PreferenceCheckError("branch_floor")
        results[scope] = {
            "statements": statements,
            "covered_statements": covered,
            "branches": branches,
            "covered_branches": branch_hits,
        }
    return results


def check_source_inventory(root: Path) -> None:
    """Require the same complete source inventory that the report must measure."""
    actual = {
        str(path.relative_to(root)) for path in root.glob("scripts/preference_*.py")
    }
    if (root / "scripts/prepare_header.py").is_file():
        actual.add("scripts/prepare_header.py")
    checker = {
        str(path.relative_to(root))
        for path in root.glob("verification/preference_*.py")
    }
    if (root / CHECKER_FILE).is_file():
        checker.add(CHECKER_FILE)
    if frozenset(actual) != RUNTIME_FILES or frozenset(checker) != CHECKER_FILES:
        raise PreferenceCheckError("source_inventory_mismatch")
