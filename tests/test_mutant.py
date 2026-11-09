"""Finite trials in fair copies; preserve the original books."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/run_mutant.py'


class MutantTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name); self.repo = self.root / 'repo'; self.repo.mkdir()
        self.git('init', '-q'); self.git('config', 'user.name', 'Trial'); self.git('config', 'user.email', 'trial@example.invalid')
        (self.repo / 'value.txt').write_text('good\n'); self.git('add', '.'); self.git('commit', '-qm', 'Establish the fair copy')
        self.head = self.git('rev-parse', 'HEAD').strip()
        (self.repo / 'untracked.txt').write_text('preserve me')
        self.patch = self.root / 'fault.diff'
        self.patch.write_text('diff --git a/value.txt b/value.txt\n--- a/value.txt\n+++ b/value.txt\n@@ -1 +1 @@\n-good\n+bad\n')
        self.record = dict(name='value-turns-bad', base_head=self.head,
                           patch=dict(path='fault.diff', sha256=hashlib.sha256(self.patch.read_bytes()).hexdigest()),
                           command=[sys.executable, '-c', 'from pathlib import Path; assert Path("value.txt").read_text()=="good\\n"'],
                           expected_red='The value differs from the contract')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], text=True, stderr=subprocess.DEVNULL)

    def snapshot(self):
        return {str(p.relative_to(self.repo)): p.read_bytes() for p in self.repo.rglob('*') if p.is_file()}

    def run_trial(self, name='out', timeout=2, env=None):
        record = self.root / 'mutant.json'; record.write_text(json.dumps(self.record))
        before = self.snapshot()
        result = subprocess.run([sys.executable, str(SCRIPT), '--repo', str(self.repo), '--mutant', str(record),
                                 '--out', str(self.root / name), '--timeout', str(timeout)], capture_output=True, text=True, timeout=15, env=env)
        self.assertEqual(self.snapshot(), before)
        path = self.root / name / 'result.json'
        return result, json.loads(path.read_text()) if path.exists() else None

    def test_failed_and_passed_and_stable_identity(self):
        run, failed = self.run_trial()
        self.assertIsNotNone(failed, run.stderr); self.assertEqual(failed['outcome'], 'FAILED')
        self.record['command'] = [sys.executable, '-c', 'print("accepted")']
        run, passed = self.run_trial('second')
        self.assertEqual(passed['outcome'], 'PASSED'); self.assertEqual(failed['patch_sha256'], passed['patch_sha256'])

    def test_blocked_patch_command_digest_and_export(self):
        self.record['patch']['sha256'] = '0' * 64
        run, row = self.run_trial('digest'); self.assertEqual(row['outcome'], 'BLOCKED')
        self.record['patch']['sha256'] = hashlib.sha256(self.patch.read_bytes()).hexdigest()
        self.record['command'] = ['missing-command-for-baker-street']
        run, row = self.run_trial('command'); self.assertEqual(row['outcome'], 'BLOCKED')
        self.record['base_head'] = '0' * 40
        run, row = self.run_trial('export'); self.assertEqual(row['outcome'], 'BLOCKED')
        self.record['base_head'] = self.head
        self.patch.write_text(self.patch.read_text().replace('-good', '-absent'))
        self.record['patch']['sha256'] = hashlib.sha256(self.patch.read_bytes()).hexdigest()
        run, row = self.run_trial('patch'); self.assertEqual(row['outcome'], 'BLOCKED')

    def test_tree_object_cannot_impersonate_a_commit(self):
        self.record['base_head'] = self.git('rev-parse', 'HEAD^{tree}').strip()
        self.record['command'] = [sys.executable, '-c', 'pass']
        run, row = self.run_trial('tree')
        self.assertEqual(row['outcome'], 'BLOCKED')
        self.assertIn('commit', row['reason'])

    def test_replacement_object_cannot_change_the_sealed_source(self):
        (self.repo / 'value.txt').write_text('other\n')
        self.git('add', 'value.txt'); self.git('commit', '-qm', 'A different book')
        replacement = self.git('rev-parse', 'HEAD').strip()
        self.git('replace', self.head, replacement)
        self.record['command'] = [sys.executable, '-c', 'pass']
        run, row = self.run_trial('replacement')
        self.assertEqual(row['outcome'], 'PASSED')
        self.assertEqual((self.root / 'replacement/scratch/value.txt').read_text(), 'bad\n')

    def test_enclosing_repository_cannot_suppress_the_patch(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True, timeout=10)
        run, row = self.run_trial('nested')
        self.assertEqual(row['outcome'], 'FAILED')
        self.assertEqual((self.root / 'nested/scratch/value.txt').read_text(), 'bad\n')

    def test_export_attributes_cannot_remove_the_sealed_files(self):
        for mode in ('tracked', 'local'):
            with self.subTest(mode=mode):
                if mode == 'tracked':
                    (self.repo / '.gitattributes').write_text('value.txt export-ignore\n')
                    self.git('add', '.gitattributes'); self.git('commit', '-qm', 'Record export advice')
                    self.record['base_head'] = self.git('rev-parse', 'HEAD').strip()
                else:
                    (self.repo / '.git/info/attributes').write_text('value.txt export-ignore\n')
                run, row = self.run_trial(mode)
                self.assertEqual(row['outcome'], 'FAILED')
                self.assertEqual((self.root / mode / 'scratch/value.txt').read_text(), 'bad\n')

    def test_sha256_source_keeps_its_object_format(self):
        source = self.root / 'sha256-repo'
        init = subprocess.run(['git', 'init', '-q', '--object-format=sha256', str(source)], capture_output=True, text=True, timeout=10)
        if init.returncode: self.skipTest('Git does not support SHA-256 repositories')
        self.repo = source
        self.git('config', 'user.name', 'Trial'); self.git('config', 'user.email', 'trial@example.invalid')
        (source / 'value.txt').write_text('good\n'); self.git('add', '.'); self.git('commit', '-qm', 'Establish a SHA-256 book')
        self.record['base_head'] = self.git('rev-parse', 'HEAD').strip()
        run, row = self.run_trial('sha256')
        self.assertEqual(row['outcome'], 'FAILED')

    def test_global_whitespace_policy_cannot_change_patch_bytes(self):
        config = self.root / 'config/git'; config.mkdir(parents=True)
        (config / 'config').write_text('[apply]\nwhitespace = fix\n')
        self.patch.write_text(self.patch.read_text().replace('+bad\n', '+bad \n'))
        self.record['patch']['sha256'] = hashlib.sha256(self.patch.read_bytes()).hexdigest()
        run, row = self.run_trial('whitespace', env=dict(os.environ, XDG_CONFIG_HOME=str(config.parent)))
        self.assertEqual(row['outcome'], 'FAILED')
        self.assertEqual((self.root / 'whitespace/scratch/value.txt').read_bytes(), b'bad \n')

    def test_trailing_space_in_source_path_is_not_trimmed(self):
        renamed = self.root / 'repo '
        self.repo.rename(renamed); self.repo = renamed
        (self.root / 'repo').mkdir()
        run, row = self.run_trial('repo /output')
        self.assertEqual(run.returncode, 2)
        self.assertIsNone(row)

    def test_whitespace_only_expected_violation_is_refused(self):
        self.record['expected_red'] = '   '
        run, row = self.run_trial('blank-violation')
        self.assertEqual(run.returncode, 2)
        self.assertIsNone(row)

    def test_global_autocrlf_cannot_undo_a_line_ending_patch(self):
        self.git('config', 'core.autocrlf', 'false')
        (self.repo / 'value.txt').write_bytes(b'good\r\n')
        self.git('add', 'value.txt'); self.git('commit', '-qm', 'Record the original line endings')
        self.record['base_head'] = self.git('rev-parse', 'HEAD').strip()
        self.patch.write_bytes(b'diff --git a/value.txt b/value.txt\n--- a/value.txt\n+++ b/value.txt\n@@ -1 +1 @@\n-good\r\n+good\n')
        self.record['patch']['sha256'] = hashlib.sha256(self.patch.read_bytes()).hexdigest()
        self.record['command'] = [sys.executable, '-c', 'from pathlib import Path; assert Path("value.txt").read_bytes()==b"good\\r\\n"']
        config = self.root / 'config/git'; config.mkdir(parents=True)
        (config / 'config').write_text('[core]\nautocrlf = true\n')
        run, row = self.run_trial('autocrlf', env=dict(os.environ, XDG_CONFIG_HOME=str(config.parent)))
        self.assertEqual(row['outcome'], 'FAILED')
        self.assertEqual((self.root / 'autocrlf/scratch/value.txt').read_bytes(), b'good\n')
        attributes = (self.root / 'autocrlf/source.git/info/attributes').read_text()
        for guard in ('-text', '-eol', '-filter', '-ident'):
            self.assertIn(guard, attributes)

    def test_nonempty_output_refuses_without_writes(self):
        out = self.root / 'out'; out.mkdir(); (out / 'keep').write_text('unchanged')
        run, row = self.run_trial(); self.assertEqual(run.returncode, 2)
        self.assertEqual(list(out.iterdir()), [out / 'keep']); self.assertEqual((out / 'keep').read_text(), 'unchanged')

    def test_output_inside_checkout_or_symlink_is_refused(self):
        for name in ('repo/output', 'alias/output'):
            if name.startswith('alias'):
                (self.root / 'alias').symlink_to(self.repo, target_is_directory=True)
            run, row = self.run_trial(name)
            self.assertEqual(run.returncode, 2); self.assertIsNone(row)

    def test_case_alias_output_cannot_enter_the_source(self):
        alias = self.root / 'REPO'
        if not alias.exists() or not alias.samefile(self.repo):
            self.skipTest('The fixture filesystem distinguishes letter case')
        run, row = self.run_trial('REPO/output')
        self.assertEqual(run.returncode, 2)
        self.assertIsNone(row)

    @unittest.skipUnless(os.name == 'posix', 'Process-group examination requires POSIX')
    def test_timeout_stops_the_command_and_grandchild(self):
        code = ('import subprocess,sys,time; from pathlib import Path; '
                'p=subprocess.Popen([sys.executable,"-c","import time;time.sleep(60)"]); '
                'Path("child.pid").write_text(str(p.pid)); time.sleep(60)')
        self.record['command'] = [sys.executable, '-c', code]
        run, row = self.run_trial(timeout=.3)
        self.assertEqual(row['outcome'], 'BLOCKED')
        pid = int((self.root / 'out/scratch/child.pid').read_text())
        for _ in range(40):
            status = subprocess.run(['ps', '-o', 'stat=', '-p', str(pid)], capture_output=True, text=True).stdout.strip()
            if not status or status.startswith('Z'):
                break
            time.sleep(.025)
        else:
            os.kill(pid, signal.SIGKILL)
            self.fail('A descendant continued after the timeout')


if __name__ == '__main__':
    unittest.main()
