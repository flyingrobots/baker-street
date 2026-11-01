"""Hash the supplied files and the exact investigator execution inputs."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
seal = json.loads((root / "sealed-source.json").read_text())
paths = ["original/capacity.py", "original/test_capacity.py", "original/CONTRACT.md", "sealed-source.json", "capture.py", "packets/moriarty.md", "roles/moriarty/baseline.py", "roles/moriarty/contract_probe.py", "roles/moriarty/manifest_probe.py"]
for relative in paths:
    data = (root / relative).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    print(json.dumps({"path": relative, "sha256": digest, "bytes": len(data), "sealed_match": digest == seal[Path(relative).name] if relative.startswith("original/") else "N/A"}, sort_keys=True))
print(json.dumps({"timestamp_utc": datetime.now(timezone.utc).isoformat(), "python": sys.version, "executable": sys.executable}))
