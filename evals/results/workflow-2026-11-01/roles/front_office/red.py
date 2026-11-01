import hashlib, importlib.util, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CANDIDATE='original'
source=ROOT / CANDIDATE / 'capacity.py'
tests=ROOT / 'repair' / 'test_capacity.py'
print(json.dumps({'candidate':CANDIDATE,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'test_sha256':hashlib.sha256(tests.read_bytes()).hexdigest(),'python':sys.version.split()[0]}))
spec=importlib.util.spec_from_file_location('capacity',source)
mod=importlib.util.module_from_spec(spec); sys.modules['capacity']=mod; spec.loader.exec_module(mod)
spec=importlib.util.spec_from_file_location('candidate_tests',tests)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(mod))
assert result.testsRun == 7, 'Expected five existing and two new tests'
print(json.dumps({'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped)}))
raise SystemExit(0 if result.wasSuccessful() else 1)
