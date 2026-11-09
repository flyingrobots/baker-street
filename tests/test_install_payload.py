"""Compare a real installation with the release and exercise its installed commands."""

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from install_fixtures import ROOT, command, inventory


class InstallPayloadTests(unittest.TestCase):
    """Read the actual distribution and run tools outside the source checkout."""

    def test_installed_inventory_matches_release_and_runs_both_commands(self) -> None:
        """The complete selected bytes and manifest agree with the actual release ZIP."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            destination = base / "installed"
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
            archive = base / "release"
            built = command(
                [
                    sys.executable,
                    str(ROOT / "scripts/build_release.py"),
                    "--version",
                    "3.4.0",
                    "--out",
                    str(archive),
                ],
                base,
            )
            self.assertEqual(built.returncode, 0, built.stderr)
            with zipfile.ZipFile(archive / "baker-street-v3.4.0.zip") as bundle:
                expected = {
                    name.removeprefix("baker-street/"): bundle.read(name)
                    for name in bundle.namelist()
                }
            self.assertEqual(inventory(destination), expected)
            self.assertFalse(
                any(
                    "evals" in name or "house-correspondence" in name
                    for name in expected
                )
            )
            header = base / "header.json"
            header.write_bytes((ROOT / "examples/triage/header.json").read_bytes())
            packet = command(
                [
                    sys.executable,
                    str(destination / "scripts/build_packet.py"),
                    "--role",
                    "holmes",
                    "--header",
                    str(header),
                    "--out",
                    str(base / "packet.md"),
                ],
                base,
            )
            self.assertEqual(packet.returncode, 0, packet.stderr)
            self.assertIn(
                "EXAMPLE-TRIAGE", (base / "packet.md").read_text(encoding="utf-8")
            )
            row: dict[str, object] = {
                "header": json.loads(header.read_text(encoding="utf-8")),
                "findings": [],
                "errata": [],
                "rulings": [],
                "path_to_ready": [],
                "followups": [],
                "probe_triage": [],
                "coverage_matrix": [],
                "decision": "READY",
                "notes": "Synthetic command fixture; no agent investigation occurred.",
            }
            record = base / "record.json"
            record.write_text(json.dumps(row), encoding="utf-8")
            case = command(
                [
                    sys.executable,
                    str(destination / "scripts/build_case.py"),
                    "--record",
                    str(record),
                    "--out",
                    str(base / "case"),
                ],
                base,
            )
            self.assertEqual(case.returncode, 0, case.stderr)
            self.assertTrue((base / "case/CASE_FILE.md").is_file())
