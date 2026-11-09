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

    def run_trial(self, name='out', timeout=2):
        record = self.root / 'mutant.json'; record.write_text(json.dumps(self.record))
        before = self.snapshot()
        result = subprocess.run([sys.executable, str(SCRIPT), '--repo', str(self.repo), '--mutant', str(record),
                                 '--out', str(self.root / name), '--timeout', str(timeout)], capture_output=True, text=True, timeout=15)
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
