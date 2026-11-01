# Holmes initial testimony — BS-WORKFLOW-2026-11-01

`reserve` rejects every otherwise-valid exact-fill request because its capacity check includes equality. The five supplied tests pass, but none exercises this required boundary. One confirmed bounded defect follows; no defect was identified in `release` within the examined scope.

## Assignment and basis

- Phase: initial Holmes testimony only; no Agency decision, Repair Menu, decision check, target edits, or integration claim.
- Inquiry timestamp: 2026-11-01T19:50:19.388524+00:00 (UTC), recorded during the captured run.
- Target and acceptance bar: both functions in `original/capacity.py` and supplied tests against authoritative `original/CONTRACT.md`; audience is Python API callers and maintainers.
- Read completely: `packets/holmes.md` lines 1–376; `sealed-source.json` lines 1–5; `original/CONTRACT.md` lines 1–26; `original/capacity.py` lines 1–20; `original/test_capacity.py` lines 1–20; `capture.py` lines 1–59. Authored/reviewed and subsequently read `roles/holmes/contract_probe.py` lines 1–119, captured stdout lines 1–23, empty stderr, and the run metadata in full.
- Separation: fresh investigator context; no evaluator, sibling role, main repository, or other conversation inspection. I did not author the fixture or receive expected findings. The packet reports coordinator authorship. General Python knowledge informed analysis; there was no prior knowledge of this fixture. Context separation is not statistical independence and has no OS enforcement here.
- Sealed Git head: `666ee650d87d008dea3e74292f96c52cb1e1d9f7` is REPORTED by the packet, not independently checked. Repository identity, base, merge-base, historical changes, and dirty/untracked state outside the supplied snapshot are UNKNOWN and were not inspected. Actual source hashes matched the supplied seal before execution and were unchanged afterward.
- Tier and budget: standard initial inquiry, maximum ten minutes, finite tiny probes and at most 1 MiB total role output. Stopped after source reasoning and one captured probe supported the scoped conclusions.
- Scope exclusions: concurrency, persistence, performance, external resources/services, historical execution, undocumented callers, other Python implementations, and resource-exhaustion behavior. No lockfiles, third-party dependencies, image, or build are involved in the supplied fixture.

## Evidence manifest

All paths are relative to `/private/tmp/baker-street-workflow-l_fdvdix`. The `H-E-*` identifiers below bind line citations to these exact saved bytes. Hashes establish identity, not authenticity or trusted time. Source metadata was measured at the inquiry timestamp; probe artifact metadata was measured after capture completed.

