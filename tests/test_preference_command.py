"""Exercise the installed preference command and its packet-builder handoff."""

import errno
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.prepare_header import load_header

ROOT = Path(__file__).resolve().parents[1]


def command(
    arguments: list[str], directory: Path, outputs: Path, *, encoding: str | None = None
) -> tuple[int, bytes, bytes]:
    """Run an owned small fixture with a deadline and file-backed output."""
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in {"PYTHONPATH", "PYTHONHOME"} and not key.startswith("GIT_")
    }
    if encoding is not None:
        environment["PYTHONIOENCODING"] = encoding
    with (
        outputs.with_suffix(".out").open("wb") as stdout,
        outputs.with_suffix(".err").open("wb") as stderr,
    ):
        result = subprocess.run(
            arguments,
            cwd=directory,
            env=environment,
            stdout=stdout,
            stderr=stderr,
            stdin=subprocess.DEVNULL,
            timeout=10,
            check=False,
        )
    with (
        outputs.with_suffix(".out").open("rb") as stdout,
        outputs.with_suffix(".err").open("rb") as stderr,
    ):
        return result.returncode, stdout.read(65537), stderr.read(65537)


class PreferenceCommandTests(unittest.TestCase):
    """Verify real installed imports; source-checkout imports cannot hide omissions."""

    def test_destination_filesystem_failure_names_the_destination(self) -> None:
        """A regular-file ancestor is refused without blaming repository reads."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            subject = base / "subject"
            code, _, error = command(
                ["git", "init", "--quiet", str(subject)], base, base / "git"
            )
            self.assertEqual(code, 0, error.decode())
            (subject / ".bakerstreetrc").write_text(
                '{"schema_version":1,"case_directory":"reviews"}', encoding="utf-8"
            )
            header = base / "header.json"
            header.write_text("{}", encoding="utf-8")
            blocker = base / "PRIVATE-DESTINATION-SENTINEL"
            blocker.write_text("ordinary file", encoding="utf-8")
            code, stdout, stderr = command(
                [
                    sys.executable,
                    "-m",
                    "scripts.prepare_header",
                    "--repository",
                    str(subject),
                    "--header",
                    str(header),
                    "--case-root",
                    str(blocker / "missing"),
                ],
                ROOT,
                base / "refusal",
            )
            self.assertEqual(code, 2)
            self.assertEqual(stdout, b"")
            self.assertIn(b"case destination", stderr)
            self.assertIn(f"errno {errno.ENOTDIR}".encode(), stderr)
            self.assertNotIn(b"repository files", stderr)
            self.assertNotIn(b"PRIVATE-DESTINATION-SENTINEL", stderr)

    def test_command_preserves_unicode_through_an_ascii_stdout(self) -> None:
        """The receiving stream does not restrict valid text in the prepared header."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            subject = base / "subject"
            code, _, error = command(
                ["git", "init", "--quiet", str(subject)], base, base / "git"
            )
            self.assertEqual(code, 0, error.decode())
            original = base / "header.json"
            expected = {"title": "caf\u00e9 \u96ea \U0001f50d"}
            original.write_text(
                json.dumps(expected, ensure_ascii=False), encoding="utf-8"
            )
            code, content, error = command(
                [
                    sys.executable,
                    "-m",
                    "scripts.prepare_header",
                    "--repository",
                    str(subject),
                    "--header",
                    str(original),
                ],
                ROOT,
                base / "prepare",
                encoding="ascii",
            )
            self.assertEqual(code, 0, error.decode())
            selected: object = json.loads(content)
            self.assertIsInstance(selected, dict)
            self.assertEqual(selected, {**expected, "plain": False, "tier": "triage"})
            self.assertEqual(error, b"")

    def test_installed_command_prepares_a_header_consumed_by_packet_builder(
        self,
    ) -> None:
        """A package outside the source checkout carries selected values into a packet."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            code, _, error = command(
                [
                    sys.executable,
                    str(ROOT / "scripts/build_release.py"),
                    "--version",
                    "3.4.0",
                    "--out",
                    str(base / "dist"),
                ],
                base,
                base / "build",
            )
            self.assertEqual(code, 0, error.decode())
            with zipfile.ZipFile(base / "dist/baker-street-v3.4.0.zip") as archive:
                archive.extractall(base / "installed")
            installed = base / "installed/baker-street"
            subject = base / "subject"
            code, _, error = command(
                ["git", "init", "--quiet", str(subject)], base, base / "git"
            )
            self.assertEqual(code, 0, error.decode())
            (subject / ".bakerstreetrc").write_text(
                '{"schema_version":1,"plain":true,"tier":"focused","case_directory":"reviews"}',
                encoding="utf-8",
            )
            code, content, error = command(
                [sys.executable, "scripts/build_packet.py", "--print-header-template"],
                installed,
                base / "template",
            )
            self.assertEqual(code, 0, error.decode())
            original = base / "header.json"
            original.write_bytes(content)
            header = load_header(original)
            for field in ("plain", "tier", "write_directory"):
                del header[field]
            header["sealed_basis"] = {"head": "a" * 40}
            original.write_text(json.dumps(header), encoding="utf-8")
            code, prepared, error = command(
                [
                    sys.executable,
                    "-m",
                    "scripts.prepare_header",
                    "--repository",
                    str(subject),
                    "--header",
                    str(original),
                    "--case-root",
                    str(base / "cases"),
                ],
                installed,
                base / "prepare",
            )
            self.assertEqual(code, 0, error.decode())
            selected = base / "prepared.json"
            selected.write_bytes(prepared)
            normalized = load_header(selected)
            expected_plain = True
            self.assertIs(normalized["plain"], expected_plain)
            self.assertEqual(normalized["tier"], "focused")
            self.assertEqual(
                normalized["write_directory"], str((base / "cases/reviews").resolve())
            )
            packet = base / "packet.md"
            code, _, error = command(
                [
                    sys.executable,
                    "scripts/build_packet.py",
                    "--role",
                    "holmes",
                    "--header",
                    str(selected),
                    "--out",
                    str(packet),
                ],
                installed,
                base / "packet",
            )
            self.assertEqual(code, 0, error.decode())
            account = packet.read_text(encoding="utf-8")
            assigned = account.split("## Assigned case header\n\n```json\n", 1)[
                1
            ].split("\n```", 1)[0]
            actual_header: object = json.loads(assigned)
            self.assertEqual(actual_header, normalized)
            self.assertFalse((base / "cases").exists())

    def test_refused_command_emits_no_partial_header_or_private_value(self) -> None:
        """A malformed repository file is refused with a safe command diagnostic."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            code, _, error = command(
                ["git", "init", "--quiet", str(base / "subject")], base, base / "git"
            )
            self.assertEqual(code, 0, error.decode())
            (base / "subject/.bakerstreetrc").write_text(
                '{"schema_version":1,"command":"PRIVATE-SENTINEL"}', encoding="utf-8"
            )
            (base / "header.json").write_text("{}", encoding="utf-8")
            code, stdout, stderr = command(
                [
                    sys.executable,
                    "-m",
                    "scripts.prepare_header",
                    "--repository",
                    str(base / "subject"),
                    "--header",
                    str(base / "header.json"),
                    "--no-plain",
                    "--tier",
                    "triage",
                ],
                ROOT,
                base / "refusal",
            )
            self.assertEqual(code, 2)
            self.assertEqual(stdout, b"")
            self.assertIn(b"inputs were refused", stderr)
            self.assertIn(b"unrecognised repository preference field", stderr)
            self.assertNotIn(b"PRIVATE-SENTINEL", stderr)

    def test_explicit_header_admission_is_bounded(self) -> None:
        """The header input rejects a scalar, oversized bytes and large integers."""
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "header.json"
            path.write_bytes(b"{}".ljust(262144))
            self.assertEqual(load_header(path), {})
            for content in (
                b"[]",
                b"{}".ljust(262145),
                b'{"budget":' + b"9" * 129 + b"}",
                b'{"budget":NaN}',
            ):
                with self.subTest(content=content[:30]), self.assertRaises(ValueError):
                    path.write_bytes(content)
                    load_header(path)
