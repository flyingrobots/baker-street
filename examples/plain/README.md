# An examination without literary flourish

Use `--plain`, or request plain voice in ordinary language, to remove literary
flourish from the entire case. This is a review instruction, not a command-line
option implemented by the packet builder. The packet field is `plain: true`.
The preference applies to initial reports, recall, repairs, the decision check,
the final account and reports enclosed for publication.

The role names identify duties. They need not supply fictional speakers.
Exact quotations of supplied evidence retain their original wording. Plain
manner changes neither the required phases nor publication authority.

## Follow a complete source examination

The following is a worked teaching account of the existing
[integer clamp example](../triage/clamp.py), not a transcript of independently
commissioned investigators or evidence of a new runtime test. Every role passage
below is illustrative. Its conclusion follows from the displayed source and
the stated integer-only contract.

```python
def clamp(value):
    """Clamp an integer to the inclusive interval [0, 10]."""
    return max(0, min(10, value))
```

For an integer input, return 0 below 0, the input from 0 through 10 inclusive,
and 10 above 10. Non-integer inputs are excluded. The source-only question needs
triage in ordinary use. The focused account below demonstrates the additional
reports and recall when that tier has independently been justified; it does not
recommend commissioning extra roles merely to populate an example.

### Case header

- Target: `examples/triage/clamp.py`; source digest
  `bafd82b4c7c832ebdbf088d988c5498768542d748cb62c6b14471ed8c8b0f61f`.
- Audience: callers supplying integers under the stated contract.
- Basis: SOURCE and INFERENCE; no target execution.
- Manner: `plain: true` throughout.
- Separation: illustrative sequential accounts by one author; no independent
  or blind agent inquiry is claimed.
- Permitted actions: read source and prepare this teaching account; no target
  edits, probes, commits or publication arise from the example's commission.
- Exclusions: other input types, performance, callers and runtime environments.

### Watson: first account, retained unchanged

The contract names the two inclusive boundaries and the expected result outside
them. A caller supplying an integer can determine the expected return value.
The account does not promise treatment of another input type. No consequential
ambiguity is identified within this audience and scope. No repair is proposed
in this first account.

### Holmes: source examination

Let `x` denote the argument `value`. For `x < 0`, the inner `min` returns `x`
and the outer `max` returns 0.
For `0 <= x <= 10`, both operations retain `x`. For `x > 10`, the inner
operation returns 10 and the outer retains it. These cases exhaust the stated
integer domain, including both boundaries. The source supports the contract.
This reasoning is not an executed test.

### Moriarty: source challenge

The boundary candidates are `-1`, `0`, `10` and `11`. Substitution in the
source expression yields `0`, `0`, `10` and `10`, respectively. This is source
reasoning, not a report that the function was run. A counterexample using a
non-integer would not refute the stated contract. No counterexample within the
examined integer domain is established, and no universal runtime assurance
follows from these observations.

### Reconciliation

The reader account and source reasoning agree within scope. There are no
findings, required repairs or disputes to adjudicate. No ledger finding event
is manufactured for a case without findings. No runtime probe was commissioned.

### Watson: recall

The first account remains unchanged. The source examination and conditional
challenge supply no required repair. Repair Menu: none. Probe Triage: no new
probe is proposed for graduation; retain this source explanation as a teaching
account. No maintained test or validation result is invented.

### Decision check

Reviewer basis: `SEQUENTIAL_SELF_CHECK`, within this illustrative account.
The three source cases cover the stated domain; the audience can determine
what to expect; the boundary challenge is labelled as reasoning; there is no
unresolved repair, dispute or decision-critical question within the stated
scope. No fresh checker or independent verification is claimed.

### Final account

Decision: READY for the stated integer contract, based on SOURCE and INFERENCE.
No required action. Runtime behaviour, other input types and surrounding callers
were not examined. The accounts are illustrative and sequential, not independent
testimony. Valid only for the recorded artifacts, environment and examined scope;
reassess affected claims when these change.

For ordinary triage of this same question, retain the header, Holmes source
examination and disclosed front-office decision check. Watson, Moriarty and recall
are not performed; name that omission once rather than inventing their reports.

## Enclose the reports without restoring the flourish

An authorised PR posting begins with the concise decision and canonical case.
Ordinarily enclose each report actually produced in its own `<details>` section,
only when its disclosure is authorised and safe. A report may be withheld or
shortened when necessary; identify the resulting coverage limit and preserve
its material conclusions, disagreements and corrections where authorised and safe.
Identify its actual author and reviewer basis. For example, this is an
illustrative enclosure of the check above, not a newly commissioned check:

```html
<details>
<summary>Decision check — illustrative sequential self-check</summary>

The stated source cases exhaust the integer contract. No runtime trial or
independent checker is claimed. No required repair remains within scope.

</details>
```

Do not replace the canonical case with this short enclosure. Preserve frozen
first accounts, recalls, disagreements and corrections separately when they
exist. Inspect the contents as well as the visible introduction: plain manner
must survive inside the collapsed sections. Redaction remains necessary.

## Preserve exact evidence

A later choice of plain manner does not rewrite a report already frozen under
another manner. Retain that original unchanged and identify its earlier manner
when enclosing an authorised copy. Newly composed recall and final conclusions
are plain. Necessary redaction or withholding affects the labelled public copy,
not the privately retained original; disclose the resulting coverage limit.

An illustrative supplied execution message may read:

```json
{"outcome":"BLOCKED","reason":"command timed out"}
```

Keep those bytes. Explain that the allowance expired and the attempt supplies
no completed trial. `BLOCKED` here describes the attempt, not automatically the
case decision. Removing flourish must not convert that message into success or
remove its uncertainty.
