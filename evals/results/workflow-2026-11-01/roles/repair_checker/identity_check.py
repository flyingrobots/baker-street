"""Bounded read-only identity check; no target import or behavior execution."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = '666ee650d87d008dea3e74292f96c52cb1e1d9f7'
HEAD = '4522b92ee31452a0d038d4c83f16b327760b03ad'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def git(worktree, *args):
    command = ['/usr/bin/git', '-C', str(ROOT / worktree), *args]
    result = subprocess.run(command, check=True, capture_output=True, timeout=2,
                            env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'})
    assert len(result.stdout) < 65536 and len(result.stderr) < 65536
    return result.stdout

print(json.dumps({'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()}))
paths = [ROOT / p for p in ['REMEDIATION_DRAFT.md', 'CASE_FILE.md', 'ERRATA.md',
    'REPAIR_PLAN.json', 'repair-identity.json', 'freeze-original-case.json',
    'repair.diff', 'capture.py', 'packets/repair-checker.md']]
for folder in ['original', 'repair']:
    paths += [ROOT / folder / name for name in ['CONTRACT.md', 'capacity.py', 'test_capacity.py']]
for role in ['front_office', 'holmes', 'watson', 'moriarty', 'checker']:
    paths += sorted(p for p in (ROOT / 'roles' / role).rglob('*') if p.is_file())
for path in paths:
    data = path.read_bytes()
    print(json.dumps({'path': str(path.relative_to(ROOT)), 'bytes': len(data), 'sha256': digest(data)}))

for worktree, expected in [('original', BASE), ('repair', HEAD)]:
    actual_head = git(worktree, 'rev-parse', 'HEAD').decode().strip()
    status = git(worktree, 'status', '--porcelain=v1', '--untracked-files=all').decode()
    assert actual_head == expected and status == ''
    for name in ['CONTRACT.md', 'capacity.py', 'test_capacity.py']:
        assert git(worktree, 'show', f'HEAD:{name}') == (ROOT / worktree / name).read_bytes()
    print(json.dumps({'worktree': worktree, 'head': actual_head, 'status': status,
                      'all_three_worktree_files_equal_commit_blobs': True}))
assert git('repair', 'rev-parse', 'HEAD^').decode().strip() == BASE
assert git('repair', 'branch', '--show-current').decode().strip() == 'fix/baker-exact-fill'
actual_diff = git('repair', 'diff', '--no-ext-diff', '--no-textconv', BASE, HEAD, '--')
assert actual_diff == (ROOT / 'repair.diff').read_bytes()
assert (ROOT / 'original/CONTRACT.md').read_bytes() == (ROOT / 'repair/CONTRACT.md').read_bytes()
original_probe = (ROOT / 'roles/moriarty/contract_probe.py').read_bytes()
assert original_probe.replace(b'root / "original"', b'root / "repair"') == (ROOT / 'roles/front_office/surrounding.py').read_bytes()
frozen = json.loads((ROOT / 'freeze-original-case.json').read_text())['sha256']
for path, expected in frozen.items():
    assert digest((ROOT / path).read_bytes()) == expected
for role in ['front_office', 'holmes', 'moriarty']:
    for path in (ROOT / 'roles' / role).glob('*/run.json'):
        record = json.loads(path.read_text())
        script = ROOT / record['command'][-1]
        assert digest(script.read_bytes()) == record['script_sha256']
print(json.dumps({'parent_and_branch_match': True, 'saved_full_diff_matches_git': True,
    'contract_unchanged': True, 'surrounding_only_import_path_changed': True,
    'all_frozen_original_case_hashes_match': True, 'all_receipt_script_hashes_match': True}))
