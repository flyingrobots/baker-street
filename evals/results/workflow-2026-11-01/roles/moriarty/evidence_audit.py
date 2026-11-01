"""Record hashes for retained evidence and recheck the supplied source seal."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
role = root / "roles/moriarty"
seal = json.loads((root / "sealed-source.json").read_text())
for name, expected in sorted(seal.items()):
    actual = hashlib.sha256((root / "original" / name).read_bytes()).hexdigest()
    print(json.dumps({"source": name, "sha256": actual, "unchanged": actual == expected}))
total = 0
for path in sorted(role.rglob("*")):
    if path.is_file():
        data = path.read_bytes()
        total += len(data)
        print(json.dumps({"path": str(path.relative_to(root)), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}, sort_keys=True))
print(json.dumps({"role_bytes_before_this_capture_outputs_and_testimony": total}))
