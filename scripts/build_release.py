#!/usr/bin/env python3
"""Build a deterministic skill-only ZIP and its SHA-256 checksum."""
import argparse
import hashlib
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
# Explicit inclusion prevents evaluation answers and future repository files
# from becoming implicit inputs to an investigator's installed skill.
SKILL_FILES = (
    'SKILL.md', 'LICENSE', 'NOTICE',
    'agents/openai.yaml', 'assets/baker-street-mark.svg', 'assets/icon.svg',
    'references/core.md', 'references/records.md', 'references/charter.md',
    'references/stateful-code-review.md',
    'roles/holmes.md', 'roles/watson.md', 'roles/moriarty.md', 'roles/checker.md',
    'scripts/build_packet.py', 'scripts/ledger.py', 'scripts/run_mutant.py', 'scripts/build_case.py',
    'scripts/preference_schema.py', 'scripts/preference_file.py',
    'scripts/__init__.py',
    'scripts/preference_roots.py', 'scripts/preference_header.py', 'scripts/prepare_header.py',
    'docs/repository-preferences.md', 'docs/decisions/0001-repository-preferences.md',
)


def build(root, destination, version):
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:-[a-zA-Z0-9.-]+)?', version):
        raise ValueError('Version must be a release number such as 3.0.0.')
    root, destination = Path(root).resolve(), Path(destination)
    payload = {}
    for name in sorted(SKILL_FILES):
        source = root / name
        if any(p.is_symlink() for p in (source, *source.parents)):
            raise ValueError(f'Symlinks are not release inputs: {name}')
        payload[name] = source.read_bytes()
    manifest = ''.join(
        f'{hashlib.sha256(data).hexdigest()}  {name}\n'
        for name, data in payload.items()
    ).encode()
    payload['SHA256SUMS'] = manifest
    destination.mkdir(parents=True, exist_ok=False)
    archive = destination / f'baker-street-v{version}.zip'
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_STORED) as bundle:
        for name, data in sorted(payload.items()):
            entry = zipfile.ZipInfo(f'baker-street/{name}', date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            bundle.writestr(entry, data)
    (destination / 'SHA256SUMS').write_text(
        f'{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n',
        encoding='utf-8',
    )
    return archive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True)
    parser.add_argument('--out', type=Path, required=True, help='New output directory; never overwritten')
    args = parser.parse_args()
    try:
        archive = build(ROOT, args.out, args.version)
    except (OSError, ValueError) as error:
        parser.exit(2, f'Release not built: {error}\n')
    print(archive)


if __name__ == '__main__':
    main()
