# Fresh original-case decision check

Case: BS-WORKFLOW-2026-11-01. Checked at 2026-11-01T20:00:13Z (UTC), with subsequent record preparation in the same bounded turn. Phase: original-case decision check. Audience: Python API callers and maintainers.

The proposed **CHANGES_REQUIRED** decision is supported: exact-fill requests violate the explicit contract, and R-1/R-2 are proportionate proposed repairs. Recommend **revise and recheck** the record before issuance: qualify the unverified coordinator-environment portion of C-6 and attach a visible correction to the overstrong M-A-3 type-probe explanation. These are evidence-accounting corrections, not new product findings or grounds to change the original decision to INVESTIGATION_REQUIRED or BLOCKED.

## Actual reviewer basis and boundaries

- Actual reviewer basis: **FRESH_AGENT**. I did not author the fixture, original testimony, recall, adjudication, or draft. My new context first received the checker assignment, inherited workstation instructions and an unrelated memory summary, then the assigned packet and supplied evidence. I had general Python knowledge but no prior fixture inspection. After reading the draft/testimony I was not blind to their conclusions, as required for this checking role.
- I am an agent checker, **not the independent human reviewer**. Independent human assessment remains PENDING. Shared model and host can correlate errors; freshness is context separation, not statistical independence or OS isolation.
- Scope: both functions and all supplied tests against `original/CONTRACT.md`; check C-1–C-6, F-1, R-1/R-2, P-1–P-9 and the exact draft decision. All were checked; none was sampled away.
- Read in full: `packets/checker.md`; `CASE_FILE_DRAFT.md`; `ADJUDICATION.md`; `sealed-source.json`; `freeze-initial.json`; all three `original/` files; all three initial testimonies; `roles/watson/WATSON_REPAIRS.md`; `capture.py`; Holmes' probe script and its run/stdout/stderr; Moriarty's four scripts and all run/stdout/stderr files under `contract-grid/`, `supplied-tests/`, `source-manifest/`, and `evidence-audit/`. Truncated combined displays were completed through smaller reads.
- Actions: file reads/listing, SHA-256 hashing, byte counting, UTC timestamp inspection, and this assigned write. **No behavioral probe, import, test execution, repair, source edit, Git command, commit, network request, shared worker/service, speech, upkeep, or delegation.** Read-only inspection was sufficient. Supplied executions remain **REPORTED** to me; source inspection of their scripts/logs is not my EXECUTED reproduction.
- Read exclusions honored: no `evaluator/`, main repository, other conversations, sibling instruction packets, or memory files. Git ancestry and coordinator packet-building history were therefore not independently inspected. The head `666ee650d87d008dea3e74292f96c52cb1e1d9f7` remains coordinator-REPORTED to this checker.
- Controls: shared host, no filesystem/credential/network sandbox. Network prohibition and read boundaries are instruction-only. No behavioral workload needed CPU/memory/time isolation. Reviewed `capture.py` implements its recorded CPU, wall, per-file, stream, process-group and role-byte monitoring controls; these are not a disk quota or comprehensive host action monitor. Its absence of memory/filesystem/network isolation is accurately disclosed by the investigators.
- Budget: at most ten minutes, at most 1 MiB role evidence. Only this small Markdown artifact is produced; no scratch workload or cleanup is needed.

## Evidence identity and citation scheme

All paths are case-root-relative. These identities were independently rehashed with `shasum -a 256`; sizes were checked with `wc -c`. Digests identify bytes, not authenticity or trusted historical timestamps.

| Ref | Saved path | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| D | CASE_FILE_DRAFT.md | 4027 | 6f43fbf3d03754afab98741fc5a47c496f83d20a2d9360926256301419826fde |
| A | ADJUDICATION.md | 3185 | 065b0479a60740a3f7ed397af89b8d0564187bec73c27af88e102c065dd0f5a8 |
| C | original/CONTRACT.md | 1179 | e117f946f77499cd1bc254a49e97ea408370c409d67e40eabff10145600fb3b1 |
| S | original/capacity.py | 830 | 85209d664496919cd2acbca588aafe68a3277733973f660f53bec0b9868c3ead |
| T | original/test_capacity.py | 583 | 82fe2b7db9124c83ddf9867a39d34a2126e369f0484bfa00162207dc56751a50 |
| SS | sealed-source.json | 263 | 533e13a1aa094b34c925a7c506218541322fdc974d1b205dc7a0550f4875aade |
| FI | freeze-initial.json | 376 | 619c3a42aa5d7d548c45d7f862882fb0ca16c794dea3c924f83927224078238f |
| H | roles/holmes/HOLMES.md | 18232 | cbda72de8a2251e3304598889b69900793dd915b8989b48563a99d23c98c8bef |
| WF | roles/watson/WATSON_FIRST.md | 8267 | f94029ab9e3f73d7543ec66e3c52ecb95a15c09c370e553c6abf880a19df2643 |
| M | roles/moriarty/MORIARTY.md | 17320 | 4febc0d980d30963eaec0dc710c1914a16ac8b4171cf96e89fec4574243ed182 |
| WR | roles/watson/WATSON_REPAIRS.md | 20435 | 3a98db829bd5edc6add07772b10008f5fff0af7095a7b89ae7bde2873c51184f |
| CAP | capture.py | 3408 | d757693b464f1a95db2f40616ae0c6e16c3d800976cfe531d75d35774b472532 |
| PK | packets/checker.md | 28176 | a3e1f2464c0930cf7ca9a19a0ba583994aeec8ab14c2c816f088a6b08aa782ca |

