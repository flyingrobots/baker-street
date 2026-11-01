# Provisional front-office adjudication

Case BS-WORKFLOW-2026-11-01, original head
`666ee650d87d008dea3e74292f96c52cb1e1d9f7`.

The coordinator authored the synthetic fixture and knows the seeded answer.
Initial investigators received only their own packets and the same frozen source;
this adjudication was written after all three testimonies returned. Their source
and methods overlap, so agreement is not statistical independence.

## Material claims and mapping

- C-1: The implementation satisfies the exact-fill contract: REFUTED by
  capacity.py lines 9–10 and actual counterexamples. H-C-4, M-C-1, W-C-2 map here.
- C-2: The release operation follows its declared guards and subtraction in source,
  and had no mismatches in the reported finite checks: SUPPORTED within those
  scopes. H-C-6/H-C-7, M-C-3, and W-C-4 map here. Do not call finite checks an
  exhaustive test of all inputs or infer production prevalence from a generated grid.
- C-3: Five supplied tests pass yet omit exact fill: SUPPORTED by H-C-9, M-C-2,
  M-A-4 and W-C-3. A green baseline suite does not discharge C-1.
- C-4: Exact-type guards reject non-plain integers; no external side effects are
  visible in these pure function bodies: SOURCE/INFERENCE plus the stated finite
  type probes only. H-C-1/H-C-8, M-C-4, W-C-4. No OS action monitor was run.
- C-5: All three source files match the frozen hashes after initial inquiries:
  SUPPORTED by rehashed source and role receipts. Git identity is verified by the
  coordinator; investigators appropriately call the supplied Git head REPORTED.
- C-6: Both initial behavioral inquiries ran on Python 3.9.6, as their receipts
  record. The frozen evaluator plan's anticipated Python 3.13.15 described the
  coordinator environment, not these later observed child runtimes. Packet building
  used 3.13.15. Preserve the plan and disclose this distinction; do not rewrite it.

F-1 combines H-F-1 and M-F-1 (and Watson's W-C-2): a valid exact fill raises
ValueError. CONFIRMED, MODERATE, REQUIRED_REPAIR, THIS_CHANGE. Real-world frequency,
prior history, and intent are UNKNOWN. The contract explicitly treats this as a
bounded repair, so no essential-use disqualifier is established. The omitted
boundary test belongs to this finding, not an additional independent defect.

The provisional original decision is CHANGES_REQUIRED because F-1 violates the
explicit acceptance bar. No other required product repair is established. This
is a draft for Watson recall and fresh checking, not the final case verdict.

## Recall assignment

Propose a bounded code correction and durable regression for F-1. Retain valid
below/above-capacity behavior, invalid-input rejection, and the clean release
control. Each proposed maintained test must demonstrate diagnostic failure on
this actual baseline and pass on a separate repaired candidate. No repair has
been implemented. Assign dispositions to every material probe: H-A-1, M-A-1,
M-A-2, M-A-3, M-A-4, and explain archival treatment of identity/audit helpers.
Keep original testimony frozen. Address all audiences within this contract;
there is no evidence authorizing migration work or new concurrency guarantees.
