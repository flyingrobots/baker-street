#!/usr/bin/env python3
"""Prepare the case papers from one authoritative record; preserve former editions."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

FILES = ('CASE_FILE.md', 'ERRATA.md', 'FINDINGS_PROVISIONAL.md')
FIELDS = {'header', 'findings', 'errata', 'rulings', 'path_to_ready', 'followups', 'probe_triage', 'coverage_matrix', 'decision'}
SEVERITY = ('CRITICAL', 'HIGH', 'MODERATE', 'LOW', 'INFORMATIONAL', 'UNKNOWN')
STATUS = ('CONFIRMED', 'HYPOTHESIS', 'CONTESTED', 'WITHDRAWN')
DISPOSITION = ('REQUIRED_REPAIR', 'INVESTIGATE', 'FOLLOW_UP', 'ACCEPTED')
BASIS = ('SOURCE', 'EXECUTED', 'REPORTED', 'INFERENCE', 'NONE')


def canonical(record):
    return json.dumps(record, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')


def identity(record):
    return hashlib.sha256(canonical(record)).hexdigest()


def validate(record):
    if not isinstance(record, dict): raise ValueError('The case record must be an object')
    missing = FIELDS - set(record)
    if missing: raise ValueError('Missing fields: ' + ', '.join(sorted(missing)))
    if set(record) - (FIELDS | {'notes'}): raise ValueError('Unrecognised case fields')
    if not isinstance(record['header'], dict) or not isinstance(record['header'].get('case_id'), str) or not record['header']['case_id'].strip():
        raise ValueError('header requires case_id')
    if record['decision'] not in ('READY', 'CHANGES_REQUIRED', 'INVESTIGATION_REQUIRED', 'BLOCKED'):
        raise ValueError('Unrecognised decision')
    for field in FIELDS - {'header', 'decision'}:
        if not isinstance(record[field], list): raise ValueError(field + ' must be a list')
    identifiers = set(); followups = []; obstacles = []
    for f in record['findings']:
        if not isinstance(f, dict): raise ValueError('A finding must be an object')
        for key in ('id', 'mechanism'):
            if not isinstance(f.get(key), str) or not f[key].strip(): raise ValueError('Finding requires ' + key)
        if f['id'] in identifiers: raise ValueError('Duplicate finding ID: ' + f['id'])
        identifiers.add(f['id'])
        if f.get('severity') not in SEVERITY or f.get('status') not in STATUS or f.get('disposition') not in DISPOSITION:
            raise ValueError('Unrecognised finding enum')
        if not isinstance(f.get('basis'), list) or not f['basis'] or any(x not in BASIS for x in f['basis']):
            raise ValueError('Finding requires recognised basis entries')
        if 'NONE' in f['basis'] and len(f['basis']) != 1: raise ValueError('NONE cannot accompany another basis')
        if not isinstance(f.get('sources'), list) or not all(isinstance(x, str) and x.strip() for x in f['sources']):
            raise ValueError('Finding sources must be a list of locators')
        if f['disposition'] == 'REQUIRED_REPAIR' and (f['status'] != 'CONFIRMED' or f['severity'] == 'INFORMATIONAL'):
            raise ValueError('Required repair needs a confirmed adverse consequence')
        if f['status'] == 'WITHDRAWN': continue
        if f['disposition'] == 'FOLLOW_UP': followups.append(f['id'])
        high_accepted = (f['severity'] == 'HIGH' and f['disposition'] == 'ACCEPTED'
                         and isinstance(f.get('user_acceptance'), str) and f['user_acceptance'].strip())
        if f['severity'] == 'CRITICAL' or (f['severity'] == 'HIGH' and not high_accepted) or f['disposition'] in ('REQUIRED_REPAIR', 'INVESTIGATE'):
            obstacles.append(f['id'])
    # Optional supplied lists are assertions, never the source of the derived lists.
    if record['followups'] and sorted(record['followups']) != sorted(followups):
        raise ValueError('followups contradict the derived findings')
    if any(not isinstance(x, str) or x not in identifiers for x in record['path_to_ready']):
        raise ValueError('path_to_ready must name existing finding IDs')
    if record['decision'] == 'READY' and obstacles:
        raise ValueError('READY contradicts unresolved findings: ' + ', '.join(obstacles))
    for field in ('errata', 'rulings', 'probe_triage', 'coverage_matrix'):
        if any(not isinstance(x, dict) for x in record[field]): raise ValueError(field + ' entries must be objects')
    return followups, obstacles


def section(title, value):
    return '\n## ' + title + '\n\n```json\n' + json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n```\n'


def render(record):
    followups, obstacles = validate(record); digest = identity(record)
    preface = '<!-- case-input-sha256: ' + digest + ' -->\n\n'
    case = preface + '# Case ' + record['header']['case_id'] + '\n\nDecision: ' + record['decision'] + '.\n'
    case += section('Case header', record['header'])
    counts = {s: sum(f['severity'] == s for f in record['findings']) for s in SEVERITY}
    case += '\n## Findings reckoning\n\n' + '\n'.join('- ' + s + ': ' + str(n) for s, n in counts.items()) + '\n'
    case += section('Why READY is withheld', obstacles)
    case += section('Findings', record['findings']) + section('Rulings', record['rulings'])
    case += section('Path to READY', record['path_to_ready']) + section('Batched follow-ups', followups)
    case += section('Probe triage', record['probe_triage']) + section('Coverage matrix', record['coverage_matrix'])
    case += section('Notes', record.get('notes', ''))
    case += '\nValid only for the recorded artifacts, environment, and examined scope. Reassess affected claims when these change.\n'
    return {'CASE_FILE.md': case, 'ERRATA.md': preface + '# Errata\n' + section('Recorded corrections', record['errata']),
            'FINDINGS_PROVISIONAL.md': preface + '# Provisional findings\n' + section('Findings', record['findings'])}


def write_case(record, out):
    docs = render(record); digest = identity(record); out = Path(out)
    if out.is_symlink(): raise ValueError('A case output cannot be a symlink')
    if out.exists() and any(p.is_symlink() for p in out.rglob('*')): raise ValueError('A case output contains a symlink')
    manifest_path = out / 'manifest.json'; old = None
    if out.exists() and any(out.iterdir()):
        if not manifest_path.is_file(): raise ValueError('Existing output has no case manifest')
        old = json.loads(manifest_path.read_text())
        for name in FILES:
            expected = old['files'][name]
            if hashlib.sha256((out / name).read_bytes()).hexdigest() != expected:
                raise ValueError('A prepared paper was amended by hand: ' + name)
        for previous in old['versions']:
            if not isinstance(previous, str) or len(previous) != 64 or any(c not in '0123456789abcdef' for c in previous):
                raise ValueError('Invalid former edition identity')
            archive = out / 'versions' / previous
            original = json.loads((archive / 'case.json').read_text())
            if identity(original) != previous: raise ValueError('A former input lost its identity')
            expected_docs = render(original)
            for name in FILES:
                if (archive / name).read_text() != expected_docs[name]:
                    raise ValueError('A former edition was amended by hand')
        if old['current'] == digest:
            if any((out / name).read_text() != docs[name] for name in FILES): raise ValueError('Unchanged input disagrees with its papers')
            return digest
    out.mkdir(parents=True, exist_ok=True)
    version = out / 'versions' / digest
    if version.exists(): raise ValueError('This former edition already exists; it must not be overwritten')
    version.mkdir(parents=True)
    for name, text in docs.items(): (version / name).write_text(text, encoding='utf-8')
    (version / 'case.json').write_bytes(canonical(record) + b'\n')
    manifest = dict(current=digest, versions=(old['versions'] if old else []) + [digest],
                    files={name: hashlib.sha256(text.encode()).hexdigest() for name, text in docs.items()})
    # The manifest is the last receipt. An interruption is detectable on the next call.
    with tempfile.TemporaryDirectory(prefix='.case-', dir=out) as tmp:
        stage = Path(tmp)
        for name, text in docs.items(): (stage / name).write_text(text, encoding='utf-8')
        (stage / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
        for name in (*FILES, 'manifest.json'): os.replace(stage / name, out / name)
    return digest


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--record', type=Path, required=True); p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    try:
        if args.record.stat().st_size > 16 * 1024 * 1024: raise ValueError('The case record exceeds sixteen MiB')
        digest = write_case(json.loads(args.record.read_text(encoding='utf-8')), args.out)
    except (OSError, ValueError, TypeError, KeyError) as exc: p.exit(2, 'Case refused: ' + str(exc) + '\n')
    print(digest)


if __name__ == '__main__': main()
