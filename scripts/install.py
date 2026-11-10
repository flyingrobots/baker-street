"""Install the reviewed skill payload into a new, explicitly admitted directory."""

import argparse
import json
import os
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import BinaryIO

from scripts.build_release import ROOT, SKILL_FILES
from scripts.install_paths import (
    InstallationTarget,
    payload_parent,
    require_binding,
    require_posix_operations,
    reserve,
)
from scripts.release_payload import read_payload

MARKER = ".baker-street-incomplete"
PENDING = ".baker-street-SKILL.pending"


class Arguments(argparse.Namespace):
    """Declare the sole optional destination argument."""

    destination: str | None


def destination_path(explicit: str | None, environment: Mapping[str, str]) -> Path:
    """Apply explicit choice, dedicated environment choice, then the host default."""
    value = (
        explicit
        if explicit is not None
        else environment.get("BAKER_STREET_DESTINATION")
    )
    if value is None:
        return Path.home() / ".agents" / "skills" / "baker-street"
    if not value or "\x00" in value:
        message = "A nonempty destination without a NUL character is required"
        raise ValueError(message)
    return Path(value).expanduser().absolute()


def verify_copy(stream: BinaryIO, content: bytes) -> None:
    """Refuse read-back bytes which differ from the complete admitted file."""
    stream.seek(0)
    if stream.read(len(content) + 1) != content:
        message = "Installed bytes differ from the admitted payload"
        raise ValueError(message)


def write_verified(directory: int, name: str, content: bytes) -> None:
    """Create a file exclusively and read back its complete bytes before return."""
    with payload_parent(directory, name) as (parent, leaf):
        flags = os.O_CREAT | os.O_EXCL | os.O_RDWR | os.O_NOFOLLOW
        with os.fdopen(os.open(leaf, flags, 0o600, dir_fd=parent), "w+b") as stream:
            stream.write(content)
            stream.flush()
            verify_copy(stream, content)


def _install(target: InstallationTarget, payload: dict[str, bytes]) -> Path:
    """Keep incomplete output and publish the entry point only after verification."""
    with reserve(target) as (parent, directory):
        write_verified(
            directory, MARKER, b"Incomplete installation; inspect before recovery.\n"
        )
        for name, content in payload.items():
            write_verified(directory, PENDING if name == "SKILL.md" else name, content)
        require_binding(parent, directory, target.path.name)
        os.link(
            PENDING,
            "SKILL.md",
            src_dir_fd=directory,
            dst_dir_fd=directory,
            follow_symlinks=False,
        )
        require_binding(parent, directory, target.path.name)
        os.unlink(PENDING, dir_fd=directory)
        os.unlink(MARKER, dir_fd=directory)
        require_binding(parent, directory, target.path.name)
    return target.path / "SKILL.md"


def main(argv: Sequence[str] | None = None) -> int:
    """Report one actual installed entry point, or a truthful retained-destination refusal."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination")
    arguments = parser.parse_args(argv, namespace=Arguments())
    target: InstallationTarget | None = None
    try:
        require_posix_operations()
        target = InstallationTarget(destination_path(arguments.destination, os.environ))
        payload = read_payload(ROOT, SKILL_FILES)
        entrypoint = _install(target, payload)
    except (OSError, ValueError, RuntimeError) as error:
        refusal = {
            "error": "installation_refused",
            "destination": str(target.path) if target else None,
            "retained_destination": target.reserved if target else False,
            "reason": str(error),
        }
        sys.stderr.write(json.dumps(refusal, ensure_ascii=True) + "\n")
        return 2
    sys.stdout.write(
        json.dumps({"entrypoint": str(entrypoint)}, ensure_ascii=True) + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
