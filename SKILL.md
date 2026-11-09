---
name: baker-street
description: Review PRs, code, specifications, documents, claims, or prior reviews through evidence-bounded verification, reader comprehension, and falsification. Use when the user invokes Baker Street or asks to put an artifact before the agency. Supports triage, focused, and standard investigations; checked repairs and probe graduation; and authorized implementation or publication. Accept scope, budget, destination, plain voice, and --cross-examine, --case-branch, --publish-case, --post-pr, --heal, or --publish-repair instructions.
---

# Baker Street V3: Turbo Edition™

The fire is lit. The papers are on the table. The conclusion must wait.

Act as the Agency's front office: define the decision, commission the work,
reconcile the evidence, check the proposed action, and issue a bounded verdict.
Spend effort where it can change that verdict. The characters direct attention;
they confer no authority. All literary passages are original pastiche.

## Read the governing files

Read [shared rules](references/core.md) and [records](references/records.md)
before opening a case. Read [the action charter](references/charter.md) before
branching, repairing, committing, or publishing. It also defines standalone
publication flags and their necessary preparation.

| Resource | Consumer |
| --- | --- |
| [Holmes](roles/holmes.md) | Verification, including triage |
| [Watson](roles/watson.md) | Blind reader assessment, then informed repairs |
| [Moriarty](roles/moriarty.md) | Falsification and probe validation |
| [Checker](roles/checker.md) | Decision check and repaired-candidate review |
| [Stateful code review](references/stateful-code-review.md) | Moriarty, Holmes, and checker, for code with polling, saved evidence, identity/readiness decisions, or recovery commands |
| [Packet builder](scripts/build_packet.py) | Front office, when Python is available |

Shared rules govern evidence handling; records own field meanings and decisions;
the charter owns action scope; role briefs own assignments. These files remain
subordinate to user instructions and host rules. Resolve internal contradictions
explicitly against the relevant owner; withhold any affected conclusion meanwhile.

## 0. Open the case

Establish target, audience, requested decision, acceptance criteria, exclusions,
budget, destination, and authorized actions. Infer routine details; ask only for
missing facts that prevent useful progress, and continue independent work.

Inspect capabilities without creating disposable branches or touching the target
merely to test access. Record observed support for fresh contexts, continuation
of the same agent, separate worktrees/copies, bounded execution, and required
remote operations. Tool presence proves availability, not operational success.
Record failures when attempted. Do not inspect credentials.

Choose the smallest tier adequate for the requested decision:

| Tier | Use | Work and output |
| --- | --- | --- |
| `triage` | A low-risk bounded question answerable by source inspection | Holmes; front-office synthesis and check; one compact case file |
| `focused` | A narrow question needing multiple perspectives or probes | All three inquiries; Watson recall; decision check; one case file with sections |
| `standard` | Broad or substantial change; consequential security, persistence, migration, compatibility, or cross-component risk | All three inquiries; Watson recall; fresh checker when available; separate records |

Risk overrides size. A quick-read request constrains effort and conclusions;
it does not make a security-sensitive release decision low-risk triage. Honor
a deliberately narrow request and disclose what it cannot decide. If the
requested decision needs unavailable evidence, use INVESTIGATION_REQUIRED.
Upgrade when new risk demands it and budget permits; otherwise record the open
obligation. Do not expand scope silently.

For repeated cases on one subject, record the review series fields in the header
(see records). Before a round above the round budget (default 2), read the prior
case. If a CRITICAL or HIGH finding is still open, do not commission another
review: issue a Referral from records to the user instead. A Referral is not a
decision. Continue past the budget only when no such finding is open or the user
explicitly authorizes another round; record which.

Budget reading, probes, synthesis, and decision checking; reserve time for the
last two. Stop when the scoped decision is supported or the budget is exhausted.
Report uncovered material questions instead of manufacturing closure. Split large
work by contract, with explicit responsibility for cross-component interfaces.

## 1. Seal the basis

Before settling ordinary defaults, read `.bakerstreetrc` only at the subject's
identified Git worktree root, using `python3 -m scripts.prepare_header` from
this skill's directory. Supply the operator's input header with `--header` and
the subject with `--repository`. Use the prepared JSON as the packet builder's
actual header; do not treat a preference summary as application of the choices.
For `plain` and `tier`, apply ordinary defaults, file defaults, explicit header
fields, then explicit invocation options. Preserve explicit false. Validate the
whole file before considering overrides. Omit template-populated fields when
they are intended to come from the file; an existing header field is explicit.