For raw artifacts, H-E-* references mean the saved-path/digest/size manifest in H; M-E-* references mean the manifest in M. HP, MP, MB, MM, MA, MAO, MAR mean the saved-path/digest entries in WR. I rehashed every listed role script and every captured run/stdout/stderr file; all matched those manifests and receipt script hashes. The source-manifest receipt additionally matches WR's recorded `fb03eb2cf92d4b60283bd58c2d9bf30493d09a8396a0c186534c271f4b9b3b26`. Current source hashes match SS, and all three initial testimony hashes match FI. This links citations below to directly reopened underlying bytes, rather than accepting testimonial agreement as verification.

## Claims and finding: every ID

Here HOLDS means the draft's assessment of the proposition holds, not that a proposition assessed REFUTED becomes true.

| ID | Result | Checked evidence, reasoning, and limits |
| --- | --- | --- |
| C-1 | **HOLDS** | Its REFUTED assessment follows from C lines 10–13 and S lines 5–11: `(0,1,1)` and `(2,3,5)` pass type/state/count guards, then equality enters the `>=` rejection. H-E-9 and M-E-10 record those same failures. Their independent contract oracles use the required inclusive boundary. SOURCE/INFERENCE plus REPORTED executions; not a new run. |
| C-2 | **HOLDS** | S lines 16–20 implement plain-integer guards, `used >= 0`, `0 < count <= used`, then subtraction. H-E-9 records zero mismatches over 121 integer pairs plus its large full release; M-E-10 records zero over 81 pairs, 14 type substitutions and three large releases. Both oracles match C lines 4–6 and 17–19. The draft correctly avoids universal runtime or production claims. |
| C-3 | **HOLDS** | T contains five methods and reservation sums 5 and 9 with capacity 8, omitting equality. H-E-9 reports five passes, and M-E-7–9 include named tests, `Ran 5 tests`, OK, exit 0. HP and MB load the supplied module rather than substituting another suite. The suite pass does not discharge C-1. |
| C-4 | **HOLDS** | S lines 5–6 and 16–17 use exact type checks before arithmetic; remaining bodies only compare, add/subtract, raise or return. Under ordinary runtime semantics this supports the plain-type and source-visible no-side-effect statements. H-E-9 reports 50 invalid-type calls, M-E-10 reports 35, all rejected. The draft's no-OS-action-monitor limitation is appropriate. These output checks do not establish sensitivity to each individual guard; see the M-A-3 correction below. |
| C-5 | **HOLDS** | SS matches all three current source hashes; H-E-9 records before/after identity; M-E-13 and MAO record matching source seals after inquiry. FI also matches each current initial testimony. Historical observations are REPORTED, current byte identity was directly checked. Git identity is expressly attributed to the coordinator, not verified by these investigators or me. No claim of OS-enforced immutability follows. |
| C-6 | **UNRESOLVED** in part | H-E-8, H-E-9, M-E-9, M-E-12 and the source-manifest receipt directly record Python 3.9.6, so that part HOLDS. The claims that a frozen plan anticipated 3.13.15 for the coordinator and that packet construction used 3.13.15 have only the coordinator's A/D assertions in my permitted evidence. I did not inspect the forbidden evaluator plan or an execution receipt for packet building. Qualify these as coordinator-REPORTED or supply permitted underlying evidence. This historical provenance gap does not affect the established API defect or required repair. |
| F-1 | **HOLDS** | C lines 10–13, S lines 9–10 and the counterexamples above establish one CONFIRMED exact-fill defect. Valid request → Python caller receives ValueError → a permitted reservation cannot complete. MODERATE is proportionate to this bounded impairment; C lines 25–26 reject treating a reproducible violation alone as essential-use disqualification. REQUIRED_REPAIR/THIS_CHANGE follows. Source reasoning supports every otherwise-valid equality case, not real-world frequency. Origin, intent and caller frequency remain UNKNOWN. The omitted boundary test belongs to the same finding. |

