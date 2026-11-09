"""Exercise preference precedence through real Git roots and actual headers."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.preference_header import prepare_header
from scripts.preference_roots import git_roots
from scripts.preference_schema import Preferences


def repository(parent: Path, name: str = "subject") -> Path:
    """Create an owned Git fixture without altering shared repository state."""
    root = parent / name
    executable = shutil.which("git")
    if executable is None:
        message = "Git is required for the real repository fixtures"
        raise RuntimeError(message)
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    subprocess.run(
        [executable, "init", "--quiet", str(root)],
        check=True,
        timeout=10,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return root


def write_preferences(root: Path, values: dict[str, object]) -> None:
    """Write an ordinary fixture including the required version."""
    (root / ".bakerstreetrc").write_text(
        json.dumps({"schema_version": 1, **values}), encoding="utf-8"
    )


class PreferenceHeaderTests(unittest.TestCase):
    """Examine the public header preparation route without replacing Git."""

    def test_absent_file_supplies_ordinary_defaults(self) -> None:
        """Unrelated fields and the caller's original header remain intact."""
        with tempfile.TemporaryDirectory() as temporary:
            root = repository(Path(temporary))
            header: dict[str, object] = {"scope": "bounded", "authorized_actions": []}
            result = prepare_header(root, header)
            self.assertEqual(
                result,
                {
                    "scope": "bounded",
                    "authorized_actions": [],
                    "plain": False,
                    "tier": "triage",
                },
            )
            self.assertEqual(header, {"scope": "bounded", "authorized_actions": []})

    def test_file_choices_reach_the_actual_header_from_a_subdirectory(self) -> None:
        """Root discovery supplies the file at the worktree root alone."""
        with tempfile.TemporaryDirectory() as temporary:
            root = repository(Path(temporary))
            child = root / "child"
            child.mkdir()
            write_preferences(root, {"plain": True, "tier": "focused"})
            write_preferences(child, {"plain": False, "tier": "standard"})
            self.assertEqual(
                prepare_header(child, {}), {"plain": True, "tier": "focused"}
            )

    def test_header_fields_override_file_choices_including_false(self) -> None:
        """An explicit header choice takes precedence over a file default."""
        with tempfile.TemporaryDirectory() as temporary:
            root = repository(Path(temporary))
            write_preferences(root, {"plain": True, "tier": "focused"})
            header: dict[str, object] = {"plain": False, "tier": "standard"}
            self.assertEqual(prepare_header(root, header), header)

    def test_invocation_overrides_header_and_file_including_false(self) -> None:
        """A supplied false invocation is not mistaken for an absent choice."""
        with tempfile.TemporaryDirectory() as temporary:
            root = repository(Path(temporary))
            write_preferences(root, {"plain": True, "tier": "standard"})
            plain = False
            result = prepare_header(
                root,
                {"plain": True, "tier": "focused"},
                invocation=Preferences(plain, "triage"),
            )
            self.assertEqual(result, {"plain": False, "tier": "triage"})

    def test_bad_file_is_refused_despite_explicit_overrides(self) -> None:
        """An invocation cannot conceal a malformed repository preference."""
        with tempfile.TemporaryDirectory() as temporary:
            root = repository(Path(temporary))
            write_preferences(root, {"command": "PRIVATE-SENTINEL"})
            with self.assertRaisesRegex(ValueError, "unrecognised") as caught:
                prepare_header(
                    root,
                    {"plain": True, "tier": "standard"},
                    invocation=Preferences(tier="triage"),
                )
            self.assertNotIn("PRIVATE-SENTINEL", str(caught.exception))

    def test_bad_header_choices_are_refused_despite_invocation_overrides(self) -> None:
        """No string coercion or silent repair conceals an invalid header."""
        with tempfile.TemporaryDirectory() as temporary:
            root = repository(Path(temporary))
            headers: list[dict[str, object]] = [
                {"plain": "false"},
                {"tier": "unknown"},
                {"tier": 1},
            ]
            for header in headers:
                with (
                    self.subTest(header=header),
                    self.assertRaises((ValueError, TypeError)),
                ):
                    prepare_header(root, header, invocation=Preferences(tier="triage"))

    def test_preferred_directory_reaches_write_directory_without_creation(self) -> None:
        """The trusted case root confines the actual header's destination."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = repository(base)
            cases = base / "cases"
            write_preferences(root, {"case_directory": "reviews"})
            result = prepare_header(root, {}, case_root=cases)
            self.assertEqual(
                result["write_directory"], str(cases.resolve() / "reviews")
            )
            self.assertFalse(cases.exists())

    def test_explicit_header_destination_does_not_require_a_case_root(self) -> None:
        """An explicit destination supersedes the ordinary directory default."""
        with tempfile.TemporaryDirectory() as temporary:
            root = repository(Path(temporary))
            write_preferences(root, {"case_directory": "reviews"})
            result = prepare_header(root, {"write_directory": "operator-choice"})
            self.assertEqual(result["write_directory"], "operator-choice")

    def test_nested_repository_does_not_inherit_enclosing_preferences(self) -> None:
        """A separately identified inner repository has its own absent file."""
        with tempfile.TemporaryDirectory() as temporary:
            outer = repository(Path(temporary))
            write_preferences(outer, {"plain": True, "tier": "standard"})
            inner = repository(outer, "inner")
            self.assertEqual(
                prepare_header(inner, {}), {"plain": False, "tier": "triage"}
            )

    def test_git_roots_refuses_a_directory_without_a_repository(self) -> None:
        """A supplied ordinary directory is not a valid subject."""
        with (
            tempfile.TemporaryDirectory() as temporary,
            self.assertRaisesRegex(ValueError, "not an available Git worktree"),
        ):
            git_roots(Path(temporary))

    def test_linked_worktree_uses_its_own_root_and_preferences(self) -> None:
        """The main checkout's file and the shared authority do not supply defaults."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = repository(base)
            linked = base / "linked"
            commands = (
                [
                    "git",
                    "-C",
                    str(root),
                    "-c",
                    "user.name=Baker Street fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "--allow-empty",
                    "-m",
                    "Establish the examination fixture",
                ],
                [
                    "git",
                    "-C",
                    str(root),
                    "worktree",
                    "add",
                    "-b",
                    "linked",
                    str(linked),
                ],
            )
            for command in commands:
                subprocess.run(
                    command,
                    check=True,
                    timeout=10,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            write_preferences(root, {"plain": True, "tier": "standard"})
            write_preferences(linked, {"plain": False, "tier": "focused"})
            self.assertEqual(
                git_roots(linked), (linked.resolve(), (root / ".git").resolve())
            )
            self.assertEqual(
                prepare_header(linked, {}), {"plain": False, "tier": "focused"}
            )
            write_preferences(linked, {"case_directory": "reviews"})
            authority_alias = root / ".GIT"
            if not authority_alias.exists():
                authority_alias.mkdir()
            if authority_alias.samefile(root / ".git"):
                with self.assertRaisesRegex(ValueError, "outside the subject"):
                    prepare_header(linked, {}, case_root=authority_alias)
            else:
                result = prepare_header(linked, {}, case_root=authority_alias)
                self.assertEqual(
                    result["write_directory"],
                    str(authority_alias.resolve() / "reviews"),
                )

    def test_root_names_with_newlines_are_refused_as_ambiguous(self) -> None:
        """The two-line root protocol cannot silently reinterpret a root name."""
        with tempfile.TemporaryDirectory() as temporary:
            root = repository(Path(temporary), "two\nlines")
            with self.assertRaisesRegex(ValueError, "unambiguous absolute roots"):
                git_roots(root)

    def test_missing_git_is_an_explicit_refusal(self) -> None:
        """The real executable-search input cannot produce successful defaults."""
        original = os.environ.get("PATH")
        os.environ["PATH"] = ""
        try:
            with self.assertRaisesRegex(ValueError, "Git is required"):
                git_roots(Path("subject"))
        finally:
            if original is None:
                del os.environ["PATH"]
            else:
                os.environ["PATH"] = original

    def test_stalled_git_inquiry_is_terminated_at_its_deadline(self) -> None:
        """A real Git process blocked on its config pipe cannot stall preparation."""
        with tempfile.TemporaryDirectory() as temporary:
            root = repository(Path(temporary))
            configuration = root / ".git/config"
            configuration.unlink()
            os.mkfifo(configuration)
            with self.assertRaisesRegex(ValueError, "exceeded five seconds"):
                git_roots(root)
