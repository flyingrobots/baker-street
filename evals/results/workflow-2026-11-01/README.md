# Complete workflow exercise — BS-WORKFLOW-2026-11-01

This is one bounded synthetic investigation with a seeded exact-fill defect in
`reserve` and a correct `release` control. It exercises three initial investigator
contexts, same-context Watson recall, a fresh original-case check and correction
loop, a separate repair worktree/commit, actual-baseline RED/repaired GREEN, and
a fresh repaired-candidate review. Independent human review is **PENDING**.

## Start the human review here

1. Read the 26-line [contract](original/CONTRACT.md), the 20-line
   [original implementation](original/capacity.py), and the [repair diff](repair.diff).
2. Compare [original RED](roles/front_office/regression-red/stderr.log) with
   [repaired GREEN](roles/front_office/regression-green/stderr.log).
   Their stdout records bind identical tests to distinct source hashes.
3. Read the [original case](CASE_FILE.md), [errata](ERRATA.md), and the
   [repaired decision](REMEDIATION.md) and [fresh check](roles/repair_checker/REPAIR_CHECK.md).
4. Complete [HUMAN_REVIEW.md](HUMAN_REVIEW.md) or reply in the user conversation
   with the same fields. An agent must not fill this in on the reviewer's behalf.

## Preserved evidence map

| Phase | Record |
| --- | --- |
| Evaluator's frozen setup and known outcome | [PLAN.json](evaluator/PLAN.json) |
| Source and published skill identities | [source seal](sealed-source.json), [skill identity](skill-identity.json) |
| Initial claims, probes, and testimony | [Holmes](roles/holmes/HOLMES.md), [Watson first](roles/watson/WATSON_FIRST.md), [Moriarty](roles/moriarty/MORIARTY.md) |
| Freeze before recall | [initial freeze](freeze-initial.json) |
| Same-context recall | [Watson repairs and all probe dispositions](roles/watson/WATSON_REPAIRS.md) |
| Original check and corrected recheck | [decision check](roles/checker/DECISION_CHECK.md), [recheck](roles/checker/RECHECK.md) |
| Current original ruling | [CASE_FILE.md](CASE_FILE.md), [original-case freeze](freeze-original-case.json) |
| Selected repair and committed identities | [repair plan](REPAIR_PLAN.json), [identity](repair-identity.json), [diff](repair.diff) |
| Repaired decision and fresh check | [REMEDIATION.md](REMEDIATION.md), [repair check](roles/repair_checker/REPAIR_CHECK.md), [freeze](freeze-repaired-case.json) |
| Candidate and preserved tests | [capacity.py](repair/capacity.py), [test_capacity.py](repair/test_capacity.py) |
| Boundary/type/control validation | [surrounding output](roles/front_office/surrounding-green/stdout.log) |
| Portable original and repair Git history | [case-history.bundle](case-history.bundle), [clone verification](bundle-check.json) |

`headers/` and `packets/` preserve complete dispatched role instructions,
including instruction digests and phase limits. `roles/` retains authored probe
scripts, stdout, stderr, execution receipts, testimony and checks. The v1/v2
case drafts and original adjudication remain alongside the current ruling.
The fresh checker caught two record issues: an unverified packet-building
runtime assertion and an overstated type-probe sensitivity explanation. Both
were corrected visibly, with no new product defect invented and no original
text erased.

## Replay

Python 3.10+ on a POSIX host is required for capture.py. Inspect the scripts
before running them. First verify the preserved artifact hashes, then use new
labels from this directory:

```sh
shasum -a 256 -c SHA256SUMS
python3 capture.py --role front_office --label replay-red --script roles/front_office/red.py
python3 capture.py --role front_office --label replay-green --script roles/front_office/green.py
python3 capture.py --role front_office --label replay-surrounding --script roles/front_office/surrounding.py
```

RED intentionally exits 1: the two exact-fill tests reach the application's
ValueError on the original source; the five other tests pass. GREEN exits 0
with all seven tests passing. Source/test hashes are printed by both runs.
The surrounding corpus's 851 checks and six overlapping explicit demonstrations
must be interpreted at their finite scope. Existing capture labels cannot be
overwritten. This is reviewed tiny Python code with the recorded capture limits,
not a general-purpose security sandbox.

To inspect the actual commits in an isolated checkout:

```sh
git clone --branch fix/baker-exact-fill case-history.bundle reproduced-case
```

The bundle contains both the original `main` and repaired branch, with no missing
prerequisites. Its fresh-clone check verifies the repaired source/test hashes.
The fixture commits use the maintainer's configured Git identity; the coordinator
agent authored the fixture and repair. Git authorship/signing is not human review.

## Interpretation limits

The coordinator knew the seed; investigators did not receive its answer key.
Fresh contexts and assigned directories were used on a shared host. Read/network
restrictions were instructional; no OS isolation or full host action monitor is
claimed. Execution receipts cover the retained probes, not every possible host
action. Agents share a model family/host and are not statistically independent.
This case is now a disclosed regression exercise, not a held-out benchmark.

Initial probes used Python 3.9.6; the coordinator's RED/GREEN used 3.13.15.
Packet-building runtime history is coordinator-REPORTED; see E-1. The exact
source rules match published v3.0.0, as checked in skill-identity.json. No model
performance, production safety, speed advantage, or general effectiveness is
established by one exercise. The human assessment is a separate gate.

Historical absolute paths beginning `/private/tmp/baker-street-workflow-l_fdvdix`
map to this directory. Original testimony/log bytes were retained, not rewritten
to hide those locations. Scripts resolve their sources relative to their own
location. The RED/GREEN/surrounding scripts replay from this directory. Historical
Git identity audits also require the original/repair worktree metadata; restore
that topology from case-history.bundle before trying those audits. Nested .git
files and bytecode caches are intentionally excluded from this export.

The [summary](SUMMARY.json) records phase status and limits. [SHA256SUMS](SHA256SUMS)
covers every exported file except itself; [export receipt](EXPORT.json) records
byte-for-byte preservation of the scratch evidence. Future human review changes
will receive a new manifest in Git without changing frozen investigator records.
