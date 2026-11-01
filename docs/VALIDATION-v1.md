# Validation record — 2026-10-31

## Completed

- The Editor’s Edition passed the skill format validator.
- The evaluation harness passed 25 unittest test methods, including synthetic controls for all 14 cases.
- Three selected cases were given to fresh-context agents with no answer keys in their supplied packets.
- All three returned responses passed their deterministic contract checks.
- Packet inputs remained identical to the canonical fixtures after those responses.

The 25 methods test the harness and two small executable fixture truths. They
are not 25 successful model reviews. Synthetic controls are generated from the
oracle specifically to exercise the grader; they are never model evidence.

## Author-agent inspection of the three responses

| Case | Observed behavior | Assessment |
| --- | --- | --- |
| case-01 | Supported the bounded integer clamp by source reasoning, reported no findings, and explicitly denied runtime execution. | Consistent with the narrow clean-case rubric. |
| case-03 | Kept the mutation outcome unresolved, refuted the claim that it ran, and identified evidence inflation in the draft as the confirmed documentation defect. | Correctly separated a hypothetical fixture defect from an established review defect. |
| case-06 | Used input 101 as a counterexample, rejected the blanket parse-only exemption, and proposed scoped wording without reopening the approved validation change. | Correctly reviewed the repair as a fresh claim. |

This inspection was performed by the same author-agent that prepared the skill
and fixtures. It is not independent human adjudication. The machine records
therefore retain `PENDING_HUMAN_REVIEW`.

Raw responses, packet manifests, task instructions, and contract outputs are
under `evals/recorded-smoke/2026-10-31/`. The skill digest is in the run record;
the separately supplied skill retains the full prompt and record formats.

## Limits

These were one trial each on three selected documentary cases. The remaining
11 cases have synthetic grader controls but have not been run against an agent
in this session. No complete multi-agent agency workflow was tested.

Contexts were fresh, but filesystems were shared. Packet-only access was an
instruction, not an enforced sandbox. Host tool traces were not exported, so
the record cannot independently verify every candidate action. Model version,
sampling settings, token cost, and wall-clock cost were not captured.

There was no original-prompt baseline, single-reviewer baseline, or plain-voice
comparison. These observations do not establish that Baker Street beats an
ordinary review or that the character voices improve results.
