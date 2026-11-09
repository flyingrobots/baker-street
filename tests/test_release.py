"""Distribution boundary and integrity checks for the installed skill."""
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('release', ROOT / 'scripts/build_release.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def source(self, temporary):
        root = Path(temporary) / 'source'
        for name in release.SKILL_FILES:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        return root

    def test_only_runtime_files_and_valid_checksums_are_distributed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.source(tmp)
            for name in ('evals/fixtures/oracle.json', 'tests/answer.py', '.git/config', 'private.txt'):
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('MUST NOT SHIP')
            archive = release.build(root, Path(tmp) / 'dist', '3.0.0')
            with zipfile.ZipFile(archive) as bundle:
                self.assertEqual(set(bundle.namelist()),
                                 {f'baker-street/{p}' for p in release.SKILL_FILES} | {'baker-street/SHA256SUMS'})
                self.assertIn('baker-street/scripts/build_packet.py', bundle.namelist())
                self.assertIn('baker-street/roles/checker.md', bundle.namelist())
                self.assertIn('baker-street/references/stateful-code-review.md', bundle.namelist())
                for line in bundle.read('baker-street/SHA256SUMS').decode().splitlines():
                    digest, name = line.split('  ', 1)
                    self.assertEqual(digest, hashlib.sha256(bundle.read('baker-street/' + name)).hexdigest())
            digest, name = (archive.parent / 'SHA256SUMS').read_text().strip().split('  ', 1)
            self.assertEqual(name, archive.name)
            self.assertEqual(digest, hashlib.sha256(archive.read_bytes()).hexdigest())

    def test_installed_skill_contains_the_case_builder(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = release.build(ROOT, Path(tmp) / 'dist', '3.2.0')
            with zipfile.ZipFile(archive) as bundle:
                self.assertIn('baker-street/scripts/build_case.py', bundle.namelist())

    def test_installed_skill_contains_the_ledger_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = release.build(ROOT, Path(tmp) / 'dist', '3.2.0')
            with zipfile.ZipFile(archive) as bundle:
                self.assertIn('baker-street/scripts/ledger.py', bundle.namelist())

    def test_archive_does_not_depend_on_source_timestamps(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.source(tmp)
            first = release.build(root, Path(tmp) / 'one', '3.0.0').read_bytes()
            for name in release.SKILL_FILES:
                os.utime(root / name, (1234567890, 1234567890))
            second = release.build(root, Path(tmp) / 'two', '3.0.0').read_bytes()
            self.assertEqual(first, second)

    def test_missing_required_file_does_not_create_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.source(tmp)
            (root / 'roles/checker.md').unlink()
            out = Path(tmp) / 'dist'
            with self.assertRaises(FileNotFoundError): release.build(root, out, '3.0.0')
            self.assertFalse(out.exists())

    def test_symlink_cannot_inject_external_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.source(tmp)
            (root / 'SKILL.md').unlink()
            secret = Path(tmp) / 'secret'
            secret.write_text('MUST NOT SHIP')
            (root / 'SKILL.md').symlink_to(secret)
            with self.assertRaises(ValueError): release.build(root, Path(tmp) / 'dist', '3.0.0')

    def test_existing_release_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'dist'
            archive = release.build(ROOT, out, '3.0.0')
            original = archive.read_bytes()
            with self.assertRaises(FileExistsError): release.build(ROOT, out, '3.0.0')
            self.assertEqual(archive.read_bytes(), original)

    def test_version_cannot_escape_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError): release.build(ROOT, Path(tmp) / 'dist', '../bad')
