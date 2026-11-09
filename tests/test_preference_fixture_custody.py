"""Keep linked-worktree fixture mutations within their owned Git authority."""

import hashlib
import os
import tempfile
import unittest
from pathlib import Path

import test_preference_cli as cli_fixture
import test_preference_header as header_fixture
from test_preference_command import command


def inventory(root: Path) -> dict[str, str]:
    """Bind the bytes of an owned operator fixture, including its Git authority."""
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file() and not path.is_symlink()
    }


class PreferenceFixtureCustodyTests(unittest.TestCase):
    """Actual inherited Git routing must grant no authority over another fixture."""

    def test_linked_fixture_preserves_a_selected_operator_repository(self) -> None:
        """The linked-worktree commands preserve the selected operator's papers."""
        self._examine_fixture(
            header_fixture.PreferenceHeaderTests(
                "test_linked_worktree_uses_its_own_root_and_preferences"
            )
        )

    def test_cli_initializer_preserves_a_selected_operator_repository(self) -> None:
        """The direct initialization call also receives no operator authority."""
        self._examine_fixture(
            cli_fixture.PreferenceCliTests(
                "test_public_command_success_and_refusals_have_distinct_streams"
            )
        )

    def _examine_fixture(self, fixture: unittest.TestCase) -> None:
        """A staged operator sentinel and all its authority bytes remain unchanged."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            operator = header_fixture.repository(base, "operator")
            (operator / "OPERATOR-SENTINEL").write_text(
                "Preserve staged work.\n", encoding="utf-8"
            )
            code, _, error = command(
                ["git", "-C", str(operator), "add", "OPERATOR-SENTINEL"],
                base,
                base / "stage",
            )
            self.assertEqual(code, 0, error.decode())
            before = inventory(operator)
            inherited = {
                key: value
                for key, value in os.environ.items()
                if key.startswith("GIT_")
            }
            result = unittest.TestResult()
            try:
                for key in inherited:
                    del os.environ[key]
                os.environ.update(
                    GIT_DIR=str(operator / ".git"), GIT_WORK_TREE=str(operator)
                )
                fixture.run(result)
            finally:
                for key in tuple(os.environ):
                    if key.startswith("GIT_"):
                        del os.environ[key]
                os.environ.update(inherited)
            self.assertEqual(
                before,
                inventory(operator),
                "The fixture changed the selected operator repository",
            )
            self.assertFalse(
                result.failures or result.errors, str(result.failures + result.errors)
            )
