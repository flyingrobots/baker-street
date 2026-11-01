# Append-only case errata

## E-1 — Runtime provenance qualification (2026-11-01T20:03:16.003722+00:00)

Original assertions: ADJUDICATION.md C-6 and CASE_FILE_DRAFT.md state that packet
construction used Python 3.13.15 and interpret the frozen evaluator plan.

Correction: both initial behavioral inquiries **recorded Python 3.9.6** in their
execution receipts. The coordinator **reports** packet construction under 3.13.15
and that its earlier plan anticipated that environment. No contemporaneous
packet-building execution receipt is supplied to the fresh checker, so that
historical statement is REPORTED, not independently verified execution evidence.
The plan remains unchanged. The receipt-supported 3.9.6 observations remain intact.

Reason/evidence: original decision check C-6 found the coordinator-history portion
unsupported by its permitted underlying evidence. This qualification affects
provenance wording only; it changes neither F-1 nor the CHANGES_REQUIRED decision.
This entry supersedes the unqualified portions of the original draft/adjudication.

## E-2 — Type-probe sensitivity overstatement (2026-11-01T20:03:16.003722+00:00)

Original assertion: Moriarty M-A-3 says the unchanged controls are valid arithmetic
states, so an invalid starting state cannot mask the input-type issue. Its summary
also says no faulty-probe correction requires an erratum.

Correction: the control tuples are valid **before** substitution. Some substituted
inputs can still be rejected by later guards or the capacity comparison if an
exact-type guard is removed. Replacing capacity in (1,1,4) with True gives sum 2
against numeric capacity 1; the remaining capacity comparison can reject it.
All 35 recorded substitutions did raise ValueError, but this does not prove every
individual type guard is necessary or that the probe is mutation-sensitive.

Basis: SOURCE/INFERENCE from roles/moriarty/contract_probe.py and original/capacity.py
lines 7–10; Watson's recall P-4 already states this limitation. **No mutation was
executed** for this correction. This is an explanatory overstatement, not a faulty
equality oracle or an additional product defect. The recorded results remain valid
at their stated output scope. P-4 remains ARCHIVE. F-1, R-1/R-2, and the original
CHANGES_REQUIRED decision are unchanged.

The raw Moriarty testimony is frozen. Readers should apply this visible correction
to M-A-3 and its no-erratum summary, rather than treating the original wording as
the current adjudication.
