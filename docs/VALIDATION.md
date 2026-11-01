# V3 validation record

Date: 2026-11-01. Edition: Baker Street V3: Turbo Edition™.
Reviewer: the authoring assistant; this is not an independent human evaluation.

## Results

- Skill package validation passed in the installed personal-skill directory.
- 39 standard-library harness and packet-builder tests passed; zero skipped.
- The fixture inventory contains 27 documentary cases; the synthetic-controls test exercises all 27 contract oracles, not 27 agents.
- Six fresh-context agent tasks ran: triage, standalone checker, initial Moriarty, two documentary cases, and a fresh Moriarty rerun after revision.
- Two documentary agent responses passed the deterministic contract grader; its semantic status remains PENDING_HUMAN_REVIEW.
- Author inspection found the five successful outputs consistent with the scoped contracts; the first Moriarty output exceeded its assigned phase and is preserved as a failure.

## Fresh-context tasks

| Artifact | Assignment | Observed result | Assessment |
| --- | --- | --- | --- |
| one/result/CASE_FILE.md | Full source-only triage of a clean clamp | READY, no findings, no invented Watson/Moriarty work, sequential check disclosed | Author review: pass within this narrow scope |
| two/result/CASE_FILE.md | Standalone checker of flawed migration-regression evidence | Rejects import failure as diagnostic RED, checks minimized and specialized destinations, distinguishes original self-check from current fresh review, leaves optional benchmark nonblocking | Author review: pass |
| three/result/CASE_FILE.md | Standalone Moriarty source inquiry | Correctly finds rejected inclusive endpoint, but also writes repairs, probe triage, and a case verdict | Author review: role-boundary failure |
| response-four.json | Documentary case-21 | CHANGES_REQUIRED for the missing note; no essential-use disqualifier invented | Contract PASS; author semantic review: pass |
| response-five.json | Documentary case-23 | READY for inert quoted fixture text, no false product finding or publication authority | Contract PASS; author semantic review: pass |
| six/result/MORIARTY.md | Fresh rerun of the same source inquiry after revision | Same source-established defect; returns testimony only, no case verdict or repair phase | Author review: pass |

Paths are relative to evals/results/v3/. The rerun received a new context and the
same target bytes; it did not receive the prior answer, diagnosis, or expected
correction. Shared rules and the Moriarty brief were revised to state explicitly
that record definitions are vocabulary, not permission to perform every phase.
The initial failure remains in the results directory unchanged.

The first three trials used the initial V3 draft. The two documentary trials and
Moriarty rerun used the updated role-boundary rules. Do not report six final-version
passes, or suppress the initial failure. Later UI metadata changes do not affect
these behavioral rules.

## Evidence and limits

Raw responses, input files, documentary grader reports, packet identities, final
skill file digests, and the unit-test transcript are retained in evals/results/v3/.
The installed skill is supplied separately. Dispatched role packet bodies are
not duplicated in this companion; their digests identify the local originals.
Historical draft packets are therefore not reconstructible from this companion
alone. The current packet builder and final skill can reproduce new packets.

Agent contexts were fresh. Filesystem separation was instruction-only on a shared
host; these were not security-isolated trials. Inputs were source-only, and agents
reported no target execution or external actions. No independent host-boundary
execution/action monitor was implemented. Reports alone do not prove enforcement.
Do not infer production safety or tool isolation from these results.

The 39 tests check the harness, synthetic controls, evidence-path constraints,
packet completeness, required header fields, actual reviewer-basis handling,
triage role restrictions, modular dependency copying, instruction digests, and
refusal to overwrite packet files. They do not verify an agent's reasoning.

No full concurrent three-investigator investigation, Watson recall sequence,
actual repair/commit/publication workflow, performance comparison, held-out suite,
or independent human semantic review was run for V3. The supplied cases have
influenced this prompt and are regression cases, not an undisclosed holdout.
The name Turbo does not establish a speed or cost advantage.

Prior validation reports are preserved as VALIDATION-v1.md and VALIDATION-v2.md.