The finite-case counts and exit interpretations were also checked against scripts and logs: Holmes has 1331 reservation-grid and 121 release-grid calls, 36 reserve-grid mismatches, 50 type cases and three large calls; its final code intentionally does not fail on those mismatches. Moriarty has 729 reservation-grid, 81 release-grid, 35 type and six large calls = 851 aggregate cases, plus six explicit overlapping demonstrations; its 22 aggregate mismatches trigger exit 1. Successful imports, named test output, boundary controls, empty behavioral stderr, and `stopped: null` support diagnostic behavior rather than setup failure. These counts describe recorded finite experiments, not independent failures or population prevalence.

## Required repairs and new factual claims

| ID | Result | Evidence and assessment |
| --- | --- | --- |
| R-1 = W-R-1 | **HOLDS**, PROPOSED | Replacing only S line 9's `>=` with `>` preserves the preceding guards and integer-sum return while matching C's inclusive success rule. Above-capacity rejection remains required; `release` is unchanged. This is source-checked intent, not implemented or validated candidate behavior. One comparison edit plus R-2 is one coherent change. |
| R-2 = W-R-2 | **HOLDS**, PROPOSED | The two proposed calls `(0,1,1)` → exact int 1 and `(2,3,5)` → exact int 5 follow independently from C lines 4–6 and 10–13. Zero and nonzero starting usage make a useful small regression pair; exception text is correctly excluded. Both examples appear as failures in H-E-9/M-E-10. The exact extracted test bytes must still fail diagnostically against the identified actual baseline and pass against the separately identified repaired module, with the five old tests and named controls retained. Wrong imports or runner failures cannot serve as RED. No extracted test has yet been validated. |

New claims in WR were checked explicitly. The proposed comparison resolves the identified source mismatch conditionally; it is not a claim of shipped behavior. Preserving below/above and invalid-input behavior is an acceptance check, not a completed result. The fixed-test literals and exact integer-type oracle are contractual. Reusing the finite corpus requires explicit candidate loading because MP currently inserts `original/`; WR calls this out. Effort ranges are estimates with stated assumptions, not measurements. No migration operation is established by this stateless contract (C lines 21–26), but WR appropriately declines to assure that unknown downstream users have nothing to do. No new persistence, concurrency, operator, dependency or publication guarantee is created.

R-1/R-2 implementation, actual-baseline extracted RED, repaired GREEN, surrounding checks, complete diff inspection, candidate identities and fresh repaired-candidate review remain outstanding. Their outstanding status is expected for this original CHANGES_REQUIRED case. It would prevent a repaired READY claim, not issuance of the original decision.

## Every probe disposition

All destinations remain PROPOSED. HOLDS below validates the disposition and stated remaining gates, not graduation.

| ID | Result | Underlying evidence and disposition check |
| --- | --- | --- |
| P-1 = W-P-1 | **HOLDS** | HP/H-E-8–10 is an omnibus investigative script, with exit 0 despite mismatch evidence. MINIMIZE_THEN_PROMOTE into R-2's two tests is appropriate; archive the original grid/control/provenance bytes. Contract-derived oracle, explicit module identity and extracted diagnostic RED/GREEN are still required. Direct promotion would be misleading. |
| P-2 = W-P-2 | **HOLDS** | MP/M-E-10–12's explicit equality cases and independently expressed inclusive oracle support the same MINIMIZE_THEN_PROMOTE destination. They feed the same two tests as P-1, with no duplicate suite. Exit 1 is mismatch-driven and not failed setup. Only the extracted tests' future baseline/candidate evidence can validate graduation. |
| P-3 = W-P-3 | **HOLDS** | MP release oracle/groups and M-E-10 show the finite release negative result. ARCHIVE is proportionate; T already retains partial/full/over-release controls. Optional reuse as surrounding candidate validation does not turn archived evidence into a newly maintained suite. No release finding or independent repair is established. |
| P-4 = W-P-4 | **HOLDS** | MP type substitutions/M-E-10 establish observed rejection for those inputs. ARCHIVE preserves them without claiming individual-guard mutation sensitivity. WR explicitly identifies masking when capacity is True. This narrowing is correct, but the conflicting frozen M-A-3 sentence needs the visible correction below. No new product defect follows. |
| P-5 = W-P-5 | **HOLDS** | MB and M-E-7–9 establish that the five-test baseline suite passes without detecting F-1. ARCHIVE the case-specific loader/receipt; keep the already-maintained tests and run them later as controls. These bytes cannot stand in for a diagnostic equality regression. |
| P-6 = W-P-6 | **HOLDS** | HP's metadata/hash sections and H-E-8–10 support identity/runtime/preservation recording, not an application contract test. ARCHIVE retains their limited purpose and distinct exit convention. Candidate identity collection remains a future validation procedure. |
| P-7 = W-P-7 | **HOLDS** | MM and source-manifest run/stdout/stderr hash the inspected sources/scripts and report Python 3.9.6. ARCHIVE is appropriate for case-specific provenance, with no claim that a repaired candidate exists. |
| P-8 = W-P-8 | **HOLDS** | MA and MAO/MAR enumerate source and artifact identities; the logged 12311 bytes explicitly precede that capture's outputs and testimony. ARCHIVE preserves the measurement at its actual scope. It is not a claim about current total role usage or a product regression. |
| P-9 = W-P-9 | **HOLDS** | FI, source/testimony manifests and current rehashes support freeze integrity and linkage. ARCHIVE preserves those records without converting identity into behavioral correctness. I did not independently reconstruct Watson's historical hashing commands. |

