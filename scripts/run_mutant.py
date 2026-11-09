#!/usr/bin/env python3
"""Try a named forgery in a fair copy; this instrument is not a sandbox."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import tarfile
import time

LIMIT = 128 * 1024 * 1024


def clean_environment():
    result = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    result["GIT_NO_REPLACE_OBJECTS"] = "1"
    return result


def inside(path, parent):
    return path == parent or parent in path.parents


def physically_inside(path, parent):
    if inside(path, parent): return True
    for ancestor in (path, *path.parents):
        if ancestor.exists() and ancestor.samefile(parent): return True
    return False


def stop_group(process):
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


def run(command, cwd, stdout, stderr, timeout):
    def limits():
        import resource
        resource.setrlimit(resource.RLIMIT_FSIZE, (LIMIT, LIMIT))
    with stdout.open('wb') as out, stderr.open('wb') as err:
        process = subprocess.Popen(command, cwd=cwd, stdout=out, stderr=err,
                                   stdin=subprocess.DEVNULL, start_new_session=True,
                                   preexec_fn=limits, env=clean_environment())
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            stop_group(process)
            raise TimeoutError('The allotted time expired')
        # A command may finish while servants remain in its process group.
        stop_group(process)
        return code


def validate(record):
    if not isinstance(record, dict):
        raise ValueError('The mutant record must be an object')
    if not isinstance(record.get('name'), str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', record['name']):
        raise ValueError('The mutant requires a stable lowercase hyphenated name')
    if not isinstance(record.get('base_head'), str) or not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', record['base_head']):
        raise ValueError('base_head requires a full commit ID')
    patch = record.get('patch')
    if not isinstance(patch, dict) or not isinstance(patch.get('path'), str) or not patch['path']:
        raise ValueError('patch requires a case-relative path')
    if not isinstance(patch.get('sha256'), str) or not re.fullmatch('[0-9a-f]{64}', patch['sha256']):
        raise ValueError('patch requires a SHA-256 digest')
    command = record.get('command')
    if not isinstance(command, list) or not command or any(not isinstance(x, str) or not x or '\0' in x for x in command):
        raise ValueError('command requires nonempty argument strings')
    if not isinstance(record.get('expected_red'), str) or not record['expected_red'].strip():
        raise ValueError('expected_red requires the intended contract violation')


def trial(repo, mutant, out, timeout):
    if os.name != 'posix':
        raise ValueError('This instrument requires POSIX process groups')
    if timeout <= 0 or not timeout < float('inf'):
        raise ValueError('timeout must be finite and positive')
    repo = repo.resolve(strict=True); out = out.resolve()
    # Reject every path into the source worktree or its shared Git authority.
    authority = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', '--git-common-dir'],
                                        text=True, timeout=10, env=clean_environment()).removesuffix('\n')
    authority = (repo / authority).resolve()
    top = Path(subprocess.check_output(['git', '-C', str(repo), 'rev-parse', '--show-toplevel'],
                                       text=True, timeout=10, env=clean_environment()).removesuffix('\n')).resolve()
    if physically_inside(out, top) or physically_inside(out, authority):
        raise ValueError('The output must lie outside the source checkout and Git authority')
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError('The output exists and is not empty')
    record = json.loads(mutant.read_text(encoding='utf-8')); validate(record)
    case = mutant.resolve().parent
    patch_path = (case / record['patch']['path']).resolve()
    if Path(record['patch']['path']).is_absolute() or not inside(patch_path, case):
        raise ValueError('The patch must remain within the case directory')
    out.mkdir(parents=True, exist_ok=True)
    result = dict(name=record['name'], patch_sha256=record['patch']['sha256'],
                  base_head=record['base_head'], command=record['command'], exit_code=None,
                  stdout='stdout.txt', stderr='stderr.txt', elapsed_seconds=0, outcome='BLOCKED')
    start = time.monotonic(); scratch = out / 'scratch'
    (out / 'stdout.txt').touch(); (out / 'stderr.txt').touch()
    try:
        if patch_path.stat().st_size > LIMIT:
            raise ValueError('The patch exceeds the size allowance')
        patch = patch_path.read_bytes()
        if hashlib.sha256(patch).hexdigest() != record['patch']['sha256']:
            raise ValueError('The patch digest does not agree')
        # Copy the verified bytes before applying; a later source edit cannot substitute another patch.
        saved_patch = out / 'applied.diff'; saved_patch.write_bytes(patch)
        kind = subprocess.check_output(['git', '-C', str(repo), 'cat-file', '-t', record['base_head']],
                                       text=True, timeout=10, env=clean_environment()).removesuffix('\n')
        if kind != 'commit':
            raise ValueError('base_head must identify a commit object')
        isolated = out / 'source.git'
        object_format = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', '--show-object-format'],
                                                text=True, timeout=10, env=clean_environment()).removesuffix('\n')
        code = run(['git', 'init', '--bare', '--object-format=' + object_format, str(isolated)], case,
                   out / 'init.stdout', out / 'init.stderr', min(timeout, 30))
        if code: raise ValueError('The isolated Git authority could not be prepared')
        objects = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', '--git-path', 'objects'],
                                          text=True, timeout=10, env=clean_environment()).removesuffix('\n')
        objects = (repo / objects).resolve()
        if '\n' in str(objects) or '\r' in str(objects):
            raise ValueError('The object-store path contains unsupported line breaks')
        (isolated / 'objects/info/alternates').write_text(str(objects) + '\n')
        (isolated / 'info/attributes').write_text('* -export-ignore -export-subst -text -eol\n')
        archive = out / 'source.tar'
        code = run(['git', '--git-dir=' + str(isolated), 'archive', '--format=tar', record['base_head']],
                   case, archive, out / 'export.stderr', min(timeout, 30))
        if code:
            raise ValueError('The source export failed')
        scratch.mkdir()
        with tarfile.open(archive) as source:
            members = source.getmembers()
            if sum(m.size for m in members) > LIMIT:
                raise ValueError('The extracted source exceeds the size allowance')
            for member in members:
                target = (scratch / member.name).resolve()
                if not inside(target, scratch) or not (member.isfile() or member.isdir()):
                    raise ValueError('The archive contains an unsafe path or unsupported link')
            source.extractall(scratch, members=members)
        code = run(['git', '--git-dir=' + str(isolated), '--work-tree=' + str(scratch),
                    '-c', 'core.bare=false', '-c', 'core.autocrlf=false', '-c', 'core.eol=lf', 'apply', '--no-index', '--whitespace=nowarn', str(saved_patch)], scratch,
                   out / 'apply.stdout', out / 'apply.stderr', min(timeout, 30))
        if code:
            raise ValueError('The patch could not be applied')
        code = run(record['command'], scratch, out / 'stdout.txt', out / 'stderr.txt', timeout)
        result.update(exit_code=code, outcome='PASSED' if code == 0 else 'FAILED')
    except (OSError, ValueError, TimeoutError, tarfile.TarError, subprocess.SubprocessError) as exc:
        result['reason'] = str(exc)
    finally:
        result['elapsed_seconds'] = time.monotonic() - start
        (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path, required=True); p.add_argument('--mutant', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True); p.add_argument('--timeout', type=float, required=True)
    args = p.parse_args()
    try:
        result = trial(args.repo, args.mutant, args.out, args.timeout)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        p.exit(2, 'Trial refused: ' + str(exc) + '\n')
    print(json.dumps(result, sort_keys=True))
    return 2 if result['outcome'] == 'BLOCKED' else 0


if __name__ == '__main__':
    raise SystemExit(main())
