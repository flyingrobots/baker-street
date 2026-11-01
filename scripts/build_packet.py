#!/usr/bin/env python3
"""Assemble a complete role packet. Does not enforce permissions or isolation."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = {"holmes", "watson", "moriarty", "checker"}
REQUIRED = {
    "case_id", "target", "requested_decision", "sealed_basis", "scope", "budget",
    "authorized_actions", "authorized_tools", "execution", "write_directory",
    "evidence_locations", "capabilities", "separation", "phase", "audience",
    "acceptance_criteria",
}


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


def build(role, header, include_charter=False):
    validate(role, header)
    paths = ["references/core.md", "references/records.md", f"roles/{role}.md"]
    if include_charter:
        paths.append("references/charter.md")
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


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--role", choices=sorted(ROLES), required=True)
    p.add_argument("--header", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--include-charter", action="store_true")
    args = p.parse_args()
    try:
        packet = build(args.role, json.loads(args.header.read_text(encoding="utf-8")),
                       args.include_charter)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x", encoding="utf-8") as f:
            f.write(packet)
    except (OSError, ValueError, TypeError) as exc:
        p.exit(2, f"Packet not written: {exc}\n")
    print(f"Wrote {args.out}; target evidence access and separation must be checked by the host.")


if __name__ == "__main__":
    main()
