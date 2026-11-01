# Original case — BS-WORKFLOW-2026-11-01

Issued decision: **CHANGES_REQUIRED**.
The original reserve implementation rejects valid exact-fill requests. A bounded
comparison repair and two diagnostic regressions are required. The release
control has no identified violation within the inspected contract and finite probes.

Valid only for the recorded artifacts, environment, and examined scope.
Reassess affected claims when these change.

## Basis and limits

Original Git head: `666ee650d87d008dea3e74292f96c52cb1e1d9f7`.
Source files and SHA-256 identities: `sealed-source.json` and `original/`.
Skill source head: `9da80cf445984157f1e61823dc93f80ae305ed7e`; complete dispatched
rules and headers are retained in `packets/` and `headers/`.
Coordinator authored this synthetic fixture and knew the expected defect;
initial investigators did not receive that answer key. Separate role contexts
share model/host and are not statistically independent or OS-isolated. Initial
Holmes and Moriarty execution receipts record Python 3.9.6. The coordinator
reports packet construction under 3.13.15; this historical assertion has no
contemporaneous packet-build receipt and is not independently verified.
No performance comparison, production coverage, or host action audit is claimed.

## Testimony and adjudication

All three original testimonies are frozen by `freeze-initial.json`.
- `roles/holmes/HOLMES.md`: source verification and finite probes.
- `roles/watson/WATSON_FIRST.md`: no-probe first reading.
- `roles/moriarty/MORIARTY.md`: falsification attempts and controls.
- `roles/watson/WATSON_REPAIRS.md`: same-context recall after first testimony
  was frozen and sibling conclusions supplied. No target changes or probes.

`ADJUDICATION.md` supplies C-1 through C-6 and the local-to-global mapping.
Apply ERRATA.md E-1 to C-6 and E-2 to Moriarty M-A-3 and its no-erratum summary.
The raw draft, adjudication, and testimony are retained; these errata are the
current qualifications. E-2 does not withdraw the observed type rejections or
claim a mutation was run.
F-1 combines H-F-1/M-F-1 and W-C-2: deterministic exact-fill rejection contrary
to CONTRACT.md lines 10–13. Severity MODERATE, CONFIRMED, REQUIRED_REPAIR,
THIS_CHANGE. Origin, intent, and real-world frequency are UNKNOWN. The supplied
contract does not make this bounded defect an essential-use disqualifier.

The five original tests pass but omit this boundary. Holmes' probe exit 0
means inquiry completion despite logged mismatches; Moriarty's exit 1 reports
observed contract mismatches, with imports and setup working. These two exit
conventions must not be confused. Negative control results remain scoped to
source reasoning and their finite cases.

## Proposed repairs and all probe dispositions

Adopt the records in `roles/watson/WATSON_REPAIRS.md`:
- R-1 = W-R-1: change only reserve's rejection comparison from >= to >.
- R-2 = W-R-2: add zero/nonzero exact-fill tests checking int type and literal
  values; prove actual-baseline diagnostic RED and repaired GREEN; retain five
  existing tests and run the named surrounding controls.
- P-1 through P-9 map directly to W-P-1 through W-P-9. P-1/P-2 minimize the
  same boundary evidence into the same two tests; P-3 through P-9 archive
  finite controls, baseline loader, and identity/audit evidence. Nothing is
  deleted. No new specialized suite is required by this bounded defect.

All repairs and maintained-test destinations are PROPOSED. Implementation and
validation have not occurred. R-1 and R-2 should form one coherent repair commit;
there is no need for a broken intermediate commit. No target source, original
contract, or initial testimony has been modified. No additional code, migration,
concurrency, or publication obligation follows from this synthetic contract.

## Decision obligations and next action

The unmet original acceptance obligation is F-1. The original candidate cannot
be called READY while it violates the inclusive boundary. Missing historical
usage data does not prevent the bounded diagnosis or require unrelated work.
After fresh checking of this draft, implement R-1/R-2 on a separate repair
worktree, preserve baseline/repair identities and diagnostic evidence, and obtain
a fresh repaired-candidate check. Preserve this original ruling unchanged.
Independent human assessment of the completed exercise is separately PENDING.

## Issuance

Issued after the fresh original decision check and same-checker recheck accepted
the corrected record. See `roles/checker/DECISION_CHECK.md`,
`roles/checker/RECHECK.md`, and `ERRATA.md`. This is the original-source ruling;
a later repair receives a separate record and decision.
