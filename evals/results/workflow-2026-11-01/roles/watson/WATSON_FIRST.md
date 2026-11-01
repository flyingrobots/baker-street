# Watson first deposition

Case: BS-WORKFLOW-2026-11-01. Recorded: 2026-11-01T19:50:11Z.
Phase: initial reader testimony only. Audience: Python API callers and maintainers.

The contract is understandable and makes exact-fill reservations valid. The implementation visibly rejects that same boundary. A caller relying on the contract can therefore receive a rejection for a permitted request; the supplied tests do not exercise that boundary.

## Prior exposure and separation

I did not author this fixture and received no expected findings. Before reading it, I had general Python knowledge, inherited workstation instructions and an unrelated workspace memory summary, and the coordinator's role assignment identifying the target and limits. I had not encountered the fixture's source or contract. I read no evaluator material, sibling testimony, main repository files, or other conversations, and used no memory files. This is a simulated assessment by an informed reader, not an observed usability study. Separate context does not imply statistical independence from other reviewers using the same model and host.

## Available material and identities

I read the assigned packet in full, the complete sealed-source manifest, and every supplied original file listed below. Paths resolve from `/private/tmp/baker-street-workflow-l_fdvdix`. The original-file SHA-256 values were calculated by file hashing and match `sealed-source.json`. The Git head `666ee650d87d008dea3e74292f96c52cb1e1d9f7` is supplied by the packet; I did not inspect Git to verify it.

| Evidence ID | Saved path | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| W-E-1 | original/CONTRACT.md | 1179 | e117f946f77499cd1bc254a49e97ea408370c409d67e40eabff10145600fb3b1 |
| W-E-2 | original/capacity.py | 830 | 85209d664496919cd2acbca588aafe68a3277733973f660f53bec0b9868c3ead |
| W-E-3 | original/test_capacity.py | 583 | 82fe2b7db9124c83ddf9867a39d34a2126e369f0484bfa00162207dc56751a50 |
| W-E-4 | sealed-source.json | 263 | 533e13a1aa094b34c925a7c506218541322fdc974d1b205dc7a0550f4875aade |

Citations below use these manifest IDs plus original-file line numbers. The instruction packet was `packets/watson.md` (21,268 bytes), including shared rules, records, Watson role brief, assigned header, and supplied instruction identities. It is authority for this assignment, not behavioral evidence about the target.

## Per-perspective answers

**Python caller — can I tell what to do?** Yes. I supply plain integers, maintain the count myself, use the returned integer as the new count, and expect `ValueError` for invalid parameters or a request beyond capacity. The contract expressly includes exact fills and releases down to zero (W-E-1, lines 3–19). It also tells me that storage and synchronization are my concern, outside this API's scope (W-E-1, lines 23–24).

**Python caller — do I need to change anything?** The supplied material describes an API, not a migration or a previous version, so no caller migration obligation is established. However, the implementation cannot fulfill my stated expectation for a valid exact fill. Reading only the contract or `reserve` docstring would not tell me that such requests are rejected: both describe rejection beyond capacity, whereas the branch includes equality (W-E-1, lines 10–13; W-E-2, lines 4–11). I cannot infer whether any existing caller encounters this boundary in practice.

**Maintainer — can I tell what to do?** I can identify the accepted inputs, outputs, exception class, and explicit scope without guessing intent. I can also identify a specific mismatch between the authoritative contract and the current source. The tests provide examples for below-capacity and over-capacity reservations, partial and complete release, and over-release, but offer no exact-fill reservation example (W-E-3, lines 5–18). Their existence does not establish that the whole contract was checked.

**Maintainer — do I need to change anything?** The source comparison establishes an inconsistency requiring attention under the acceptance contract; this first deposition does not select a repair. There is no supplied release history, changelog, operator procedure, or compatibility baseline from which to determine when it arose or whether downstream migration is needed.

**Operator perspective.** No distinct deployment, persistent-state, or external-resource operation is promised. The explicit exclusions are clear; I identify no operator instruction gap within them (W-E-1, lines 21–26).

## Cited observations

**W-C-1 — Exact-fill expectation.** Assessment: SUPPORTED. Basis: SOURCE. The authoritative text promises success exactly when `used + count <= capacity` for a valid starting state and positive count, expressly including equality (W-E-1, lines 10–13). There is no consequential ambiguity in that wording.

**W-C-2 — Exact-fill source mismatch.** Assessment: SUPPORTED. Basis: SOURCE and INFERENCE. With the illustrative inputs `reserve(5, 3, 8)`, all types and starting-state/count checks permit progression, but the `used + count >= capacity` branch raises `ValueError("capacity exceeded")` instead of returning 8 (W-E-2, lines 5–11). This is a source-derived walkthrough, not an executed reproduction. The same branch applies to valid exact-fill requests generally. Trigger: a permitted positive reservation exactly uses the remaining capacity. Affected audience/state: a caller maintaining an in-memory count. Consequence: a valid request is rejected and the count cannot advance to full capacity through that call. Actual call frequency, historical origin, and author intent are UNKNOWN. No catastrophic consequence or loss of essential use is established; the contract expressly distinguishes a reproducible violation from such a disqualifier (W-E-1, lines 25–26).

**W-C-3 — Supplied test coverage is narrower than the contract.** Assessment: SUPPORTED. Basis: SOURCE. The two reservation tests use sums 5 and 9 with capacity 8, omitting sum 8 (W-E-3, lines 5–9). No supplied tests check Boolean or other non-integer rejection, nonpositive counts, or invalid starting states. This is a coverage observation, not evidence that those untested behaviors are broken, and not a claim about test results.

**W-C-4 — Other inspected paths are understandable.** Assessment: SUPPORTED within source-reading scope. Basis: SOURCE and INFERENCE. Exact type checks reject Boolean and other non-plain-integer values with `ValueError`; explicit guards reject invalid starting states and counts. `release` guards its stated range and returns `used - count`, including zero on a valid complete release (W-E-2, lines 5–8 and 16–20; W-E-1, lines 4–6 and 17–19). There is no source-visible caller-state mutation in either function. This is a bounded reading of these short functions, not runtime verification or a universal defect-free certification.

## Reading scope and execution limits

Read completely: `packets/watson.md`; `sealed-source.json`; `original/CONTRACT.md` lines 1–26; `original/capacity.py` lines 1–20; `original/test_capacity.py` lines 1–20. Directory enumeration of `original/` returned exactly these three original files.

I ran local file-reading, directory-listing, line-numbering, hashing, byte-counting, and timestamp commands only. I did not import the module, run the supplied tests, run probes, execute project scripts, use network/credentials/shared services, or modify source. No behavioral execution, runtime/dependency inspection, or historical test result is claimed. Probe outcome is N/A because first-deposition probes are prohibited, not because setup failed.

The case's filesystem and network restrictions are instruction-only, not OS-enforced isolation. Actual actions stayed within the supplied original files, manifest, assigned packet, and assigned output directory. Only this testimony was written, well below the 1 MiB output budget. Concurrency, persistence, performance, external resources, prior versions, and deployment compatibility were not investigated. No repairs, probe destinations, or Agency verdict are issued.

This first deposition is frozen on return. Any later correction or recall must use a separate artifact and preserve these bytes.
