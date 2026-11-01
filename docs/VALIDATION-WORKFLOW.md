# Validation follow-up — 2026-11-01

The CI and installable-release work is complete. One bounded investigation and
repair workflow has been executed and preserved. **Independent human review is
PENDING**; James Ross volunteered to perform it. Agent checks do not satisfy
that gate. The [review entry point](../evals/results/workflow-2026-11-01/README.md)
links the small source, contract, diff, logs, verdicts, and human response form.

This report supplements [the historical V3 report](VALIDATION.md); it does not
rewrite its earlier observations or turn its untested items into blanket passes.

## Repository tests and CI

The suite now runs 46 tests with zero skips. The missing packet-builder path
raises a test error; two subprocess regressions confirm test discovery exits
nonzero for both the default skill path and an explicit BAKER_SKILL_DIR.
The packet-builder absence is no longer a successful nine-test skip.

[GitHub Actions run 41344147896](https://github.com/flyingrobots/baker-street/actions/runs/41344147896)
passed the suite on Python 3.10 and 3.13 at commit
`2c28ccc33a31f15b86108bf435e8eb3288ccd07e`. These are harness/package tests,
not a claim of agent effectiveness. The small workflow runs on main pushes,
pull requests, and manual dispatch, with read-only contents permission.

## Installation and release

[Installation instructions](INSTALL.md) give exact documented host routes and
explicitly identify unverified or unavailable integrations. The
[minimal example](../examples/triage/README.md) has a complete packet header;
its packet was actually built. The local installation snippet was exercised
with an isolated mocked home directory. No live API upload or every host UI
was tested.

The signed [v3.0.0 release](https://github.com/flyingrobots/baker-street/releases/tag/v3.0.0)
points to `2c28ccc33a31f15b86108bf435e8eb3288ccd07e`. Its ZIP is 61,180 bytes,
SHA-256 `9845c91183b50c3d655a7918d699884fbe243324a8d3714a6547bc9aba921eb3`.
Both assets were downloaded from the public release and matched the local
build; all 14 payload hashes in the internal manifest also matched. The ZIP
contains only explicitly selected skill, attribution, artwork, role, reference,
and packet-builder files plus that manifest. Evaluation answers and this
workflow evidence are excluded. The ordinary GitHub source archive remains the
full public repository, so install the named skill ZIP rather than that archive.

## Complete synthetic workflow

Case [BS-WORKFLOW-2026-11-01](../evals/results/workflow-2026-11-01/README.md)
uses one seeded inclusive-capacity defect in reserve and one correct release
function as a clean control. Three fresh investigator contexts identified the
supported defect without inventing a control defect. Watson's first testimony
was frozen before same-context recall. A fresh original checker required two
record corrections, which were retained as visible errata and rechecked before
the original CHANGES_REQUIRED verdict was issued.

The separate repair changes one comparison and adds two maintained regression
tests in one coherent signed commit. On the actual original source, both new
tests reach the application's erroneous ValueError while all five existing
tests pass. The identical test file runs seven passes on the repair. A finite
surrounding corpus of 851 grid/type/large-number cases reports no mismatches,
with six additional overlapping boundary demonstrations. A fresh repair checker
accepted the evidence and candidate; the separately issued repaired verdict is
READY within that synthetic contract. The original decision stays frozen.

All instructions, testimony, scripts, stdout/stderr, run receipts, drafts,
corrections, decisions, and source snapshots are retained. The verified Git
bundle preserves both actual fixture commits. The export manifest checks every
retained file. Raw investigator records were not rewritten for publication.
The [human review form](../evals/results/workflow-2026-11-01/HUMAN_REVIEW.md)
remains empty pending the reviewer's own assessment.

## Limits

The coordinator authored the fixture and knew its seed. Investigators were
instructed not to access the answer key; their shared host was not an OS sandbox.
The retained execution receipts do not provide a complete host action trace.
Fresh contexts share a model family and cannot establish statistical independence.
Exact model revision, sampling settings, and full per-role token costs were not
exposed in retained evidence. Initial probes ran Python 3.9.6; coordinator
RED/GREEN ran 3.13.15. An earlier packet-building runtime claim was explicitly
qualified as reported rather than independently captured.

Only finite, reviewed standard-library scripts ran; there were no heavy builds,
Docker workers, external application writes, or production integration. The
export is about 408 KiB, including about 26 KiB of stdout/stderr logs, within the
10 MiB case and 1 MiB log budgets. Capture deadlines and output limits are
recorded; no OS memory, credential, or network isolation is claimed.

One disclosed exercise does not establish general effectiveness, production
safety, comparative advantage, or speedup. Human review and broader controlled
replication remain distinct from the completed agent workflow.
