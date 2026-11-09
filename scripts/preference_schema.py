"""Decode bounded, flat repository preferences without admitting authority."""

import json
from dataclasses import dataclass
from typing import TypeGuard

MAX_PREFERENCE_BYTES = 8192
FIELDS = frozenset({"schema_version", "plain", "tier", "case_directory"})
TIERS = frozenset({"triage", "focused", "standard"})


def _plain(value: object) -> bool | None:
    """Admit only an absent value or an exact Boolean."""
    if value is None or isinstance(value, bool):
        return value
    message = "The plain preference must be a Boolean"
    raise ValueError(message)


def _tier(value: object) -> str | None:
    """Admit only a named review tier or absence."""
    if value is None:
        return None
    if isinstance(value, str) and value in TIERS:
        return value
    message = "The tier preference must be triage, focused or standard"
    raise ValueError(message)


def _directory(value: object) -> str | None:
    """Admit a bounded relative subdirectory, preserving its exact spelling."""
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        message = "The case_directory preference must be a nonempty string"
        raise ValueError(message)
    if len(value.encode("utf-8")) > 1024:
        message = "The case_directory preference exceeds 1024 UTF-8 bytes"
        raise ValueError(message)
    if "\\" in value or any(
        ord(character) < 32 or ord(character) == 127 for character in value
    ):
        message = "The case_directory preference contains a forbidden character"
        raise ValueError(message)
    parts = value.split("/")
    if len(parts) > 16 or any(part in {"", ".", ".."} for part in parts):
        message = "The case_directory preference must name a relative subdirectory"
        raise ValueError(message)
    if ":" in parts[0]:
        message = "The case_directory preference must not name a drive or scheme"
        raise ValueError(message)
    return value


@dataclass(frozen=True, slots=True)
class Preferences:
    """Hold immutable ordinary defaults, never commands or permissions.

    Construction validates all members, including construction through
    dataclasses.replace. Raw file values enter through decode_preferences.
    """

    plain: bool | None = None
    tier: str | None = None
    case_directory: str | None = None

    def __post_init__(self) -> None:
        """Validate every supported construction path."""
        _plain(self.plain)
        _tier(self.tier)
        _directory(self.case_directory)


def _flat_document(text: str) -> None:
    """Refuse containers beyond the root before recursive JSON decoding."""
    quoted = False
    escaped = False
    depth = 0
    for character in text:
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
        elif character == '"':
            quoted = True
        elif character in "[{":
            depth += 1
            if depth > 1 or character == "[":
                message = "Repository preferences must be a flat object"
                raise ValueError(message)
        elif character == "}":
            depth -= 1


def _integer(token: str) -> int:
    """Bound numeric work before conversion."""
    if len(token) > 8:
        message = "A preference integer exceeds eight characters"
        raise ValueError(message)
    return int(token)


def _not_a_number(token: str) -> object:
    """Refuse floating-point and nonstandard numbers without echoing input."""
    del token
    message = "Floating-point and nonfinite preferences are not supported"
    raise ValueError(message)


def _unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Preserve the decoder's string keys and refuse duplicates."""
    fields: dict[str, object] = {}
    for key, value in pairs:
        if key in fields:
            message = "A repository preference field is repeated"
            raise ValueError(message)
        fields[key] = value
    return fields


def _is_object_mapping(value: object) -> TypeGuard[dict[object, object]]:
    """Narrow container shape only; every key and value remains untrusted."""
    return isinstance(value, dict)


def _fields(document: object) -> dict[str, object]:
    """Validate the decoded object before admitting its fields."""
    if not _is_object_mapping(document):
        message = "Repository preferences must be an object"
        raise ValueError(message)
    raw: dict[object, object] = document
    fields: dict[str, object] = {}
    for key, value in raw.items():
        if not isinstance(key, str) or key not in FIELDS:
            message = "An unrecognised repository preference field is present"
            raise ValueError(message)
        fields[key] = value
    version = fields.get("schema_version")
    if type(version) is not int or version != 1:
        message = "Repository preferences require integer schema_version 1"
        raise ValueError(message)
    for key in ("plain", "tier", "case_directory"):
        if key in fields and fields[key] is None:
            message = "An optional preference must be absent rather than null"
            raise ValueError(message)
    return fields


def decode_preferences(content: bytes) -> Preferences:
    """Read at most 8192 UTF-8 bytes into strictly validated ordinary defaults.

    This pure operation performs no filesystem access, command execution or
    publication. Invalid syntax, size, structure, version and values raise
    ValueError; undecodable UTF-8 raises its UnicodeDecodeError subtype.
    """
    if len(content) > MAX_PREFERENCE_BYTES:
        message = "Repository preferences exceed 8192 bytes"
        raise ValueError(message)
    text = content.decode("utf-8")
    _flat_document(text)
    document: object = json.loads(
        text,
        object_pairs_hook=_unique_pairs,
        parse_int=_integer,
        parse_float=_not_a_number,
        parse_constant=_not_a_number,
    )
    fields = _fields(document)
    return Preferences(
        plain=_plain(fields.get("plain")),
        tier=_tier(fields.get("tier")),
        case_directory=_directory(fields.get("case_directory")),
    )
