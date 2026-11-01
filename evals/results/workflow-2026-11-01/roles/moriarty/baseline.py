"""Run only the inspected, supplied five-test unittest module."""
from pathlib import Path
import sys
import unittest

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "original"))
import test_capacity

suite = unittest.defaultTestLoader.loadTestsFromModule(test_capacity)
result = unittest.TextTestRunner(verbosity=2).run(suite)
print(f"supplied_tests_run={result.testsRun} successful={result.wasSuccessful()}")
raise SystemExit(0 if result.wasSuccessful() else 1)
