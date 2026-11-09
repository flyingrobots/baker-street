"""Examine the clerk's derived copies and preserved former editions."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CaseBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('case_builder', ROOT / 'scripts/build_case.py')
        cls.module = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.module)

    def record(self):
        header = {key: 'Recorded fixture value' for key in self.module.packet_schema.REQUIRED}
        header.update(case_id='CASE-1', tier='triage', plain=False, sealed_basis={'head': 'a' * 40})
        return dict(header=header, findings=[],
                    errata=[], rulings=[], path_to_ready=[], followups=[], probe_triage=[],
                    coverage_matrix=[], decision='READY', notes='A synthetic account.')

    def finding(self, **changes):
        value = dict(id='F-1', mechanism='A recorded defect', severity='LOW', status='CONFIRMED',
                     basis=['SOURCE'], sources=['contract'], disposition='FOLLOW_UP')
        value.update(changes); return value

    def test_golden_determinism_and_version_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'case'; row = self.record()
            first = self.module.write_case(row, out)
            before = {str(p.relative_to(out)): p.read_bytes() for p in out.rglob('*') if p.is_file()}
            self.assertEqual(self.module.write_case(row, out), first)
            self.assertEqual(before, {str(p.relative_to(out)): p.read_bytes() for p in out.rglob('*') if p.is_file()})
            row['errata'] = [{'id': 'ER-1', 'original': 'former statement', 'correction': 'corrected statement', 'notes': 'reason'}]
            second = self.module.write_case(row, out)
            self.assertNotEqual(first, second)
            self.assertEqual((out / 'versions' / first / 'CASE_FILE.md').read_bytes(), before['CASE_FILE.md'])
            self.assertIn('ER-1', (out / 'ERRATA.md').read_text())
            self.assertIn(second, (out / 'CASE_FILE.md').read_text())

    def test_decision_precedence_and_user_acceptance(self):
        for change in ({'severity': 'HIGH'}, {'severity': 'CRITICAL'}, {'disposition': 'REQUIRED_REPAIR'}, {'disposition': 'INVESTIGATE'}):
            row = self.record(); row['findings'] = [self.finding(**change)]
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.module.render(row)
        row = self.record(); row['findings'] = [self.finding(severity='HIGH', disposition='ACCEPTED', user_acceptance='Maintainer expressly accepts this finding: supplied evidence')]
        self.module.render(row)
        row['findings'][0]['severity'] = 'CRITICAL'
        with self.assertRaises(ValueError): self.module.render(row)

    def test_counts_and_followups_are_derived(self):
        row = self.record(); row['findings'] = [self.finding(), self.finding(id='F-2', severity='MODERATE')]
        docs = self.module.render(row)
        self.assertIn('LOW: 1', docs['CASE_FILE.md']); self.assertIn('MODERATE: 1', docs['CASE_FILE.md'])
        self.assertIn('F-1', docs['FINDINGS_PROVISIONAL.md']); self.assertIn('F-2', docs['CASE_FILE.md'])
        row['followups'] = ['F-3']
        with self.assertRaises(ValueError): self.module.render(row)

    def test_missing_required_case_header_field_names_the_refusal(self):
        row = self.record()
        row['header'].pop('requested_decision', None)
        with self.assertRaisesRegex(ValueError, 'requested_decision'):
            self.module.render(row)

    def test_current_receipt_cannot_disagree_with_the_edition_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); row = self.record(); self.module.write_case(row, out)
            path = out / 'manifest.json'; manifest = json.loads(path.read_text())
            manifest['current'] = '0' * 64; path.write_text(json.dumps(manifest))
            row['notes'] = 'new edition'
            before = {str(p.relative_to(out)): p.read_bytes() for p in out.rglob('*') if p.is_file()}
            with self.assertRaises(ValueError): self.module.write_case(row, out)
            self.assertEqual(before, {str(p.relative_to(out)): p.read_bytes() for p in out.rglob('*') if p.is_file()})

    def test_receipt_cannot_omit_a_preserved_edition(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); row = self.record(); self.module.write_case(row, out)
            row['notes'] = 'second'; self.module.write_case(row, out)
            path = out / 'manifest.json'; manifest = json.loads(path.read_text())
            manifest['versions'] = manifest['versions'][-1:]; path.write_text(json.dumps(manifest))
            row['notes'] = 'third'
            before = {str(p.relative_to(out)): p.read_bytes() for p in out.rglob('*') if p.is_file()}
            with self.assertRaises(ValueError): self.module.write_case(row, out)
            self.assertEqual(before, {str(p.relative_to(out)): p.read_bytes() for p in out.rglob('*') if p.is_file()})

    def test_missing_field_duplicate_id_and_tampering_are_refused(self):
        row = self.record(); del row['coverage_matrix']
        with self.assertRaisesRegex(ValueError, 'coverage_matrix'): self.module.render(row)
        row = self.record(); row['findings'] = [self.finding(), self.finding()]
        with self.assertRaises(ValueError): self.module.render(row)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); row = self.record(); self.module.write_case(row, out)
            (out / 'CASE_FILE.md').write_text('hand amendment')
            row['notes'] = 'new input'
            with self.assertRaises(ValueError): self.module.write_case(row, out)

    def test_repin_refuses_contradictory_or_incomplete_receipts(self):
        packet = self.module.packet_schema
        for corruption in ('head', 'head_sameprefix', 'role', 'status', 'orphan'):
            with self.subTest(corruption=corruption), tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp); header = self.record()['header']
                packet.repin('holmes', header, 'a' * 40, out)
                path = out / 'manifest.json'; manifest = json.loads(path.read_text())
                if corruption == 'orphan':
                    (out / 'holmes-cccccccccccc.md').write_text('interrupted packet')
                else:
                    field = 'head' if corruption == 'head_sameprefix' else corruption
                    manifest['packets'][0][field] = {'head': 'c' * 40, 'head_sameprefix': 'a' * 12 + 'c' * 28, 'role': 'watson', 'status': 'INVENTED'}[corruption]
                    path.write_text(json.dumps(manifest))
                before = {p.name: p.read_bytes() for p in out.iterdir()}
                with self.assertRaises(ValueError): packet.repin('holmes', header, 'b' * 40, out)
                self.assertEqual(before, {p.name: p.read_bytes() for p in out.iterdir()})

    def test_case_cli_preserves_editions_and_refuses_an_interrupted_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'case.json'; out = root / 'papers'
            row = self.record(); source.write_text(json.dumps(row))
            command = [sys.executable, str(ROOT / 'scripts/build_case.py'), '--record', str(source), '--out', str(out)]
            def invoke():
                return subprocess.run(command, capture_output=True, text=True, timeout=10)
            first = invoke(); self.assertEqual(first.returncode, 0, first.stderr)
            before = {str(p.relative_to(out)): p.read_bytes() for p in out.rglob('*') if p.is_file()}
            self.assertEqual(invoke().returncode, 0)
            self.assertEqual(before, {str(p.relative_to(out)): p.read_bytes() for p in out.rglob('*') if p.is_file()})
            row['errata'] = [{'id': 'ER-1', 'correction': 'A recorded amendment'}]
            source.write_text(json.dumps(row)); second = invoke()
            self.assertEqual(second.returncode, 0, second.stderr)
            old_digest = first.stdout.strip()
            self.assertEqual((out / 'versions' / old_digest / 'CASE_FILE.md').read_bytes(), before['CASE_FILE.md'])
            row['notes'] = 'A third edition'; source.write_text(json.dumps(row))
            controller = ("import importlib.util,json,sys;from pathlib import Path;"
                          "s=importlib.util.spec_from_file_location('trial',sys.argv[1]);"
                          "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
                          "original=m.os.replace; count=[0]\n"
                          "def interrupted(a,b):\n"
                          " count[0]+=1\n"
                          " if count[0]==2: raise OSError('controlled interruption')\n"
                          " original(a,b)\n"
                          "m.os.replace=interrupted\n"
                          "m.write_case(json.loads(Path(sys.argv[2]).read_text()),Path(sys.argv[3]))\n")
            broken = subprocess.run([sys.executable, '-c', controller, str(ROOT / 'scripts/build_case.py'), str(source), str(out)],
                                    capture_output=True, text=True, timeout=10)
            self.assertNotEqual(broken.returncode, 0)
            self.assertIn('controlled interruption', broken.stderr)
            interrupted_state = {str(p.relative_to(out)): p.read_bytes() for p in out.rglob('*') if p.is_file()}
            retry = invoke(); self.assertEqual(retry.returncode, 2)
            self.assertIn('Case refused', retry.stderr)
            self.assertEqual(interrupted_state, {str(p.relative_to(out)): p.read_bytes() for p in out.rglob('*') if p.is_file()})

    def test_header_template_and_repin_preserve_former_packet(self):
        command = [sys.executable, str(ROOT / 'scripts/build_packet.py')]
        result = subprocess.run(command + ['--print-header-template'], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        header = json.loads(result.stdout)
        self.assertIn('case_id', header)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'header.json'; source.write_text(json.dumps(header))
            for head in ('a' * 40, 'b' * 40):
                result = subprocess.run(command + ['--role', 'holmes', '--header', str(source), '--out', str(root / 'packets'), '--repin', head], capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / 'packets/holmes-aaaaaaaaaaaa.md').exists())
            manifest = json.loads((root / 'packets/manifest.json').read_text())
            self.assertEqual(manifest['packets'][0]['status'], 'SUPERSEDED')
            self.assertEqual(manifest['packets'][1]['status'], 'CURRENT')
            before = {p.name: p.read_bytes() for p in (root / 'packets').iterdir()}
            result = subprocess.run(command + ['--role', 'holmes', '--header', str(source), '--out', str(root / 'packets'), '--repin', 'b' * 40], capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(before, {p.name: p.read_bytes() for p in (root / 'packets').iterdir()})


if __name__ == '__main__': unittest.main()
