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
        planned = section.split('Still planned:', 1)[1].split('.', 1)[0]
        self.assertIn('delta reviews for follow-up cases', planned)
        self.assertIn('a findings ledger', planned)
        self.assertIn('named mutants run in a scratch copy', planned)
        self.assertNotIn('round budget', planned)
        self.assertNotIn('consequence floor', planned)
        self.assertNotIn('None of it is in the current release.', section)

    def test_consequence_fallback_allows_explicit_acceptance(self):
        rule = words('references/records.md').split('Adverse consequence:', 1)[1].split('## Attempts', 1)[0]
        self.assertIn(
            'A CONFIRMED finding that fails this rule is FOLLOW_UP by default, and any proposed repairs '
            'have scope FOLLOW_UP; it may instead be ACCEPTED with an explicit basis.',
            rule,
        )
        self.assertIn('A user acceptance required by repository rules or severity precedence must still come from the user.', rule)
        decisions = words('references/records.md').split('## Decisions', 1)[1].split('## Referrals', 1)[0]
        self.assertIn(
            'The one exception is an ACCEPTED HIGH finding with a recorded, explicit user acceptance '
            'and its basis; the decision statement names that finding and acceptance.',
            decisions,
        )
