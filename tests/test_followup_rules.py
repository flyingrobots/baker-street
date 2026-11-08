"""Regression checks for the authorized PR #8 follow-ups."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def words(path):
    return ' '.join((ROOT / path).read_text(encoding='utf-8').split())


class FollowupRuleTests(unittest.TestCase):
    def test_skill_defers_required_repairs_to_records(self):
        text = words('SKILL.md')
        self.assertIn('All tiers: apply the adverse-consequence rule in records to required repairs.', text)
        self.assertNotIn('All tiers: tie required repairs to contracts or acceptance criteria.', text)
