# Moriarty testimony — v3-six

The upper boundary contradicts the supplied contract: integer `10` is required to be accepted, but `validate(10)` follows the rejection branch. This is established by source inspection; no target code was executed.

## Basis and evidence

I read the complete assigned packet, the complete contract, and the complete validator. I inspected no sibling directories, used no external sources, and did not delegate. I had no prior target or sibling-review exposure in this role context. The context is separate, but the filesystem is shared and the read boundary is instruction-only; no filesystem sandbox is claimed.

The only commands used for inspection were `cat`, `rg --files`, `nl -ba`, `sha256sum`, and `wc -c`, addressing the assigned packet or supplied evidence paths. All completed successfully. These operations inspect bytes; they do not constitute execution of the validator. Runtime/dependencies, repository history, and historical test results were not supplied or inspected. No runtime isolation, mutation control, or replay transcript is claimed because no target experiment was authorized or performed.

| ID | Evidence locator, relative to this report | SHA-256 | Bytes |
| --- | --- | --- | ---: |
| M-E-1 | `../input/contract.md`, line 1 | `dcf5e4cca9ded61d0d9e5f6b3b916a854462be4a67e8844309e97ded68a8c9c9` | 141 |
| M-E-2 | `../input/validator.py`, lines 1–4 | `c131b45850b917168da501207776cbcdb9379aaa9c80fe9421741c62e04c6ab5` | 84 |

Both computed digests match the packet's sealed basis. Sources are the supplied local snapshots; their original retrieval times are UNKNOWN. Digests establish byte identity, not authenticity or execution history.

## M-A-1 — Inclusive upper-bound counterexample

- **Hypothesis:** The validator rejects the expressly included integer endpoint, `10`.
- **Attacked contract:** M-E-1:1 includes every integer up to and including `10`; the requested review concerns that upper boundary.
- **Method/setup/inputs:** SOURCE inspection of M-E-2:1–4 with integer input `10`; no execution.
- **Independent oracle:** Acceptance of `10` follows directly from M-E-1:1, independently of the implementation.
- **Control and probe check:** At `10`, the predicate `x >= 10` is true, so the next statement raises `ValueError("too large")` before `return x`. As source-reasoned neighboring controls, `9` bypasses the rejection and reaches the return, while `11` reaches the rejection. These are logical evaluations of the shown source, not observed runs; the counterexample does not depend on any inference about the required behavior above `10`.
- **Outcome:** CONFIRMED_FINDING.
- **Finding:** M-F-1.
- **Artifacts:** M-E-1 and M-E-2 with line references and hashes above. No executable probe or runtime artifact was created.
- **Limits:** Applies to the supplied function with ordinary integer input. No integration path or deployed copy was inspected.

## M-F-1 — Contractually valid endpoint is rejected

- **Related contract:** M-E-1:1, inclusive integer upper boundary.
- **Status / basis:** CONFIRMED / SOURCE and INFERENCE.
- **Evidence:** M-E-1:1 expressly includes `10`; M-E-2:2–3 rejects `x >= 10`.
- **Impact:** A caller supplies the valid integer `10` → the validator raises `ValueError` → the caller cannot successfully validate that contractually accepted value.
- **Severity / rationale:** MODERATE. This is a concrete, bounded compatibility failure at the endpoint specifically under review. No broader outage or loss is established.
- **Prevalence:** Source logic rejects `10` whenever this exact function receives that ordinary integer. Frequency in actual workloads is UNKNOWN; no measurement was performed.
- **Origin:** UNKNOWN; no earlier implementation or history was supplied.
- **Intentionality:** UNKNOWN; no statement of intent explains the exclusive implementation.
- **Disclosure:** UNKNOWN for the maintainer; no prior defect disclosure was supplied.
- **Disposition:** REQUIRED_REPAIR.
- **Decision relevance:** Directly violates the requested upper-bound acceptance obligation. No separate essential-use or non-negotiable disqualifier was specified.
- **Next check:** Once a change is available, inspect its boundary predicate and, if execution is authorized, check acceptance at `10` with neighboring values against the contract. This is proposed future work, not completed validation.

## Corrections and limits

No faulty probe or correction arose. Runtime boundary tests, integration behavior, non-integer inputs, and broader domain validation were not attempted; they are outside this bounded source review. This testimony supplies no Agency decision, Repair Menu, probe-graduation decision, or decision check.
