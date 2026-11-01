"""Finite contract oracle, explicit boundary controls, and invalid-type probes."""
import itertools
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "repair"))
from capacity import reserve, release


def observed(function, args):
    try:
        value = function(*args)
        return ("int", value) if type(value) is int else ("wrong_type", repr(value))
    except ValueError:
        return ("ValueError",)
    except Exception as error:
        return ("unexpected_exception", type(error).__name__, str(error))


def reserve_oracle(used, count, capacity):
    # CONTRACT.md lines 4-13: plain ints, valid starting state, positive
    # demand fitting into the remaining capacity; equality must be accepted.
    if not all(type(value) is int for value in (used, count, capacity)):
        return ("ValueError",)
    if used < 0 or capacity < used or count < 1:
        return ("ValueError",)
    return ("int", used + count) if count <= capacity - used else ("ValueError",)


def release_oracle(used, count):
    # CONTRACT.md lines 4-6 and 17-19.
    if not all(type(value) is int for value in (used, count)):
        return ("ValueError",)
    if used < 0 or count < 1 or count > used:
        return ("ValueError",)
    return ("int", used - count)


class IntegerSubclass(int):
    pass


def run_group(name, function, oracle, cases):
    cases = list(cases)
    mismatches = []
    for args in cases:
        expected = oracle(*args)
        actual = observed(function, args)
        if actual != expected:
            mismatches.append({"args": list(map(repr, args)), "expected": expected, "actual": actual})
    print(json.dumps({"group": name, "cases": len(cases), "mismatches": mismatches}, sort_keys=True))
    return len(mismatches)


for args in [(2, 2, 5), (2, 3, 5), (2, 4, 5), (0, 1, 1), (0, 0, 0), (5, 1, 5)]:
    print(json.dumps({"boundary": args, "expected": reserve_oracle(*args), "actual": observed(reserve, args)}))

failures = 0
failures += run_group("reserve_integer_grid", reserve, reserve_oracle, itertools.product(range(-2, 7), repeat=3))
failures += run_group("release_integer_grid", release, release_oracle, itertools.product(range(-2, 7), repeat=2))
bad_types = [True, False, 1.0, "1", None, IntegerSubclass(1), object()]
reserve_types = []
release_types = []
for value in bad_types:
    for position in range(3):
        args = [1, 1, 4]
        args[position] = value
        reserve_types.append(tuple(args))
    for position in range(2):
        args = [2, 1]
        args[position] = value
        release_types.append(tuple(args))
failures += run_group("reserve_type_rejection", reserve, reserve_oracle, reserve_types)
failures += run_group("release_type_rejection", release, release_oracle, release_types)
large = 10 ** 100
failures += run_group("reserve_large_integer", reserve, reserve_oracle, [(large, 1, large + 2), (large, 1, large + 1), (large, 1, large)])
failures += run_group("release_large_integer", release, release_oracle, [(large, 1), (large, large), (large, large + 1)])
print(json.dumps({"total_grid_type_large_cases": 851, "total_mismatches": failures, "seed": "N/A: exhaustive fixed domains"}))
raise SystemExit(1 if failures else 0)
