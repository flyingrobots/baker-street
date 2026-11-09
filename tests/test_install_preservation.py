"""Preserve existing bytes and truthful failure during installation refusals."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

from install_fixtures import ROOT, command, inventory, source_copy

from scripts.install import destination_path


class InstallPreservationTests(unittest.TestCase):
    """Exercise real path, source and write failures without substituted operations."""

    def test_default_and_explicit_destination_precedence_without_home_writes(
        self,
    ) -> None:
        """Compute the default; explicit arguments precede the dedicated variable."""
        self.assertEqual(
            destination_path(None, {}), Path.home() / ".agents/skills/baker-street"
        )
        self.assertEqual(
            destination_path("explicit", {"BAKER_STREET_DESTINATION": "other"}),
            (Path.cwd() / "explicit"),
        )
        self.assertEqual(
            destination_path(None, {"BAKER_STREET_DESTINATION": "other"}),
            Path.cwd() / "other",
        )
        for bad in ("", "\x00"):
            with self.subTest(destination=bad), self.assertRaises(ValueError):
                destination_path(bad, {})

    def test_occupied_file_and_symlinked_parent_preserve_existing_bytes(self) -> None:
        """No refusal follows a final or parent link into an existing installation."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            existing = base / "existing"
            existing.mkdir()
            (existing / "kept").write_bytes(b"preserve these bytes")
            alias = base / "alias"
            alias.symlink_to(existing, target_is_directory=True)
            final = base / "final"
            final.symlink_to(existing, target_is_directory=True)
            occupied = base / "occupied"
            occupied.write_bytes(b"occupied name")
            before = inventory(base)
            for destination in (
                alias / "new",
                final,
                occupied,
                base / ".." / "refused",
                Path("/"),
            ):
                result = command(
                    [
                        sys.executable,
                        "-m",
                        "scripts.install",
                        "--destination",
                        str(destination),
                    ],
                    ROOT,
                )
                with self.subTest(destination=destination):
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertEqual(result.stdout, "")
                    self.assertFalse(json.loads(result.stderr)["retained_destination"])
                    self.assertEqual(before, inventory(base))

    def test_missing_source_is_refused_before_destination_parents_are_created(
        self,
    ) -> None:
        """Admit all selected source bytes before making any destination directory."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            source = source_copy(base)
            (source / "roles/checker.md").unlink()
            before = inventory(source)
            destination = base / "new parents" / "skill"
            result = command(
                [
                    sys.executable,
                    "-m",
                    "scripts.install",
                    "--destination",
                    str(destination),
                ],
                source,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertFalse(destination.parent.exists())
            self.assertFalse(json.loads(result.stderr)["retained_destination"])
            self.assertEqual(before, inventory(source))

    def test_file_size_limit_interrupts_copy_without_publishing_the_entrypoint(
        self,
    ) -> None:
        """An actual OS write refusal retains the marker and refuses a second attempt."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            destination = base / "partial"
            program = "import resource, runpy; resource.setrlimit(resource.RLIMIT_FSIZE, (4096, 4096)); runpy.run_module('scripts.install', run_name='__main__')"
            result = command(
                [sys.executable, "-c", program, "--destination", str(destination)], ROOT
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertTrue(json.loads(result.stderr)["retained_destination"])
            self.assertTrue((destination / ".baker-street-incomplete").is_file())
            self.assertFalse((destination / "SKILL.md").exists())
            before = inventory(destination)
            again = command(
                [
                    sys.executable,
                    "-m",
                    "scripts.install",
                    "--destination",
                    str(destination),
                ],
                ROOT,
            )
            self.assertEqual(again.returncode, 2, again.stderr)
            self.assertEqual(before, inventory(destination))
