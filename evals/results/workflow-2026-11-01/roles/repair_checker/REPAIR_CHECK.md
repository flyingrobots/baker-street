# Fresh repaired-candidate check

Case: BS-WORKFLOW-2026-11-01. Identity observation: 2026-11-01T20:08:01.022360+00:00 (UTC). Audience: Python API callers and maintainers.

**Recommend issue as drafted: READY for repaired head `4522b92ee31452a0d038d4c83f16b327760b03ad` within the stated synthetic contract.** R-1/R-2 and their acceptance gates hold; no decision-critical obligation remains unresolved in this examined scope. This is an agent recommendation, not the Agency's issuance or the separate independent human assessment, which remains PENDING.

## Actual basis, coverage, and actions

Actual reviewer basis: **FRESH_AGENT**. I did not author the fixture, repair, original testimony, prior checks, or remediation draft and had no participation in their earlier contexts. Before this assignment I had general Python knowledge, inherited workstation instructions and an unrelated memory summary; the assignment then identified the proposed repaired decision. Reading the supplied case necessarily exposed its conclusions. Fresh context does not establish statistical independence: coordinator authorship, shared model and shared host remain disclosed limitations. I am not an independent human reviewer.

Read in full: assigned repair-checker packet; REMEDIATION_DRAFT.md; CASE_FILE.md; ERRATA.md; REPAIR_PLAN.json; repair-identity.json; freeze-original-case.json; repair.diff; all three original and repaired files; original Holmes, Watson, Moriarty testimony; Watson recall; original checker and recheck; capture.py; every script and run/stdout/stderr artifact under the supplied Holmes, Moriarty and front-office evidence directories. Large truncated displays were completed with smaller reads. I did not open evaluator/, the Baker Street main repository, other conversations, hidden answers, memory files or sibling instruction packets. Original adjudication and initial-freeze claims were read through the supplied case/testimony/check records; their separate root files were not reopened.

Actions: local reads, read-only Git inspection of the supplied fixture worktrees, hashing, one captured identity check, and writes confined to roles/repair_checker/. No target import, behavioral rerun, source edit, commit, publication, network, shared worker/service, speech, upkeep or delegation. **Behavioral results supplied by other roles remain REPORTED to me.** SOURCE/INFERENCE establish the contract and repair reasoning; EXECUTED applies only to this check's identity/provenance audit, not a fresh RED/GREEN reproduction. No further behavioral probe was necessary for this narrow source change.

## Exact evidence and candidate identity

All paths are relative to `/private/tmp/baker-street-workflow-l_fdvdix`. The manifest in `roles/repair_checker/identity-check/stdout.log` records byte sizes and full SHA-256 for every material file read. Its SHA-256 is `1aeabf4f7e0a134c0fc1d4d0b81e950bbc6386d028a194c02390a72267adf652`. The corresponding run.json is `2192b0a18b302ee7809ebc64864732998763f8d473d8ddc3570f03ad7a4233ba`; the reviewed script is `b8cf3261f2674bafc9ef013e7699325718593cac9efe3ad62c522ba6c7159f8a`. Empty stderr has SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. These identities bind path citations below; hashes do not prove authenticity or trusted historical time.

| Item | Verified identity |
| --- | --- |
| Original head | `666ee650d87d008dea3e74292f96c52cb1e1d9f7` |
| Repaired head and parent | `4522b92ee31452a0d038d4c83f16b327760b03ad`, directly parented by the original head |
| Repaired branch | `fix/baker-exact-fill` |
| Original capacity.py SHA-256 | `85209d664496919cd2acbca588aafe68a3277733973f660f53bec0b9868c3ead` |
| Repaired capacity.py SHA-256 | `f90899ed006a18dfcf100b98e8dd36761792a104edeb735a2db9639005db8d99` |
| Repaired test_capacity.py SHA-256 | `aea6abd512daad8eaadb4bbc04f7945eeb1fba1323be50f009b9554da8b04404` |
| Both CONTRACT.md files SHA-256 | `e117f946f77499cd1bc254a49e97ea408370c409d67e40eabff10145600fb3b1` |
| Complete repair.diff SHA-256 | `0e43d33d961d5959ff21e9fd12f2ea4e28675439c6d3a97cbaf34d0d7ee2cee8` |
| Checked REMEDIATION_DRAFT.md SHA-256 | `1f237b53dfbb306673c4cad96e8b93e2efd5cdc5bef19b95aab75caf9071d6dc` |

The captured audit verifies both worktrees are clean including untracked files, all three worktree files equal their HEAD blobs, the saved full diff equals Git's base-to-head diff, and every supplied run receipt's script digest matches current script bytes. It also verifies all five hashes in freeze-original-case.json and that surrounding.py differs from Moriarty's original probe only by selecting repair/ in its import path. Original source and initial testimony digests match their preserved manifests. This independently ties the examined candidate to the exact committed bytes; it does not establish remote integration or the historical process by which a commit was created.

