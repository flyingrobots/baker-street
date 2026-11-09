# Records and decisions

Contents: [header](#case-header), [evidence](#evidence-manifest),
[claims](#claims), [findings](#findings), [attempts](#attempts),
[repairs](#repairs), [probes](#probe-dispositions), [checks](#decision-check),
[decisions](#decisions), [referrals](#referrals), [corrections](#errata-and-remediation),
[layouts](#layouts).

Use canonical enums below; prose may explain them. Global IDs are C-n, F-n,
A-n, R-n, P-n, E-n. Before reconciliation use role-prefixed IDs such as H-C-1
or M-A-1. Retain a mapping rather than renumbering original testimony. UNKNOWN
means unavailable; N/A means inapplicable, with a reason.

## Case header

Record case ID; timestamp with timezone; target; requested decision; audiences;
acceptance criteria including any non-negotiable intended-use bar; sealed basis;
dirty/untracked inputs; scope/exclusions; tier/reason; budget/stop condition;
capabilities; execution controls; actual separation; author overlap; authorized
actions/tools; evidence locations; assigned write directory; phase; plain-voice
preference; and actual reviewer basis for a checker.

For build_packet.py, provide JSON with nonempty case_id, target,
requested_decision, sealed_basis, scope, budget, authorized_actions,
authorized_tools, execution, write_directory, evidence_locations, capabilities,
separation, phase, audience, acceptance_criteria; tier is triage/focused/standard
and plain is boolean. Structured fields may be arrays/objects. Explicit UNKNOWN,
NONE, or N/A with a reason is preferable to omission. Checker packets also require
reviewer_basis. The header contains facts and limits, not diagnoses or answers.

Optional review series fields link repeated cases on one subject. Give
review_series, round, and prior_case together, or omit all three:

- review_series: a stable nonempty string naming the reviewed subject, such as
  github:owner/repo/pull/12. Use one fixed form for every case on that subject.
- round: an integer of 1 or more. Booleans are not integers.
- prior_case: NONE when round is 1; otherwise an object with nonempty case_id
  and reviewed_head: the full lowercase SHA-1 or SHA-256 ID that case reviewed.
- round_budget: optional integer of 1 or more; default 2. It requires the other
  three fields.

Optional `review_basis` is `FULL`, or an object with `method` equal to
`DELTA_ANCESTOR` or `DELTA_RANGE_DIFF`, and full lowercase commit IDs `from_head`
and `to_head`. A delta requires `round` above 1, `from_head` equal to
`prior_case.reviewed_head`, and different heads. The front office verifies that
`to_head` is the sealed candidate. Omission preserves the former packet format.

## Evidence manifest

Each material source: ID, locator, saved case-relative path, full object ID or
SHA-256, byte size, retrieval time for mutable sources. Record repository identity,
base/head/merge-base, reviewed dirty inputs, runtime/dependencies, lockfiles/config,
and actual image IDs. Map temporary paths and display aliases to saved artifacts.
Never invent hashes or observations.

Cite repository bytes as repo:path#Lstart-Lend@full-object-id; cite other evidence
by saved path and digest, directly or through its manifest entry. Executed probes
also identify command, working directory, inputs/oracle, stdout, stderr, exit,
seed/corpus, environment, limits, and cleanup. Retain larger data when needed to
support a claim. Digests do not prove truth, authenticity, or a trusted timestamp.

## Claims

Fields: ID; exact scoped proposition; asserting source; assessment; basis;
evidence; reasoning; limits. Split independently assessable compound propositions.
A count, an execution, coverage, and a behavioral guarantee are different claims.

| Assessment | Meaning |
| --- | --- |
| SUPPORTED | Evidence supports the precise scope stated |
| REFUTED | Evidence contradicts it |
| UNRESOLVED | Evidence is insufficient |
| CONTESTED | Cited disagreement remains unresolved |
| PLANNED | Honestly framed future work, not delivered behavior |

| Basis | Meaning |
| --- | --- |
| SOURCE | Inspection of artifact bytes |
| EXECUTED | Execution performed within this case, with preserved artifacts |
| REPORTED | An observation or execution supplied by another source |
| INFERENCE | Reasoning from identified evidence |
| NONE | No supporting evidence |

Multiple bases are allowed; NONE cannot accompany another basis. SOURCE inspection
of a transcript is not EXECUTED verification of its commands.

## Findings

Fields: ID; related claims/contracts; status; basis; evidence; impact as trigger
→ affected audience/state → consequence; severity/rationale; prevalence; origin;
intentionality; disclosure by audience; disposition; decision relevance; next
check. Decision relevance names the acceptance obligation or explains why the
finding does not prevent this scoped decision.

- Status: CONFIRMED / HYPOTHESIS / CONTESTED / WITHDRAWN.
- Severity: CRITICAL / HIGH / MODERATE / LOW / INFORMATIONAL / UNKNOWN.
- Origin: INTRODUCED / EXPOSED / PRE_EXISTING / UNKNOWN.
- Intentionality: YES / NO / UNKNOWN, based on stated intent, not mind-reading.
- Disclosure: DISCLOSED / UNDISCLOSED / UNKNOWN, naming the audience.
- Disposition: REQUIRED_REPAIR / INVESTIGATE / FOLLOW_UP / ACCEPTED.

CRITICAL means catastrophic compromise/loss; HIGH means serious integrity or
compatibility failure or loss of essential use; MODERATE means meaningful bounded
impairment; LOW means minor impairment; INFORMATIONAL means no identified adverse
consequence; UNKNOWN means consequences cannot yet be assessed. Uncertainty is
not low impact. A supported conditional impact can be described while its trigger
remains a hypothesis; state both separately.

Estimate prevalence only with evidence. Disclosure may fulfill a documentation
obligation without reducing impact. Prior existence, intent, and relative
performance multipliers do not mechanically determine severity. Judge severity
by impact if triggered, not by present likelihood; "latent" or "rare today" does
not lower it. Record likelihood as prevalence. Hypotheses cannot
justify defect-repair obligations until established; investigation may be required.
Risk acceptance needs an explicit basis, not a preference to finish. Withdrawn
findings retain no active obligation.

Adverse consequence: a finding can be REQUIRED_REPAIR only when its status is
CONFIRMED and its impact chain names at least one of (a) a violation of a
recorded contract or acceptance criterion, (b) a named audience that would take
a wrong action because of it, or (c) a loss of integrity, security,
compatibility or essential intended use. A CONFIRMED CRITICAL or HIGH finding
whose impact chain supports its severity meets (c). An INFORMATIONAL finding has
no identified adverse consequence, so it cannot be REQUIRED_REPAIR. A CONFIRMED
finding that fails this rule is FOLLOW_UP by default, and any proposed repairs
have scope FOLLOW_UP; it may instead be ACCEPTED with an explicit basis.
A user acceptance required by repository rules or severity precedence must still
come from the user.
The exception is a finding of UNKNOWN severity whose consequence bears on the
requested decision: it is INVESTIGATE until that consequence is assessed.
Unconfirmed findings keep their existing dispositions: HYPOTHESIS or CONTESTED
may need INVESTIGATE; WITHDRAWN is ACCEPTED with no active repair. This rule
applies to every finding type, not to prose alone.

## Attempts

Fields: ID; hypothesis; attacked contract; method/setup/inputs/oracle/control;
outcome; finding IDs; artifacts; limits. Outcomes:
CONFIRMED_FINDING / NOT_REPRODUCED / INCONCLUSIVE / BLOCKED / NOT_ATTEMPTED.
BLOCKED here is an attempt outcome, not the case decision. A failed import is
BLOCKED; a proposed experiment is NOT_ATTEMPTED; a negative result applies only
to that method and conditions. Errata correct faulty probes without erasure.

## Repairs

Fields: ID; finding IDs; type; concrete edit; audience; rationale; effort range
and assumptions; disposition; scope; dependencies; acceptance check; validation.
Types: DOC / CHANGELOG / PR_BODY / TEST / CODE / CI. Dispositions are the finding
dispositions above. Scope is THIS_CHANGE or FOLLOW_UP; scope is not authorization.
Validation is PROPOSED or VALIDATED, with basis/limits. Validated wording does not
imply implementation, integration, or execution.

Order by impact and decision necessity, then yield per effort. Do not require
cosmetic preferences; they fail the adverse-consequence rule in Findings. Keep wider improvements separate. Check new factual claims
in replacement text, especially assurances that an audience has nothing to do.

## Probe dispositions

Fields: ID; originating attempt/artifacts; intended contract; disposition;
rationale; proposed suite/budget; linked repairs; validation and remaining work.

| Value | Destination |
| --- | --- |
| PROMOTE | A maintained test already expressing the intended contract |
| MINIMIZE_THEN_PROMOTE | A minimal regression extracted from a larger experiment |
| RETAIN_IN_SPECIALIZED_SUITE | Dedicated compatibility, migration, property, fuzz, or performance coverage |
| ARCHIVE | Investigative evidence, including corrected faulty probes |

Check all four decisions. For every maintained-test destination, verify the oracle
follows from the contract independently of implementation; distinguish setup from
diagnostic failure; control state/environment; preserve fixtures/seeds/dependency
identities; justify maintenance cost. Demonstrate detection of the intended defect
or a deliberate mutation before declaring a test validated. Label mutation
calibration separately from historical reproduction. Validate an extracted test,
not merely its original probe. Benchmarks need absolute measurements, workload,
repetitions, variance, and a justified threshold. A destination can stay PROPOSED
pending this work; it blocks release only when the requested decision depends on
it. A faulty probe is archived and cannot establish a product regression.

## Decision check

Fields: actual reviewer basis (FRESH_AGENT or SEQUENTIAL_SELF_CHECK); prior
exposure/author overlap; checked IDs; per-ID HOLDS/FAILS/UNRESOLVED with evidence;
new claims in repairs; incomplete checks/decision relevance; exact draft decision;
recommendation; sampled eligible IDs, seed, algorithm, and selected IDs if used.
Recheck material edits made after the check.

Always examine every decision obligation (including material uncertainty),
material reassurance, required repair, probe disposition, and the decision.
Optional sampling adds up to five remaining SUPPORTED claims. Prefer a deterministic
method: sort eligible IDs by SHA-256 of UTF-8 seed + newline + ID, break ties by ID,
and take the first five or all if fewer. Record the actual method and inputs.

## Decisions

| Decision | Meaning and example |
| --- | --- |
| READY | No unresolved acceptance obligation within agreed, examined scope; a checked narrow claim can be ready while broader areas remain excluded |
| CHANGES_REQUIRED | Established findings require named bounded repairs; e.g. a required migration note is missing |
| INVESTIGATION_REQUIRED | Missing or conflicting decision-critical evidence prevents a responsible decision; e.g. whether migration preserves records remains unresolved |
| BLOCKED | A demonstrated disqualifier prevents essential intended use or violates an explicit non-negotiable bar; e.g. migration reproducibly destroys required data |

Apply BLOCKED for an established disqualifier; otherwise INVESTIGATION_REQUIRED
for decision-critical uncertainty; otherwise CHANGES_REQUIRED for established
required repairs; otherwise READY. Explain the contract making a defect
disqualifying. Routine acceptance failure is not automatically BLOCKED; a blocked
tool is not a product disqualifier. A BLOCKED defect can be repairable. List all
remaining obligations regardless of precedence. Optional follow-ups below HIGH
severity or irrelevant uncertainty do not prevent scoped READY; missing critical checks do.

Severity precedence: a finding is open unless WITHDRAWN. An open CRITICAL or HIGH
finding prevents READY, whatever its disposition, including FOLLOW_UP, INVESTIGATE,
and ACCEPTED. An open CRITICAL finding that prevents essential intended use or
violates a non-negotiable bar is a disqualifier: BLOCKED. The one exception is an
ACCEPTED HIGH finding with a recorded, explicit user acceptance and its basis;
the decision statement names that finding and acceptance. Reviewers cannot supply
that acceptance, and no acceptance permits READY with an open CRITICAL finding. No letter
grades, votes, or universal certifications.

Material missing coverage stays visible in the decision statement, whatever else
holds. Every non-READY decision names the exact, minimal set of repair IDs (and investigation
obligations) whose completion would make it READY, each tied to its finding IDs,
so the case states the path to READY in one place. Judge each round against the
recorded acceptance criteria and these rules, never relative to a prior round.
A delta basis narrows what the case examines; it does not change the standard of judgment.
Do not repeat reviews to reach a target decision. A decision does not replace the
repository's own review or publishing authorization.

Round budget: before a case opens with round above round_budget, read the prior
case. If any CRITICAL or HIGH finding is open (not WITHDRAWN), commission no
investigators and issue a Referral. If none is open, the round may continue; the
case records that it exceeded the budget and why. An explicit user authorization
for another round also permits it; record that authorization.

## Referrals

A Referral returns a stalled series to the user. It is not a decision: the prior
case's decision stays current, and no decision value is added. Fields: series;
case IDs of the rounds examined; each open CRITICAL or HIGH finding ID with the
round where it first appeared; pattern; question for the user; what the Agency
will do after each answer. Patterns classify only the open CRITICAL and HIGH
findings.

| Pattern | Meaning | Question for the user |
| --- | --- | --- |
| PERSISTENT | An open finding was raised in an earlier round and stayed open after at least one repair | Accept it under the ACCEPTED HIGH rule, dispute it with evidence, or change the repair approach |
| RECURRENT | Every open finding is new in the latest round, and an earlier round also had a different CRITICAL or HIGH finding | Rescope or split the change |
| NEW | Every open finding is new in the latest round, and no earlier round had a CRITICAL or HIGH finding | Authorize one more round to repair it, or rescope the change |
| MIXED | More than one pattern applies to different findings | Ask each applicable question, per finding |

A CRITICAL finding cannot be accepted into READY; for it, only dispute or a
changed repair approach applies.

## Errata and remediation

Errata are append-only: ID, timestamp, original assertion, correction, reason,
evidence, affected decisions. Add visible pointers in rendered wrappers; leave
original testimony unchanged. A correction may supersede an old ruling; retain
both and identify the current one.

Each repair run gets a separate record: original/repaired/upstream heads; selected
repair IDs; dependencies/commit map; RED/GREEN identities/results; surrounding
checks; probe graduations; reviewer basis; remaining issues; new decision for the
repaired head. Publication and integration are separate facts. A fixed artifact
does not retroactively make the original verdict wrong.

## Layouts

Triage/focused: one CASE_FILE.md with header/manifest, inquiries actually performed,
findings/adjudication, repairs/probes if any, decision check, errata, decision/next
action, and limits. State omissions briefly; no empty companion files or imaginary
witnesses. Preserve any blind Watson deposition verbatim before recall. Keep raw
replay artifacts separate when needed.

Standard: CASE_FILE.md, HOLMES.md, WATSON_FIRST.md, MORIARTY.md,
WATSON_REPAIRS.md, DECISION_CHECK.md, ERRATA.md, MANIFEST.md, relevant
evidence/<role>/ files. Honor explicit multi-file requests in other tiers.
Summaries preserve uncertainty and link evidence. Testimony does not substitute
for evidence. Keep the executive finding to three sentences; avoid repeating
whole Repair Menus in public comments.

In every tier, list the repairs of FOLLOW_UP findings under a "Batched follow-ups"
heading in CASE_FILE.md so they stay in view. A batched follow-up whose finding is
not CRITICAL or HIGH does not change the decision. Severity precedence still applies: an open
CRITICAL or HIGH finding prevents READY whatever its disposition, so the path to
READY names its repair, or for a HIGH finding its recorded user acceptance. When
the user authorizes a repair on the same series, the repair may include them.

In every tier, when stateful code review applies, CASE_FILE.md includes its
coverage matrix (see references/stateful-code-review.md).

## Mutants

Give each deliberate fault a stable descriptive name, such as
`reserve-rejects-exact-fill`: lowercase words joined by hyphens. Within one
review series, the same name must identify the same patch SHA-256; a different
patch requires another name. The reviewer compares the case records to enforce
this rule; the runner does not consult the findings ledger.

A mutant JSON record contains `name`, `base_head` (full lowercase commit ID),
`patch` (an object with case-relative `path` and `sha256`), `command` (an argument
list including the intended filter), and `expected_red` (the contract violation
which the trial must report). The JSON file's directory is the case directory.

`scripts/run_mutant.py --repo PATH --mutant RECORD.json --out DIRECTORY
--timeout SECONDS` exports tracked files at `base_head` with `git archive`,
uses a case-owned bare Git authority with read-only object-store alternates,
unsets export-ignore/export-subst and text/eol/filter/ident attributes,
disables automatic line conversion, applies the verified patch bytes
with an explicit work-tree through `git apply`, and runs the command in the
fair copy. An existing nonempty output is refused without writes. Output within
the source checkout or shared Git authority, including resolved symlink aliases,
is refused. Archive links and unsafe paths are unsupported and give BLOCKED.
The per-file output allowance is 128 MiB; extracted source also has a 128 MiB
allowance. The host must account for aggregate concurrent stores and logs.

`result.json` records `name`, `patch_sha256`, `base_head`, `command`, `exit_code`,
relative stdout/stderr paths, `elapsed_seconds`, and `outcome`. PASSED means the
patched command exited zero; FAILED means it started and exited nonzero. BLOCKED
means export, digest, patch, command startup, or timeout prevented a completed
trial; `reason` explains the obstacle. Refused arguments produce exit 2 before
output; a recorded BLOCKED result also exits 2. PASSED and FAILED exit 0 from
the runner; consult the recorded outcome, not the runner's exit alone.

Only the reviewer may record KILLED, after the failure output is checked against
`expected_red`. A failed import alone is not diagnostic RED. Retain the result,
patch, command output and source identity with the case.

The runner's own writes remain in the output directory; the supplied command
is arbitrary code and a fair copy is not a sandbox. A command can deliberately
write through absolute paths, create files elsewhere, or detach from its process
group. Such commands require host-enforced isolation protecting the source,
credentials, network and storage. The POSIX runner kills its process group on
timeout and completion; descendants which remain in that group cannot continue.
No claim is made about descendants which deliberately establish a new session.
Docker is optional host provision, not a requirement of the protocol.

## The authoritative case record

Keep `case.json` outside the subject checkout. Its required fields are `header`
(an object containing nonempty `case_id` and the case particulars above),
`findings` (objects with unique `id`, `mechanism`, `severity`, `status`, `basis`
as a list of evidence enums, `sources` as locator strings, and `disposition`),
`errata`, `rulings`, `path_to_ready`, `followups`, `probe_triage`, `coverage_matrix`,
and `decision`. Empty collections are lists. `notes` is optional, and every
entry object admits its own `notes`. Record HIGH acceptance under a finding's
`user_acceptance` as the explicit human decision and its basis; the builder
cannot authenticate the person or judge the truth of that evidence.

`path_to_ready` names finding IDs. A supplied nonempty `followups` list must
agree with the IDs derived from active FOLLOW_UP findings; an empty list requests
derivation. Counts include all recorded findings by severity. The “why READY
is withheld” list is derived from active critical/high, required-repair, and
investigation obligations, retaining the explicit HIGH user-acceptance exception.
The builder refuses a READY decision with any such unresolved obligation.
It checks structural consistency; it does not replace consequence judgment,
testimony, a checker, or the complete decision rules.

`scripts/build_case.py --record case.json --out DIRECTORY` prepares the three
case papers with a SHA-256 of canonical UTF-8 JSON (sorted keys, compact separators,
no NaN). Repeating unchanged input verifies the papers and makes no writes.
Changed input produces another immutable `versions/<digest>/` edition, including
its input record; the former edition remains. The current root papers are replaced
only after preparation, and `manifest.json` is the last receipt. The receipt
binds current file hashes and the edition chain. Hand amendments, missing papers,
and unknown pre-existing output are refused. An interrupted multi-file replacement
is detectable and refused on retry; retain the last complete edition for recovery.
These files are evidence, not a claim of filesystem transaction isolation.

Append errata to the input record; never erase earlier testimony. The renderer
retains prior input editions, but the author and checker still judge whether a
new correction faithfully preserves and supersedes the original assertions.

The packet header schema is the Case header section above. Obtain its complete
field form with `scripts/build_packet.py --print-header-template`; replace all
`REPLACE` values with the recorded facts before assignment. The form has a
structured `sealed_basis.head`. `--repin FULL_HEAD --out DIRECTORY` writes
`<role>-<first-12-head-digits>.md` beneath that directory, records full identities
and packet digests in `manifest.json`, and marks older packets of that role
SUPERSEDED. It changes the copied header's head (and delta `to_head`, if present),
not the supplied header file. It refuses an existing packet name, including a
short-prefix collision, and preserves prior packet bytes. No Git object existence,
access control, or target evidence export is inferred from packet preparation.

## Findings ledger

Keep `findings.jsonl` in the user's case store, outside the subject checkout.
Append one JSON object per finding event. Never edit or delete an earlier entry;
record a correction in a later line. Never include finding text, source code,
or private document contents. Real books remain held-out evaluation material.

For a standalone case without review series fields, use `series` equal to
`case:` followed by the exact `case_id`, and use `round` 1. This is a ledger
projection only: do not require new series fields in the case or alter the
packet header. A later linked series uses its recorded series identity; do not
silently join earlier standalone entries.

Required fields: `series` (the header's `review_series`, or the standalone mapping), `case_id`, `round`,
`reviewed_head` (full lowercase commit ID, or `N/A` with `reviewed_head_reason`),
`tier`, `finding_id`, `raised_by`, `event`, `severity`, `status`, `disposition`,
`recorded_at` (ISO 8601 with timezone), and `cost`. Use the existing severity,
status and disposition enums. `tier` is triage/focused/standard; `raised_by` is
holmes/watson/moriarty/checker/front_office/blind_pass and remains fixed for a
finding. `event` is RAISED/CHANGED/REPAIRED/WITHDRAWN. Cost has `elapsed_seconds`
and `tokens`, each a nonnegative integer or `UNKNOWN`. Unknown fields are refused.

`scripts/ledger.py summarize --ledger PATH [--json]` reads without alteration.
The latest physical line for each `(series, finding_id)` supplies its state,
severity and current round. `raised` counts all distinct findings, including
those later withdrawn. `confirmed`, `withdrawn` and `repaired` are exclusive
subsets: withdrawal takes precedence, then repair, then confirmed status.
An unconfirmed finding belongs to none of those three subsets. Their sum need
not equal `raised`. The per-role and per-round tables describe latest states;
`discovery_by_round` separately counts the first recorded round. A ledger may
begin with an already known finding, so first recorded does not prove discovery.

Cost means the finding-event cost, not a repeated whole-case charge. Medians use
known values on latest entries, by their current round, independently per metric.
`null` means no known value. Integer medians remain exact; a half-integer beyond
the exact floating-point range is an exact decimal string ending in `.5`. Cases with no findings are absent: these figures
cannot measure total case cost, zero-finding work, or which round pays its fee.
Do not copy a case-wide charge onto every finding. Missing costs stay UNKNOWN.
An empty book gives zero findings and empty round tables. Every malformed line,
missing field, or unknown enum is refused with exit 2 and its line number.
