"""Read the bounded reviewed inclusion list and construct its checksum manifest."""

import hashlib
import os
import stat
from pathlib import Path, PurePosixPath

FILE_BYTES = 1048576
PAYLOAD_BYTES = 4194304


def read_payload(root: Path, names: tuple[str, ...]) -> dict[str, bytes]:
    """Read regular, unsymlinked selected files before any destination is created."""
    payload: dict[str, bytes] = {}
    total = 0
    for name in sorted(names):
        parts = PurePosixPath(name).parts
        if (
            not parts
            or name.startswith("/")
            or ".." in parts
            or "\\" in name
            or str(PurePosixPath(name)) != name
            or name == "SHA256SUMS"
            or name in payload
        ):
            message = "Invalid release inclusion name"
            raise ValueError(message)
        source = root / name
        if any(path.is_symlink() for path in (source, *source.parents)):
            message = f"Symlinks are not release inputs: {name}"
            raise ValueError(message)
        flags = (
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        )
        with os.fdopen(os.open(source, flags), "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                message = f"Regular release input required: {name}"
                raise ValueError(message)
            content = stream.read(FILE_BYTES + 1)
        total += len(content)
        if len(content) > FILE_BYTES or total > PAYLOAD_BYTES:
            message = "Release payload exceeds its byte allowance"
            raise ValueError(message)
        payload[name] = content
    payload["SHA256SUMS"] = "".join(
        f"{hashlib.sha256(content).hexdigest()}  {name}\n"
        for name, content in payload.items()
    ).encode("utf-8")
    return payload
