"""Observe the public command's streams without replacing its real dependencies."""

import io
import json
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from scripts.prepare_header import main


class PreferenceCliTests(unittest.TestCase):
    """Exercise exit status and complete output through the public command."""

    def test_public_command_success_and_refusals_have_distinct_streams(self) -> None:
        """Success emits one header; refusal emits no partial header."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            executable = shutil.which("git")
            if executable is None:
                message = "Git is required for the command fixture"
                raise RuntimeError(message)
            subprocess.run(  # noqa: S603  # PREF-CLI-FIXTURE: Fixed Git init in an owned directory.
                [executable, "init", "--quiet", str(base / "subject")],
                check=True,
                timeout=10,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            header = base / "header.json"
            header.write_text('{"budget":17}', encoding="utf-8")
            arguments = ["--repository", str(base / "subject"), "--header", str(header)]
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = main([*arguments, "--no-plain", "--tier", "focused"])
            self.assertEqual(result, 0)
            actual: object = json.loads(stdout.getvalue())
            self.assertEqual(actual, {"budget": 17, "plain": False, "tier": "focused"})
            self.assertEqual(stderr.getvalue(), "")
            for content in (
                "[]",
                '{"budget":1e9999}',
                '{"plain":"false"}',
                '{"scope":"\\ud800"}',
            ):
                header.write_text(content, encoding="utf-8")
                stdout, stderr = io.StringIO(), io.StringIO()
                with (
                    self.subTest(content=content),
                    redirect_stdout(stdout),
                    redirect_stderr(stderr),
                ):
                    result = main(arguments)
                self.assertEqual(result, 2)
                self.assertEqual(stdout.getvalue(), "")
                self.assertIn("inputs were refused", stderr.getvalue())
            header.unlink()
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = main(arguments)
            self.assertEqual(result, 2)
            self.assertEqual(stdout.getvalue(), "")
            self.assertIn("files could not be read", stderr.getvalue())
