# Baker Street V3: Turbo Edition™

**Evidence-led review. Checked repairs. A little fog outside the window.**

The fire is lit. Three readers have taken their places. One will inspect the
account, one will ask what its reader can understand, and one will try the
window to see whether it was ever locked.

None of them is entitled to be right.

Baker Street reviews code, pull requests, specifications, documents, claims,
and previous reviews. It preserves the evidence behind its findings, checks
its own proposed repairs, and gives a decision with explicit limits. With
permission, it turns useful probes into maintained tests, implements repairs,
and reassesses the repaired artifact without rewriting history.

Turbo means fewer unnecessary steps and better-defined handoffs. It is a name,
not a measured speedup or a claim that this method outperforms a single reviewer.

## Pick the inquiry you need

| Tier | Suitable task | What happens |
| --- | --- | --- |
| triage | A small, low-risk source question | Holmes checks; the front office synthesizes and self-checks; one compact case |
| focused | A narrow question needing several perspectives or probes | Three inquiries, Watson recall, decision check; one case with labeled sections |
| standard | Broad change or consequential security, persistence, migration, compatibility, or interface risk | Three inquiries, recall, fresh checker when available; separate evidence records |

Risk overrides diff size. A two-line authentication change does not become
low-risk because it fits on a postcard. A quick-read request limits what the
agency can conclude; it does not grant a shortcut to a broad release assurance.

## Who does what?

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

Start with [installation instructions](docs/INSTALL.md), the
[v3.0.0 skill package](https://github.com/flyingrobots/baker-street/releases/tag/v3.0.0),
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

V3 separates the front office, shared rules, record definitions, action charter,
and four role briefs. The packet builder assembles the rules, complete schemas,
role assignment, header, and instruction digests. It fails on missing required
header fields and refuses to overwrite a packet.

```bash
python3 scripts/build_packet.py --role holmes --header /path/to/header.json --out /path/to/packets/holmes.md
```

The header format is in `references/records.md`. Include the charter for action
or repair assignments. The builder neither copies target evidence nor enforces
access control, blindness, sandboxing, or authorization. Verify those separately.
Without Python, assemble the same packet manually.

## Test the Agency

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
repair evidence; its independent human review is pending.

## Repository contents and history

| Path | Contents |
| --- | --- |
| `SKILL.md`, `references/`, `roles/` | V3 protocol, shared records, action charter, and investigator briefs |
| `scripts/`, `agents/`, `assets/` | Packet builder, host metadata, and artwork |
| `tests/` | Harness and packet-builder tests |
| `examples/triage/` | Minimal source-only worked example and packet header |
| `evals/fixtures/`, `evals/catalog.json`, `evals/run.py` | 27 documentary cases and their preparation/grading tools |
| `evals/recorded-smoke/` | Preserved V1 and V2 trial records |
| `evals/results/v3/` | Preserved V3 responses, failures, reruns, digests, and test transcript |
| `evals/results/workflow-2026-11-01/` | Complete synthetic investigation, raw probes, checked repair, Git history bundle, and pending human review |
| `docs/` | Evaluation protocol, editor's notes, validation reports, and import provenance |
| `baker-street-v3-repository.patch` | Original companion package, retained unchanged |

All supplied development and evaluation records are retained, including observed
failures. The supplied package contained no Git repository or earlier commits;
it cannot reconstruct the original development commit history or missing draft
skill versions. See [the import record](docs/IMPORT.md) for exact preservation
boundaries and the supplied icon's digest discrepancy.

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

## License

Copyright 2026 James Ross and Baker Street contributors.

Licensed under the [Apache License, Version 2.0](LICENSE). See [NOTICE](NOTICE)
for attribution.
