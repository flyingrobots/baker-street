"""Exercise real POSIX file admission and preference destination confinement."""

import os
import tempfile
import unittest
from pathlib import Path

from scripts.preference_file import case_destination, read_preferences
from scripts.preference_schema import Preferences


class PreferenceFileTests(unittest.TestCase):
    """Use owned real files; no filesystem double supplies the safety evidence."""

    def test_absence_does_not_read_an_ancestor(self) -> None:
        """A neighbouring preference file supplies no worktree defaults."""
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            (parent / ".bakerstreetrc").write_text(
                '{"schema_version":1,"plain":true}', encoding="utf-8"
            )
            subject = parent / "subject"
            subject.mkdir()
            self.assertEqual(read_preferences(subject), Preferences())

    def test_regular_file_preserves_admitted_values(self) -> None:
        """The actual file route retains false and the chosen tier."""
        with tempfile.TemporaryDirectory() as temporary:
            subject = Path(temporary)
            (subject / ".bakerstreetrc").write_text(
                '{"schema_version":1,"plain":false,"tier":"focused"}',
                encoding="utf-8",
            )
            expected_plain = False
            self.assertEqual(
                read_preferences(subject), Preferences(expected_plain, "focused")
            )

    def test_missing_root_is_not_an_absent_preference(self) -> None:
        """An invalid repository location must not acquire ordinary defaults."""
        with (
            tempfile.TemporaryDirectory() as temporary,
            self.assertRaises(FileNotFoundError),
        ):
            read_preferences(Path(temporary) / "missing")

    def test_final_symlinks_are_refused_even_with_valid_contents(self) -> None:
        """Neither an existing nor a dangling final link is followed."""
        with tempfile.TemporaryDirectory() as temporary:
            subject = Path(temporary)
            target = subject / "elsewhere"
            target.write_text('{"schema_version":1}', encoding="utf-8")
            preference = subject / ".bakerstreetrc"
            for destination in (target, subject / "missing"):
                with self.subTest(destination=destination.name):
                    preference.symlink_to(destination)
                    try:
                        with self.assertRaises(OSError):
                            read_preferences(subject)
                    finally:
                        preference.unlink()

    def test_nonregular_files_are_refused_without_waiting_for_a_writer(self) -> None:
        """An unopened pipe and a directory cannot serve as preference files."""
        with tempfile.TemporaryDirectory() as temporary:
            subject = Path(temporary)
            preference = subject / ".bakerstreetrc"
            os.mkfifo(preference)
            try:
                with self.assertRaisesRegex(ValueError, "must be regular"):
                    read_preferences(subject)
            finally:
                preference.unlink()
            preference.mkdir()
            with self.assertRaisesRegex(ValueError, "must be regular"):
                read_preferences(subject)

    def test_actual_file_byte_limit_and_decode_failure_are_retained(self) -> None:
        """A valid padded file passes at the bound and fails above it."""
        with tempfile.TemporaryDirectory() as temporary:
            subject = Path(temporary)
            preference = subject / ".bakerstreetrc"
            ordinary = b'{"schema_version":1}'
            preference.write_bytes(ordinary.ljust(8192))
            self.assertEqual(read_preferences(subject), Preferences())
            preference.write_bytes(ordinary.ljust(8193))
            with self.assertRaisesRegex(ValueError, "exceed 8192 bytes"):
                read_preferences(subject)
            preference.write_bytes(ordinary + b"\xff")
            with self.assertRaises(UnicodeDecodeError):
                read_preferences(subject)


