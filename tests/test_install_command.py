"""Exercise the maintained installation command in owned destinations."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

from install_fixtures import ROOT, command, inventory


class InstallCommandTests(unittest.TestCase):
    """Require a complete installation and preservation of an occupied name."""

    def test_command_installs_into_a_new_destination_with_spaces(self) -> None:
        """The actual command reports the installed entry point in JSON."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            destination = base / "agent skills" / "baker street"
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
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            self.assertEqual(
                json.loads(result.stdout), {"entrypoint": str(destination / "SKILL.md")}
            )
            self.assertTrue((destination / "references/core.md").is_file())
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
            self.assertEqual(again.returncode, 2)
            self.assertEqual(again.stdout, "")
            self.assertEqual(before, inventory(destination))

    def test_make_install_uses_the_dedicated_environment_destination(self) -> None:
        """Make passes no operator path through shell interpolation."""
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary).resolve() / "skills $(false); literal"
            result = command(
                ["make", "--no-print-directory", "install"],
                ROOT,
                {"BAKER_STREET_DESTINATION": str(destination)},
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                json.loads(result.stdout.splitlines()[-1]),
                {"entrypoint": str(destination / "SKILL.md")},
            )
            self.assertTrue((destination / "SKILL.md").is_file())
