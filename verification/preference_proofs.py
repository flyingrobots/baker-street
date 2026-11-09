"""Read bounded proof records and admit their primitive shapes."""

import json
from pathlib import Path
from typing import TypeGuard

PROOF_BYTES = 1048576


class PreferenceCheckError(ValueError):
    """A supplied proof does not establish a required admission condition."""


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
    try:
        return json.loads(
            read_text(path),
            object_pairs_hook=unique_fields,
            parse_int=proof_integer,
            parse_constant=proof_constant,
        )
    except RecursionError as error:
        raise PreferenceCheckError("proof_nesting_limit") from error