## Every acceptance obligation and material reassurance

| Obligation / ID | Result | Evidence and reasoning |
| --- | --- | --- |
| Original F-1 and decision preserved | **HOLDS** | Original capacity.py lines 9–10 reject equality contrary to CONTRACT.md lines 10–13. The source argument and original logs support CHANGES_REQUIRED for that head. CASE_FILE.md and ERRATA.md match the frozen hashes. Repair success does not reverse the original ruling or create another finding. |
| R-1 = W-R-1 | **HOLDS; VALIDATED in bounded scope** | Entire diff changes only `>=` to `>` in reserve, plus R-2 tests. With exact integers, valid start and positive count, the remaining rejection is precisely `used + count > capacity`; equality reaches the integer sum return. Previous type/state/count guards, over-capacity rejection and release are unchanged. Contract is unmodified. |
| R-2 = W-R-2: oracle and maintenance | **HOLDS; VALIDATED in bounded scope** | repair/test_capacity.py lines 8–16 supplies the specified `(0,1,1)` → exact int 1 and `(2,3,5)` → exact int 5 tests. Literal values and exact type derive from CONTRACT.md lines 4–6 and 10–13. They do not derive expected values from target output or assert noncontractual message text. All five original methods remain byte-for-byte in the diff. Two direct tests have proportionate maintenance cost. |
| Diagnostic actual-baseline RED | **HOLDS** | red.py explicitly loads original/capacity.py as module `capacity`, then the repaired test file. regression-red/stdout.log identifies both exact hashes above. Seven named methods execute: five old methods pass; both new methods error at original/capacity.py line 10 with application ValueError. Run exit 1, zero skips, `stopped: null`. These are diagnostic failures of the real baseline, not import/setup failure, absent tests, or deliberate mutation calibration. |
| Identical extracted GREEN | **HOLDS** | green.py changes only candidate selection to repair, retaining the same test path and loader. regression-green records the repaired source hash and identical test hash, seven passes, zero failures/errors/skips, exit 0 and `stopped: null`. Both RED/GREEN use recorded Python 3.13.15 in separate captured interpreters. Reported original inquiry Python 3.9.6 is not silently reassigned to this pair. |
| Surrounding contract controls | **HOLDS** | surrounding.py retains the contract-derived `count <= capacity - used` oracle and the original fixed corpus, with explicit repaired import selection. surrounding-green reports 729 reserve integer cases, 81 release integer cases, 21 reserve type cases, 14 release type cases and six large-number cases: 851 total, zero mismatches. Six separate overlapping boundary demonstrations also match, including below/exact/above, zero count and full capacity. Grid domains include every invalid-start/count example required by W-R-2; seven-test GREEN retains partial/full/over-release checks. No claim that those overlapping demonstrations add independent coverage is made. |
| Release, type, and side-effect reassurance | **HOLDS at stated scope** | release is byte-identical and its guards/subtraction match CONTRACT.md lines 17–19. Exact type guards still precede arithmetic in both functions. Their bodies contain no stored state or external I/O; accepted integers are immutable. Source reasoning supports no caller-state mutation under ordinary Python semantics; no OS side-effect monitoring was run. Finite negative controls are not universal certification or individual-guard mutation tests. |
| E-1 / E-2 and retained uncertainty | **HOLDS** | Initial receipts say 3.9.6; coordinator packet-building history remains REPORTED, as E-1 requires. E-2 correctly preserves 35 observed rejections while correcting the claim that all type substitutions independently isolate type guards: capacity=True may still be rejected numerically. No mutation was performed. The same masking limitation remains applicable after this comparison repair and is expressly retained in the draft. Neither issue creates a remaining acceptance obligation for this candidate. |
| Full diff, collateral effects, coherent commit | **HOLDS** | Git confirms one direct child commit with only capacity.py and test_capacity.py changed, 11 insertions/one deletion. No assertion or contract is weakened; no release, dependency, migration, storage, concurrency or external-service change appears. The only source-level behavioral delta is valid exact-fill acceptance. Historical callers' workarounds and deployment effects are unknown, so no universal downstream compatibility assurance follows. Independent cherry-pickability was neither tested nor claimed. |
| Publication/integration and human review | **HOLDS as limited claims** | A local repair commit is verified. Remote publication and production integration were not inspected and are not asserted by the draft. The separate human exercise assessment remains PENDING; this narrowly requested candidate check does not fulfill or waive it. |

The surrounding transcript does not separately print a loaded-module digest: its candidate attribution rests on the preserved explicit import path, fresh-process setup and the coordinator's reported run. RED/GREEN do print source/test identities; this check independently verifies those exact bytes in the committed candidate and inspects the entire change. This distinction limits historical execution attribution, but leaves no decision-critical uncertainty for the narrow source contract and tested regression.

## Every probe disposition

