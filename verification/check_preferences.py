"""Admit preference coverage and exception records; the CLI requires Python 3.13."""

import argparse
import ast
import io
import json
import re
import sys
import tokenize
from collections.abc import Sequence
from datetime import date, datetime, timezone
from pathlib import Path
from typing import TypeGuard

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
PROOF_BYTES = 1048576


class PreferenceCheckError(ValueError):
    """A supplied proof does not establish a required admission condition."""


class Arguments(argparse.Namespace):
    """Declare the paths supplied to the repository-only command."""

    coverage: Path
    root: Path


def object_mapping(value: object) -> TypeGuard[dict[object, object]]:
    """Narrow only the container, retaining untrusted keys and values."""
    return isinstance(value, dict)


def object_array(value: object) -> TypeGuard[list[object]]:
    """Narrow an array without admitting its elements."""
    return isinstance(value, list)


def mapping(value: object) -> dict[str, object]:
    """Require an object whose field names are strings."""
    if not object_mapping(value) or any(not isinstance(key, str) for key in value):
        raise PreferenceCheckError("object_required")
    return {key: item for key, item in value.items() if isinstance(key, str)}


def text(value: object) -> str:
    """Require a nonempty string without coercion."""
    if not isinstance(value, str) or not value.strip():
        raise PreferenceCheckError("text_required")
    return value


def strings(value: object) -> list[str]:
    """Require a nonempty array of distinct strings."""
    if not object_array(value) or not value:
        raise PreferenceCheckError("string_array_required")
    result = [text(item) for item in value]
    if len(set(result)) != len(result):
        raise PreferenceCheckError("duplicate_string")
    return result


def integer(value: object) -> int:
    """Admit nonnegative exact integer counts, including zero."""
    if type(value) is not int or value < 0:
        raise PreferenceCheckError("count_required")
    return value


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
    if frozenset(files) != RUNTIME_FILES | frozenset({CHECKER_FILE}):
        raise PreferenceCheckError("coverage_inventory_mismatch")
    results: dict[str, dict[str, int]] = {}
    for scope, names in (("runtime", RUNTIME_FILES), ("checker", {CHECKER_FILE})):
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


def read_text(path: Path) -> str:
    """Read at most one MiB from an owned regular proof or source file."""
    if path.is_symlink() or not path.is_file():
        raise PreferenceCheckError("regular_proof_file_required")
    with path.open("rb") as stream:
        content = stream.read(PROOF_BYTES + 1)
    if len(content) > PROOF_BYTES:
        raise PreferenceCheckError("proof_size_limit")
    return content.decode("utf-8")


