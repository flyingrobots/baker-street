"""Exercise source suppressions and exception-registry correspondence."""

import tempfile
import unittest
from pathlib import Path

from preference_proof_fixtures import SOURCE, TODAY, exception, fixture, registry

from verification.preference_exceptions import check_exceptions
from verification.preference_proofs import PreferenceCheckError
from verification.preference_suppressions import definitions, source_exceptions


class PreferenceCheckTests(unittest.TestCase):
    """Examine the named admission obligations with fixed independent inputs."""

    def test_suppression_requires_the_prescribed_preceding_comment(self) -> None:
        """A factual reason uses the recorded grammar at the immediately prior line."""
        valid = (
            "def inquire():\n"
            "    # policy-exception: PREF-EXAMPLE -- Fixed inquiry.\n"
            "    subprocess.run(arguments)  # noqa: S603\n"
        )
        for source in (
            valid,
            valid.replace(
                "Fixed inquiry.", "Fixed inquiry; noqa names one diagnostic."
            ),
        ):
            with self.subTest(source=source):
                self.assertEqual(
                    source_exceptions({"example.py": source}),
                    {
                        "PREF-EXAMPLE": ("S603", "example.py", ("inquire",)),
                    },
                )

    def test_legacy_detached_and_multiple_diagnostic_annotations_are_refused(
        self,
    ) -> None:
        """The old trailing form and misplaced metadata cannot replace the protocol."""
        prefix = (
            "def inquire():\n    # policy-exception: PREF-EXAMPLE -- Fixed inquiry.\n"
        )
        invalid = (
            "def inquire():\n    subprocess.run(arguments)  # noqa: S603  # PREF-EXAMPLE: Fixed inquiry.\n",
            "def inquire():\n    subprocess.run(arguments)  # noqa: S603\n",
            prefix + "\n    subprocess.run(arguments)  # noqa: S603\n",
            prefix.replace("Fixed inquiry.", " ")
            + "    subprocess.run(arguments)  # noqa: S603\n",
            prefix + "    subprocess.run(arguments)  # noqa: S603, S602\n",
            "def inquire():\n    value = 1 # policy-exception: PREF-EXAMPLE -- Fixed inquiry.\n    subprocess.run(arguments)  # noqa: S603\n",
            "# policy-exception: PREF-EXAMPLE -- Fixed inquiry.\nsubprocess.run(arguments)  # noqa: S603\n",
            "# pragma: no branch\n",
        )
        for source in invalid:
            with self.subTest(source=source), self.assertRaises(PreferenceCheckError):
                source_exceptions({"example.py": source})

    def test_current_registry_and_source_waiver_agree(self) -> None:
        """One identified source call has one justified, unexpired record."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture(root)
            self.assertEqual(check_exceptions(root, registry(), {"lint": {}}, TODAY), 1)

    def test_registry_requires_metadata_and_existing_symbols(self) -> None:
        """Missing metadata, malformed identities and absent symbols are refused."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture(root)
            cases: list[tuple[str, object]] = [
                ("id", "bad id"),
                ("diagnostic", "PT009,PT027"),
                ("path", "outside.py"),
                ("symbols", []),
                ("symbols", ["absent"]),
                ("symbols", ["inquire", "inquire"]),
                ("reason", ""),
                ("risk", None),
                ("approver", False),
                ("compensating_check", 17),
                ("rule", ""),
            ]
            for field, value in cases:
                with (
                    self.subTest(field=field, value=value),
                    self.assertRaises(PreferenceCheckError),
                ):
                    check_exceptions(
                        root,
                        registry({**exception(), field: value}),
                        {"lint": {}},
                        TODAY,
                    )
            for field in ("owner", "tracking", "review_condition", "expires"):
                document = registry()
                del document[field]
                with self.subTest(field=field), self.assertRaises(PreferenceCheckError):
                    check_exceptions(root, document, {"lint": {}}, TODAY)

    def test_registry_rejects_missing_orphaned_duplicate_and_expired_entries(
        self,
    ) -> None:
        """The observed suppression and registry must correspond in both directions."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture(root)
            bad_documents: list[object] = [
                {**registry(), "schema_version": True},
                {**registry(), "entries": None},
                {**registry(), "entries": [None]},
                {**registry(), "entries": []},
                {**registry(), "entries": [exception(), exception()]},
                {
                    **registry(),
                    "entries": [exception(), {**exception(), "id": "SECOND"}],
                },
                registry({**exception(), "id": "ORPHAN"}),
                registry({**exception(), "expires": "2026-11-07"}),
                registry({**exception(), "expires": "invalid"}),
            ]
            for document in bad_documents:
                with self.subTest(document=document), self.assertRaises(ValueError):
                    check_exceptions(root, document, {"lint": {}}, TODAY)
            self.assertEqual(
                check_exceptions(
                    root,
                    registry({**exception(), "expires": TODAY.isoformat()}),
                    {"lint": {}},
                    TODAY,
                ),
                1,
            )

    def test_source_suppression_must_be_exact_unique_and_inside_a_function(
        self,
    ) -> None:
        """A broad pragma, repeated identity or module-level exception is refused."""
        for source in (
            "# ruff: noqa\n",
            "# type: ignore\n",
            "# pragma: no cover\n",
            "# pyright: ignore\n",
            "# noqa: S603  # PREF-EXAMPLE: Outside a function.\n",
            SOURCE + SOURCE.replace("inquire", "another"),
        ):
            with self.subTest(source=source), self.assertRaises(PreferenceCheckError):
                source_exceptions({"example.py": source})
        self.assertEqual(
            source_exceptions({"empty.py": "# ordinary remark\npass\n"}), {}
        )
        nested = "class Outer:\n    async def query(self):\n        def inner():\n            pass\n"
        self.assertEqual(
            set(definitions(nested)), {"Outer", "Outer.query", "Outer.query.inner"}
        )
        with self.assertRaisesRegex(PreferenceCheckError, "ambiguous_symbol"):
            definitions("def repeated(): pass\ndef repeated(): pass\n")

    def test_configuration_cannot_add_a_broad_or_unregistered_waiver(self) -> None:
        """Configured exceptions must be permitted, registered and annotated."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture(root)
            for lint in (
                {"ignore": ["S603"]},
                {"extend-ignore": ["S603"]},
                {"extend-per-file-ignores": {"x.py": ["S603"]}},
                {"per-file-ignores": {"absent.py": ["PT009"]}},
                {"per-file-ignores": {"scripts/preference_roots.py": ["S603"]}},
                {"per-file-ignores": {"scripts/preference_roots.py": ["PT009"]}},
            ):
                with self.subTest(lint=lint), self.assertRaises(PreferenceCheckError):
                    check_exceptions(root, registry(), {"lint": lint}, TODAY)

    def test_framework_waiver_has_named_classes_and_an_adjacent_reason(self) -> None:
        """A configured framework exception cannot drift from its source classes."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture(root)
            (root / "tests").mkdir()
            path = "tests/test_preference_example.py"
            (root / path).write_text(
                "import unittest\nclass Example(unittest.TestCase):\n    pass\n",
                encoding="utf-8",
            )
            entry = {
                **exception(),
                "id": "PREF-EXAMPLE-PT009",
                "diagnostic": "PT009",
                "path": path,
                "symbols": ["Example"],
            }
            document = {**registry(), "entries": [exception(), entry]}
            config = {"lint": {"per-file-ignores": {path: ["PT009"]}}}
            with self.assertRaisesRegex(
                PreferenceCheckError, "configured_reason_required"
            ):
                check_exceptions(root, document, config, TODAY)
            (root / "verification/ruff.toml").write_text(
                f'[lint.per-file-ignores]\n"{path}" = ["PT009"] # PREF-EXAMPLE-PT009: unittest assertions.\n',
                encoding="utf-8",
            )
            self.assertEqual(check_exceptions(root, document, config, TODAY), 2)
            (root / path).write_text(
                "import unittest\nclass Example(unittest.TestCase):\n"
                "    def inquire(self):\n"
                "        # policy-exception: PREF-EXAMPLE-PT009 -- Conflicting identity.\n"
                "        subprocess.run(arguments)  # noqa: S603\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                PreferenceCheckError, "duplicate_suppression_identity"
            ):
                check_exceptions(root, document, config, TODAY)
            (root / path).write_text("class Example:\n    pass\n", encoding="utf-8")
            with self.assertRaisesRegex(
                PreferenceCheckError, "framework_scope_mismatch"
            ):
                check_exceptions(root, document, config, TODAY)
