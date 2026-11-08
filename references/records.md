# Records and decisions

Contents: [header](#case-header), [evidence](#evidence-manifest),
[claims](#claims), [findings](#findings), [attempts](#attempts),
[repairs](#repairs), [probes](#probe-dispositions), [checks](#decision-check),
[decisions](#decisions), [corrections](#errata-and-remediation), [layouts](#layouts).

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
recorded contract or acceptance criterion, or (b) a named audience that would
take a wrong action because of it. An INFORMATIONAL finding has no identified
adverse consequence, so it cannot be REQUIRED_REPAIR. A CONFIRMED finding that
fails this rule is FOLLOW_UP, and its repairs have scope FOLLOW_UP. Unconfirmed
findings keep their existing dispositions: HYPOTHESIS or CONTESTED may need
INVESTIGATE; WITHDRAWN is ACCEPTED with no active repair. This rule applies to
every finding type, not to prose alone.

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
Do not repeat reviews to reach a target decision. A decision does not replace the
repository's own review or publishing authorization.

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

In every tier, list FOLLOW_UP-scope repairs under a "Batched follow-ups" heading
in CASE_FILE.md so they stay in view. They do not change the decision. When the
user authorizes a repair on the same series, the repair may include them.

In every tier, when stateful code review applies, CASE_FILE.md includes its
coverage matrix (see references/stateful-code-review.md).