def unique_fields(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Refuse repeated JSON fields instead of silently retaining the last value."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise PreferenceCheckError("duplicate_proof_key")
        result[key] = value
    return result


def proof_integer(token: str) -> int:
    """Bound integer conversion before admitting a JSON numeric token."""
    if len(token) > 16:
        raise PreferenceCheckError("proof_integer_limit")
    return int(token)


def proof_constant(_token: str) -> object:
    """Refuse nonfinite constants which are outside the JSON proof format."""
    raise PreferenceCheckError("nonfinite_proof_constant")


def load_json(path: Path) -> object:
    """Read one bounded JSON proof, preserving duplicate-field refusals."""
    return json.loads(
        read_text(path),
        object_pairs_hook=unique_fields,
        parse_int=proof_integer,
        parse_constant=proof_constant,
    )


def definitions(source: str) -> dict[str, tuple[int, int, str]]:
    """Record qualified class and function extents without executing source."""
    result: dict[str, tuple[int, int, str]] = {}

    def visit(node: ast.AST, prefix: str) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix + child.name
                if name in result or child.end_lineno is None:
                    raise PreferenceCheckError("ambiguous_symbol")
                kind = "function"
                if isinstance(child, ast.ClassDef):
                    kind = (
                        "test"
                        if any(
                            ast.unparse(base) == "unittest.TestCase"
                            for base in child.bases
                        )
                        else "class"
                    )
                result[name] = (child.lineno, child.end_lineno, kind)
                visit(child, name + ".")
            else:
                visit(child, prefix)

    visit(ast.parse(source), "")
    return result


def source_exceptions(
    sources: dict[str, str],
) -> dict[str, tuple[str, str, tuple[str, ...]]]:
    """Inventory exact source suppressions and their actual enclosing symbols."""
    result: dict[str, tuple[str, str, tuple[str, ...]]] = {}
    pattern = r"# noqa: (S603)  # ([A-Z][A-Z0-9-]+): \S.+"
    for path, source in sources.items():
        symbols = definitions(source)
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            if token.type != tokenize.COMMENT:
                continue
            if not any(
                marker in token.string.lower()
                for marker in (
                    "noqa",
                    "type: ignore",
                    "pyright: ignore",
                    "pragma: no cover",
                )
            ):
                continue
            match = re.fullmatch(pattern, token.string)
            if match is None:
                raise PreferenceCheckError("unsupported_source_suppression")
            diagnostic, identifier = match.groups()
            candidates = [
                name
                for name, (start, end, kind) in symbols.items()
                if kind == "function" and start <= token.start[0] <= end
            ]
            if not candidates or identifier in result:
                raise PreferenceCheckError("ambiguous_source_suppression")
            symbol = max(candidates, key=lambda name: name.count("."))
            result[identifier] = (diagnostic, path, (symbol,))
    return result


def check_metadata(
    entry: dict[str, object], registry: dict[str, object], today: date
) -> None:
    """Require each entry's effective metadata and an unexpired canonical date."""
    for field in ("owner", "tracking", "review_condition", "expires"):
        text(entry.get(field, registry.get(field)))
    for field in ("rule", "reason", "risk", "compensating_check", "approver"):
        text(entry.get(field))
    expiry = text(entry.get("expires", registry.get("expires")))
    expires = date.fromisoformat(expiry)
    if expires.isoformat() != expiry or expires < today:
        raise PreferenceCheckError("expired_or_invalid_entry")


def registry_records(
    document: object,
    sources: dict[str, str],
    today: date,
) -> dict[str, tuple[str, str, tuple[str, ...]]]:
    """Require identified, justified, current entries with existing named symbols."""
    registry = mapping(document)
    if (
        type(registry.get("schema_version")) is not int
        or registry.get("schema_version") != 1
    ):
        raise PreferenceCheckError("registry_version")
    values = registry.get("entries")
    if not object_array(values):
        raise PreferenceCheckError("entries_required")
    result: dict[str, tuple[str, str, tuple[str, ...]]] = {}
    for value in values:
        entry = mapping(value)
        check_metadata(entry, registry, today)
        identifier = text(entry.get("id"))
        diagnostic = text(entry.get("diagnostic"))
        path = text(entry.get("path"))
        names = strings(entry.get("symbols"))
        if re.fullmatch(r"[A-Z][A-Z0-9-]+", identifier) is None or identifier in result:
            raise PreferenceCheckError("duplicate_or_invalid_identity")
        if re.fullmatch(r"[A-Z]+[0-9]+", diagnostic) is None:
            raise PreferenceCheckError("one_diagnostic_required")
        if path not in sources or not set(names) <= definitions(sources[path]).keys():
            raise PreferenceCheckError("missing_exception_scope")
        record = (diagnostic, path, tuple(sorted(names)))
        if record in result.values():
            raise PreferenceCheckError("duplicate_exception_scope")
        result[identifier] = record
    return result


def configured_exceptions(
    config: object,
    config_source: str,
    sources: dict[str, str],
    records: dict[str, tuple[str, str, tuple[str, ...]]],
) -> dict[str, tuple[str, str, tuple[str, ...]]]:
    """Reconcile only the named unittest framework exceptions with Ruff settings."""
    lint = mapping(mapping(config).get("lint"))
    if any(
        lint.get(field)
        for field in ("ignore", "extend-ignore", "extend-per-file-ignores")
    ):
        raise PreferenceCheckError("broad_lint_suppression")
    configured = mapping(lint.get("per-file-ignores", {}))
    result: dict[str, tuple[str, str, tuple[str, ...]]] = {}
    for path, value in configured.items():
        if path not in sources:
            raise PreferenceCheckError("unknown_configured_scope")
        for diagnostic in strings(value):
            if diagnostic not in {"PT009", "PT027"}:
                raise PreferenceCheckError("unsupported_file_suppression")
            matches = [
                identifier
                for identifier, record in records.items()
                if record[:2] == (diagnostic, path)
            ]
            if len(matches) != 1:
                raise PreferenceCheckError("missing_configured_exception")
            identifier = matches[0]
            lines = [
                line
                for line in config_source.splitlines()
                if re.fullmatch(
                    rf"\s*[\"']{re.escape(path)}[\"']\s*=.*", line.split("#", 1)[0]
                )
            ]
            if (
                len(lines) != 1
                or re.search(rf"(?:# |; ){re.escape(identifier)}: \S", lines[0]) is None
            ):
                raise PreferenceCheckError("configured_reason_required")
            classes = tuple(
                sorted(
                    name
                    for name, (_, _, kind) in definitions(sources[path]).items()
                    if kind == "test"
                )
            )
            if not classes or records[identifier][2] != classes:
                raise PreferenceCheckError("framework_scope_mismatch")
            result[identifier] = (diagnostic, path, classes)
    return result


def check_exceptions(root: Path, registry: object, config: object, today: date) -> int:
    """Reject missing, orphaned, duplicate, expired or incorrectly scoped waivers.

    This establishes correspondence and required metadata, not review approval.
    Parent owner, tracking, removal condition and expiry are explicit defaults.
    """
    paths = {
        *root.glob("scripts/preference_*.py"),
        *root.glob("tests/test_preference_*.py"),
    }
    paths.update(
        root / name
        for name in ("scripts/prepare_header.py", CHECKER_FILE)
        if (root / name).exists()
    )
    sources = {str(path.relative_to(root)): read_text(path) for path in paths}
    records = registry_records(registry, sources, today)
    observed = source_exceptions(sources)
    configured = configured_exceptions(
        config, read_text(root / "verification/ruff.toml"), sources, records
    )
    if set(observed) & set(configured):
        raise PreferenceCheckError("duplicate_suppression_identity")
    if records != {**observed, **configured}:
        raise PreferenceCheckError("missing_or_orphaned_exception")
    return len(records)


def check_source_inventory(root: Path) -> None:
    """Require the same complete source inventory that the report must measure."""
    actual = {
        str(path.relative_to(root)) for path in root.glob("scripts/preference_*.py")
    }
    if (root / "scripts/prepare_header.py").is_file():
        actual.add("scripts/prepare_header.py")
    if frozenset(actual) != RUNTIME_FILES or not (root / CHECKER_FILE).is_file():
        raise PreferenceCheckError("source_inventory_mismatch")


def main(argv: Sequence[str] | None = None) -> int:
    """Read bounded proofs and report exact admitted counts, or refuse with code 2."""
    if sys.version_info < (3, 13):
        sys.stderr.write("Preference checks require Python 3.13.\n")
        return 2
    import tomllib

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage", type=Path, required=True)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args(argv, namespace=Arguments())
    try:
        root: Path = args.root
        check_source_inventory(root)
        coverage = check_coverage(load_json(args.coverage))
        count = check_exceptions(
            root,
            load_json(root / "verification/exceptions.json"),
            tomllib.loads(read_text(root / "verification/ruff.toml")),
            datetime.now(timezone.utc).date(),
        )
    except PreferenceCheckError as error:
        sys.stderr.write(
            f"Preference checks refused: incomplete or invalid proof ({error}).\n"
        )
        return 2
    except (OSError, ValueError, TypeError, SyntaxError, tokenize.TokenError):
        sys.stderr.write("Preference checks refused: incomplete or invalid proof.\n")
        return 2
    sys.stdout.write(json.dumps({"coverage": coverage, "exceptions": count}) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