class PreferenceDestinationTests(unittest.TestCase):
    """Resolve names without creating a case or conferring write permission."""

    def test_absent_directory_does_not_require_a_case_root(self) -> None:
        """An ordinary manner preference makes no destination demand."""
        subject = Path("subject")
        self.assertIsNone(case_destination(Preferences(), None, subject, subject))

    def test_directory_requires_an_operator_case_root(self) -> None:
        """The repository alone cannot select the surrounding host directory."""
        subject = Path("subject")
        with self.assertRaisesRegex(ValueError, "requires an operator case root"):
            case_destination(
                Preferences(case_directory="reviews"), None, subject, subject
            )

    def test_confined_destination_is_returned_without_creation(self) -> None:
        """An exact relative spelling selects a path below the supplied root."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            root = base / "cases"
            destination = case_destination(
                Preferences(case_directory="two words/reviews"),
                root,
                base / "subject",
                base / "authority",
            )
            self.assertEqual(destination, root / "two words/reviews")
            self.assertFalse(root.exists())

    def test_symlink_escape_is_refused(self) -> None:
        """A relative name cannot escape through an existing directory link."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "cases"
            root.mkdir()
            (root / "reviews").symlink_to(base / "outside", target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "escapes the operator case root"):
                case_destination(
                    Preferences(case_directory="reviews/new"),
                    root,
                    base / "subject",
                    base / "authority",
                )

    def test_subject_and_shared_authority_are_both_forbidden(self) -> None:
        """A linked worktree does not make its common Git authority available."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            for directory in ("subject/reviews", "authority/reviews"):
                with (
                    self.subTest(directory=directory),
                    self.assertRaisesRegex(ValueError, "outside the subject"),
                ):
                    case_destination(
                        Preferences(case_directory=directory),
                        base,
                        base / "subject",
                        base / "authority",
                    )

    def test_link_back_to_case_root_is_not_a_subdirectory(self) -> None:
        """An admitted spelling may still resolve to the root itself."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "again").symlink_to(root, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "escapes the operator case root"):
                case_destination(
                    Preferences(case_directory="again"), root, root / "subject", root
                )

    def test_symlink_cycles_are_refused_as_unresolved_destinations(self) -> None:
        """A link cycle cannot become the case root, destination or ancestor."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "cases"
            root.mkdir()
            cycle = root / "cycle"
            cycle.symlink_to(cycle, target_is_directory=True)
            for case_root, directory in (
                (cycle, "reviews"),
                (root, "cycle"),
                (root, "cycle/new"),
            ):
                with (
                    self.subTest(directory=directory),
                    self.assertRaises((ValueError, OSError)),
                ):
                    case_destination(
                        Preferences(case_directory=directory),
                        case_root,
                        base / "subject",
                        base / "authority",
                    )

    def test_regular_files_cannot_be_case_directory_ancestors(self) -> None:
        """A regular file cannot serve as the case root, destination or ancestor."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "cases"
            root.mkdir()
            folio = root / "folio"
            folio.write_text("ordinary file", encoding="utf-8")
            for case_root, directory in (
                (folio, "reviews"),
                (root, "folio"),
                (root, "folio/new"),
            ):
                with (
                    self.subTest(directory=directory),
                    self.assertRaises((ValueError, OSError)),
                ):
                    case_destination(
                        Preferences(case_directory=directory),
                        case_root,
                        base / "subject",
                        base / "authority",
                    )

    def test_subject_aliases_follow_physical_identity_not_letter_case(self) -> None:
        """Case aliases are forbidden; distinct directories remain valid."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            subject = base / "subject"
            subject.mkdir()
            alias = base / "SUBJECT"
            if not alias.exists():
                alias.mkdir()
            preferences = Preferences(case_directory="reviews")
            if alias.samefile(subject):
                with self.assertRaisesRegex(ValueError, "outside the subject"):
                    case_destination(preferences, alias, subject, base / "authority")
            else:
                self.assertEqual(
                    case_destination(preferences, alias, subject, base / "authority"),
                    alias.resolve() / "reviews",
                )

    def test_common_authority_alias_is_distinct_from_subject_exclusion(self) -> None:
        """A physical alias of shared authority is forbidden outside the subject too."""
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            subject = base / "subject"
            subject.mkdir()
            authority = base / "authority"
            authority.mkdir()
            alias = base / "AUTHORITY"
            if not alias.exists():
                alias.mkdir()
            preferences = Preferences(case_directory="reviews")
            if alias.samefile(authority):
                with self.assertRaisesRegex(ValueError, "outside the subject"):
                    case_destination(preferences, alias, subject, authority)
            else:
                self.assertEqual(
                    case_destination(preferences, alias, subject, authority),
                    alias.resolve() / "reviews",
                )
