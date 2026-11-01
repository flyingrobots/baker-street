# Moriarty initial testimony

Case: BS-WORKFLOW-2026-11-01. Phase: initial testimony only. Audience: Python API callers and maintainers. Observation timestamp: 2026-11-01T19:50:43.238556+00:00 (recorded by the source-manifest probe). Target: the three supplied files under `original/`; `CONTRACT.md` is the acceptance authority. Tier: standard; budget: one inquiry of at most 10 minutes and 1 MiB role output. All paths below resolve from `/private/tmp/baker-street-workflow-l_fdvdix`.

One contract violation is established: valid exact-fill reservations are rejected. The supplied five tests pass, while a finite independent contract probe exposes that boundary failure. No additional violation was found in the examined release and invalid-type cases; these finite results do not establish universal correctness.

## Basis, separation, and controls

I read `packets/moriarty.md`, `capture.py`, `sealed-source.json`, and all of `original/CONTRACT.md`, `original/capacity.py`, and `original/test_capacity.py`. I wrote and read only my assigned `roles/moriarty/` evidence in addition to those authorized inputs. I did not inspect the evaluator, sibling roles, main repository, other conversations, or hidden expectations. The packet reports that the coordinator authored the fixture; I did not author it. This role received a separate context, but shared models and host can correlate errors; there is no claim of statistical independence or OS-enforced blindness.

The supplied header reports Git head `666ee650d87d008dea3e74292f96c52cb1e1d9f7`. I did not inspect a repository to verify its relationship to these files. Repository identity, base/merge-base, and dirty/untracked repository state are UNKNOWN because repository access was excluded. Reviewed evidence identity is instead established by the supplied SHA-256 seal, checked after the behavior probes and again in the evidence audit. All three source hashes matched. No source was edited, and there were no commits, publication, delegation, network requests, external services, Docker, or shared workers/caches.

I inspected the fixture and runner before execution. The fixture is small pure Python with no imports, filesystem access, network access, state storage, or subprocess calls. The supplied test module imports `unittest` and the fixture; its five methods were inspected. Investigator probes use only the standard library and fixed, finite collections. Their writes are the runner's captured outputs in the assigned role directory; bytecode writing is disabled.

Actual execution was host Python 3.9.6, executable `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`; the reported compiler is Clang 21.0.0. No third-party dependencies, package installation, lockfiles, or image IDs apply. The wrapper passes only `PATH=os.defpath`, `PYTHONDONTWRITEBYTECODE=1`, and per-run `TMPDIR` in the child's environment. This avoids inheriting credential environment variables, but filesystem credentials remain readable: there is no credential filesystem isolation, mount restriction, network sandbox, or memory quota. Network prohibition is instruction-only. Trusted reviewed code and small finite inputs bound the actual experiment; scratch space is not represented as a sandbox.

`capture.py` supplies a 20-second wall deadline, 10-second CPU limit, 1 MiB per-file size limit, 64-file-descriptor limit, 64 KiB per stdout/stderr stream, and polling of aggregate role file bytes against 1 MiB. It kills the probe process group on limits/failure and after leader completion. These controls are scoped monitoring, not a filesystem quota; no outputs were written outside this directory by the reviewed probes. Each capture completed in less than 0.08 seconds with `stopped: null`. No subprocesses are launched by the probe scripts themselves. All scripts and logs are retained; there is no disposable external runtime data to clean up.

## Evidence manifest

The table identifies saved source bytes. Citations to E-1/E-2/E-3 below include line ranges, interpreted against these exact hashes. The seal is an identity assertion, not proof of provenance or a trusted timestamp.

| ID | Saved path | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| M-E-1 | `original/capacity.py` | 830 | `85209d664496919cd2acbca588aafe68a3277733973f660f53bec0b9868c3ead` |
| M-E-2 | `original/CONTRACT.md` | 1179 | `e117f946f77499cd1bc254a49e97ea408370c409d67e40eabff10145600fb3b1` |
| M-E-3 | `original/test_capacity.py` | 583 | `82fe2b7db9124c83ddf9867a39d34a2126e369f0484bfa00162207dc56751a50` |
| M-E-4 | `sealed-source.json` | 263 | `533e13a1aa094b34c925a7c506218541322fdc974d1b205dc7a0550f4875aade` |
| M-E-5 | `capture.py` | 3408 | `d757693b464f1a95db2f40616ae0c6e16c3d800976cfe531d75d35774b472532` |
| M-E-6 | `packets/moriarty.md` | 21193 | `cac87977411b3da88dba06fc4d785e04b7747cf3180a37970e11d3c5c4b652b9` |

