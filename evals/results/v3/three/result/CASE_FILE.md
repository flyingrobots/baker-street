# v3-three — Moriarty source review

The upper boundary does not follow the supplied contract: `validate(10)` takes the rejection branch although 10 is explicitly accepted. This is a source-established boundary defect; no target code was executed. The recommended decision is **CHANGES_REQUIRED**, with the comparison corrected and the boundary checked before acceptance.

## Header and actual basis

- Case: v3-three; phase: initial; tier: focused; audience: maintainer; plain voice.
- Review date: 2026-11-01 UTC; exact clock time UNKNOWN.
- Target: `/workspace/scratch/dbe9dc8cb21c/smoke-v3/three/input`.
- Requested decision: whether the upper boundary follows the supplied contract.
- Acceptance obligation: the accepted integer domain includes 10. No additional non-negotiable intended-use bar is supplied.
- Budget: one bounded source review, completed after inspecting both supplied files.
- Authorized actions: read supplied evidence and write this response in the assigned result directory. Target edits, target execution, delegation, publication, and external lookup were not authorized and were not performed.
- Evidence inspected: complete `packet.md`, complete `input/contract.md`, and complete `input/validator.py`. File enumeration found those two evidence files. No sibling directories or external sources were inspected.
- Separation: fresh assigned-role context, shared filesystem, prompt-only evidence boundary; no claimed filesystem sandbox. Prior exposure to sibling conclusions: NONE. Authorship of reviewed target: NONE known. Decision-check basis: SEQUENTIAL_SELF_CHECK.
- Actual execution: local file listing, display, hashing, and byte counting only; no imports, tests, project scripts, or other target execution. Network was unused. Filesystem isolation and credential protections were not independently verified; CPU/memory limits UNKNOWN. Read commands completed with exit 0; each display was bounded to at most 8,000 output tokens. No execution artifacts or target cleanup were needed.
- Repository identity, base/head/merge-base, dirty/untracked state, runtime/dependencies, and lockfiles: UNKNOWN; none were supplied or needed to establish this narrow source defect.
- Assigned output: `/workspace/scratch/dbe9dc8cb21c/smoke-v3/three/result/CASE_FILE.md`.

## Evidence manifest

The observed SHA-256 values match the sealed basis in the packet. These are supplied local files, not independently authenticated historical records. Paths below are relative to this result directory; the files remain at their supplied locations.

| ID | Supplied evidence / case-relative path | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| M-E-1 | `../input/contract.md` | 141 | `dcf5e4cca9ded61d0d9e5f6b3b916a854462be4a67e8844309e97ded68a8c9c9` |
| M-E-2 | `../input/validator.py` | 84 | `c131b45850b917168da501207776cbcdb9379aaa9c80fe9421741c62e04c6ab5` |

## Claim and attack

**M-C-1 — The validator's upper boundary conforms to the supplied inclusive maximum of 10.** Assessment: REFUTED. Basis: SOURCE and INFERENCE. Asserting source: the requested acceptance proposition, not a separate claim by the implementation author. Evidence: M-E-1 line 1; M-E-2 lines 1–4. The contract includes 10, but the guard `x >= 10` is true for integer 10 and leads directly to `ValueError("too large")`. This establishes the contradiction by inspection; it is not a report of an observed runtime exception.

**M-A-1 — Inclusive boundary is incorrectly rejected.** Attacked contract: acceptance of integer 10. Method: inspect the contract independently of the implementation, then trace the supplied four-line function for 10. Oracle: M-E-1 explicitly includes 10. Source controls: for integer 9 the guard is false and reaches `return x`; for integer 11 it is true and reaches the same rejection branch. These are source deductions, not executed cases. Outcome: CONFIRMED_FINDING, linked to M-F-1. Artifacts: M-E-1 and M-E-2. Limits: no runtime, integration, historical-execution, non-integer, or broader compatibility claim.

## Finding and bounded repairs

