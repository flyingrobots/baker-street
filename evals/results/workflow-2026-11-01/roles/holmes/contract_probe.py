"""Finite contract checks against fully inspected case input; no target writes."""
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'original'


def metadata(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data), 'lines': len(data.splitlines())}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def result(function, args):
    try:
        value = function(*args)
        return ('return', type(value).__name__, value)
    except Exception as error:
        return ('raise', type(error).__name__)


def reserve_oracle(used, count, capacity):
    # CONTRACT.md lines 4-13: valid start, positive count, inclusive upper bound.
    if any(type(value) is not int for value in (used, count, capacity)):
        return ('raise', 'ValueError')
    if used < 0 or capacity < used or count <= 0 or used + count > capacity:
        return ('raise', 'ValueError')
    return ('return', 'int', used + count)


def release_oracle(used, count):
    # CONTRACT.md lines 4-6 and 17-19: a positive release at most the used count.
    if any(type(value) is not int for value in (used, count)):
        return ('raise', 'ValueError')
    if used < 0 or count <= 0 or count > used:
        return ('raise', 'ValueError')
    return ('return', 'int', used - count)


print('timestamp_utc:', datetime.datetime.now(datetime.timezone.utc).isoformat())
print('environment:', json.dumps({'python': sys.version, 'platform': platform.platform(), 'bytecode_disabled': sys.dont_write_bytecode}))
manifest = json.loads((ROOT / 'sealed-source.json').read_text())
before = {name: metadata(SOURCE / name) for name in manifest}
print('source_manifest:', json.dumps(before, sort_keys=True))
print('case_metadata:', json.dumps([metadata(ROOT / path) for path in ['sealed-source.json', 'capture.py', 'packets/holmes.md']], sort_keys=True))
assert all(before[name]['sha256'] == digest for name, digest in manifest.items()), 'Supplied source differs from seal'
capacity = load('capacity', SOURCE / 'capacity.py')
tests = load('case_supplied_tests', SOURCE / 'test_capacity.py')
suite = unittest.defaultTestLoader.loadTestsFromModule(tests)
ran = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
print('supplied_tests:', json.dumps({'run': ran.testsRun, 'failures': len(ran.failures), 'errors': len(ran.errors), 'successful': ran.wasSuccessful()}))

reserve_mismatches = []
release_mismatches = []
reserve_cases = 0
release_cases = 0
for used in range(-2, 9):
    for count in range(-2, 9):
        release_cases += 1
        observed = result(capacity.release, (used, count))
        expected = release_oracle(used, count)
        if observed != expected:
            release_mismatches.append({'args': [used, count], 'expected': expected, 'observed': observed})
        for maximum in range(-2, 9):
            reserve_cases += 1
            observed = result(capacity.reserve, (used, count, maximum))
            expected = reserve_oracle(used, count, maximum)
            if observed != expected:
                reserve_mismatches.append({'args': [used, count, maximum], 'expected': expected, 'observed': observed})
print('integer_matrix:', json.dumps({'range_inclusive': [-2, 8], 'reserve_cases': reserve_cases, 'release_cases': release_cases, 'reserve_mismatch_count': len(reserve_mismatches), 'release_mismatch_count': len(release_mismatches)}))
print('reserve_mismatches:', json.dumps(reserve_mismatches))
print('release_mismatches:', json.dumps(release_mismatches))

class IntSubclass(int):
    pass

non_plain = [True, False, 1.0, 1.5, None, '1', [], {}, (), IntSubclass(1)]
type_cases = 0
type_mismatches = []
for function, valid_args in [(capacity.reserve, [1, 1, 4]), (capacity.release, [2, 1])]:
    for index in range(len(valid_args)):
        for value in non_plain:
            args = valid_args.copy()
            args[index] = value
            observed = result(function, args)
            type_cases += 1
            if observed != ('raise', 'ValueError'):
                type_mismatches.append({'function': function.__name__, 'index': index, 'value_type': type(value).__name__, 'observed': observed})
print('type_cases:', json.dumps({'total': type_cases, 'mismatches': type_mismatches}))
large = 10 ** 100
large_cases = [
    ('reserve', [large, large, 2 * large + 1]),
    ('reserve', [large, large, 2 * large]),
    ('release', [large, large]),
]
for name, args in large_cases:
    observed = result(getattr(capacity, name), args)
    expected = (reserve_oracle if name == 'reserve' else release_oracle)(*args)
    print('large_integer_case:', json.dumps({'function': name, 'args': args, 'expected': expected, 'observed': observed}))
after = {name: metadata(SOURCE / name) for name in manifest}
print('source_unchanged:', before == after)
assert before == after, 'Source changed during probe'
assert ran.wasSuccessful(), 'Supplied tests failed'
# Exit success means the inquiry completed; recorded contract mismatches are evidence,
# not a claim that the target passed its contract.
