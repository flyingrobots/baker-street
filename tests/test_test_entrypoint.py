"""The public unittest command must fail when the required skill is missing."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class TestEntrypointTests(unittest.TestCase):
    def test_missing_packet_builder_is_an_error(self):
        for explicit_override in (False, True):
            with self.subTest(explicit_override=explicit_override), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                tests = root / 'tests'
                tests.mkdir()
                shutil.copy2(Path(__file__).with_name('test_packets.py'), tests)
                env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
                env.pop('BAKER_SKILL_DIR', None)
                if explicit_override:
                    env['BAKER_SKILL_DIR'] = str(root / 'missing-skill')
                result = subprocess.run(
                    [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                    cwd=root, env=env, capture_output=True, text=True, timeout=20,
                )
                self.assertNotEqual(result.returncode, 0, result.stderr)
                self.assertIn('Required packet builder missing', result.stderr)
                self.assertNotIn('skipped=', result.stderr)
