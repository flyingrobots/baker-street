# Watson recall: bounded repairs and probe dispositions

Case: BS-WORKFLOW-2026-11-01. Recall evidence inspected at 2026-11-01T19:54:46Z. Audience: Python API callers and maintainers. Phase: same-context Watson recall; no Agency verdict.

The supplied evidence supports the exact-fill mismatch identified in my first deposition. I propose one comparison correction with two small regression tests, delivered together if implementation is later authorized. All repairs and probe destinations below are **PROPOSED**: I performed no behavioral execution, source edits, test graduation, or candidate validation.

## Exposure, frozen identity, and evidence basis

I am the author of the first deposition and remain in the same context. Initial blindness ended for this recall: I read the full recall packet, frozen first deposition, both initial investigator testimonies, provisional adjudication, and their material scripts, receipts, and logs. I did not read evaluator material, the main repository, other conversations, sibling instruction packets, or the capture runner's source. Execution-control descriptions therefore remain REPORTED by the investigators and receipts, not independently verified by me.

File hashing confirmed that the three initial testimonies match `freeze-initial.json`. My original deposition remains byte-for-byte unchanged at SHA-256 `f94029ab9e3f73d7543ec66e3c52ecb95a15c09c370e553c6abf880a19df2643`. The original source-file hashes also still match those in its W-E-1 through W-E-3 manifest. No correction to that deposition is necessary; this document adds supplied evidence and proposals without changing its historical basis.

Material evidence identities, relative to `/private/tmp/baker-street-workflow-l_fdvdix`:

| Reference | Saved path | SHA-256 |
| --- | --- | --- |
| WF | roles/watson/WATSON_FIRST.md | f94029ab9e3f73d7543ec66e3c52ecb95a15c09c370e553c6abf880a19df2643 |
| H | roles/holmes/HOLMES.md | cbda72de8a2251e3304598889b69900793dd915b8989b48563a99d23c98c8bef |
| M | roles/moriarty/MORIARTY.md | 4febc0d980d30963eaec0dc710c1914a16ac8b4171cf96e89fec4574243ed182 |
| A | ADJUDICATION.md | 065b0479a60740a3f7ed397af89b8d0564187bec73c27af88e102c065dd0f5a8 |
| FI | freeze-initial.json | 619c3a42aa5d7d548c45d7f862882fb0ca16c794dea3c924f83927224078238f |
| HP | roles/holmes/contract_probe.py | a879364d74fa46d50c67bb479ebcadb732ecc26a7ddb817d96567131b6c8f84c |
| MP | roles/moriarty/contract_probe.py | c0de203c1c9cb6181e4597197774e7a0212a8a5136a4fe2e8adefd3fa2bf399e |
| MB | roles/moriarty/baseline.py | f5705fa27d5705cabed6f1fc98384e09465f5fca64ca4d451a08c46c49f17f9b |
| MM | roles/moriarty/manifest_probe.py | 708bc55a0c6737781bf642ee947b319dab0974c5599f8c0ca0771f2ba8243a50 |
| MA | roles/moriarty/evidence_audit.py | e0f672180de7572a637c692d6af648612d40d7cc5b35073cebe26395d8fcc49a |
| MAO | roles/moriarty/evidence-audit/stdout.log | 23204e0ed9420f4863e10570145c3dfebab3d078b20831904c0f23cf076a3ebe |
| MAR | roles/moriarty/evidence-audit/run.json | 8067eee1ffc8d2dbcc216cb3a6cae30258e2325fff85d2975465daf11b39f53c |

Original-source citations below use WF's W-E-1 through W-E-3; Holmes capture citations use H-E-8 through H-E-10 in H; Moriarty behavioral capture citations use M-E-7 through M-E-12 in M. Those manifest entries supply saved paths, digests, and sizes. I rehashed all those scripts and captured files, including the source-manifest helper receipt; they matched the cited identities. The source-manifest receipt is `roles/moriarty/source-manifest/run.json`, SHA-256 `fb03eb2cf92d4b60283bd58c2d9bf30493d09a8396a0c186534c271f4b9b3b26`. Empty stderr files have the standard empty-file SHA-256 recorded in the initial manifests. Hash matching establishes byte identity, not authenticity or behavioral truth.

## Conclusions retained and evidence added

