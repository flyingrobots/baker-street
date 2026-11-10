"""Keep installation workflow expressions within their supported GitHub contexts."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class InstallWorkflowTests(unittest.TestCase):
    """Examine the actual workflow's conventional job-level environment mappings."""

    def test_job_environment_does_not_use_the_step_only_runner_context(self) -> None:
        """GitHub rejects runner expressions before jobs exist at this scope."""
        source = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        inside = False
        for line in source.splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            indentation = len(line) - len(line.lstrip())
            if indentation <= 4:
                inside = line == "    env:"
            if inside:
                with self.subTest(line=line):
                    self.assertNotRegex(line, r"\$\{\{\s*runner\.")
