"""Run fixed installation trials and preserve their owned source inventories."""

import os
import shutil
import subprocess
from pathlib import Path

from scripts.build_release import SKILL_FILES

ROOT = Path(__file__).resolve().parents[1]


def command(
    arguments: list[str], directory: Path, overrides: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    """Run fixed installation trials without inherited Python lookup paths."""
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in {"PYTHONPATH", "PYTHONHOME", "BAKER_STREET_DESTINATION"}
    }
    environment.update(overrides or {})
    # policy-exception: INSTALL-FIXTURE-COMMAND -- Fixed commands and owned fixture paths.
    return subprocess.run(  # noqa: S603
        arguments,
        cwd=directory,
        env=environment,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )


def inventory(root: Path) -> dict[str, bytes]:
    """Read ordinary files in an owned tree without traversing symbolic links."""
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in root.rglob("*")
        if not path.is_symlink() and path.is_file()
    }


def source_copy(base: Path) -> Path:
    """Copy the actual reviewed inputs and maintained commands into owned space."""
    root = base / "source"
    names = (
        *SKILL_FILES,
        "scripts/build_release.py",
        "scripts/release_payload.py",
        "scripts/install.py",
        "scripts/install_paths.py",
    )
    for name in names:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    return root
