"""Identify the subject worktree and common Git authority with bounded output."""

import os
import select
import shutil
import subprocess
import time
from pathlib import Path


def git_roots(repository: Path) -> tuple[Path, Path]:
    """Return resolved worktree and shared-authority roots, or refuse.

    Git receives an argument vector, no inherited GIT_* settings, no user or
    system configuration, no input and no permission to prompt. The read-only
    rev-parse command has five seconds and 32768 output bytes. Diagnostics do
    not disclose Git's output. Newlines in root names are unsupported. No
    command, hook or credential is obtained from repository preferences.
    """
    executable = shutil.which("git")
    if executable is None:
        message = "Git is required to identify the subject repository"
        raise ValueError(message)
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    environment.update(
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_TERMINAL_PROMPT="0",
    )
    command = [
        executable,
        "-c",
        "core.fsmonitor=false",
        "-C",
        str(repository),
        "rev-parse",
        "--path-format=absolute",
        "--show-toplevel",
        "--git-common-dir",
    ]
    content = _bounded_git_output(command, environment)
    root, common = decode_root_names(content)
    return root.resolve(strict=True), common.resolve(strict=True)


def decode_root_names(content: bytes) -> tuple[Path, Path]:
    """Examine the two names supplied by the bounded Git inquiry."""
    names = [os.fsdecode(name) for name in content.removesuffix(b"\n").split(b"\n")]
    if len(names) != 2 or any(not Path(name).is_absolute() for name in names):
        message = "Git did not supply two unambiguous absolute roots"
        raise ValueError(message)
    return Path(names[0]), Path(names[1])


def _bounded_git_output(command: list[str], environment: dict[str, str]) -> bytes:
    """Read only this fixed Git inquiry, with a deadline and finite buffer."""
    deadline = time.monotonic() + 5
    with subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        env=environment,
    ) as process:
        try:
            stream = process.stdout
            if stream is None:
                message = "The Git inquiry has no output stream"
                raise ValueError(message)
            content = bytearray()
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not select.select([stream], [], [], remaining)[0]:
                    message = "The Git root inquiry exceeded five seconds"
                    raise ValueError(message)
                part = os.read(stream.fileno(), 4096)
                if not part:
                    break
                content.extend(part)
                if len(content) > 32768:
                    message = "The Git root inquiry exceeded 32768 bytes"
                    raise ValueError(message)
            code = process.wait(timeout=max(0.001, deadline - time.monotonic()))
            if code:
                message = "The subject is not an available Git worktree"
                raise ValueError(message)
            return bytes(content)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=1)
