# Issued remediation — BS-WORKFLOW-2026-11-01

Issued repaired-candidate decision: **READY**, after fresh repaired-candidate
check. Valid only for this synthetic capacity contract, the identified source,
and the recorded source reasoning and finite validation. Independent human
review of the exercise remains PENDING.

## Identity and scope

- Original/upstream main head: `666ee650d87d008dea3e74292f96c52cb1e1d9f7`.
- Repaired head: `4522b92ee31452a0d038d4c83f16b327760b03ad` on `fix/baker-exact-fill`.
- Workspaces: original/ remains at the original head; repair/ is a separate Git
  worktree. Both have clean tracked state. Shared Git metadata is not a sandbox.
- Selected repairs: R-1 and R-2, from W-R-1/W-R-2, for F-1 only.
- One coherent commit contains the comparison correction and two tests; no
  failing intermediate commit was made. See repair.diff and repair-identity.json.
- Original contract and release function are unchanged. The five supplied test
  methods are retained. No dependency, migration, persistence, concurrency, or
  external resource feature was added.

## Actual-baseline RED and repaired GREEN

The identical test file SHA-256 `aea6abd512daad8eaadb4bbc04f7945eeb1fba1323be50f009b9554da8b04404` was loaded against
explicit source paths in separate captured Python 3.13.15 processes. The scripts
print loaded candidate identity and test identity; capture retains command,
working directory, script digest, exit, stdout/stderr, and limits.

| Phase | Candidate source | Result | Saved evidence |
| --- | --- | --- | --- |
| RED | original/capacity.py, SHA-256 85209d664496919cd2acbca588aafe68a3277733973f660f53bec0b9868c3ead | Seven tests run; five old pass; both new exact-fill tests error at the application's ValueError; exit 1 | roles/front_office/regression-red/ and red.py |
| GREEN | repair/capacity.py, SHA-256 f90899ed006a18dfcf100b98e8dd36761792a104edeb735a2db9639005db8d99 | All seven tests pass, zero skips; exit 0 | roles/front_office/regression-green/ and green.py |
| Surrounding | Same repaired source | 851 grid/type/large-number cases, zero mismatches, plus six explicit overlapping boundary demonstrations; exit 0 | roles/front_office/surrounding-green/ and surrounding.py |

RED is an actual defective-baseline reproduction, not a deliberate mutation or
an import/setup error: the traceback identifies reserve's capacity rejection,
while the five existing methods pass. The new methods cover exact fill from
zero and nonzero usage, requiring exact integer type and literal expected values.

The surrounding corpus preserves Moriarty's independent contract oracle and
case list; only its import path changes from original/ to repair/. Its finite
release cases remain a clean control, with no mismatches. Negative type results
remain output checks, not proof of each individual guard's mutation sensitivity;
ERRATA.md E-2 still applies. The baseline initial inquiries used Python 3.9.6;
this RED/GREEN pair uses one consistent 3.13.15 interpreter.

## Probe destinations and reassessment obligations

P-1/P-2: MINIMIZE_THEN_PROMOTE, now implemented as the same two maintained tests
in the repaired fixture, with diagnostic RED/GREEN for those exact test bytes.
Status is VALIDATED only for this bounded regression gate, following fresh
checking of the candidate and evidence. No duplicated suite.
P-3 through P-9: ARCHIVE; raw probes, original controls, identity helpers and
all earlier testimony remain intact. The broader grids are surrounding case
validation, not a newly maintained specialized test suite.

The original CASE_FILE.md remains CHANGES_REQUIRED; its freeze is unchanged.
A repaired READY recommendation does not retroactively change that ruling.
No live production integration or remote publication of the fixture branch is
claimed. This local synthetic repair is evidence for the workflow exercise.

## Controls and remaining limits

Same reviewed pure-Python fixture and capture.py limits: 20-second wall deadline,
10 CPU seconds, 1 MiB per-file and monitored per-role budget, 64 KiB per output
stream, process-group cleanup. No Docker or dependency builds. No OS network,
filesystem, credential, or memory sandbox; no full host action trace. Calls and
outputs are finite and small. Shared models/host can correlate errors.

The fresh repair checker inspected the entire diff, loaded source/test identities,
actual-baseline RED, GREEN, surrounding controls, R-1/R-2 and all P dispositions,
collateral effects and the proposed decision. The check held without required
revisions; see roles/repair_checker/REPAIR_CHECK.md. Human semantic review and general
production effectiveness remain separate; no superiority or speedup is claimed.

## Issuance

Front office issued this record at 2026-11-01T20:12:16.376855+00:00 after the fresh checker
held the preserved REMEDIATION_DRAFT.md. Only phase/status wording and this
issuance receipt differ from the checked draft. The checker independently
audited identity; the supplied behavioral executions remained REPORTED to that
checker. Human review of the complete exercise is still PENDING.