All four canonical destinations were considered. PROMOTE is not suitable for either investigative script; existing maintained tests need retention. MINIMIZE_THEN_PROMOTE has the bounded justified destination above. No separate compatibility/migration/fuzz/performance obligation justifies RETAIN_IN_SPECIALIZED_SUITE. ARCHIVE is justified for the remaining controls and provenance. The lack of already-validated extracted tests is honestly disclosed, not an original-decision blocker beyond the named future repair validation.

## Required record revisions and proposed erratum

1. **Qualify C-6 and the draft's packet-build statement.** Suggested wording: “Both initial behavioral inquiries recorded Python 3.9.6. The coordinator reports that packet building used 3.13.15 and that its earlier plan anticipated that environment; the fresh checker did not inspect underlying evidence for those coordinator-history statements.” Preserve the old plan and original testimony. Alternatively provide a permitted receipt for rechecking; no evaluator access is requested.
2. **Add an append-only erratum and visible wrapper pointer for M-A-3.** Original: “The unchanged controls are valid arithmetic states, so an invalid starting state cannot mask the input-type issue.” Correction: “The original control tuples are valid before substitution, but some substituted inputs can be rejected by later validation or the capacity comparison even without a type guard. For example, replacing capacity in `(1,1,4)` with `True` yields sum 2 against numeric capacity 1; a remaining capacity comparison can reject it. All 35 recorded type cases raised ValueError, but this does not establish that each exact-type guard is independently necessary or mutation-sensitive.” Reason: the probe's input construction and S's later branches contradict the stronger diagnostic assurance. Basis: SOURCE/INFERENCE from MP's type loop and S lines 7–10; no mutation was executed. Affected records: frozen M-A-3 and its “no faulty-probe correction needs an erratum” summary; WR's P-4 already supplies the correct limitation. Preserve both original testimony and observed results. No change to F-1, R-1/R-2, P-4's ARCHIVE destination, or the proposed decision is needed.

The second correction concerns an overstatement about probe sensitivity, not a faulty equality oracle or a failed product reproduction. Do not withdraw the 35 observed rejections, invent a second defect, demand an unrelated type-suite repair, or claim mutant calibration occurred. Recheck these changed material record passages before final issuance; do not silently edit the frozen testimony.

## Exact draft decision and recommendation

The exact operative text in D is:

> Draft decision: **CHANGES_REQUIRED**, pending fresh decision check.
> The original reserve implementation rejects valid exact-fill requests. A bounded
> comparison repair and two diagnostic regressions are required. The release
> control has no identified violation within the inspected contract and finite probes.

**Decision check: HOLDS.** The explicit unmet acceptance obligation is inclusive exact-fill success, established in source and recorded counterexamples. There is no established disqualifier under C lines 25–26, so BLOCKED is inappropriate. No unresolved decision-critical evidence prevents the bounded diagnosis, so INVESTIGATION_REQUIRED is unnecessary. The established F-1 repair obligation requires CHANGES_REQUIRED; original READY would contradict the contract. Release reassurance is appropriately limited to inspected source and finite checks.

**Recommendation: revise and recheck the two record issues, then issue the same CHANGES_REQUIRED decision.** This is a checker recommendation, not the Agency's issued ruling. No further behavioral experiment is needed to settle this original decision. Do not reinterpret this check as candidate validation, integration, publication, or independent human sign-off.

Incomplete checks: coordinator packet-build/plan history and Git ancestry are not independently verified; neither changes this decision's API acceptance assessment. Historical callers, prevalence, intent, deployments, other runtimes, resource exhaustion, concurrency, persistence and performance remain outside the examined evidence/scope. No universal defect-free certification is given.

Sampling: N/A. Cross-examination sampling was not separately assigned; every C-1–C-6, F-1, R-1/R-2, P-1–P-9 and the draft decision was checked. Eligible remaining IDs, seed, algorithm and selected sample are N/A because there is no sampled subset.
