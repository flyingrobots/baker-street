# Baker Street V3: Turbo Edition™

**Code review with an evidence trail and a checked path to repair.**

> *From the notebooks of John H. Watson, M.D.*
>
> The gentleman who climbed our stair that evening carried a thick bundle of
> papers, and he laid it before Holmes with the air of a man surrendering a
> burden. "I want only your opinion, Mr. Holmes. Is it sound, or is it not?"
>
> Holmes did not touch the bundle. "You do not want my opinion, sir. An opinion
> you might have had from the porter, and very nearly as cheaply. You want a
> record: what was examined, upon what evidence each conclusion rests, what must
> be mended, and what I did not look at. You want something a stranger could
> take up a twelvemonth hence and check, line by line, without once taking my
> word for anything." He drew the lamp nearer. "That is what we provide here."

Baker Street is an agent skill that turns a review request into a **case file**:
a decision, the evidence supporting it, the changes required, and the limits of
what was checked. Give it a PR, source file, specification, or disputed claim.
Use it when you need to explain a merge decision, reproduce a suspected defect,
or establish that a fix addresses the original failure.

[Install the skill](docs/INSTALL.md) · [Browse a complete case](evals/results/workflow-2026-11-01/README.md)

## What you get

> I have seen Holmes's case files run to a single sheet and to a stout volume.
> But I never saw one that did not begin with its verdict. "The reader is a
> busy man, Watson," he once told me. "Give him the conclusion at once. Then
> give him the means to doubt it."

The main deliverable is `CASE_FILE.md`. Here is a condensed example from our
[recorded synthetic investigation](evals/results/workflow-2026-11-01/CASE_FILE.md):

```text
Decision: CHANGES_REQUIRED

F-1: reserve() rejects a valid request that exactly fills capacity.
     reserve(2, 3, 5) should return 5; it raises ValueError.

Evidence: The contract explicitly accepts equality. Source inspection
          and recorded probes confirm that the implementation rejects it.

R-1: Change the rejection comparison from >= to >.
R-2: Add exact-fill regressions from zero and nonzero usage; demonstrate
     that they fail on the original code and pass on the repair.

Limits: The release() control has no identified violation in the examined
        source and finite probes. Concurrency and external storage are excluded.
```

A small inquiry produces one compact case. Larger reviews also retain investigator
reports, source identities, probe scripts and results, and the decision check.
You can follow a finding back to its evidence and see what remains unresolved.

When you authorize implementation, the repair gets its own validation, commit, and
verdict. In this example, both new regressions failed on the original code and
all seven tests passed on the fix. The [repaired case](evals/results/workflow-2026-11-01/REMEDIATION.md)
received a scoped READY verdict; the original CHANGES_REQUIRED record remains.
The exercise's independent human review is pending and has no assigned reviewer.

## How it differs from a normal code review

> "There is nothing novel in our methods," Holmes remarked, filling his pipe from
> the toe of the Persian slipper. "Every careful investigator does these things
> when he remembers to. The difference is that here we are not permitted to
> forget."

Careful reviewers may already use these practices. Baker Street makes them
explicit parts of an agent review:

- **An inspectable basis.** Findings identify the reviewed revision and supporting
  evidence. Source reasoning, supplied reports, and probes actually run remain
  distinct, so you can challenge the conclusion without guessing its basis.
- **Different review passes.** Beyond triage, verification, reader comprehension,
  and attempts to falsify claims get separate attention. Watson's first reading is preserved
  before he sees the other investigators' findings and proposes repairs.
- **A check of the review itself.** A checker examines the decision, required
  repairs, and material assurances. Corrections stay visible alongside the
  original testimony. The case states whether this was a fresh review or a self-check.
- **Tests that demonstrate the defect.** New regressions must fail for the
  intended reason before their repaired pass counts. Actual-baseline failures
  and deliberate mutation checks are labeled separately. The case explains
  which investigative probes become maintained tests and which are archived.

The benefit is a review another person can audit and a repair whose validation
addresses the original finding. The extra investigation takes effort; choose
triage for a small source question. We have not established that Baker Street
finds more bugs or runs faster than a conventional review. “Turbo” is the edition
name, not a benchmark result.

> I asked Holmes once whether the name did not promise rather more than he could
> prove. "It promises nothing at all, Watson," said he. "It is a name. Had I
> called the agency the Swiftest in London, you might fairly hold me to it."

## Pick the inquiry you need

