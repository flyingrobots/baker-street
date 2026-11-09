"""Read one bounded repository preference snapshot without granting authority."""

import os
import stat
from pathlib import Path

from scripts.preference_schema import (
    MAX_PREFERENCE_BYTES,
    Preferences,
    decode_preferences,
)


def read_preferences(repository_root: Path) -> Preferences:
    """Read `.bakerstreetrc` at an already identified Git worktree root.

    The caller identifies the subject's actual root; this operation neither
    discovers a repository nor searches ancestors or a home directory. An absent
    file yields unset preferences. All other open, type and decoding failures
    propagate. The POSIX reader pins the root directory and file descriptors,
    refuses a final symlink and nonregular files without waiting on a pipe, and
    reads at most 8193 bytes. It creates no file or directory.
    """
    if os.name != "posix" or not hasattr(os, "O_NOFOLLOW"):
        message = "Preference reading requires POSIX O_NOFOLLOW admission"
        raise ValueError(message)
    flags = os.O_RDONLY | os.O_CLOEXEC
    root_descriptor = os.open(repository_root, flags | os.O_DIRECTORY)
    try:
        try:
            descriptor = os.open(
                ".bakerstreetrc",
                flags | os.O_NOFOLLOW | os.O_NONBLOCK,
                dir_fd=root_descriptor,
            )
        except FileNotFoundError:
            return Preferences()
        try:
            information = os.fstat(descriptor)
            if not stat.S_ISREG(information.st_mode):
                message = "The repository preference file must be regular"
                raise ValueError(message)
            if information.st_size > MAX_PREFERENCE_BYTES:
                message = "Repository preferences exceed 8192 bytes"
                raise ValueError(message)
            with os.fdopen(descriptor, "rb", closefd=False) as stream:
                content = stream.read(MAX_PREFERENCE_BYTES + 1)
            return decode_preferences(content)
        finally:
            os.close(descriptor)
    finally:
        os.close(root_descriptor)


def _case_path(path: Path) -> Path:
    """Resolve existing links and admit only directory ancestors or missing tails."""
    try:
        resolved = path.resolve()
    except RuntimeError as error:
        message = "A case destination contains an unresolved symbolic link"
        raise ValueError(message) from error
    for ancestor in (resolved, *resolved.parents):
        try:
            information = ancestor.lstat()
        except FileNotFoundError:
            continue
        if not stat.S_ISDIR(information.st_mode):
            message = "A case destination requires resolved directory ancestors"
            raise ValueError(message)
    return resolved


def case_destination(
    preferences: Preferences,
    case_root: Path | None,
    repository_root: Path,
    git_common_directory: Path,
) -> Path | None:
    """Resolve a preference beneath a trusted operator's case root.

    Return None when no directory preference is present. Otherwise require a
    case root, resolve existing links, and refuse escapes or destinations in the
    subject checkout or its shared Git authority. Paths need not exist. This
    creates nothing and makes no promise against later filesystem changes; the
    eventual writer must repeat admission when it acts. Resolution errors
    propagate instead of selecting an alternate destination.
    """
    if preferences.case_directory is None:
        return None
    if case_root is None:
        message = "A case_directory preference requires an operator case root"
        raise ValueError(message)
    root = _case_path(case_root)
    destination = _case_path(root / preferences.case_directory)
    if destination == root or not destination.is_relative_to(root):
        message = "The preferred destination escapes the operator case root"
        raise ValueError(message)
    for forbidden in (repository_root.resolve(), git_common_directory.resolve()):
        if destination.is_relative_to(forbidden):
            message = "The preferred destination must remain outside the subject"
            raise ValueError(message)
    return destination
