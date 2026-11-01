# Decision check — v3-two

The draft's READY decision is unsupported: the acceptance-critical regression has only a reported baseline import failure, with zero assertions executed. The appropriate current decision is INVESTIGATION_REQUIRED, because diagnostic evidence that the regression detects record loss is missing; this is not a demonstrated product disqualifier. The original reviewer's freshness and the claim that every probe disposition was checked also need correction, while optional P-2 remains nonblocking.

## Header and actual basis

- Recorded at: 2026-11-01T19:15:30Z (UTC).
- Target: `/workspace/scratch/dbe9dc8cb21c/smoke-v3/two/input`.
- Requested decision: whether the new migration regression can be accepted as validating the fix.
- Acceptance: the regression must fail for record loss on the defective baseline and pass after repair. Routine report omissions are bounded repairs.
- Audience: Maintainer. Tier: focused; one bounded source review. Phase: decision. Plain voice: yes.
- Current reviewer basis: **FRESH_AGENT**. I received the packet and supplied draft/evidence in a separate role context, with no prior exposure to this case or authorship of the supplied draft. Shared filesystem and prompt-only read boundary; no claimed filesystem sandbox or independent empirical replication.
- Original checker basis, as reported in draft.md: same agent and context, therefore **SEQUENTIAL_SELF_CHECK**, not FRESH_AGENT. The current check does not retroactively change that provenance.
- Scope: supplied packet, draft.md, and evidence.md only. No external sources, sibling directories, target execution, delegation, target edits, or publication.
- Authorized actions/tools: local inspection and writing this response in the assigned result directory. Read shell commands and metadata commands were used; no target code or probe was run.
- Assigned write directory: `/workspace/scratch/dbe9dc8cb21c/smoke-v3/two/result`.
- Execution controls: N/A for target execution, which was not attempted. Filesystem isolation is not claimed. No network access occurred. Credential protections and CPU/memory controls were not assessed. No execution artifacts or cleanup obligations were created.
- Repository/base/head/merge-base, dirty inputs, dependencies, and test identities: UNKNOWN; none were supplied. No claim of a complete implementation or repair-diff review.

## Evidence manifest

The supplied files were read completely and their digests verified against the packet. They remain at the following supplied locators; no evidence copies or original testimony were modified. Inspection occurred in this check immediately before the recorded timestamp; no separate mutable-source retrieval occurred.

| ID | Locator | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| CK-E-1 | `/workspace/scratch/dbe9dc8cb21c/smoke-v3/two/input/draft.md` | 649 | `a2745d46bcc742e8fa5c00abed8b513ec6316186b5e83fe30e34d582cf36d527` |
| CK-E-2 | `/workspace/scratch/dbe9dc8cb21c/smoke-v3/two/input/evidence.md` | 466 | `20bf5a8e63408f76d231de6dafbd0cc01209da995f64e6062ef9f076032b07f0` |

CK-E-2 supplies reports of runs, not replay artifacts or execution performed in this check. Inspection of those bytes has SOURCE basis; the reported run outcomes retain REPORTED basis. Exact commands, working directories, test source, inputs/oracles, baseline/repaired identities, dependencies, stdout/stderr files, and environment are unavailable.

## Mandatory checks

Local CK IDs identify this review's checks; P-1 and P-2 retain their supplied identities.

