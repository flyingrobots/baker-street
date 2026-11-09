"""Trials of the commonplace book; no real case particulars are admitted."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/ledger.py'


class LedgerTests(unittest.TestCase):
    def record(self, **changes):
        value = dict(series='series-a', case_id='case-a', round=1,
                     reviewed_head='a' * 40, tier='focused', finding_id='F-1',
                     raised_by='holmes', event='RAISED', severity='LOW',
                     status='CONFIRMED', disposition='REQUIRED_REPAIR',
                     recorded_at='2026-11-09T00:00:00+00:00',
                     cost=dict(elapsed_seconds=10, tokens=100))
        value.update(changes)
        return value

    def run_summary(self, lines, *args):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'findings.jsonl'
            path.write_text(''.join((json.dumps(x) if not isinstance(x, str) else x) + '\n' for x in lines))
            return subprocess.run([sys.executable, str(SCRIPT), 'summarize', '--ledger', str(path), *args],
                                  capture_output=True, text=True, timeout=10)

    def summary(self, lines):
        result = self.run_summary(lines, '--json')
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_latest_states_keep_series_separate(self):
        lines = [self.record(), self.record(event='WITHDRAWN', status='WITHDRAWN', disposition='ACCEPTED', round=2),
                 self.record(series='series-b', raised_by='watson', severity='MODERATE'),
                 self.record(finding_id='F-2', raised_by='moriarty', round=2, event='REPAIRED')]
        out = self.summary(lines)
        self.assertEqual(out['total_findings'], 3)
        self.assertEqual(out['by_role']['holmes']['LOW']['withdrawn'], 1)
        self.assertEqual(out['by_role']['holmes']['LOW']['confirmed'], 0)
        self.assertEqual(out['by_role']['moriarty']['LOW']['repaired'], 1)
        self.assertEqual(out['by_round']['2']['LOW']['raised'], 2)
        self.assertEqual(out['discovery_by_round']['1'], 2)
        self.assertEqual(out['discovery_by_round']['2'], 1)
        self.assertEqual(out['median_cost_by_round']['2']['elapsed_seconds'], 10)

    def test_standalone_case_mapping_is_prescribed(self):
        records = (ROOT / 'references/records.md').read_text()
        self.assertIn('For a standalone case without review series fields', records)
        self.assertIn('`case:` followed by the exact `case_id`', records)
        self.assertIn('use `round` 1', records)

    def test_invalid_utf8_reports_the_physical_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'bad.jsonl'
            path.write_bytes((json.dumps(self.record()) + '\n').encode() * 2 + b'\xff\n')
            result = subprocess.run([sys.executable, str(SCRIPT), 'summarize', '--ledger', str(path)],
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertIn('line 3', result.stderr)

    def test_large_integer_cost_median_remains_exact(self):
        huge = 10 ** 1000
        out = self.summary([self.record(cost=dict(tokens=huge, elapsed_seconds=huge)),
                            self.record(finding_id='F-2', cost=dict(tokens=huge, elapsed_seconds=huge))])
        self.assertEqual(out['median_cost_by_round']['1']['tokens'], huge)

    def test_empty_and_unknown_costs(self):
        self.assertEqual(self.summary([])['total_findings'], 0)
        out = self.summary([self.record(cost={'elapsed_seconds': 'UNKNOWN', 'tokens': 'UNKNOWN'})])
        self.assertEqual(out['median_cost_by_round']['1'], {'elapsed_seconds': None, 'tokens': None})

    def test_text_and_json_have_the_same_counts(self):
        lines = [self.record()]
        self.assertEqual(json.loads(self.run_summary(lines).stdout), self.summary(lines))

    def test_invalid_lines_fail_closed(self):
        missing = self.record(); del missing['tier']
        bad = [missing, self.record(raised_by='outsider'), self.record(round=True),
               self.record(cost={'tokens': -1, 'elapsed_seconds': 0}),
               self.record(recorded_at='2026-11-09T00:00:00'),
               self.record(reviewed_head='abc'), self.record(private_text='forbidden')]
        for line in bad:
            with self.subTest(line=line):
                result = self.run_summary([line], '--json')
                self.assertEqual(result.returncode, 2)
                self.assertIn('line 1', result.stderr)
                self.assertEqual(result.stdout, '')
        result = self.run_summary([self.record(), self.record(), '{bad'])
        self.assertEqual(result.returncode, 2)
        self.assertIn('line 3', result.stderr)

    def test_ten_thousand_events_have_distinct_pair_total(self):
        lines = [self.record(series='series-' + str(i % 7), finding_id='F-' + str(i % 31),
                             round=1 + i % 3) for i in range(10000)]
        self.assertEqual(self.summary(lines)['total_findings'], len({(x['series'], x['finding_id']) for x in lines}))


if __name__ == '__main__':
    unittest.main()
