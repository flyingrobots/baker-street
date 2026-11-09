"""Prepare a case header from explicit inputs and bounded repository defaults."""

import argparse
import json
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TypeGuard

from scripts.preference_header import prepare_header
from scripts.preference_schema import Preferences

HEADER_BYTES = 262144


class Arguments(argparse.Namespace):
    """Declare the values supplied by the argument parser."""

    repository: Path
    header: Path
    case_root: Path | None
    plain: bool | None
    tier: str | None


def _is_mapping(value: object) -> TypeGuard[dict[object, object]]:
    """Narrow container shape while retaining untrusted keys and values."""
    return isinstance(value, dict)


def _is_header(value: object) -> TypeGuard[dict[str, object]]:
    """Admit the root object and string-key shape without trusting its values."""
    return _is_mapping(value) and all(isinstance(key, str) for key in value)


def _integer(token: str) -> int:
    """Bound integer conversion in the explicit header input."""
    if len(token) > 128:
        message = "A header integer exceeds 128 characters"
        raise ValueError(message)
    return int(token)


def _constant(token: str) -> object:
    """Refuse nonfinite JSON constants without quoting their source."""
    del token
    message = "Nonfinite header values are not supported"
    raise ValueError(message)


def load_header(path: Path) -> dict[str, object]:
    """Read an operator-supplied JSON header, bounded to 262144 UTF-8 bytes.

    This explicit input is not discovered in the subject repository. File and
    decoding errors propagate. Deep JSON may be refused with RecursionError;
    the command reports that refusal without producing a partial header.
    """
    with path.open("rb") as stream:
        content = stream.read(HEADER_BYTES + 1)
    if len(content) > HEADER_BYTES:
        message = "The header exceeds 262144 bytes"
        raise ValueError(message)
    value: object = json.loads(
        content.decode("utf-8"), parse_int=_integer, parse_constant=_constant
    )
    if not _is_header(value):
        message = "The supplied header must be an object"
        raise ValueError(message)
    return value


def main(argv: Sequence[str] | None = None) -> int:
    """Write the prepared header to stdout, or a refusal to stderr with code 2."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--header", type=Path, required=True)
    parser.add_argument("--case-root", type=Path)
    parser.add_argument("--plain", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--tier", choices=("triage", "focused", "standard"))
    args = parser.parse_args(argv, namespace=Arguments())
    try:
        header = prepare_header(
            args.repository,
            load_header(args.header),
            invocation=Preferences(plain=args.plain, tier=args.tier),
            case_root=args.case_root,
        )
        encoded = json.dumps(header, ensure_ascii=False, indent=2, allow_nan=False)
        encoded.encode("utf-8")
    except OSError:
        sys.stderr.write("Header not prepared: repository files could not be read.\n")
        return 2
    except (ValueError, TypeError, RecursionError, subprocess.SubprocessError):
        sys.stderr.write("Header not prepared: the supplied inputs were refused.\n")
        return 2
    sys.stdout.write(encoded + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
