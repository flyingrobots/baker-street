"""Reconcile source and configured exceptions with justified registry records."""

import re
from datetime import date
from pathlib import Path

from verification.preference_coverage import CHECKER_FILES
from verification.preference_proofs import (
    PreferenceCheckError,
    mapping,
    object_array,
    read_text,
    strings,
    text,
)
from verification.preference_suppressions import definitions, source_exceptions


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
        *root.glob("tests/*preference*.py"),
    }
    paths.update(
        root / name
        for name in (
            "scripts/prepare_header.py",
            "verification/__init__.py",
            *CHECKER_FILES,
        )
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