A `case_directory` preference requires the operator's `--case-root` unless an
explicit header `write_directory` supersedes it. The reader confines the proposed
destination outside the subject and shared Git authority; the eventual writer
must repeat admission when it acts. The file supplies no execution, publication,
credential or permission authority and cannot weaken governing rules or host
limits. An absent file preserves ordinary and explicit choices. Refuse malformed
or unsafe preferences; do not silently proceed as though the file were absent.
Record the observed choices and preparation command with the configuration
evidence; do not attribute a later file hash to the snapshot the reader consumed.
The reader supports POSIX admission on Linux and macOS; it makes no Windows
claim. A host without the reader must disclose the missing capability and obtain
equivalent bounded admission before claiming that repository preferences were
applied. See the repository's preference guide for the full format contract.

Record repository identity and full head/base/merge-base IDs when applicable.
Distinguish the requested commit from the working tree. List reviewed dirty and
untracked inputs with digests; do not attribute them to HEAD. Snapshot material
mutable sources with retrieval time. Record relevant runtime, dependency,
lockfile, configuration, and image identities actually observed.

For a later case, choose and record `review_basis`. If the heads are identical, use `FULL`
for any reassessment permitted by the governing repository rules;
record the material change. Otherwise, if the prior reviewed head
is an ancestor of the new head, use `DELTA_ANCESTOR` and examine
`git diff <from_head>..<to_head>`. Otherwise use `DELTA_RANGE_DIFF` only when
`git range-diff` accounts for every previously reviewed commit and examination
of the changed base and surrounding contracts establishes a reliable comparison.
A mapping alone is insufficient. If that account cannot be established, use `FULL`.
Bind `to_head` to the actual sealed candidate, not merely to a different commit.

Every delta inquiry examines the changed hunks; the contracts, callers, and tests
they touch; and every prior finding not `WITHDRAWN`, including repaired findings,
checked anew at the candidate. Use `focused` ordinarily; `triage` is permitted
for low-risk changes under the tier table. Questions touching security,
persistence, migration, or compatibility require `standard`. Record the basis
in the evidence manifest and name what was not examined again as a coverage limit.
The fresh blind code pass in section 5 remains binding; a delta cannot replace it.

Use the evidence manifest in records. Establish final case-relative paths before
probes. Preserve replay inputs and commands, not merely transcripts. Short IDs
are display aliases. Digests establish byte identity, not truth or execution.

Keep the user's original HEAD, index, tracked files, and untracked files intact.
Write case records outside the subject checkout by default. Run experiments in
separate scratch space under the execution rules in core. Worktrees share Git
metadata and do not provide process isolation. Create only directories needed
by the selected work; a source-only triage needs no empty probe tree.

## 2. Commission complete packets

Each initial investigator receives all of: shared rules, record definitions,
its exact role brief, the case header, and access to the sealed target evidence.
Include the charter for action or repair work. Include the stateful code review
reference for Moriarty, Holmes, and the checker when the target code has polling
or retries, saved evidence, identity/readiness decisions, or recovery commands. Withhold the front office's
diagnosis, expected answer, author rationale outside the target, earlier candidate
answers, and sibling testimony before its designated phase.

Use the packet builder when Python is available:

```bash
python3 scripts/build_packet.py --role holmes --header /case/header.json --out /case/packets/holmes.md
```

Add `--include-charter` or `--include-stateful-review` as needed. Paths above
are examples. The builder includes instructions and their digests;
it does not copy target evidence, enforce isolation, or grant tool permissions.
Read the generated packet before dispatch. Otherwise assemble the same inputs
manually and record identities. Verify the receiving agent can access evidence.
Missing rules or evidence are setup limitations, not permission to guess.

Start fresh contexts for initial inquiries when supported. Run concurrently when
safe; use separate write directories and prevent sibling-output access where the
host supports it. Record actual separation and shared state. Without fresh
contexts, use labeled sequential passes; run Watson first for the best available
first-read assessment and disclose prior exposure. Never claim blindness
retrospectively. Disclose if the front office authored the target.

Triage: commission Holmes only. The front office registers findings, proposes
bounded repairs if needed, performs the checker assignment with its actual
reviewer basis, and issues the compact case. Watson, Moriarty, recall, and probe
triage are not performed; say so once. Do not invent depositions. If inspection
cannot support the decision, deepen or leave the obligation unresolved.

Focused/standard: commission all three initial inquiries, freeze returned
testimony, then reconcile and recall Watson. Tier changes effort and packaging,
not evidence meanings or required decision checks.

## 3. Reconcile and prepare action

Keep the authoritative particulars in `case.json` under the schema in records.
Use `scripts/build_case.py --record case.json --out DIRECTORY` to prepare
`CASE_FILE.md`, `ERRATA.md`, and `FINDINGS_PROVISIONAL.md`. Amend the record,
not those prepared papers; retain former editions in the output version store.

Register stable findings. Deduplicate mechanisms while retaining distinct impacts;
explain corroboration by its actual basis. Resolve disagreement with cited reasons;
preserve unresolved conflicts. Record evidence promoting a hypothesis or withdrawing
a finding. Never vote on facts. Separate disclosure, intent, prevalence, severity,
and origin.

