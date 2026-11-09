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

    def test_readme_records_the_delivered_correspondence(self):
        section = words('README.md').split('## The correspondent’s amendments', 1)[1].split('## Repository contents', 1)[0]
        for phrase in ('round budget and referral', 'consequence floor', 'delta examinations',
                       'external findings book', 'named forgeries', 'authoritative `case.json`'):
            self.assertIn(phrase, section)
        self.assertNotIn('Still planned:', section)
        self.assertNotIn('None of it is in the current release.', section)
        for name in ('build_case.py', 'ledger.py', 'run_mutant.py'):
            self.assertIn(name, section)
            self.assertTrue((ROOT / 'scripts' / name).is_file(), name)

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