> "One does not summon the whole of Scotland Yard to find a mislaid umbrella,"
> Holmes said. "Nor does one send a single constable to a bank in Threadneedle
> Street because its broken lock is a small one. Fit the force to the danger,
> Watson. The size of the parcel tells you nothing."

| Tier | Suitable task | What happens |
| --- | --- | --- |
| triage | A small, low-risk source question | Holmes checks; the front office synthesizes and self-checks; one compact case |
| focused | A narrow question needing several perspectives or probes | Three inquiries, Watson recall, decision check; one case with labeled sections |
| standard | Broad change or consequential security, persistence, migration, compatibility, or interface risk | Three inquiries, recall, fresh checker when available; separate evidence records |

Risk overrides diff size. A two-line authentication change does not become
low-risk because it fits on a postcard. A quick-read request limits what the
agency can conclude; it does not grant a shortcut to a broad release assurance.

Repeated cases on one PR have a round budget, two by default. When a CRITICAL or
HIGH finding is still open after the budget, the agency sends you a Referral
instead of reviewing again.

## Who does what?

> Our household at that time was a small one, though crowded with opinion.
> Holmes weighed the evidence. I was set to read the papers as an ordinary man
> would read them, and to say plainly where I lost my way. And our old adversary,
> or someone very like him, was engaged to try every means of breaking the thing
> we were asked to trust. Behind us all sat a quiet clerk whose only duty was to
> doubt our conclusions before any client saw them.

| Role | Question | Boundary |
| --- | --- | --- |
| Holmes | What does the evidence establish? | Checks material claims against the artifact and its contracts |
| Watson, first pass | What will the intended reader understand? | Reads blind where possible; no probes or repair prescriptions |
| Moriarty | Under what conditions does it fail? | Seeks counterexamples and checks his own probes; zero findings is valid |
| Watson, recall | What should change, and how will we know? | Proposes bounded repairs and destinations for useful probes |
| Checker | Does our own conclusion hold? | Checks decision obligations, assurances, repairs, and every probe disposition |
| Front office | What decision follows? | Reconciles, preserves corrections, and issues the case |

Fresh contexts reduce direct anchoring. Shared models, sources, environments,
and oracles still permit shared errors. The case records the separation actually
achieved. When separate agents are unavailable, the passes are explicitly
sequential. Nobody earns an independence badge by changing hats.

## Use it

> The agency keeps no premises of its own. It lodges wherever it is received.
> Its host provides the lamp, the table, the writing paper and the locked
> cupboard. The agency brings only its methods, and it must say plainly which of
> these comforts it was in fact given.