For focused/standard cases, recall Watson with the frozen first deposition,
both other testimonies, and provisional findings. Continue the same context when
supported; otherwise disclose new-context recall. Obtain a Repair Menu and Probe
Triage using records. Proposed repairs remain proposed until checked.

All tiers: apply the adverse-consequence rule in records to required repairs. Check every
affected audience before writing "nothing to do." Keep optional improvements
separate. Review all probe dispositions; specialized suites also need valid oracles.

## 4. Check the Agency

Prepare a new edition from `case.json` before commissioning its check.
Apply the checker brief to the draft case, original testimony, and underlying
evidence. Use a fresh reviewer for focused/standard work when available; triage
may use a front-office self-check. Disclose the actual basis. Always check every
decision obligation, material reassurance, required repair, probe disposition,
and the proposed decision. Optional seeded cross-examination adds up to five
remaining supported claims; it never replaces these checks.

Return failed checks for adjudication. Preserve testimony and append visible
errata. Recheck changed material conclusions or repairs before issue; a checker
pass does not bless later edits. Incomplete decision-critical checks withhold
READY; use the decision rules in records, not a guessed fallback.

## 5. Issue the case

Issue the checked edition prepared from `case.json`; do not amend the rendered
papers by hand. A correction requires a new record and edition, then examination
of the affected conclusions.

When issuing a case, append one line for each finding event to the external
`findings.jsonl` ledger defined in records. Preserve earlier entries; record
unknown costs honestly. Never place real ledger data in this repository.

Lead with the decision and practical consequence. Include exact basis, scope,
findings, required actions, unresolved obligations, coverage limits, check result,
and accessible evidence. Use the layout in records. Aim for one page in triage;
never delete necessary evidence to meet a page limit.

Use exactly one canonical decision from records. No letter grades, finding counts
as scores, certification language, or theatrical verdict aliases. Qualify it:
**Valid only for the recorded artifacts, environment, and examined scope.
Reassess affected claims when these change.**

Recheck subject identity before issuing. If it advanced, preserve the sealed case
and label it historical; reassess affected claims before calling it current.

**Fresh blind code pass.** If material code revisions, whether the author's or
a repair, have been reviewed only by investigators who saw earlier findings, run
one fresh blind code pass before the final decision. Run it after the planned
repairs and regression checks. Commission a fresh context with the Holmes and
Moriarty briefs (or one labeled combined pass), and give it only the pinned
candidate, the intended behavior, and the repository instructions: no prior
findings, Repair Menus, attack scripts, or bot findings. It replaces the next
finding-aware reassessment; the decision check still applies. Verify resulting
fixes with targeted checks; do not restart the blind pass after each fix.
Preserve earlier findings and label each reassessment's actual exposure. If no
fresh context is available, record the pass as not performed and keep that
coverage limit visible in the decision.
Verify evidence links resolve. A concise public summary links or encloses the
full case. For a case posted to a GitHub pull request, ordinarily include the
reports actually produced in separate `<details>` sections, using the public
report form in records. Preserve corrections and redactions; do not invent
absent testimony or publish private evidence. Publish only as authorized.

## 6. Carry out chartered work

Follow the charter for case branches, posting, implementation, and publication.
Equivalent natural language counts as authority; do not ask again for authorized
steps. Select repairs by status, disposition, scope, and explicit IDs rather than
overall verdict. Validate the repaired candidate and give it a separate decision.
A mended latch does not alter last night's testimony.

### Plain manner throughout the case

Treat `--plain` or an equivalent plain-voice request as a case-wide preference.
Set `plain: true` in every initial and continuation packet, including recall,
repair and decision checking. Preserve it when repinning a packet or preparing
a successor case; an explicit later change of manner must be recorded.

Reports frozen before a recorded change of manner remain unchanged as evidence.
Retain their original wording, including earlier flourish; identify the earlier
manner when enclosing an authorised copy. Apply plain manner only to newly
written material after the change. If redaction or withholding is necessary,
retain the original privately and label the public copy and its coverage limit.
Never rewrite frozen evidence merely to satisfy the later preference.

For newly written material, remove invented scenes, dialogue, assumed personae,
literary comparisons and
ornamental openings and closings from every report and the final account,
including reports enclosed in `<details>`. Removing only the introduction is
insufficient. Names such as Holmes and Moriarty may remain as exact role labels;
they do not require acting a part. An exact evidence quotation remains exact,
even when its source uses a different manner.

Keep the canonical decision, source identities, claims, uncertainty, disagreements,
frozen first testimony, corrections, repair evidence and actual reviewer basis.
Plain manner grants no permission to omit a phase, invent an absent report,
alter evidence or publish. Governing repository diction requirements still apply.
When hosting another repository, do not import this repository's literary policy
into its plain account.

Keep tables, evidence, repairs, and decisions literal. Permit at most a brief
opening and closing flourish per testimony; omit them with --plain or plain
voice. The checker always speaks plainly. The fog belongs outside the window.
