"""Reserve new POSIX installation directories without following parent links."""

import os
from collections.abc import Iterator
from contextlib import ExitStack, contextmanager, suppress
from dataclasses import dataclass
from pathlib import Path


@dataclass
class InstallationTarget:
    """Keep the requested name and whether this attempt reserved its directory."""

    path: Path
    reserved: bool = False


def require_posix_operations() -> None:
    """Refuse missing descriptor operations before making directories."""
    operations = (os.open, os.mkdir, os.stat, os.link, os.unlink)
    if (
        os.name != "posix"
        or not hasattr(os, "O_NOFOLLOW")
        or not hasattr(os, "O_DIRECTORY")
        or any(operation not in os.supports_dir_fd for operation in operations)
    ):
        message = "POSIX directory descriptor operations are required"
        raise ValueError(message)


def open_directory(name: str, parent: int) -> int:
    """Open one existing directory without following its final component."""
    return os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)


@contextmanager
def reserve(target: InstallationTarget) -> Iterator[tuple[int, int]]:
    """Create parents deliberately and reserve an absent final name exclusively."""
    path = target.path
    if not path.is_absolute() or ".." in path.parts or len(path.parts) > 64:
        message = "An absolute destination without parent traversal is required"
        raise ValueError(message)
    if len(path.parts) < 2:
        message = "The filesystem root is not an installation destination"
        raise ValueError(message)
    with ExitStack() as cleanup:
        parent = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        cleanup.callback(os.close, parent)
        for component in path.parts[1:-1]:
            try:
                child = open_directory(component, parent)
            except FileNotFoundError:
                os.mkdir(component, mode=0o700, dir_fd=parent)
                child = open_directory(component, parent)
            cleanup.callback(os.close, child)
            parent = child
        os.mkdir(path.name, mode=0o700, dir_fd=parent)
        target.reserved = True
        directory = open_directory(path.name, parent)
        cleanup.callback(os.close, directory)
        yield parent, directory


def require_binding(parent: int, directory: int, name: str) -> None:
    """Refuse a final name which no longer denotes the reserved directory."""
    observed = os.stat(name, dir_fd=parent, follow_symlinks=False)
    owned = os.fstat(directory)
    if (observed.st_dev, observed.st_ino) != (owned.st_dev, owned.st_ino):
        message = "The installation destination changed during the copy"
        raise ValueError(message)


@contextmanager
def payload_parent(directory: int, name: str) -> Iterator[tuple[int, str]]:
    """Open or create the reviewed payload's parents within the reserved tree."""
    parts = name.split("/")
    if any(part in {"", ".", ".."} for part in parts) or "\\" in name:
        message = "A relative canonical payload name is required"
        raise ValueError(message)
    with ExitStack() as cleanup:
        parent = directory
        for component in parts[:-1]:
            with suppress(FileExistsError):
                os.mkdir(component, mode=0o700, dir_fd=parent)
            parent = open_directory(component, parent)
            cleanup.callback(os.close, parent)
        yield parent, parts[-1]
