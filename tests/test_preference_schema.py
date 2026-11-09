"""Exercise the public preference decoder against the versioned flat contract."""

import json
import unittest
from dataclasses import FrozenInstanceError, replace
from itertools import product

from scripts.preference_schema import Preferences, decode_preferences


class PreferenceSchemaTests(unittest.TestCase):
    """Keep exact values, refusal boundaries and immutable defaults observable."""

    def test_defaults_leave_ordinary_choices_unset(self) -> None:
        """Absence is distinct from an explicit false preference."""
        self.assertEqual(decode_preferences(b'{"schema_version":1}'), Preferences())

    def test_explicit_false_is_preserved(self) -> None:
        """The invocation must be able to distinguish false from absence."""
        result = decode_preferences(b'{"schema_version":1,"plain":false}')
        expected_plain = False
        self.assertIs(result.plain, expected_plain)

    def test_valid_combinations_preserve_exact_values(self) -> None:
        """Oracle: the documented Cartesian product of ordinary field values."""
        directories = ("reviews", "two words", 'a"b', "a{b}", "é/folio", "trail ")
        for plain, tier, directory in product(
            (False, True), ("triage", "focused", "standard"), directories
        ):
            with self.subTest(plain=plain, tier=tier, directory=directory):
                content = json.dumps(
                    {
                        "schema_version": 1,
                        "plain": plain,
                        "tier": tier,
                        "case_directory": directory,
                    }
                ).encode()
                self.assertEqual(
                    decode_preferences(content), Preferences(plain, tier, directory)
                )

    def test_duplicate_fields_are_refused(self) -> None:
        """A duplicate cannot silently override the former value."""
        with self.assertRaisesRegex(ValueError, "repeated"):
            decode_preferences(b'{"schema_version":1,"plain":true,"plain":false}')

    def test_unknown_fields_do_not_echo_private_contents(self) -> None:
        """Unrecognised preferences cannot become execution authority."""
        with self.assertRaisesRegex(ValueError, "unrecognised") as caught:
            decode_preferences(b'{"schema_version":1,"command":"PRIVATE-SENTINEL"}')
        self.assertNotIn("PRIVATE-SENTINEL", str(caught.exception))

    def test_only_integer_version_one_is_admitted(self) -> None:
        """Neither Boolean equality nor string coercion establishes a version."""
        for content in (
            b"{}",
            b'{"schema_version":true}',
            b'{"schema_version":false}',
            b'{"schema_version":2}',
            b'{"schema_version":"1"}',
            b'{"schema_version":null}',
            b'{"schema_version":-1}',
        ):
            with self.subTest(content=content), self.assertRaises(ValueError):
                decode_preferences(content)

    def test_present_null_is_not_an_absent_optional(self) -> None:
        """Explicit null must not silently restore a default."""
        for key in ("plain", "tier", "case_directory"):
            with (
                self.subTest(key=key),
                self.assertRaisesRegex(ValueError, "absent rather than null"),
            ):
                decode_preferences(
                    json.dumps({"schema_version": 1, key: None}).encode()
                )

    def test_nonboolean_plain_is_refused(self) -> None:
        """Only exact JSON Booleans choose plain manner."""
        for value in (0, 1, "true", "false"):
            with (
                self.subTest(value=value),
                self.assertRaisesRegex(ValueError, "plain.*Boolean"),
            ):
                decode_preferences(
                    json.dumps({"schema_version": 1, "plain": value}).encode()
                )

    def test_unknown_tiers_and_wrong_tier_types_are_refused(self) -> None:
        """Tier spelling is an exact finite contract."""
        for value in ("FOCUSED", "unknown", 1, False):
            with (
                self.subTest(value=value),
                self.assertRaisesRegex(ValueError, "tier preference"),
            ):
                decode_preferences(
                    json.dumps({"schema_version": 1, "tier": value}).encode()
                )

    def test_unsafe_directory_spellings_are_refused(self) -> None:
        """A repository cannot select an arbitrary host destination."""
        for value in (
            "",
            " ",
            "/outside",
            "..",
            "a/../b",
            "./a",
            "a//b",
            "a/",
            "C:other",
            "a\\b",
            "a\n",
            "a\x7f",
            1,
            False,
            "/".join(["a"] * 17),
        ):
            with (
                self.subTest(value=value),
                self.assertRaisesRegex(ValueError, "case_directory"),
            ):
                decode_preferences(
                    json.dumps({"schema_version": 1, "case_directory": value}).encode()
                )

    def test_directory_bound_counts_utf8_bytes(self) -> None:
        """The bound concerns retained bytes, not just character count."""
        allowed = "é" * 512
        self.assertEqual(
            decode_preferences(
                json.dumps({"schema_version": 1, "case_directory": allowed}).encode()
            ).case_directory,
            allowed,
        )
        with self.assertRaisesRegex(ValueError, "1024 UTF-8 bytes"):
            decode_preferences(
                json.dumps(
                    {"schema_version": 1, "case_directory": allowed + "é"}
                ).encode()
            )

    def test_c1_controls_are_refused_without_rejecting_adjacent_text(self) -> None:
        """Refuse every C1 control and retain the next printable code point."""
        for codepoint in range(0x80, 0xA0):
            with (
                self.subTest(codepoint=codepoint),
                self.assertRaisesRegex(ValueError, "forbidden character"),
            ):
                decode_preferences(
                    json.dumps(
                        {
                            "schema_version": 1,
                            "case_directory": "reviews/" + chr(codepoint),
                        }
                    ).encode()
                )
        directory = "reviews/" + chr(0xA0) + "folio"
        self.assertEqual(
            decode_preferences(
                json.dumps({"schema_version": 1, "case_directory": directory}).encode()
            ).case_directory,
            directory,
        )

    def test_file_size_is_bounded_before_decoding(self) -> None:
        """A valid padded document cannot bypass the admission byte ceiling."""
        ordinary = b'{"schema_version":1}'
        self.assertEqual(decode_preferences(ordinary.ljust(8192)), Preferences())
        with self.assertRaisesRegex(ValueError, "exceed 8192 bytes"):
            decode_preferences(ordinary.ljust(8193))

    def test_containers_are_refused_before_recursive_decoding(self) -> None:
        """Even a deeply nested short document has no admitted structure."""
        for content in (b"[]", b'{"schema_version":1,"plain":{}}', b"{" * 1000):
            with (
                self.subTest(content=content[:40]),
                self.assertRaisesRegex(ValueError, "flat object"),
            ):
                decode_preferences(content)

    def test_root_must_be_an_object(self) -> None:
        """Scalar JSON values do not form repository preferences."""
        for content in (b"true", b"null", b"1", b'"folio"'):
            with (
                self.subTest(content=content),
                self.assertRaisesRegex(ValueError, "must be an object"),
            ):
                decode_preferences(content)

    def test_noninteger_numbers_are_refused_during_decoding(self) -> None:
        """The numeric decoder refuses before ordinary field validation."""
        for token in ("1.0", "1e9999", "NaN", "Infinity", "-Infinity"):
            with (
                self.subTest(token=token),
                self.assertRaisesRegex(ValueError, "Floating-point and nonfinite"),
            ):
                decode_preferences(('{"schema_version":' + token + "}").encode())

    def test_numeric_tokens_are_bounded_before_conversion(self) -> None:
        """The diagnostic distinguishes the work bound from a wrong version."""
        with self.assertRaisesRegex(ValueError, "eight characters"):
            decode_preferences(('{"schema_version":' + "9" * 1000 + "}").encode())

    def test_malformed_encoding_and_syntax_are_refused(self) -> None:
        """A decode failure is not an empty successful preference set."""
        for content in (
            b"\xff",
            b'{"schema_version":1}\xff',
            b"",
            b"{",
            b'{"schema_version":1,}',
            b'{"schema_version":1}{}',
        ):
            with self.subTest(content=content), self.assertRaises(ValueError):
                decode_preferences(content)

    def test_values_are_immutable(self) -> None:
        """Ordinary field assignment cannot alter an admitted preference."""
        preferences = decode_preferences(b'{"schema_version":1,"plain":false}')
        assignments = {"plain": True, "tier": "standard", "case_directory": "elsewhere"}
        for field, value in assignments.items():
            with self.subTest(field=field), self.assertRaises(FrozenInstanceError):
                setattr(preferences, field, value)

    def test_replace_revalidates_plain(self) -> None:
        """Replacement invokes the same admission contract as construction."""
        preferences = decode_preferences(b'{"schema_version":1,"plain":false}')
        with self.assertRaisesRegex(ValueError, "plain.*Boolean"):
            replace(preferences, plain="false")