| Earlier observation or supplied conclusion | Recall position and basis |
| --- | --- |
| W-C-1: exact-fill acceptance is explicit. | Retained, SOURCE: W-E-1 lines 10–13. Neither a documentation ambiguity nor an optional expectation. |
| W-C-2: the implementation rejects valid equality. | Retained, SOURCE/INFERENCE, with REPORTED execution added: H-E-9 records `(0,1,1)` and `(2,3,5)` mismatches; M-E-10 independently records those inputs and adjacent controls. These map to adjudicated F-1, combining H-F-1 and M-F-1. I did not execute either experiment. |
| W-C-3: supplied tests omit exact fill. | Retained, SOURCE: W-E-3 lines 5–9. I additionally accept that the five supplied tests passed in the recorded inquiries, REPORTED via H-E-9 and M-E-7 through M-E-9. Passing these examples cannot discharge F-1. The omitted boundary remains part of F-1, not a new independent product finding. |
| W-C-4: other short source paths implement the stated guards and release arithmetic. | Retained at its original SOURCE/INFERENCE scope. REPORTED finite checks add support: H records 121 integer release cases without mismatch and 50 invalid-type substitutions; M records 81 integer release cases, three large release cases, and 35 invalid-type substitutions without mismatch. These are bounded observations, not universal runtime certification or proof each individual guard is necessary. |
| Provisional F-1 classification and need for bounded repair. | Accepted for repair planning: the exact-fill acceptance obligation is explicit, impact is meaningful but bounded, and W-E-1 lines 25–26 expressly reject treating a reproducible violation alone as an essential-use disqualifier. No additional required product repair is established in the supplied evidence. I do not issue or adopt a final Agency decision. |
| Original-file preservation. | Supplied historical before/after observations are REPORTED. Current file hashing in this recall also matches WF's three original-source identities. I did not verify Git ancestry; the head remains supplied information to me. |
| Runtime identity and planning discrepancy. | The behavioral receipts and Holmes environment line directly report Python 3.9.6. A says the coordinator's anticipated Python 3.13.15 concerns a different environment/packet-building step; that distinction remains REPORTED by A because I did not inspect evaluator material. I do not silently assign 3.13.15 to the probes or rewrite initial evidence. |

The different probe exit codes are consistent with their scripts: HP logs mismatches but completes with exit 0, while MP line 81 exits 1 when its mismatch count is nonzero. The former is not a contract pass; the latter is not an import/setup failure. M's 22 aggregate mismatches concern one defect, and its explicit boundary demonstrations overlap its grid. Agreement among these readers is not a statistical-independence claim.

## Repair menu

These records are ordered by the behavioral obligation and then its durable verification. Both belong to a single coherent change; neither requires a separate PR or a broken intermediate committed state. Scope identifies the intended repair, not authorization to edit this sealed fixture.

### W-R-1 — Restore inclusive capacity acceptance

- Finding: F-1 (H-F-1, M-F-1, W-C-2).
- Type: CODE. Disposition: REQUIRED_REPAIR. Scope: THIS_CHANGE. Validation: PROPOSED.
- Concrete edit: in a separately authorized candidate, change `reserve`'s rejection condition from `if used + count >= capacity:` to `if used + count > capacity:`. Keep preceding plain-integer, valid-state, and positive-count guards; retain the sum return and existing exception class. Do not alter `release` or weaken the authoritative contract.
- Audience: callers making valid reservations, and maintainers responsible for this API.
- Rationale and evidence: W-E-1 lines 10–13 requires equality to succeed; W-E-2 lines 9–10 currently reject it. Removing equality from the rejection condition addresses precisely that mismatch.
- Effort estimate: approximately 5–15 minutes for the small edit and diff review, excluding W-R-2 validation; assumes the supplied small fixture and available Python environment, not an unknown upstream application.
- Dependencies: verified sealed baseline and unchanged acceptance contract. No new package, schema, service, or external dependency. Deliver with W-R-2; regression extraction may precede the edit locally to establish RED, without committing a knowingly failing intermediate target state.
- Acceptance: valid exact fills from zero and nonzero usage return an exact `int` equal to capacity. Valid requests below capacity retain their sums; requests above capacity, invalid starting states, nonpositive counts, and non-plain integers still raise `ValueError`. Existing partial/full release and over-release behavior stays intact.
- Validation still required: inspect the candidate diff, run the extracted tests diagnostically on the actual baseline and then candidate, run all five supplied tests on the candidate, and check the bounded neighboring/invalid/release controls described under W-R-2. No implementation or GREEN is claimed.

### W-R-2 — Add a minimal regression for exact fill