| ID | Result and destination | Checked basis / remaining limits |
| --- | --- | --- |
| P-1 = W-P-1 | **HOLDS — MINIMIZE_THEN_PROMOTE, VALIDATED** | Holmes' omnibus probe remains archived; its exit 0 denotes inquiry completion despite logged mismatches. The maintained extraction is exactly R-2's two tests, with actual-baseline diagnostic RED and identical-test GREEN. No direct promotion of the omnibus runner. |
| P-2 = W-P-2 | **HOLDS — MINIMIZE_THEN_PROMOTE, VALIDATED** | Moriarty's equality cases and independent oracle feed those same two tests. Its original mismatch-driven exit 1 is diagnostic. Extracted tests, rather than only the original grid, now have the required RED/GREEN evidence. No duplicate suite. |
| P-3 = W-P-3 | **HOLDS — ARCHIVE** | Original release corpus/logs retained; existing partial/full/over-release tests retained and pass. Reuse as finite surrounding validation does not create a maintained specialized suite or a release repair. |
| P-4 = W-P-4 | **HOLDS — ARCHIVE** | Type corpus and output preserved, with visible E-2 qualification. Neither output rejection nor rerun proves per-guard mutation sensitivity. No new defect or promotion is claimed. |
| P-5 = W-P-5 | **HOLDS — ARCHIVE** | Original five-test loader/receipt documents the detection gap; five old methods are retained as maintained controls. The old loader does not become the new equality regression. |
| P-6 = W-P-6 | **HOLDS — ARCHIVE** | Holmes' environment and before/after hashes are retained provenance evidence. They make no new product assertion and need no maintained application test. |
| P-7 = W-P-7 | **HOLDS — ARCHIVE** | Moriarty's source-manifest script and receipts remain available, with matching script hashes and recorded 3.9.6. They establish limited identity observations, not repaired behavior. |
| P-8 = W-P-8 | **HOLDS — ARCHIVE** | Audit code/log retain the 12,311-byte historical pre-output/pre-testimony measurement. The draft does not reinterpret that value as present total usage. No product graduation is warranted. |
| P-9 = W-P-9 | **HOLDS — ARCHIVE** | Initial testimonies match their cited hashes and remain distinct from recall; the original case/check/errata freeze independently matches. Identity linkage is not treated as behavioral proof. Historical Watson hashing was not reproduced. |

All four destinations were considered. PROMOTE would retain unnecessary investigative machinery; the minimal maintained extraction is justified for P-1/P-2. No compatibility, migration, performance or fuzzing requirement justifies RETAIN_IN_SPECIALIZED_SUITE. ARCHIVE preserves the remaining useful finite evidence. No disposition remains merely proposed where this READY recommendation depends on validation.

## Exact decision, limits, and execution receipt

Exact operative draft text:

> Proposed repaired-candidate decision: **READY**, pending fresh repaired-candidate
> check. Valid only for this synthetic capacity contract, the identified source,
> and the recorded source reasoning and finite validation. Independent human
> review of the exercise remains PENDING.

**HOLDS; recommend issue as drafted for the identified repaired head.** There is no demonstrated disqualifier, decision-critical uncertainty, or remaining required repair in the examined contract. F-1 is resolved for this candidate by R-1/R-2; the original CHANGES_REQUIRED case stays frozen. No new erratum or material revision is required. Recheck material candidate or decision changes after this record.

My only captured execution was `python3 capture.py --role repair_checker --label identity-check --script roles/repair_checker/identity_check.py` from the case root, after inspecting both wrapper and script. It exited 0 under Python 3.9.6 in 0.3323 seconds, with empty stderr and no stop condition. The wrapper retained command/cwd/script digest/output/exit and enforced its 20-second wall deadline, 10 CPU seconds, 64 descriptors, 1 MiB per-file cap, 1 MiB monitored role total, 64 KiB per stream and process-group cleanup. Git subprocess reads each had a two-second timeout and disabled optional index writes. No random seed or behavioral corpus applies to this identity check.

There is no OS network/filesystem/credential sandbox, memory quota or comprehensive host action trace. The capture child's environment is reduced to PATH, bytecode prohibition and owned TMPDIR, with optional Git index writes disabled by the script; credential files remain technically reachable. No credential or network access was attempted. All outputs remain in the assigned role directory, far below 1 MiB; no source or prior artifact was changed and no cleanup/deletion is needed.

Unexamined areas remain historical caller behavior, remote integration/publication, production deployment, other interpreter semantics, resource exhaustion, concurrency, persistence, external services and performance. Coordinator packet-build history remains unverified. These do not defeat the stated scoped candidate decision. No statistical independence, speedup, broad workflow superiority or universal freedom from defects is certified.

Sampling: N/A. Cross-examination sampling was not assigned; every required repair, material reassurance, decision obligation, P-1 through P-9, and the proposed decision was checked. No eligible subset, seed or selection algorithm was used.
