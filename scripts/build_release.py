#!/usr/bin/env python3
"""Build a deterministic skill-only ZIP and its SHA-256 checksum."""
import argparse
import hashlib
from pathlib import Path
import re
import zipfile

if __name__ == '__main__' and not __package__:
    from release_payload import read_payload
else:
    from scripts.release_payload import read_payload

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
)


def build(root, destination, version):
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:-[a-zA-Z0-9.-]+)?', version):
        raise ValueError('Version must be a release number such as 3.0.0.')
    root, destination = Path(root).resolve(), Path(destination)
    payload = read_payload(root, SKILL_FILES)
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
