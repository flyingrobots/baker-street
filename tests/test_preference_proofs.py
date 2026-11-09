"""Exercise bounded proof reads and the admission command."""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from preference_proof_fixtures import fixture, proof, registry

from verification.check_preferences import main
from verification.preference_coverage import check_coverage
from verification.preference_proofs import (
    PROOF_BYTES,
    PreferenceCheckError,
    load_json,
    read_text,
)


class PreferenceCheckTests(unittest.TestCase):
    """Examine the named admission obligations with fixed independent inputs."""

    def test_proof_read_is_bounded_regular_and_utf8(self) -> None:
        """No directory, symlink, oversized or undecodable proof is admitted."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "proof.json"
            path.write_text("{}", encoding="utf-8")
            self.assertEqual(read_text(path), "{}")
            link = root / "link"
            link.symlink_to(path)
            for bad in (root, link):
                with self.subTest(path=bad), self.assertRaises(PreferenceCheckError):
                    read_text(bad)
            path.write_bytes(b" " * (PROOF_BYTES + 1))
            with self.assertRaisesRegex(PreferenceCheckError, "proof_size_limit"):
                read_text(path)
            path.write_bytes(b"\xff")
            with self.assertRaises(UnicodeError):
                read_text(path)

    def test_json_proof_refuses_duplicates_nonfinite_values_and_long_integers(
        self,
    ) -> None:
        """Codec admission happens before numeric counts or registry records are used."""
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "proof.json"
            path.write_text('{"count":17}', encoding="utf-8")
            self.assertEqual(load_json(path), {"count": 17})
            for content, reason in (
                ('{"count":1,"count":2}', "duplicate_proof_key"),
                ('{"count":NaN}', "nonfinite_proof_constant"),
                ('{"count":12345678901234567}', "proof_integer_limit"),
            ):
                path.write_text(content, encoding="utf-8")
                with (
                    self.subTest(content=content),
                    self.assertRaisesRegex(PreferenceCheckError, reason),
                ):
                    load_json(path)

    def test_command_reports_admission_and_refusal_distinctly(self) -> None:
        """Supported tools report exact counts; older interpreters explicitly refuse."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            coverage = fixture(root)
            arguments = ["--root", str(root), "--coverage", str(coverage)]
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = main(arguments)
            if sys.version_info < (3, 13):
                self.assertEqual(result, 2)
                self.assertIn("require Python 3.13", stderr.getvalue())
                self.assertEqual(stdout.getvalue(), "")
                return
            self.assertEqual(result, 0, stderr.getvalue())
            self.assertEqual(stderr.getvalue(), "")
            self.assertEqual(
                json.loads(stdout.getvalue()),
                {"coverage": check_coverage(proof()), "exceptions": 1},
            )
            for content in ("not JSON", "[]", json.dumps({"files": {}})):
                coverage.write_text(content, encoding="utf-8")
                stdout, stderr = io.StringIO(), io.StringIO()
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    result = main(arguments)
                self.assertEqual(result, 2)
                self.assertEqual(stdout.getvalue(), "")
                self.assertIn("incomplete or invalid proof", stderr.getvalue())
            coverage.unlink()
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                self.assertEqual(main(arguments), 2)
            coverage.write_text(json.dumps(proof()), encoding="utf-8")
            (root / "scripts/preference_unexpected.py").write_text(
                "pass\n", encoding="utf-8"
            )
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(main(arguments), 2)

    def test_empty_registry_cannot_admit_an_embedded_effective_suppression(
        self,
    ) -> None:
        """The complete admission route must refuse the actual Ruff-accepted form."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            coverage = fixture(root)
            (root / "scripts/preference_roots.py").write_text(
                "import subprocess\n\ndef inquire(arguments):\n"
                "    subprocess.run(arguments, check=True)  # ordinary explanation  # noqa: S603\n",
                encoding="utf-8",
            )
            (root / "verification/exceptions.json").write_text(
                json.dumps({**registry(), "entries": []}), encoding="utf-8"
            )
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = main(["--root", str(root), "--coverage", str(coverage)])
            self.assertEqual(result, 2)
            self.assertEqual(stdout.getvalue(), "")
            reason = (
                "require Python 3.13"
                if sys.version_info < (3, 13)
                else "unsupported_source_suppression"
            )
            self.assertIn(reason, stderr.getvalue())
