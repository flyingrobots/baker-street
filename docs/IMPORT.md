# Repository import — 2026-11-01

This tree combines the supplied Baker Street V3 skill folder and its companion
repository patch. All 187 files added by the patch were imported. The original
patch and the separately supplied validation report remain at the root.

## Supplied history

The package contains V1 and V2 validation reports and recorded smoke trials,
V3 trial responses and reruns, instruction digests, fixtures, and the harness.
Original failures remain preserved alongside later corrections.

No `.git` directory, Git bundle, commit sequence, or full V1/V2 skill sources
were supplied. Earlier Git commits cannot be recovered from this patch: every
entry is a new-file addition to a snapshot. Historical draft role packets are
also incomplete, as described in [V3 validation](VALIDATION.md). This import
preserves all supplied history without claiming it is the complete original
development history.

## Preserved source identity

`baker-street-v3-repository.patch` SHA-256:

```text
d490d79ff1308c15a84f872678a20f546645e07241a4fa88989da2f5f376c24e
```

The separately supplied `baker-street-v3-VALIDATION.md` is byte-identical to
`docs/VALIDATION.md` from the patch. Both copies are retained.

Eleven of the twelve supplied skill files match the historical
[`final-skill-sha256.json`](../evals/results/v3/final-skill-sha256.json).
`assets/icon.svg` differs from its recorded digest. The supplied icon and the
historical manifest are both preserved unchanged; this import does not claim
the icon is the exact version recorded during the original validation.

## Repository integration changes

- Adapted the README to the combined root-level skill and development layout,
  with working command examples and explicit history limits.
- Made packet tests default to this repository's skill instead of a separate
  `skills/baker-street` folder, and updated the evaluation instructions.
- Added `.DS_Store` to `.gitignore`.
- Added the Apache 2.0 license and attribution notice at the owner's request.

The original patch retains the prior bytes of all modified companion files.
Skill instructions, the packet builder, fixtures, and historical evaluation
records were not modified during integration.

## Import validation

On Python 3.13.15, `make test` passed all 39 tests with zero skips. Preparing
`case-01` with `--skill-dir .` and verifying the resulting packet passed.
The packet included the modular skill instructions and excluded evaluator
answers, the catalog, and the original repository patch.

The [test transcript](../evals/results/repository-import/unit-tests.log) and
[check record](../evals/results/repository-import/checks.json) are separate
from the historical V3 evidence. These are harness and packaging checks;
no new model-agent evaluation or semantic review was performed.
