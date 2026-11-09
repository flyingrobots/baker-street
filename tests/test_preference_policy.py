"""Keep the preference exceptions confined to their stated diagnostics."""

import io
import json
import re
import tokenize
import unittest
from pathlib import Path
from typing import TypeGuard

ROOT = Path(__file__).resolve().parents[1]


def object_mapping(value: object) -> TypeGuard[dict[object, object]]:
    """Narrow the container while retaining untrusted keys and values."""
    return isinstance(value, dict)


def object_array(value: object) -> TypeGuard[list[object]]:
    """Narrow an array without assuming the shape of its elements."""
    return isinstance(value, list)


def entries() -> list[dict[str, object]]:
    """Read the maintained registry with explicit container checks."""
    document: object = json.loads(
        (ROOT / "verification/exceptions.json").read_text(encoding="utf-8")
    )
    if not object_mapping(document) or not object_array(document.get("entries")):
        message = "The exception registry requires an entries array"
        raise ValueError(message)
    values = document["entries"]
    if not object_array(values):
        message = "The exception registry requires an entries array"
        raise ValueError(message)
    admitted: list[dict[str, object]] = []
    for value in values:
        if not object_mapping(value):
            message = "An exception entry must be an object"
            raise ValueError(message)
        entry: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                message = "An exception field name must be a string"
                raise TypeError(message)
            entry[key] = item
        admitted.append(entry)
    return admitted


class PreferencePolicyTests(unittest.TestCase):
    """Check suppression contracts independently of the runtime preferences."""

    def test_ci_runs_coverage_and_exception_admission(self) -> None:
        """The quality job must execute the checks rather than merely describe them."""
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("coverage run --branch", workflow)
        self.assertIn("coverage json", workflow)
        self.assertIn("python verification/check_preferences.py --coverage", workflow)

    def test_each_registry_entry_names_one_diagnostic(self) -> None:
        """An entry cannot silently combine separately justified diagnostics."""
        for entry in entries():
            with self.subTest(identifier=entry.get("id")):
                diagnostic = entry.get("diagnostic")
                self.assertIsInstance(diagnostic, str)
                if isinstance(diagnostic, str):
                    self.assertRegex(diagnostic, r"^[A-Z]+[0-9]+$")

    def test_process_diagnostic_is_never_suppressed_for_a_whole_file(self) -> None:
        """A later unrelated process call must still receive its own examination."""
        profile = (ROOT / "verification/ruff.toml").read_text(encoding="utf-8")
        section = profile.split("[lint.per-file-ignores]", 1)[1].split("\n[", 1)[0]
        self.assertIsNone(re.search(r"['\"]S603['\"]", section))

    def test_process_exception_has_one_adjacent_identified_reason(self) -> None:
        """The exact call carries its registry identity and an explanatory reason."""
        for entry in entries():
            if entry.get("diagnostic") != "S603":
                continue
            identifier, path = entry.get("id"), entry.get("path")
            if not isinstance(identifier, str) or not isinstance(path, str):
                message = "An exception needs a string identity and path"
                raise TypeError(message)
            source = (ROOT / path).read_text(encoding="utf-8")
            comments = {
                token.start[0]: token.string
                for token in tokenize.generate_tokens(io.StringIO(source).readline)
                if token.type == tokenize.COMMENT
            }
            pattern = rf"# policy-exception: {re.escape(identifier)} -- \S.+"
            with self.subTest(identifier=identifier):
                self.assertEqual(
                    sum(
                        comment == "# noqa: S603"
                        and re.fullmatch(pattern, comments.get(line - 1, ""))
                        is not None
                        for line, comment in comments.items()
                    ),
                    1,
                )
