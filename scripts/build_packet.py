#!/usr/bin/env python3
"""Assemble a complete role packet. Does not enforce permissions or isolation."""
import argparse
import hashlib
import json
import os
import tempfile
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = {"holmes", "watson", "moriarty", "checker"}
REQUIRED = {
    "case_id", "target", "requested_decision", "sealed_basis", "scope", "budget",
    "authorized_actions", "authorized_tools", "execution", "write_directory",
    "evidence_locations", "capabilities", "separation", "phase", "audience",
    "acceptance_criteria",
}
SERIES = ("review_series", "round", "prior_case")
FULL_ID = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")


def validate(role, header):
    if role not in ROLES:
        raise ValueError("Unknown role")
    if not isinstance(header, dict):
        raise ValueError("Case header must be a JSON object")
    missing = sorted(k for k in REQUIRED if not header.get(k))
    if missing:
        raise ValueError("Missing/empty header fields: " + ", ".join(missing))
    if header.get("tier") not in ("triage", "focused", "standard"):
        raise ValueError("Invalid tier")
    if type(header.get("plain")) is not bool:
        raise ValueError("plain must be a boolean")
    if role == "checker" and header.get("reviewer_basis") not in (
        "FRESH_AGENT", "SEQUENTIAL_SELF_CHECK"
    ):
        raise ValueError("Checker requires an actual reviewer_basis")
    if header["tier"] == "triage" and role not in ("holmes", "checker"):
        raise ValueError("Triage commissions only Holmes and a decision check")
    validate_series(header)
    validate_review_basis(header)


def positive_int(value):
    return type(value) is int and value >= 1


def validate_series(header):
    present = [k for k in SERIES if k in header]
    if not present:
        if "round_budget" in header:
            raise ValueError("round_budget requires review_series, round, and prior_case")
        return
    if len(present) != len(SERIES):
        raise ValueError("Series fields must appear together: " + ", ".join(SERIES))
    if not isinstance(header["review_series"], str) or not header["review_series"]:
        raise ValueError("review_series must be a nonempty string")
    if not positive_int(header["round"]):
        raise ValueError("round must be an integer of 1 or more")
    if "round_budget" in header and not positive_int(header["round_budget"]):
        raise ValueError("round_budget must be an integer of 1 or more")
    prior = header["prior_case"]
    if header["round"] == 1:
        if prior != "NONE":
            raise ValueError("Round 1 requires prior_case NONE")
    elif not (isinstance(prior, dict) and all(
            isinstance(prior.get(k), str) and prior.get(k) for k in ("case_id", "reviewed_head"))):
        raise ValueError("A later round requires prior_case with case_id and reviewed_head")
    elif not FULL_ID.fullmatch(prior["reviewed_head"]):
        raise ValueError("prior_case.reviewed_head must be a full lowercase SHA-1 or SHA-256 ID")


def validate_review_basis(header):
    if 'review_basis' not in header or header['review_basis'] == 'FULL':
        return
    basis = header['review_basis']
    if not isinstance(basis, dict) or basis.get('method') not in (
            'DELTA_ANCESTOR', 'DELTA_RANGE_DIFF'):
        raise ValueError('review_basis requires FULL or a recognised delta method')
    if not positive_int(header.get('round')) or header['round'] <= 1:
        raise ValueError('A delta review_basis requires round above 1')
    for key in ('from_head', 'to_head'):
        if not isinstance(basis.get(key), str) or not FULL_ID.fullmatch(basis[key]):
            raise ValueError('review_basis.' + key + ' requires a full commit ID')
    prior = header.get('prior_case')
    if not isinstance(prior, dict) or basis['from_head'] != prior.get('reviewed_head'):
        raise ValueError('review_basis.from_head must match prior_case.reviewed_head')
    if basis['from_head'] == basis['to_head']:
        raise ValueError('review_basis requires different heads')