**M-F-1 — The inclusive endpoint is excluded.**

- Related claim/contract: M-C-1; M-E-1 line 1.
- Status: CONFIRMED. Basis: SOURCE and INFERENCE. Evidence: M-E-2 lines 2–3, compared with M-E-1 line 1.
- Impact: integer input 10 → caller supplying an explicitly accepted endpoint → validation raises instead of returning the input.
- Severity: MODERATE; a bounded, meaningful contract failure at the stated acceptance boundary. No evidence establishes loss of essential use or another disqualifying consequence.
- Prevalence: the inspected function rejects the boundary value whenever this path is used with integer 10; real-world call frequency UNKNOWN.
- Origin: UNKNOWN; no revision history supplied. Intentionality: UNKNOWN. Disclosure: UNKNOWN for the maintainer; no disclosure record supplied.
- Disposition: REQUIRED_REPAIR. Decision relevance: directly defeats the sole requested acceptance obligation. Next check: inspect the corrected comparison and verify acceptance of 10 with rejection immediately above the limit.

| Repair | Type / scope / audience | Concrete action and acceptance check | Effort / dependencies / validation |
| --- | --- | --- | --- |
| M-R-1 | CODE / THIS_CHANGE / maintainer | Change `if x >= 10:` to `if x > 10:`. Check that integer 10 reaches `return x` and integer 11 reaches the rejection branch. Required for M-F-1. | One-line edit assuming the supplied function is the relevant implementation; integration effort UNKNOWN. No dependency beyond supplied contract. PROPOSED; not edited or executed. |
| M-R-2 | TEST / THIS_CHANGE / maintainer | Add boundary regression checks for returned value 10 and rejection of 11; optionally retain 9 as a neighboring accepted control. Establish that the check for 10 fails against the original comparison and passes after M-R-1. Supports M-F-1 acceptance checking. | Small test once a harness is available; harness UNKNOWN. Depends on execution authorization and environment. PROPOSED, not a validated maintained test or an additional established product defect. |

## Probe disposition

**M-P-1:** Origin: source inquiry M-A-1 and evidence M-E-1/M-E-2. Intended contract: inclusive maximum 10. Disposition: ARCHIVE this source reasoning as investigative evidence. PROMOTE is inapplicable because there is no maintained executable probe; MINIMIZE_THEN_PROMOTE is unnecessary for this already minimal input; RETAIN_IN_SPECIALIZED_SUITE is unwarranted for this ordinary boundary check. A future ordinary regression test is proposed in M-R-2, with an oracle derived from the contract. Suite/budget: a small unit test, subject to the project's unsupplied harness. Validation: source inquiry completed; executable test, state controls, dependency identities, and demonstration against the original comparison remain unperformed. No faulty probe was produced.

## Decision check and current decision

Sequential self-check, not an independent witness: M-C-1, M-A-1, and M-F-1 HOLDS by the explicit inclusion of 10 and the `>= 10` guard. M-R-1 HOLDS as a proposed correction under ordinary integer comparison; it makes no claim of implementation or integration. M-R-2 and M-P-1 HOLDS as proposed future testing and archival disposition, with execution and test calibration explicitly absent. No optional supported claims were sampled; all decision-relevant records were checked.

Exact checked decision: **CHANGES_REQUIRED — correct the boundary comparison and check acceptance of integer 10 before accepting the supplied upper boundary.** This HOLDS: the supplied evidence establishes the required bounded repair, so more investigation is not needed to identify the defect. BLOCKED is not justified because the supplied contract does not establish an essential-use disqualifier beyond routine acceptance failure. Acceptance of a repaired target is not adjudicated here.

Remaining obligations: implement M-R-1 in the relevant target and check the repaired boundary; M-R-2 provides a proposed regression-test method. Unexamined contracts: non-integer input handling, alternative implementations/callers, environment-specific behavior, and all behavior beyond this integer boundary. No broader safety or compatibility assurance is given. Errata: NONE.
