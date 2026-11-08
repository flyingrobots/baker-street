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

    def test_readme_distinguishes_implemented_rules_from_planned_work(self):
        section = words('README.md').split('## In preparation', 1)[1].split('## Repository contents', 1)[0]
        self.assertIn('The round budget with referral to the user and the consequence floor for required repairs are implemented on main.', section)
        self.assertIn('Still planned:', section)
        self.assertNotIn('None of it is in the current release.', section)
