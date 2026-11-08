# Stateful code review

Read when the packet includes this file. It applies to code whose correctness
depends on polling or retries, saved evidence, identity, switch or readiness
decisions, or generated recovery commands. It changes which attempts are made;
it grants no authority to publish, mutate production, or add an approval step.
Shared rules and records still govern evidence, attempts, and decisions.

## Scope

Apply only the rows relevant to the changed behavior and the requested decision.
A document audit or a pure formatter needs no retry or refusal lifecycle. Reuse
the repository's tests and its real producers and readers. Bound the work by
hypothesis and budget; do not manufacture findings or fill rows with unrelated work.

## Required attempts

| Behavior | Attempt | Evidence to retain |
| --- | --- | --- |
| Polling or retry loops | Before reading the branches, enumerate the loop's distinct outcomes and define the expected evidence and latest-error precedence. Exercise relevant outcome pairs: failure then a different failure, completed-unready then failure, and recovery. Vary remaining budget near expiry and during sleep. Model probe duration as well as supplied outcomes. Distinguish dependency failure from cancellation caused by the collector's own deadline. | Run the real loop with controlled clock and transport seams. Assert completed evidence, latest collection error, evidence age, rendered diagnosis, and total budget separately. Use a transition table or generated short traces when the outcome set is small; do not stop at the examples that motivated the change. |
| Saved positive evidence | Pair a fresh valid receipt with each relevant newer refusal, revocation, route change, or generation invalidation. | Name the authoritative negative predicate and establish whether it dominates the saved positive. Vary fields and transitions; a private-file permission refusal is not a service-token refusal. |
| Identity, switch, or readiness decisions | Find the runtime owner of the same decision, its callers, wire format, and repository guidance before accepting a second predicate. | Use the canonical reader, or record why a stricter condition is intended. Exercise a real disagreement candidate and at least one actual producer envelope; record which policy decides acceptance. Interrupt each required proof before and during execution: acceptance follows completed proof, and an incomplete read becomes neither a verified match nor a definitive mismatch. |
| CLI and recovery commands | Exercise parser-to-result wiring and inspect rendered recovery commands for each affected actor, including an operator acting for another owner where supported. | Assert that owner, workspace, checkout, and role match between observation and remedy. Command construction needs no live credential or production mutation. |
| Repository conventions | Read the applicable local review instructions and run the available checks. | Cite compliance or a justified exception for constrained values, imports, ownership, and cohesion. Name the native review command or provider actually checked and its result; one unavailable provider does not establish that the repository's native reviewer is unavailable. Lint success alone does not establish these rules. |

For an assembled or remote program, execute the complete program in a separate
process at least once with the real imports, result construction, producer
formats, and final parser. Use an isolated fixture and provider or transport
seams where needed, under the execution rules in core. Exercise slow or failed
dependency stages against their declared budgets. Where the contract permits
independent observations after a failure, verify that they are still collected.
Provider seams do not establish live-provider or SSH acceptance.

An extracted-function witness establishes only that function under the supplied
dependencies. It does not establish imports, parser wiring, agreement with the
canonical policy, actor authorization, shell behavior, or remote execution.
Record those as untested boundaries rather than extending the result to them.

## Failed attacks

Record every attempt with the attempt fields in records. For a NOT_REPRODUCED
outcome also record the exercised sequence, the asserted property, the executable
witness (command and code or log reference, or NONE with a reason), and the
untested boundary. A NOT_REPRODUCED attempt establishes only the property it
exercised, under its method and conditions. It is not certification.

## Regression sensitivity

For each material correction, retain a witness that fails on the old behavior
and passes on the repair, following the RED/GREEN rules in the charter. Where
practical, remove the correction in a disposable copy and require the witness to
fail again; label that as mutation calibration. Use the actual producer's
envelope or the canonical reader where agreement matters. A fixture built only
from the implementation's own assumptions cannot establish that agreement.

## Coverage matrix and decision

The case file carries a coverage matrix with one line per row above: EXERCISED,
NOT_EXERCISED, or INAPPLICABLE with a reason, plus the attempt IDs, asserted
property, code or log reference, outcome, and material untested cases. A
NOT_EXERCISED row that covers a material invariant is a coverage limit and stays
visible in the decision. A material invariant with feasible runnable verification
cannot support READY from inspection alone; leave it as an open obligation
(INVESTIGATION_REQUIRED) until the attempt is made.

When learning from a miss, preserve the old decision and the failed witness.
Replaying known misses validates regression obligations, not generalization. A
fresh reviewer on a repaired, already-known case does not make that case held
out. A claim of broader effectiveness needs defects and clean controls withheld
from protocol development and reviewer prompts, with false positives and review
time recorded as well as supported findings. That evaluation is required only
for that claim, not for each case decision.