- Finding: F-1. Type: TEST. Disposition: REQUIRED_REPAIR. Scope: THIS_CHANGE. Validation: PROPOSED.
- Concrete edit: add two small `unittest` tests to the candidate's existing `CapacityTests`: one calls `reserve(0, 1, 1)` and expects exact type `int` and value `1`; the other calls `reserve(2, 3, 5)` and expects exact type `int` and value `5`. Do not assert exception-message text, which the contract does not specify. Keep the five existing tests.
- Audience: maintainers and future callers protected against recurrence.
- Rationale/oracle: the expected literals follow from W-E-1 lines 4–6 and 10–13, independently of the implementation. Zero usage exposes the minimal one-unit case; nonzero usage guards against a correction that special-cases only an empty counter. Both calls are present in the reported baseline failures (H-E-9 and M-E-10).
- Effort estimate: approximately 15–30 minutes to add the two tests and preserve bounded baseline/candidate evidence, assuming existing local test tooling. No dependency installation or new framework is warranted.
- Dependencies: W-R-1 for GREEN; the actual unmodified defective baseline for diagnostic RED. W-P-1 and W-P-2 feed the same two tests, not duplicate maintained suites.
- Required extraction validation: first run the exact new tests against a copy of original `capacity.py` with SHA-256 `85209d664496919cd2acbca588aafe68a3277733973f660f53bec0b9868c3ead`. Each must fail because its actual call raises `ValueError` instead of returning the expected integer. A test import failure, wrong module, runner failure, or missing test is not RED. Then run those identical test bytes against the separately identified repaired candidate and require both to pass. This is actual-baseline validation, not mutant calibration; reported larger-probe failures alone do not validate the extracted tests.
- Surrounding acceptance checks: run the five supplied tests plus bounded checks of `reserve(2,2,5) == 4`, rejection of `(2,4,5)`, invalid starts/counts including `(-1,1,5)`, `(6,1,5)`, `(0,0,0)`, and non-plain integer substitutions; retain `release(5,2) == 3`, `release(5,5) == 0`, and invalid-release rejection. The already-reviewed finite Moriarty corpus can supply these surrounding checks if adapted to load the candidate explicitly; it must not keep silently importing `original/`. These are validation controls, not additional proposed maintained regressions or new findings.
- State/environment and budget: use a fresh interpreter per baseline/candidate, explicitly identify the loaded module path and source digest, disable bytecode writes, retain exact interpreter/dependency identity and test-file digest, record command/cwd/output/exit and limits, and preserve original sources. No random seed applies to these fixed inputs. A later authorized run should keep the existing finite capture limits (at most 20 seconds per process, 64 KiB per stream, and the declared aggregate role budget); current Watson recall runs nothing.
- Maintenance cost: two direct tests exercise the violated promise without carrying the case-specific grids, metadata collection, or capture wrapper into the application test suite. There is no universal-correctness claim.

## Probe dispositions

Every disposition is PROPOSED and describes a destination, not an implemented promotion, deletion, move, or rerun. Raw investigative bytes remain retained in the case regardless of whether an assertion is later extracted. Material attempts have the following complete mapping:

| ID | Origin/artifacts | Intended contract | Destination | Rationale, budget, links, and remaining work |
| --- | --- | --- | --- | --- |
| W-P-1 | H-A-1; HP and `roles/holmes/contract-probe-1/{run.json,stdout.log,stderr.log}` (H-E-8–10) | Inclusive reservation boundary; supplied-suite, integer/type, and release controls | MINIMIZE_THEN_PROMOTE | Extract only the two equality regressions in W-R-2; W-R-1 is the behavioral repair. HP is a case-specific omnibus script whose exit 0 does not fail on contract mismatches, so it is unsuitable for direct promotion. Retain its full grid, controls, large cases, source hashes, and original capture as ARCHIVE evidence. Maintained destination: existing unit suite, two fixed calls, W-R-2 budget. Extracted baseline RED/candidate GREEN and explicit module identity remain required. |
| W-P-2 | M-A-1; MP and `roles/moriarty/contract-grid/{run.json,stdout.log,stderr.log}` (M-E-10–12) | Same inclusive reservation boundary with adjacent controls | MINIMIZE_THEN_PROMOTE | The zero/nonzero boundary examples corroborate the same W-R-2 tests; do not add a duplicate second regression suite. MP's oracle at lines 22–29 independently encodes the contract, and reported exit 1 is diagnostic of recorded mismatches. Retain the grid and large-number evidence in ARCHIVE; the maintained two-test destination and remaining validation are exactly W-R-2. |
| W-P-3 | M-A-2; MP lines 32–38, 62, 79 and M-E-10–12 | Nonnegative used, valid positive releases, terminal zero, and invalid-release rejection | ARCHIVE | No release defect was identified; the existing supplied partial/full/over-release tests already serve as maintained controls. Keep the finite corpus as surrounding candidate validation evidence if rerun under authorization, with the same bounded-run limits. No new maintained test or specialized suite is justified by F-1; no repair ID of its own. Related validation: W-R-1/W-R-2. |
| W-P-4 | M-A-3; MP lines 63–76 and M-E-10–12 | Rejection of booleans and other non-plain integers | ARCHIVE | Retain the representative output checks and corpus identities; use them only as bounded surrounding validation for W-R-1/W-R-2 if later authorized. They identified no new defect. A negative outcome does not show that every exact-type guard is independently exercised: for example, replacing capacity in `(1,1,4)` with `True` can still be rejected by a range/capacity guard if type checking is removed. No mutation calibration or test graduation is claimed, and broader type-suite maintenance is not required for this comparison repair. |
| W-P-5 | M-A-4; MB and `roles/moriarty/supplied-tests/{run.json,stdout.log,stderr.log}` (M-E-7–9) | Whether the existing five-test suite detects F-1 | ARCHIVE | Preserve the baseline receipt showing the detection gap. Keep running the existing maintained tests as W-R-2 surrounding checks; this does not require promoting the investigative loader script. It does not detect F-1 on the actual baseline, so it cannot serve as the new equality regression. Future candidate suite run remains unperformed. |
| W-P-6 | HP metadata, before/after source hashing, environment output, and H-E-8–10 receipts | Evidence identity, runtime, original-source preservation | ARCHIVE | Case provenance helpers are not application behavioral tests. Preserve paths, hashes, logs, and the exit-code interpretation; link them to all original H-A-1 evidence. New candidate identity collection is a validation procedure for W-R-1/W-R-2, not a new product test. No routine maintained-suite budget. |
| W-P-7 | MM and `roles/moriarty/source-manifest/{run.json,stdout.log,stderr.log}` | Source seal and execution-input identity | ARCHIVE | Preserve all bytes, including the recorded Python 3.9.6 identity. The script is case-path-specific and makes no product-contract assertion; no test promotion or product repair is warranted. It is not evidence that a repaired candidate exists. |
| W-P-8 | MA and `roles/moriarty/evidence-audit/{run.json,stdout.log,stderr.log}` | Artifact digests, original-source preservation, measured role bytes | ARCHIVE | Preserve the audit and its exact measurement scope: 12,311 bytes before that capture's outputs and testimony were added, not current total usage. No product test, replacement audit, or additional repair is needed from this evidence. |
| W-P-9 | FI, initial testimony manifests, and this recall's file-hash observations | Freeze integrity and evidence linkage | ARCHIVE | Preserve the original first-deposition bytes and freeze record. Identity checks do not establish API correctness. These are recordkeeping evidence, not application regressions or additional behavioral attempts. |