Start with [installation instructions](docs/INSTALL.md), the
[v3.1.0 skill package](https://github.com/flyingrobots/baker-street/releases/tag/v3.1.0),
and the [minimal worked example](examples/triage/README.md).

This repository includes the complete skill and its development companion.
The skill entry point is [SKILL.md](SKILL.md) at the repository root. Install
or load that folder using your agent host's skill mechanism; keep `references/`,
`roles/`, `scripts/`, `agents/`, and `assets/` alongside `SKILL.md`.

The skill is a review protocol, not a standalone agent service. Your host supplies
the model, tools, fresh agent contexts, permissions, and storage. Python 3.10+
is needed only for the packet builder and evaluation harness.

```text
Use Baker Street to check this function's boundary claim. Triage, plain voice.
```

```text
Use Baker Street on this PR at the supplied full head and base IDs.
Focus on stored-data reads and public schema compatibility. Spend 20 minutes.
Save the case separately; do not edit the target or post comments.
```

```text
Use Baker Street on this previous case. Recheck every blocker and reassurance
against the underlying evidence. --cross-examine
```

```text
Heal R-2 and R-4 in a separate local branch, keeping their dependencies together.
Validate the candidate and give it a new verdict. Do not publish it.
```

These are instructions to an agent, not commands implemented by a service.
The host supplies tools, execution boundaries, and storage.

## Decisions with distinct meanings

> Holmes permitted the agency four verdicts, and he would hear of no fifth.
> "Not 'promising', Watson. Not 'very nearly sound', and above all not marks out
> of ten, as though we were judging the vegetable marrows at a parish show. Each
> verdict tells the client exactly what he must do next. A verdict that does not
> do so is mere decoration."

| Decision | Meaning |
| --- | --- |
| READY | No unresolved acceptance obligation within the examined scope |
| CHANGES_REQUIRED | Established findings need named, bounded repairs |
| INVESTIGATION_REQUIRED | Missing or conflicting decision-critical evidence prevents a responsible decision |
| BLOCKED | A demonstrated disqualifier prevents essential intended use or violates an explicit non-negotiable bar |

A missing required migration note is ordinarily CHANGES_REQUIRED. Unknown
migration integrity calls for INVESTIGATION_REQUIRED. Demonstrated destruction
of data the migration must preserve can justify BLOCKED. The intended-use
contract, not the dramatic possibilities, determines the classification.

READY is scoped. A test count is not a coverage proof. A supplied transcript is
not a run performed by the reviewer. Execution provenance and execution isolation
are different facts. An unsuccessful attack does not certify the target.

## Repairs and durable tests

> When the Agency's advice had been taken and the window latch replaced, Holmes
> would not hear of altering a single word of the earlier report. "It was true
> when it was written, and the new latch does not make it false. Write a fresh
> account of the fresh latch, Watson, and put the two side by side. And before
> you swear the new one holds, show me that the old one would have failed the
> same trial."

Useful probes have four possible destinations: PROMOTE, MINIMIZE_THEN_PROMOTE,
RETAIN_IN_SPECIALIZED_SUITE, and ARCHIVE. All receive a check. Maintained tests
need a contract-derived oracle, controlled state, diagnostic failure evidence,
and a justified maintenance cost. A proposed destination remains proposed until
validated; optional future work does not automatically block an unrelated decision.

Defective-baseline RED and deliberate-mutation calibration are labeled separately.
Failed imports never count as diagnostic RED. A repaired pass alone does not prove
the test detects the original defect. Code and tests may share a coherent commit;
independent cherry-picking is claimed only after checking the stated application.

The original testimony and verdict remain on record. Corrections use visible
errata. A repair gets its own identity, validation, and decision. Publication and
integration are separate events.

## Optional actions

> No client's instruction, however eager, empowers the agency to burn a letter,
> to force a lock that is not ours, or to rewrite another man's ledger. We may
> carry a sealed report to the door we are directed to. We may mend what we are
> asked to mend. Beyond that we do not go.

| Request | What it authorizes |
| --- | --- |
| --case-branch | Prepare and commit a separate local case branch |
| --publish-case | Prepare that branch if needed, then publish to the authorized destination |
| --post-pr | Post a concise decision comment to the identified PR; no implicit evidence push |
| --heal | Implement selected established repairs, verify, and commit locally |
| --publish-repair | Prepare and verify the candidate if needed, then publish the authorized companion PR or requested alternative |
| --plain | Remove literary flourishes without changing evidence standards |

Equivalent natural language has equal standing. Do not ask again for authority
already given. These flags do not authorize merge, force-push, unrelated deletion,
or rewriting the subject branch. The original checkout remains intact.

## Complete investigator packets

> Each of us received his instructions in a sealed envelope. It contained the
> whole of the rules, his own particular charge, and the particulars of the case.
> It did not contain Holmes's private suspicions, nor what any of the others had
> said. "A witness who has heard the other witnesses," Holmes observed, "is no
> longer a witness. He is a chorus."

V3 separates the front office, shared rules, record definitions, action charter,
and four role briefs. The packet builder assembles the rules, complete schemas,
role assignment, header, and instruction digests. It fails on missing required
header fields and refuses to overwrite a packet.

```bash
python3 scripts/build_packet.py --role holmes --header /path/to/header.json --out /path/to/packets/holmes.md
```

The header format is in `references/records.md`. Include the charter for action
or repair assignments (`--include-charter`). Add `--include-stateful-review` for
code with polling, saved evidence, identity or readiness decisions, or generated
recovery commands; `references/stateful-code-review.md` lists the required
attempts and the coverage matrix the case must carry. The builder neither copies target evidence nor enforces
access control, blindness, sandboxing, or authorization. Verify those separately.
Without Python, assemble the same packet manually.

## Test the Agency

> It was Holmes's practice, every so often, to set a false trail for his own
> agents and see who followed it. The trail might be a forged receipt, a
> confident falsehood, or a fault so well hidden that only the closest reading
> would find it. He kept the answers locked in his desk, where no agent could
> look before he had given his account. "A method that has never been tried
> against a trap," said he, "is only a habit with a good opinion of itself."

Python 3.10+; standard library only. No model API is built into the harness.
Run these commands from the repository root:

```bash
make test
python3 evals/run.py list
python3 evals/run.py prepare --case case-01 --out /tmp/baker-01 --skill-dir .
```

Without Make, run `python3 -m unittest discover -s tests -v`. Tests use the
skill in this repository by default; set `BAKER_SKILL_DIR` to test another
complete skill folder. Use a fresh output directory for each prepared packet.

Give a fresh agent only the prepared packet and its `TASK.md`. Keep oracle files,
catalog titles, prior answers, and evaluator notes outside its access. Save its
JSON response and grade from the evaluator's checkout:

```bash
python3 evals/run.py grade --case case-01 --response /tmp/response.json --packet /tmp/baker-01
```

The 27 documentary cases check evidence inflation, false positives, scoped
repairs, provenance, decisions, probe destinations, and authority. Deterministic
checks validate specified classifications and structural consistency. They leave
`semantic_status` as `PENDING_HUMAN_REVIEW`; correct labels beside unsupported
reasoning are not a pass. Packet-builder tests check assembly, not agent behavior.

Read [the evaluation protocol](docs/EVALUATION.md), [actual validation](docs/VALIDATION.md),
and [editor's notes](docs/EDITOR-NOTES.md). The historical validation report
distinguishes harness tests, fresh-context tasks, author review, limitations,
and observed failures. The [November 2026 follow-up](docs/VALIDATION-WORKFLOW.md)
adds CI, release verification, and a complete synthetic investigation with
repair evidence. Its independent human review is pending and has no assigned
reviewer; an author of Baker Street cannot perform it.

> The difficulty, as Holmes freely admitted, was that he had laid every one of
> those traps himself. "I know where each of them lies, Watson, and so, I fear,
> do my agents, after a fashion. What we want is a stranger's trap, and a
> stranger to judge us by it." He has been looking for such a stranger ever since.

## In preparation

> A correspondent from the provinces, who had employed the agency upon real
> affairs, wrote to tell us where our methods had cost him dear. Holmes read the
> letter twice, the second time with evident pleasure.

The round budget with referral to the user and the consequence floor for required
repairs are implemented on main. Still planned: delta reviews for follow-up cases,
a findings ledger, and named mutants run in a scratch copy. The field report and
remaining work are tracked in
[flyingrobots/baker-street#6](https://github.com/flyingrobots/baker-street/issues/6).

## Repository contents and history

| Path | Contents |
| --- | --- |
| `SKILL.md`, `references/`, `roles/` | V3 protocol, shared records, action charter, and investigator briefs |
| `scripts/`, `agents/`, `assets/` | Packet builder, release builder, host metadata, and artwork |
| `tests/` | Harness, packet-builder, and release tests |
| `examples/triage/` | Minimal source-only worked example and packet header |
| `evals/fixtures/`, `evals/catalog.json`, `evals/run.py` | 27 documentary cases and their preparation/grading tools |
| `evals/recorded-smoke/` | Preserved V1 and V2 trial records |
| `evals/results/v3/` | Preserved V3 responses, failures, reruns, digests, and test transcript |
| `evals/results/workflow-2026-11-01/` | Complete synthetic investigation, raw probes, checked repair, Git history bundle, and pending human review |
| `docs/` | Evaluation protocol, editor's notes, validation reports, and import provenance |

All supplied development and evaluation records are retained, including observed
failures. The original companion patch and the separately supplied validation
report were removed from the root in commit `b75b5dd`. [The import record](docs/IMPORT.md)
keeps the patch's digest and notes that the report is byte-identical to
`docs/VALIDATION.md`, which remains. The supplied package contained no Git
repository or earlier commits; it cannot reconstruct the original development
commit history or missing draft skill versions. The import record also gives the
exact preservation boundaries and the supplied icon's digest discrepancy.

## Provenance and contribution

This edition combines James's original Baker Street concept, its stated Wesley
SHA-lock HOLMES/BLADE lineage, the Editor's Editions, and Claude's modular rewrite.
It does not claim conformance to an independently inspected Wesley/BLADE standard.
The atmosphere draws on Sir Arthur Conan Doyle; the literary lines are original
pastiche, not attributed quotations. Use plain voice whenever the occasion calls
for a quieter room.

Contribute small artifacts with checkable contracts, clean controls, and explicit
limits. Measure missed defects, false findings, evidence inflation, repair quality,
decision quality, and cost separately. Preserve false alarms as useful evidence.

> "Bring me your small puzzles," Holmes said, as the last of the evening's
> visitors went down the stair. "Bring them with the answer sealed, so that I
> cannot see it. And when I am wrong, Watson, write it down in ink. A detective
> who keeps only his successes is keeping a scrapbook, not a record."

## License

Copyright 2026 James Ross and Baker Street contributors.

Licensed under the [Apache License, Version 2.0](LICENSE). See [NOTICE](NOTICE)
for attribution.