Execution evidence is retained without rewriting. The two behavioral scripts are `roles/moriarty/baseline.py` (SHA-256 `f5705fa27d5705cabed6f1fc98384e09465f5fca64ca4d451a08c46c49f17f9b`) and `roles/moriarty/contract_probe.py` (SHA-256 `c0de203c1c9cb6181e4597197774e7a0212a8a5136a4fe2e8adefd3fa2bf399e`). Input domains and oracle are fully contained in the latter; no random seed or external corpus applies.

| ID | Saved artifact | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| M-E-7 | `roles/moriarty/supplied-tests/stdout.log` | 37 | `7155ebe4ddd90de96ede15a7e733f25d67cc3247729c58549b75f1ff9c456d5d` |
| M-E-8 | `roles/moriarty/supplied-tests/stderr.log` | 397 | `103a732cbea3b898ebc26c6d72d42d16346544011b51a8a702056d46b19db85e` |
| M-E-9 | `roles/moriarty/supplied-tests/run.json` | 596 | `1824c31c2ec0fe7edec1f33bf3cf4d866ccacb68b4c383de6a87640e2bdfd0ac` |
| M-E-10 | `roles/moriarty/contract-grid/stdout.log` | 2939 | `51d8d6cc0e91761e462349ae6ead18bda38e40012160214f358494a227007284` |
| M-E-11 | `roles/moriarty/contract-grid/stderr.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| M-E-12 | `roles/moriarty/contract-grid/run.json` | 602 | `2d911dc9d254ab69945ed3f853b7ea32b6817a5a2668be4dbabf361dba8f4659` |
| M-E-13 | `roles/moriarty/source-manifest/stdout.log` | 1574 | `5950db7dbf28b947a2d1a7195cf5becd2914f2a30b8b7dd0e96a13146071fab6` |

`roles/moriarty/evidence-audit/stdout.log` records these artifact sizes/hashes, repeat source-seal checks, and 12,311 bytes of role files before that audit's captured outputs and this testimony were added. Its script is `roles/moriarty/evidence_audit.py`, SHA-256 `e0f672180de7572a637c692d6af648612d40d7cc5b35073cebe26395d8fcc49a`; its `run.json` retains its execution receipt. The original source-manifest script and receipt are also retained.

## Claims examined

| ID | Scoped proposition and asserting source | Assessment | Basis and evidence | Limits |
| --- | --- | --- | --- | --- |
| M-C-1 | Valid exact fills must return `used + count`; M-E-2 lines 10-13. | REFUTED as an implementation conformance claim | SOURCE, EXECUTED: M-E-1 lines 9-10 reject equality; M-E-10 reproduces it. | Counterexamples and a source-level boundary argument, not a claim about historical releases. |
| M-C-2 | The supplied five tests pass on the supplied source in this case. | SUPPORTED | EXECUTED: M-E-7 through M-E-9. | Five specific tests only; no exact-fill reserve test exists in M-E-3 lines 4-18. |
| M-C-3 | Release agrees with the stated oracle on 81 integer pairs, 14 invalid-type cases, and three large-integer cases. | SUPPORTED | EXECUTED: M-E-10; oracle from M-E-2 lines 4-6 and 17-19. | No universal behavioral certification or deployment claim. |
| M-C-4 | Reserve rejects the 21 tested non-plain-integer inputs with ValueError. | SUPPORTED | EXECUTED: M-E-10; exact-type guards also visible in M-E-1 lines 5-6. | Representative invalid types, not every possible Python object. |
| M-C-5 | Supplied source bytes still matched the supplied seal after behavioral execution. | SUPPORTED | EXECUTED: M-E-13 and evidence-audit output. | Verifies byte identity at observations, not Git ancestry or authenticity. |

## Attempts

### M-A-1 — Reservation equality boundary

- Hypothesis and attacked contract: a valid request using all remaining capacity is incorrectly rejected, contrary to M-E-2 lines 10-12.
- Method/setup: execute `contract_probe.py` through the inspected capture runner against `original/capacity.py`, loaded by placing only `original/` ahead of the normal import path.
- Inputs and controls: explicit `(2,2,5)`, `(2,3,5)`, `(2,4,5)` distinguish below, exact, and above capacity. Additional explicit inputs are `(0,1,1)`, `(0,0,0)`, `(5,1,5)`. Enumerate all 729 triples in `[-2,6]^3`; separately test `(N,1,N+2)`, `(N,1,N+1)`, `(N,1,N)` for `N=10**100`.
- Oracle: independently transcribe the contract into plain-integer validation, a valid initial state, positive count, and `count <= capacity - used`. Equality is explicitly required by the contract, not inferred from the implementation. Below/above controls and exact-fill examples were checked by direct arithmetic.
- Outcome: CONFIRMED_FINDING, M-F-1. `(2,3,5)` and `(0,1,1)` raise ValueError instead of returning 5 and 1. The exhaustive grid has 21 mismatches, all valid exact fills; the large-integer cases add one exact-fill mismatch. The controls match their oracle.
- Artifacts: M-E-10 through M-E-12, script hash above. Exit 1 is deliberate after reporting observed mismatches; it is diagnostic failure, not failed setup. stderr is empty and the capture did not stop the probe.
- Limits: 22 mismatches in the 851 grid/type/large aggregate; the six separately printed boundary calls overlap the grid and are not six independent discoveries. Source reasoning establishes the affected equality class; runtime frequency is UNKNOWN. No mutation or repair was run.

### M-A-2 — Release range and terminal zero

- Hypothesis and attacked contract: release accepts invalid counts, rejects valid full releases, or returns the wrong difference, violating M-E-2 lines 17-19.
- Method/setup/inputs: same preserved contract probe, all 81 integer pairs in `[-2,6]^2`; three additional pairs `(N,1)`, `(N,N)`, `(N,N+1)` with `N=10**100`.
- Oracle/control: require nonnegative used and `1 <= count <= used`, otherwise ValueError; valid output is `used - count`. The domain includes zero starting state, negative values, zero count, full release, over-release, and ordinary partial release.
- Outcome: NOT_REPRODUCED. All 84 range/arithmetic cases agree with the oracle, including returning zero after full release. Finding IDs: N/A, no violation identified by this method.
- Artifacts: M-E-10 through M-E-12 and `contract_probe.py`.
- Limits: finite input domain and three large-number cases; no persistence/concurrency/performance claims. Shared execution with other attempt groups is not independent corroboration.

### M-A-3 — Plain-integer boundary

- Hypothesis and attacked contract: bools or other non-plain integers pass validation, violating M-E-2 lines 4-6.
- Method/setup/inputs: substitute `True`, `False`, `1.0`, `"1"`, `None`, an `int` subclass instance, and `object()` into each position of valid reserve `(1,1,4)` and release `(2,1)` calls. Seven types times three/two positions gives 21 reserve plus 14 release cases.
- Oracle/control: every substituted call must raise ValueError regardless of apparent numerical equality. The unchanged controls are valid arithmetic states, so an invalid starting state cannot mask the input-type issue.
- Outcome: NOT_REPRODUCED; all 35 calls raise ValueError as required. Finding IDs: N/A.
- Artifacts: M-E-10 through M-E-12 and `contract_probe.py`.
- Limits: representative types only. No custom hostile metaclass or side-effect hooks were executed; source uses exact `type(...) is int` tests before arithmetic.

### M-A-4 — Existing-suite detection

- Hypothesis and attacked contract: the supplied test suite exposes the exact-fill defect already identified in source.
- Method/setup/inputs/oracle: load the inspected `test_capacity.py` with the standard-library unittest loader and run all discovered tests; success is the suite's own assertions, not a separate statement of full contractual coverage.
- Outcome: NOT_REPRODUCED as a suite detection attempt: five tests ran and passed. This is compatible with M-F-1 because the reserve tests check `(2,3,8)` and `(6,3,8)`, neither an exact fill (M-E-3 lines 5-9).
- Artifacts: `baseline.py`, M-E-7 through M-E-9. Exit 0; 0.0759 seconds; no setup failure.
- Limits: passing this suite does not refute the broader contract finding. Missing boundary coverage is evidence about detection, not a separately asserted product defect.

Exact replay commands, all from the case root:

```sh
python3 capture.py --role moriarty --label supplied-tests --script roles/moriarty/baseline.py
python3 capture.py --role moriarty --label contract-grid --script roles/moriarty/contract_probe.py
python3 capture.py --role moriarty --label source-manifest --script roles/moriarty/manifest_probe.py
python3 capture.py --role moriarty --label evidence-audit --script roles/moriarty/evidence_audit.py
```

Capture labels create directories exclusively; replay must use fresh labels while retaining these original outputs. Supplied-tests exited 0 in 0.0759 seconds; contract-grid exited 1 in 0.0539 seconds; source-manifest exited 0 in 0.0628 seconds; evidence-audit exited 0 in 0.0563 seconds. These are bounded execution observations, not benchmarks.

## Finding M-F-1

- Related claim/contract: M-C-1; M-E-2 lines 10-13, especially explicit exact-fill acceptance.
- Status: CONFIRMED. Basis: SOURCE and EXECUTED.
- Evidence: M-E-1 lines 9-10 uses `used + count >= capacity` as the rejection condition. M-E-10 independently observes rejection at exact fill and acceptance below it. Its oracle is grounded in the separate contract.
- Impact: valid starting state plus positive count with `used + count == capacity` → Python callers attempting to allocate all remaining capacity → ValueError instead of the promised new count. If a caller continues with smaller reservations, the implementation can leave capacity unused; callers expecting a successful exact fill instead face an exception. For capacity 1, the only positive valid reservation from zero is rejected. None of these observations establishes data corruption or an essential-use disqualifier under the supplied contract.
- Severity: MODERATE, a meaningful bounded impairment of the reservation API. The contract explicitly states at lines 25-26 that a reproducible violation requires bounded repair and is not by itself catastrophic or an essential-use disqualifier.
- Prevalence: the source deterministically rejects the entire valid exact-fill class. Observed: 21 such integer-grid inputs, one large-integer input, plus overlapping explicit demonstrations. Real-world request frequency is UNKNOWN.
- Origin: UNKNOWN; no permitted history evidence. Intentionality: UNKNOWN; no stated intent to reject equality. Disclosure: UNKNOWN for existing callers/maintainers; no supplied disclosure describes this limitation, and the authoritative contract states the opposite.
- Disposition: REQUIRED_REPAIR, because the acceptance contract requires a bounded repair for a reproducible violation. This is a finding disposition, not a Repair Menu or implementation prescription.
- Decision relevance: violates the explicit acceptance obligation for exact fills. No Agency verdict is issued here.
- Next check: once a candidate exists, verify exact-fill acceptance together with retained rejection of over-capacity and invalid inputs against the same authoritative contract. No candidate or change has been reviewed in this testimony.

## Coverage and remaining limits

Both functions and all supplied tests were read in full. Runtime coverage comprises five supplied tests and 857 direct contract-probe calls: six printed boundary demonstrations plus 851 grid/type/large cases. Those 851 are 729 reserve grid, 81 release grid, 21 reserve type, 14 release type, three reserve large-integer, and three release large-integer calls. The two explicitly printed exact-fill failures are duplicates of grid cases; there is only one product finding.

No observed setup failure or faulty-probe correction needs an erratum. The oracle, its boundary arithmetic, case totals, and output were inspected before returning this testimony. No instructions in the supplied target evidence attempted to redirect the inquiry.

Side-effect freedom was assessed by SOURCE inspection: exact-type checks precede plain-integer comparisons/arithmetic, and there are no writes, external calls, or stored state. It was not independently instrumented at runtime. Arbitrarily huge allocations, asynchronous interpreter failures, hostile runtime monkey-patching, additional Python versions, broad object fuzzing, and performance campaigns were not attempted. Concurrency, persistence, external resources, and thread safety are explicitly excluded by M-E-2 lines 21-24 and were not investigated. These omissions do not erase the established narrow counterexample, and the negative attempts certify nothing beyond their stated methods.

This is the complete initial role testimony. No repair implementation, probe-graduation decision, Agency decision, or self-appointed decision check is included.
