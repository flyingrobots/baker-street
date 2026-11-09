"""Packet assembly checks; these do not measure agent behavior."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SKILL = Path(os.environ.get('BAKER_SKILL_DIR', Path(__file__).resolve().parents[1])).resolve()


class PacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (SKILL/'scripts/build_packet.py').is_file():
            raise FileNotFoundError(
                f'Required packet builder missing: {SKILL / "scripts/build_packet.py"}. '
                'Restore the complete skill or set BAKER_SKILL_DIR to its folder.'
            )
        spec = importlib.util.spec_from_file_location('packet_builder', SKILL/'scripts/build_packet.py')
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def header(self):
        h = {key: 'Explicit fixture value' for key in self.module.REQUIRED}
        h.update(tier='focused', plain=True, reviewer_basis='SEQUENTIAL_SELF_CHECK')
        return h

    def test_review_basis_accepts_full_and_both_delta_methods(self):
        for basis in ('FULL', {'method': 'DELTA_ANCESTOR', 'from_head': 'a' * 40,
                              'to_head': 'b' * 40},
                      {'method': 'DELTA_RANGE_DIFF', 'from_head': 'a' * 40,
                       'to_head': 'b' * 40}):
            h = self.series(2, review_basis=basis)
            self.module.build('holmes', h)

    def test_review_basis_rejects_invalid_deltas(self):
        valid = {'method': 'DELTA_ANCESTOR', 'from_head': 'a' * 40, 'to_head': 'b' * 40}
        cases = [self.series(1, review_basis=valid),
                 self.series(2, review_basis=dict(valid, from_head='c' * 40)),
                 self.series(2, review_basis=dict(valid, to_head='a' * 40)),
                 self.series(2, review_basis=dict(valid, method='UNKNOWN')),
                 self.series(2, review_basis=dict(valid, from_head='a' * 7)),
                 self.series(2, review_basis=dict(valid, to_head='b' * 7)),
                 self.series(2, review_basis={}), self.series(2, review_basis=[]),
                 self.series(2, review_basis='DELTA_ANCESTOR')]
        for h in cases:
            with self.subTest(header=h), self.assertRaises(ValueError):
                self.module.build('holmes', h)

    def test_same_head_reassessment_uses_full_basis(self):
        skill = (SKILL / 'SKILL.md').read_text()
        self.assertIn('If the heads are identical, use `FULL`', skill)
        self.module.build('holmes', self.series(2, review_basis='FULL'))

    def test_absent_review_basis_does_not_change_packet(self):
        h = self.header()
        packet = self.module.build('holmes', h)
        self.assertNotIn('review_basis', packet.split('## Assigned case header', 1)[1])
        self.assertEqual(packet, self.module.build('holmes', dict(h)))

    def test_all_roles_receive_complete_rules_and_schemas(self):
        for role in self.module.ROLES:
            with self.subTest(role=role):
                packet = self.module.build(role, self.header())
                for name in ('references/core.md', 'references/records.md', f'roles/{role}.md'):
                    self.assertIn((SKILL/name).read_text(), packet)

    def test_instruction_digests_match_included_bytes(self):
        packet = self.module.build('holmes', self.header())
        for name in ('references/core.md', 'references/records.md', 'roles/holmes.md'):
            self.assertIn(hashlib.sha256((SKILL/name).read_bytes()).hexdigest(), packet)

    def test_missing_governing_file_fails_closed(self):
        old = self.module.ROOT
        try:
            with tempfile.TemporaryDirectory() as tmp:
                self.module.ROOT = Path(tmp)
                with self.assertRaises(FileNotFoundError):
                    self.module.build('holmes', self.header())
        finally:
            self.module.ROOT = old

    def test_header_omission_is_rejected(self):
        for key in self.module.REQUIRED:
            h = self.header(); del h[key]
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.module.build('holmes', h)

    def test_no_watson_or_moriarty_in_triage(self):
        h = self.header(); h['tier'] = 'triage'
        for role in ('watson', 'moriarty'):
            with self.assertRaises(ValueError): self.module.build(role, h)
        self.module.build('holmes', h)
        self.module.build('checker', h)

    def test_actual_checker_basis_is_required_and_preserved(self):
        h = self.header()
        self.assertIn('SEQUENTIAL_SELF_CHECK', self.module.build('checker', h))
        del h['reviewer_basis']
        with self.assertRaises(ValueError): self.module.build('checker', h)

    def test_plain_is_boolean_not_truthy_string(self):
        h = self.header(); h['plain'] = 'false'
        with self.assertRaises(ValueError): self.module.build('holmes', h)

    def series(self, round_number=2, **overrides):
        h = self.header()
        h.update(review_series='github:flyingrobots/baker-street/pull/12', round=round_number,
                 prior_case=({'case_id': 'CASE-1', 'reviewed_head': 'a' * 40}
                             if round_number != 1 else 'NONE'))
        h.update(overrides)
        return h

    def test_valid_series_fields_are_accepted_and_preserved(self):
        sha256_head = {'case_id': 'CASE-1', 'reviewed_head': 'b' * 64}
        for h in (self.series(1), self.series(2), self.series(2, round_budget=3),
                  self.series(2, round_budget=2), self.series(2, prior_case=sha256_head)):
            with self.subTest(header=h):
                packet = self.module.build('holmes', h)
                assigned = packet.split('## Assigned case header\n\n```json\n', 1)[1].split('\n```', 1)[0]
                self.assertEqual(json.loads(assigned), json.loads(json.dumps(h)))

    def test_header_without_series_fields_is_unchanged(self):
        h = self.header()
        self.assertEqual(self.module.build('holmes', h), self.module.build('holmes', dict(h)))
        assigned = self.module.build('holmes', h).split('## Assigned case header', 1)[1]
        self.assertNotIn('review_series', assigned)

    def test_invalid_series_fields_are_rejected(self):
        cases = {
            'round zero': self.series(0),
            'round string': self.series('2'),
            'round boolean': self.series(True),
            'round 2 without prior case': self.series(2, prior_case='NONE'),
            'round 1 with prior case': self.series(1, prior_case={'case_id': 'CASE-1', 'reviewed_head': 'a' * 40}),
            'prior case missing head': self.series(2, prior_case={'case_id': 'CASE-1'}),
            'prior case empty id': self.series(2, prior_case={'case_id': '', 'reviewed_head': 'a' * 40}),
            'prior head short': self.series(2, prior_case={'case_id': 'CASE-1', 'reviewed_head': 'a' * 12}),
            'prior head not hex': self.series(2, prior_case={'case_id': 'CASE-1', 'reviewed_head': 'x'}),
            'prior head uppercase': self.series(2, prior_case={'case_id': 'CASE-1', 'reviewed_head': 'A' * 40}),
            'empty series': self.series(2, review_series=''),
            'budget zero': self.series(2, round_budget=0),
            'budget boolean': self.series(2, round_budget=True),
            'budget without series': dict(self.header(), round_budget=2),
        }
        for key in ('review_series', 'round', 'prior_case'):
            partial = self.series(2); del partial[key]
            cases[f'missing {key}'] = partial
        for name, h in cases.items():
            with self.subTest(name), self.assertRaises(ValueError):
                self.module.build('holmes', h)

    def test_charter_is_included_when_requested(self):
        self.assertIn((SKILL/'references/charter.md').read_text(),
                      self.module.build('watson', self.header(), include_charter=True))

    def test_stateful_review_is_included_only_when_requested(self):
        reference = (SKILL/'references/stateful-code-review.md').read_text()
        self.assertNotIn(reference, self.module.build('moriarty', self.header()))
        for role in self.module.ROLES:
            with self.subTest(role=role):
                packet = self.module.build(role, self.header(), include_stateful_review=True)
                self.assertIn(reference, packet)
                self.assertIn(hashlib.sha256((SKILL/'references/stateful-code-review.md')
                                             .read_bytes()).hexdigest(), packet)

    def test_cli_includes_stateful_review_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            header = Path(tmp)/'header.json'; header.write_text(json.dumps(self.header()))
            out = Path(tmp)/'moriarty.md'
            result = subprocess.run([sys.executable, str(SKILL/'scripts/build_packet.py'),
                                     '--role', 'moriarty', '--header', str(header), '--out', str(out),
                                     '--include-stateful-review'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn((SKILL/'references/stateful-code-review.md').read_text(), out.read_text())

    def test_cli_writes_once_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            header = Path(tmp)/'header.json'; header.write_text(json.dumps(self.header()))
            out = Path(tmp)/'packets/checker.md'
            cmd = [sys.executable, str(SKILL/'scripts/build_packet.py'), '--role', 'checker',
                   '--header', str(header), '--out', str(out)]
            first = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = out.read_bytes()
            second = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(second.returncode, 2)
            self.assertEqual(out.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
