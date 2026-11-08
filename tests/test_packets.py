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