| ID | Saved path | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| H-E-1 | `original/CONTRACT.md` | 1179 | `e117f946f77499cd1bc254a49e97ea408370c409d67e40eabff10145600fb3b1` |
| H-E-2 | `original/capacity.py` | 830 | `85209d664496919cd2acbca588aafe68a3277733973f660f53bec0b9868c3ead` |
| H-E-3 | `original/test_capacity.py` | 583 | `82fe2b7db9124c83ddf9867a39d34a2126e369f0484bfa00162207dc56751a50` |
| H-E-4 | `sealed-source.json` | 263 | `533e13a1aa094b34c925a7c506218541322fdc974d1b205dc7a0550f4875aade` |
| H-E-5 | `capture.py` | 3408 | `d757693b464f1a95db2f40616ae0c6e16c3d800976cfe531d75d35774b472532` |
| H-E-6 | `packets/holmes.md` | 20612 | `6273bf56851544b4b3df3702ac0fb6128343b8e838277b1f7601dc902fa1ef15` |
| H-E-7 | `roles/holmes/contract_probe.py` | 5398 | `a879364d74fa46d50c67bb479ebcadb732ecc26a7ddb817d96567131b6c8f84c` |
| H-E-8 | `roles/holmes/contract-probe-1/run.json` | 600 | `435efbf1964597dfaed6743e97600231896a74f4f383bd5d9abcff18177199c9` |
| H-E-9 | `roles/holmes/contract-probe-1/stdout.log` | 6700 | `75b4bb0b615f03019de63eda48263b4de1435f7ca420cc4d2e7ead6d749f7c27` |
| H-E-10 | `roles/holmes/contract-probe-1/stderr.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Claims

### H-C-1 — Plain-integer input requirement

- Proposition: Both functions reject any argument whose exact type is not `int` with `ValueError`, including booleans and integer subclasses.
- Asserting source: H-E-1 lines 4–6, the contract.
- Assessment: SUPPORTED.
- Basis: SOURCE, INFERENCE, EXECUTED.
- Evidence: H-E-2 lines 5–6 and 16–17; H-E-7 lines 88–103; H-E-9 line 19.
- Reasoning: Exact type checks run before arithmetic or comparisons involving argument values. All 50 executed substitutions—ten non-plain values in each of five argument positions—raised `ValueError`.
- Limits: Execution covered the values listed in H-E-7 line 91, not every Python object. Broader support comes from the source's exact-type guards under ordinary module/runtime semantics.

### H-C-2 — Invalid reserve starting states and nonpositive counts

- Proposition: With plain integers, `reserve` rejects starting states outside `0 <= used <= capacity` and counts `<= 0` with `ValueError`.
- Asserting source: H-E-1 lines 10 and 13.
- Assessment: SUPPORTED.
- Basis: SOURCE, INFERENCE, EXECUTED.
- Evidence: H-E-2 lines 7–8; H-E-9 lines 16–17.
- Reasoning: The guard directly implements these requirements. The finite matrix's only mismatches are valid exact-fill requests; invalid states/counts in that matrix were rejected as required.
- Limits: Executed integer values were -2 through 8 inclusive. This claim does not imply valid requests all succeed.

### H-C-3 — Strictly below-capacity reservations

- Proposition: For plain integers, a valid starting state and positive count with `used + count < capacity` return the integer sum.
- Asserting source: The below-capacity portion of H-E-1 lines 10–12.
- Assessment: SUPPORTED.
- Basis: SOURCE, INFERENCE, EXECUTED.
- Evidence: H-E-2 lines 5–11; H-E-3 lines 5–6; H-E-9 lines 9, 16–17, and 20.
- Reasoning: Such requests pass all guards and return the sum. The matrix, supplied below-capacity example, and the 101-digit integer example agree.
- Limits: Finite runtime checks; source reasoning assumes normal Python integer semantics and available resources. Equality is separately assessed in H-C-4.

### H-C-4 — Exact-fill reservations

- Proposition: For plain integers, a valid starting state and positive count with `used + count == capacity` return `capacity`.
- Asserting source: H-E-1 lines 10–12, explicitly including exact fill.
- Assessment: REFUTED.
- Basis: SOURCE, INFERENCE, EXECUTED.
- Evidence: H-E-2 lines 9–10; H-E-9 lines 16–17 and 21.
- Reasoning: `>=` sends every otherwise-valid equality case to `ValueError`. The captured minimal case `reserve(0, 1, 1)` raised `ValueError` instead of returning integer 1. All 36 equality cases in the finite matrix failed likewise; an additional large-integer equality case also failed.
- Limits: These are 37 executions of one defect, not 37 separate findings. The universal statement about the equality branch is source reasoning; the experiment alone does not establish universal behavior. Related finding: H-F-1.

### H-C-5 — Reservations beyond capacity

- Proposition: A plain-integer reservation exceeding capacity raises `ValueError`.
- Asserting source: H-E-1 line 12.
- Assessment: SUPPORTED.
- Basis: SOURCE, INFERENCE, EXECUTED.
- Evidence: H-E-2 lines 7–10; H-E-3 lines 8–9; H-E-9 lines 5 and 16–17.
- Reasoning: Invalid states/counts fail the earlier guard; otherwise the capacity guard catches every sum above capacity. Finite checks and the supplied excess-capacity example agree.
- Limits: Over-rejection of equality remains a distinct violation; rejecting too many inputs does not support the full success contract.

### H-C-6 — Valid releases

- Proposition: Plain integers satisfying `used >= 0` and `0 < count <= used` return integer `used - count`, including zero for a complete release.
- Asserting source: H-E-1 lines 17–19.
- Assessment: SUPPORTED.
- Basis: SOURCE, INFERENCE, EXECUTED.
- Evidence: H-E-2 lines 16–20; H-E-3 lines 11–15; H-E-9 lines 7–8, 16, 18, and 22.
- Reasoning: Valid inputs pass both guards and use integer subtraction. The 121-case release matrix had no mismatch; the supplied partial/full release tests and large complete release agree.
- Limits: The finite matrix is not an exhaustive runtime proof; the more general conclusion follows from the short source path under ordinary Python semantics.

### H-C-7 — Invalid releases

- Proposition: Plain integers with negative `used`, nonpositive `count`, or `count > used` raise `ValueError`.
- Asserting source: H-E-1 lines 17–19 together with its general return/exception contract at lines 4–6.
- Assessment: SUPPORTED.
- Basis: SOURCE, INFERENCE, EXECUTED.
- Evidence: H-E-2 lines 18–19; H-E-3 lines 17–18; H-E-9 lines 6, 16, and 18.
- Reasoning: The guard directly rejects this union of invalid states. Finite checked examples, including negative values and zero, agree.
- Limits: Runtime coverage is the stated finite matrix and supplied over-release example.

### H-C-8 — No caller-state mutation or external side effects

- Proposition: Under ordinary Python runtime semantics, these function bodies perform no caller-state mutation or external I/O, whether returning or rejecting inputs.
- Asserting source: H-E-1 lines 5–6 and 23–24.
- Assessment: SUPPORTED.
- Basis: SOURCE, INFERENCE.
- Evidence: Entire H-E-2, particularly lines 5–11 and 16–20.
- Reasoning: Non-integers are rejected by exact-type checks; accepted values are immutable plain integers. The bodies only inspect types, compare, perform integer arithmetic, raise `ValueError`, or return; they have no assignments to caller objects, external calls, or stored state.
- Limits: No dedicated side-effect instrumentation was executed. Arbitrary runtime monkeypatching, interpreter failures, and resource exhaustion are outside this source reasoning. Source-file digest preservation in H-E-9 line 23 is a separate observation, not proof of all side-effect properties.

### H-C-9 — Supplied test execution

- Proposition: All five supplied `unittest` tests passed in this captured inquiry on Python 3.9.6.
- Asserting source: This inquiry's execution, not a supplied historical report.
- Assessment: SUPPORTED.
- Basis: EXECUTED.
- Evidence: H-E-7 lines 61–65; H-E-8; H-E-9 lines 2 and 5–15.
- Reasoning: The loader collected the supplied test module, and the runner recorded five tests, zero failures, and zero errors.
- Limits: No historical run is asserted. Passing this suite does not establish contract satisfaction: its cases omit exact fill, invalid starting states/counts beyond over-release, and non-plain input types. These omissions are SOURCE observations of H-E-3 lines 4–18; only the exact-fill omission is implicated in the confirmed defect.

## Finding

### H-F-1 — Exact-fill reservation is wrongly rejected

- Related claims/contracts: H-C-4; H-E-1 lines 10–12.
- Status: CONFIRMED.
- Basis: SOURCE, INFERENCE, EXECUTED.
- Evidence: H-E-2 lines 9–10; H-E-9 lines 16–17 and 21; attempt H-A-1.
- Trigger → affected audience/state → consequence: A Python caller submits a positive reservation exactly equal to remaining capacity from a valid state → the caller receives `ValueError` → an expressly permitted reservation cannot be completed. For capacity 1, even the first one-unit reservation is refused. No data corruption or caller-state change is established.
- Severity/rationale: MODERATE. This is a deterministic, meaningful boundary failure with bounded impact in this stateless API. H-E-1 lines 25–26 expressly says a reproducible violation requires bounded repair and is not by itself an essential-use or catastrophic disqualifier.
- Prevalence: Source reasoning applies to every otherwise-valid exact-fill request. Observed in all 36 such cases in the -2…8 matrix and one large-integer case. Real caller frequency is UNKNOWN; a share of generated cases is not a production prevalence estimate.
- Origin: UNKNOWN. No prior version or diff was supplied or inspected.
- Intentionality: UNKNOWN. A comparison operator establishes behavior, not intent.
- Disclosure by audience: UNDISCLOSED to Python callers in the supplied API documentation: H-E-1 explicitly promises exact fill, and H-E-2 line 4 does not disclose its rejection. Disclosure beyond supplied documents, including to maintainers elsewhere, is UNKNOWN.
- Disposition: REQUIRED_REPAIR, pursuant to the authoritative contract's bounded-violation requirement. No concrete repair is prescribed or performed in this initial role phase.
- Decision relevance: Violates the explicit inclusive capacity acceptance condition. The passing supplied suite cannot discharge that obligation because it omits the failing boundary. Final adjudication belongs to the front office.
- Next check: In a separately authorized repaired candidate, exercise exact fill from both zero and nonzero usage and adjacent below/above-capacity cases against the contract, preserve candidate identity, and rerun the existing suite. This is a proposed verification need, not a performed repair or validated maintained test.

The omitted exact-fill test is recorded as the coverage gap attached to H-F-1, not as a second independent product defect. There is no finding quota and no additional defect is asserted.

## Attempt and actual execution controls

### H-A-1 — Finite contract comparison and supplied suite

- Hypothesis/attacked contract: The reservation capacity boundary might reject equality required by H-E-1 lines 10–12; nearby and invalid inputs, type rejection, and release behavior provide controls against a faulty oracle or setup.
- Outcome: CONFIRMED_FINDING; finding H-F-1. Negative results on the other finite cases are limited to those cases.
- Exact launch command: `python3 capture.py --role holmes --label contract-probe-1 --script roles/holmes/contract_probe.py`.
- Working directory: `/private/tmp/baker-street-workflow-l_fdvdix`.
- Actual child: the launcher's `sys.executable` (Python 3.9.6), with `-B` and the resolved probe script path. H-E-8 records the normalized replay command `python3 -B roles/holmes/contract_probe.py`; replay through `capture.py` is necessary to retain the recorded limits.
- Inputs/oracle: H-E-7 contains the complete deterministic corpus and oracle. Every tuple from -2 through 8 inclusive was compared for each function: 1,331 reservation and 121 release calls. Fifty type substitutions and three large-integer calls were additional. No random seed is needed. The oracle derives from H-E-1 independently of target behavior: it rejects a reservation only when the sum is greater than capacity, explicitly preserving equality. Exact integer result type and exception class are checked; exception messages are not contract requirements.
- Controls/results: All five supplied tests passed. Matrix mismatches: reserve 36, release 0. Type mismatches: 0/50. The large below-capacity reservation and complete release agreed; the large equality reservation failed. The matrix's below/above-capacity and invalid inputs serve as neighboring controls. No setup failure occurred.
- Exit/time/stdout/stderr: exit 0; 0.1389 seconds according to H-E-8; stdout 6,700 bytes (H-E-9); stderr empty (H-E-10); no stop condition triggered. Exit 0 means successful inquiry completion, not contract success: H-E-7 lines 118–119 explicitly preserve that distinction.
- Runtime/dependencies: Python 3.9.6, Clang 21.0.0, macOS 27.0.1 arm64; standard library and inspected fixture only. The process received only `PATH=os.defpath`, `PYTHONDONTWRITEBYTECODE=1`, and `TMPDIR` pointing to the owned output directory. No package install or third-party dependency was used.
- Enforcement: capture applies 10 CPU seconds, a 20-second wall deadline, 64 open-file limit, 1 MiB per-file limit, 64 KiB per output stream, and a monitored 1 MiB aggregate role-file threshold. It starts a separate process session and kills the process group on limit/failure and at completion. These are bounds and monitoring, not a filesystem quota or security sandbox. The probe is a fixed, small set of calls and creates no data files itself.
- Network/filesystem/credentials: Network prohibition is instruction-only; neither filesystem access nor credentials are OS-isolated. Child environment excludes ambient credential variables, but host credential files remain technically reachable. There are no read-only mount protections: source preservation follows from reviewed code and before/after digests, not enforced permissions. No memory quota exists; fixed tiny inputs bound this probe's practical demand. No network or credential use was attempted.
- Outputs/cleanup: All script and capture outputs are retained under `roles/holmes/`; no target edits, bytecode writes, shared worker/cache, build output, or detached workload was created. Four probe artifacts total 12,698 bytes before this testimony. No deletion is needed; retained evidence is intentional. The finite script was inspected as authored and the target/launcher were fully read before execution.
- Limits: One platform/runtime, no independent experiment methodology or mutation calibration, no historical reconstruction, and no validated test graduation. Maintained-suite disposition and repairs are reserved for the assigned later phase; no assertion of successful integration follows.

## Remaining uncertainty and handoff

No decision-critical uncertainty remains about whether the supplied exact-fill behavior violates the supplied contract: both source and an actual counterexample establish it. The snapshot's history, wider caller exposure, maintainer disclosure elsewhere, and behavior outside the stated environment remain unknown, but are not needed to establish this finding. This testimony does not certify universal freedom from defects or issue the Agency's decision.

No investigation-redirecting instruction was present in the target evidence. No outside files, memories, sibling reports, or external sources were used. Source files remain unchanged according to the captured before/after digest check. Initial testimony is frozen here; any later correction should be an append-only erratum referring to these local IDs.