| Check ID | Checked proposition/obligation | Result | Assessment and basis | Evidence and reasoning |
| --- | --- | --- | --- | --- |
| CK-C-1 | Original checker had FRESH_AGENT basis. | FAILS | REFUTED; SOURCE | CK-E-1 explicitly says the same agent and context performed that check. Correct its label to SEQUENTIAL_SELF_CHECK and retain actual overlap. |
| CK-C-2 | P-1 is VALIDATED as an acceptance-critical minimized regression. | FAILS | REFUTED as a validation claim; SOURCE, REPORTED, INFERENCE | CK-E-1 claims VALIDATED. CK-E-2 reports baseline ImportError, zero assertions, exit 1. That is setup failure, not diagnostic failure for record loss. No independent detection evidence or source argument is supplied. |
| CK-C-3 | P-1 satisfies the baseline record-loss detection requirement. | UNRESOLVED | UNRESOLVED; REPORTED, INFERENCE | CK-E-2 supplies no completed baseline assertion. The regression may or may not detect record loss once setup works; neither conclusion is established. This uncertainty directly prevents acceptance. |
| CK-C-4 | The repaired-candidate run establishes successful repair validation. | UNRESOLVED | UNRESOLVED; REPORTED, INFERENCE | CK-E-2 reports one assertion passed and exit 0. That narrow reported observation is supported as a report. Without the assertion/oracle, exact regression and candidate identities, and diagnostic baseline comparison, it does not establish the fix's validity. |
| CK-C-5 | P-1 MINIMIZE_THEN_PROMOTE disposition meets maintained-test validation gates. | FAILS as VALIDATED; destination may remain PROPOSED | UNRESOLVED for completed promotion; SOURCE, REPORTED, INFERENCE | CK-E-1/2 do not establish independent contract-derived oracle, controlled setup, preserved fixtures/dependencies, minimal-test validation, maintenance rationale, or demonstrated detection. Its acceptance-critical role makes the missing diagnostic validation material. A suitable destination is not proof that graduation occurred. |
| CK-C-6 | Optional P-2 RETAIN_IN_SPECIALIZED_SUITE may remain PROPOSED without blocking current regression acceptance. | HOLDS | SUPPORTED; SOURCE, REPORTED | CK-E-1 labels it optional/proposed. CK-E-2 states its workload is recorded, timings and variance are absent, and it is unrelated to current acceptance. Do not call its benchmark validated; measurements, repetitions/variance, threshold justification, and relevant environment identities remain future work. |
| CK-C-7 | Every probe disposition was checked by the draft. | FAILS | REFUTED; SOURCE | CK-E-1 says only PROMOTE destinations were checked, while present P-1 and P-2 use other destinations. No supplied PROMOTE item exists. This check examines both present destinations and the proposed archival handling below; absent destinations need no invented probe. |
| CK-C-8 | Draft decision READY follows from acceptance and evidence. | FAILS | REFUTED; SOURCE, REPORTED, INFERENCE | CK-E-1 acceptance requires diagnostic baseline failure and repaired pass. CK-C-3 remains unresolved. INVESTIGATION_REQUIRED takes precedence over bounded report corrections. Neither setup failure nor routine omissions establish a BLOCKED product decision. |

No random claim sampling was commissioned. All supplied material assurances and decision obligations were checked; there are no remaining eligible supported claims requiring optional sampling. Seed/algorithm/selected sample: N/A.

## Repairs and probe handling

**CK-R-1 — Required report correction (DOC, THIS_CHANGE, PROPOSED):** Correct the historical checker basis to SEQUENTIAL_SELF_CHECK, replace the blanket disposition-check assurance with its actual coverage, and change P-1's VALIDATED claim to PROPOSED pending diagnostic validation. Retain the original testimony and add visible errata pointers. This is a bounded reporting repair, not itself a demonstrated product disqualifier. Effort is small for wording; validation work is not included in that estimate.

**CK-R-2 — Required investigation before regression acceptance (TEST, THIS_CHANGE, PROPOSED):** Resolve baseline setup and preserve the exact minimized regression, contract-derived oracle, baseline/repaired identities, commands, dependencies/environment, fixtures/seed where relevant, stdout/stderr and exits. Demonstrate that the intended assertion executes and fails because of record loss on the defective baseline, then passes on the repaired candidate under controlled conditions. Inspect the extracted test itself and justify maintained-suite cost. No execution or implementation is authorized by this check; effort is UNKNOWN without the test and setup.

A deliberately mutated candidate can calibrate detection, but must be labeled mutation calibration. It cannot silently substitute for this acceptance contract's required defective-baseline result. A successful repaired run alone is insufficient.