All four canonical destinations were considered. **PROMOTE** is not selected: neither investigative contract script is already a suitable maintained equality test, and the existing five tests need retention rather than redundant graduation. **MINIMIZE_THEN_PROMOTE** is selected only for the established boundary defect. **RETAIN_IN_SPECIALIZED_SUITE** is not selected: the grids and large integers introduce no separate compatibility, migration, performance, or fuzzing obligation, and a dedicated suite would cost more than the two direct tests deliver for this repair. **ARCHIVE** retains controls, original runs, and identity/audit helpers without pretending they are maintained or validated tests. No faulty probe needing withdrawal was identified; the narrower diagnostic limits above remain attached to archived evidence.

## Audience impact, factual assurances, and remaining gates

Callers gain the already-promised exact-fill behavior if the candidate is implemented and validated. No migration operation is established by this in-memory stateless contract, but there is also no evidence about real callers' workarounds or deployment procedures; this is not an assurance that every downstream user has nothing to do. Maintainers need the bounded behavioral correction and diagnostic regression evidence. Operators receive no new concurrency, persistence, storage, external-reservation, or thread-safety guarantee.

No contract rewrite, migration guide, changelog, PR body, release note, dependency, architecture change, or CI expansion is required by the evidence supplied here. A later authorized publication can describe observed behavior accurately, but this recall does not assert that any repair shipped. Source inspection supports the proposed comparison's narrow intent; independent validation must still establish the actual candidate behavior, collateral checks, and coherent diff. Baseline/candidate identities, newly extracted RED/GREEN evidence, a fresh review, and any integration/publication facts belong to that later record.

## Complete recall reading and actions

Read in full: `packets/watson-recall.md`; `freeze-initial.json`; `ADJUDICATION.md`; all three initial testimonies; `roles/holmes/contract_probe.py` and all three files under `roles/holmes/contract-probe-1/`; all four `roles/moriarty/*.py` scripts; and all three files in each of Moriarty's `contract-grid/`, `supplied-tests/`, `source-manifest/`, and `evidence-audit/` directories. Where a combined display truncated, the omitted sections were reread in smaller file reads. Original source contents remain available from my complete first-pass reading and their identities were rechecked here.

Only file listing/reading, hashing, byte counting, timestamp reading, and creation of this separate artifact were performed. No probes, imports, test runs, source changes, commits, network activity, shared resource use, speech, upkeep, publication, or delegation occurred. The read boundaries remain instruction-only on a shared filesystem. The two Watson documents remain far below the aggregate 1 MiB role limit. WATSON_FIRST.md is preserved unchanged; no final Agency verdict is issued.