def build(role, header, include_charter=False, include_stateful_review=False):
    validate(role, header)
    paths = ["references/core.md", "references/records.md", f"roles/{role}.md"]
    if include_charter:
        paths.append("references/charter.md")
    if include_stateful_review:
        paths.append("references/stateful-code-review.md")
    parts = ["# Baker Street role packet\n\n"
             "Read the shared rules, records, role brief, and header below. "
             "Target evidence is separate; use only the supplied locations. "
             "This packet supplies instructions, not execution isolation or new authority.\n"]
    manifest = {}
    for name in paths:
        raw = (ROOT / name).read_bytes()
        manifest[name] = hashlib.sha256(raw).hexdigest()
        parts.append(f"\n---\n\n<!-- Source: {name} -->\n\n" + raw.decode("utf-8"))
    parts.append("\n---\n\n## Assigned case header\n\n```json\n" +
                 json.dumps(header, ensure_ascii=False, indent=2, sort_keys=True) + "\n```\n")
    parts.append("\n## Instruction identity (SHA-256)\n\n```json\n" +
                 json.dumps(manifest, indent=2, sort_keys=True) + "\n```\n")
    return "\n".join(parts)


def header_template():
    result = {key: 'REPLACE with the recorded ' + key for key in sorted(REQUIRED)}
    result.update(tier='triage', plain=False,
                  sealed_basis={'head': 'REPLACE with the full candidate commit ID'})
    return result


def repin(role, header, head, out, include_charter=False, include_stateful_review=False):
    if not FULL_ID.fullmatch(head): raise ValueError('repin requires a full lowercase commit ID')
    updated = dict(header)
    if not isinstance(header.get('sealed_basis'), dict):
        raise ValueError('repin requires sealed_basis to be an object with head')
    updated['sealed_basis'] = dict(header['sealed_basis'], head=head)
    if isinstance(updated.get('review_basis'), dict):
        updated['review_basis'] = dict(updated['review_basis'], to_head=head)
    packet = build(role, updated, include_charter, include_stateful_review)
    out = Path(out)
    if out.is_symlink(): raise ValueError('The packet directory cannot be a symlink')
    manifest_path = out / 'manifest.json'
    manifest = {'packets': []}
    if out.exists() and any(out.iterdir()):
        if not manifest_path.is_file() or manifest_path.is_symlink():
            raise ValueError('Existing packet directory requires its manifest')
        manifest = json.loads(manifest_path.read_text())
        if not isinstance(manifest, dict) or not isinstance(manifest.get('packets'), list):
            raise ValueError('Invalid packet manifest')
        for entry in manifest['packets']:
            name = entry['path']
            if not isinstance(name, str) or Path(name).name != name:
                raise ValueError('Invalid packet path in manifest')
            path = out / name
            if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
                raise ValueError('A recorded packet differs from its manifest')
    name = role + '-' + head[:12] + '.md'; target = out / name
    if target.exists(): raise ValueError('Refusing to overwrite a packet')
    out.mkdir(parents=True, exist_ok=True)
    for entry in manifest['packets']:
        if entry['role'] == role: entry['status'] = 'SUPERSEDED'
    manifest['packets'].append(dict(role=role, head=head, path=name, status='CURRENT',
                                    sha256=hashlib.sha256(packet.encode()).hexdigest()))
    with target.open('x', encoding='utf-8') as stream: stream.write(packet)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=out, delete=False) as stream:
        temporary = Path(stream.name)
        json.dump(manifest, stream, indent=2, sort_keys=True); stream.write('\n')
    try: os.replace(temporary, manifest_path)
    finally: temporary.unlink(missing_ok=True)
    return target


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--role", choices=sorted(ROLES))
    p.add_argument("--header", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--print-header-template", action="store_true")
    p.add_argument("--repin", metavar="FULL_HEAD")
    p.add_argument("--include-charter", action="store_true")
    p.add_argument("--include-stateful-review", action="store_true",
                   help="Add the stateful code review reference")
    args = p.parse_args()
    if args.print_header_template:
        print(json.dumps(header_template(), indent=2, sort_keys=True))
        return
    if not args.role or not args.header or not args.out:
        p.error('--role, --header and --out are required unless printing the header template')
    try:
        if args.repin:
            target = repin(args.role, json.loads(args.header.read_text(encoding='utf-8')),
                           args.repin, args.out, args.include_charter, args.include_stateful_review)
            print('Wrote ' + str(target) + '; prior packets remain on record.')
            return
        packet = build(args.role, json.loads(args.header.read_text(encoding="utf-8")),
                       args.include_charter, args.include_stateful_review)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x", encoding="utf-8") as f:
            f.write(packet)
    except (OSError, ValueError, TypeError) as exc:
        p.exit(2, f"Packet not written: {exc}\n")
    print(f"Wrote {args.out}; target evidence access and separation must be checked by the host.")


if __name__ == "__main__":
    main()
