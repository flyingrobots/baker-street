"""Exercise installation admission and source bounds with real owned files."""

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from scripts.install import main, verify_copy
from scripts.install_paths import (
    InstallationTarget,
    payload_parent,
    require_binding,
    reserve,
)
from scripts.release_payload import FILE_BYTES, read_payload

ROOT = Path(__file__).resolve().parents[1]


class InstallAdmissionTests(unittest.TestCase):
    """Admit bounded ordinary files and retain evidence on explicit refusal."""

    def test_main_reports_success_and_refusal_with_actual_copies(self) -> None:
        """Exercise command admission directly as well as the separate process trials."""
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary).resolve() / "parents" / "new"
            arguments = ["--destination", str(destination)]
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                self.assertEqual(main(arguments), 0)
            self.assertEqual(
                json.loads(stdout.getvalue()),
                {"entrypoint": str(destination / "SKILL.md")},
            )
            self.assertEqual(stderr.getvalue(), "")
            for bad in (str(destination), ""):
                stdout, stderr = io.StringIO(), io.StringIO()
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    self.assertEqual(main(["--destination", bad]), 2)
                self.assertEqual(stdout.getvalue(), "")
                self.assertEqual(
                    json.loads(stderr.getvalue())["error"], "installation_refused"
                )

    def test_source_bounds_names_links_and_nonregular_inputs_are_refused(self) -> None:
        """No selected file or combined payload may exceed the recorded allowance."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            path = root / "SKILL.md"
            path.write_bytes(b"reviewed instructions")
            payload = read_payload(root, ("SKILL.md",))
            self.assertEqual(payload["SKILL.md"], b"reviewed instructions")
            self.assertIn(b"  SKILL.md\n", payload["SHA256SUMS"])
            for names in (
                ("../outside",),
                ("/outside",),
                ("a/./b",),
                ("SHA256SUMS",),
                ("SKILL.md", "SKILL.md"),
            ):
                with self.subTest(names=names), self.assertRaises(ValueError):
                    read_payload(root, names)
            alias = root / "alias"
            alias.symlink_to(path)
            with self.assertRaises(ValueError):
                read_payload(root, ("alias",))
            fifo = root / "fifo"
            os.mkfifo(fifo)
            with self.assertRaises(ValueError):
                read_payload(root, ("fifo",))
            path.write_bytes(b"x" * (FILE_BYTES + 1))
            with self.assertRaises(ValueError):
                read_payload(root, ("SKILL.md",))
            names = tuple(f"part-{index}" for index in range(5))
            for name in names:
                (root / name).write_bytes(b"x" * FILE_BYTES)
            with self.assertRaises(ValueError):
                read_payload(root, names)

    def test_reservation_refuses_traversal_and_changed_final_binding(self) -> None:
        """Descriptor ownership does not grant authority to follow a replaced name."""
        for path in (
            Path("relative"),
            Path("/"),
            Path("/boundary/../refused"),
            Path("/").joinpath(*(["a"] * 64)),
        ):
            with (
                self.subTest(path=path),
                self.assertRaises(ValueError),
                reserve(InstallationTarget(path)),
            ):
                self.fail("An invalid reservation was admitted")
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            target = InstallationTarget(base / "reserved")
            with reserve(target) as (parent, directory):
                target.path.rename(base / "moved")
                target.path.mkdir()
                with self.assertRaises(ValueError):
                    require_binding(parent, directory, target.path.name)

    def test_installation_files_respect_the_unexcepted_locality_limit(self) -> None:
        """No installation source or test file has an approved locality exception."""
        paths = {
            *ROOT.glob("scripts/install*.py"),
            *ROOT.glob("tests/*install*.py"),
            ROOT / "scripts/release_payload.py",
            ROOT / "verification/check_install_coverage.py",
            ROOT / "verification/check_install_coverage.py",
        }
        for path in sorted(paths):
            lines = path.read_text(encoding="utf-8").splitlines()
            count = sum(
                bool(line.strip()) and not line.lstrip().startswith("#")
                for line in lines
            )
            with self.subTest(path=path.name):
                self.assertLessEqual(count, 300)

    def test_readback_refuses_corruption_and_extra_bytes(self) -> None:
        """The read-back comparison checks actual file bytes, including the tail."""
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "copy"
            expected = b"complete admitted bytes"
            for content in (b"corrupt", expected + b"extra", expected):
                path.write_bytes(content)
                with path.open("rb") as stream:
                    if content == expected:
                        verify_copy(stream, expected)
                    else:
                        with self.assertRaisesRegex(
                            ValueError, "Installed bytes differ"
                        ):
                            verify_copy(stream, expected)

    def test_measured_source_inventory_is_complete(self) -> None:
        """New installation modules cannot silently escape the fixed measurement."""
        paths = {
            str(path.relative_to(ROOT)) for path in ROOT.glob("scripts/install*.py")
        }
        paths.add("scripts/release_payload.py")
        self.assertEqual(
            paths,
            {
                "scripts/install.py",
                "scripts/install_paths.py",
                "scripts/release_payload.py",
            },
        )

    def test_admission_instrument_inventory_is_complete(self) -> None:
        """The admission command remains a separately measured named source."""
        paths = {
            str(path.relative_to(ROOT))
            for path in ROOT.glob("verification/check_install*.py")
        }
        self.assertEqual(paths, {"verification/check_install_coverage.py"})

    def test_payload_parent_cannot_leave_the_reserved_directory(self) -> None:
        """Even a mistaken supplied payload name receives no parent authority."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            target = InstallationTarget(base / "reserved")
            with reserve(target) as (_, directory):
                for name in ("../outside", "/outside", "a//b", "a/./b", "a\\b"):
                    with (
                        self.subTest(name=name),
                        self.assertRaises(ValueError),
                        payload_parent(directory, name),
                    ):
                        self.fail("A noncanonical payload name was admitted")
            self.assertEqual(list(target.path.iterdir()), [])
