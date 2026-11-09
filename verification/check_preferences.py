"""Admit preference proof files through the Python 3.13 repository command."""

import argparse
import json
import sys
import tokenize
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path

from verification.preference_coverage import check_coverage, check_source_inventory
from verification.preference_exceptions import check_exceptions
from verification.preference_proofs import PreferenceCheckError, load_json, read_text


class Arguments(argparse.Namespace):
    """Declare the paths supplied to the repository-only command."""

    coverage: Path
    root: Path


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
