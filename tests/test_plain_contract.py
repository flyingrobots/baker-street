"""Check the frozen-evidence precedence required by the plain-manner contract."""

import unittest
from pathlib import Path


class PlainContractTests(unittest.TestCase):
    """Retain the explicit rule whose absence permits alteration of evidence."""

    def test_a_later_plain_choice_preserves_frozen_testimony(self) -> None:
        """Oracle: the case's style choice cannot rewrite its frozen evidence."""
        root = Path(__file__).resolve().parents[1]
        instructions = " ".join((root / "SKILL.md").read_text(encoding="utf-8").split())
        self.assertIn(
            "Reports frozen before a recorded change of manner remain unchanged as evidence.",
            instructions,
        )