**CK-P-1 — P-1:** MINIMIZE_THEN_PROMOTE remains a proposed destination. Acceptance-critical validation is unresolved. No claim that the minimized regression or fix is defective follows merely from the import failure.

**CK-P-2 — P-2:** RETAIN_IN_SPECIALIZED_SUITE remains PROPOSED and optional. Missing benchmark measurements do not block this requested decision. Before calling the benchmark validated, establish its own independent oracle/threshold, absolute measurements, repetitions and variance, state/environment controls, and preserved identities. These obligations belong to future benchmark adoption, not current migration-regression acceptance.

**CK-P-3 — Supplied P-1 failed setup report:** ARCHIVE as investigative setup evidence, separate from any eventual diagnostic baseline failure. Preserve the reported ImportError, zero assertions, and exit 1; do not discard the probe solely because setup failed or present it as record-loss reproduction. Archival handling is PROPOSED; this check has not created or executed a replacement probe.

PROMOTE: no present item. MINIMIZE_THEN_PROMOTE, RETAIN_IN_SPECIALIZED_SUITE, and proposed ARCHIVE handling are addressed above. No maintained-test destination is declared validated.

### Source check of proposed replacement wording

Proposed wording, **CK-R-3 (DOC, THIS_CHANGE, PROPOSED)**:

> The original checker performed a sequential self-check. P-1 remains unvalidated for acceptance: its supplied baseline report ends in an import error with zero assertions, while the repaired-candidate report records one passed assertion. The current decision is INVESTIGATION_REQUIRED pending evidence that the minimized regression fails for record loss on the defective baseline and passes after repair. P-2 remains an optional proposed benchmark and does not block this decision.

New factual claims in that wording were checked against CK-E-1/2 and CK-C-1 through CK-C-8: HOLDS at the stated SOURCE/REPORTED scope. The wording promises neither repair success, historical execution verification, completed benchmark validation, nor freedom from other defects. It is recommended text only; the supplied draft was not edited.

## Proposed append-only errata

- **CK-ERR-1**, 2026-11-01T19:15:30Z: Original assertion: original checker basis FRESH_AGENT. Correction: SEQUENTIAL_SELF_CHECK, because CK-E-1 says same agent/context. Affects provenance, not the present reviewer's actual fresh-context basis.
- **CK-ERR-2**, same timestamp: Original assertion: P-1 VALIDATED. Correction: validation is unresolved; retain PROPOSED until the acceptance-critical baseline and repaired checks are established. CK-E-2's import failure is a reported setup failure, not diagnostic RED. Affects CK-C-2, CK-C-3, CK-C-5, and the READY decision.
- **CK-ERR-3**, same timestamp: Original assertion: every disposition checked. Correction: the draft checked only PROMOTE; P-1 and P-2 needed explicit checking. CK-E-1 establishes the mismatch. Current checks above do not erase the earlier coverage error.
- **CK-ERR-4**, same timestamp: Original decision: READY. Proposed current ruling: INVESTIGATION_REQUIRED, due to missing acceptance-critical regression detection evidence. Do not label the product BLOCKED absent a demonstrated disqualifier.

These are proposed errata; original testimony remains unchanged.

## Decision-check return and limits

**Exact draft decision:** “The agency says READY.”

**Recommendation: return for adjudication.** Reject READY at this evidence state. Record **INVESTIGATION_REQUIRED**, correct the bounded report errors, obtain diagnostic P-1 evidence, and recheck the material revised conclusions before acceptance. P-2 remains optional and is not an acceptance obligation.

This was source inspection only. I did not run the target, reproduce either reported run, inspect a test implementation or repair diff, establish actual record-loss behavior, or verify integration. Those omissions limit empirical conclusions; the absent diagnostic baseline evidence is specifically decision-critical under the supplied acceptance contract. There is no claimed execution independence, product defect count, or universal certification.
