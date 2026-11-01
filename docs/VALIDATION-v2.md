# Editor’s Edition v2 validation — 2026-10-31

The final skill passes its format validator and all local reference links
resolve. The companion harness passes 29 unittest methods, including synthetic
contract controls for all 20 fixtures. Those controls test the grader; they
are not 20 model reviews.

## Focused forward trials

Three initial fresh-context trials exercised the new v2 behaviors. Each packet
contained the skill and inputs but no oracle. All three responses passed the
contract grader. Author-agent semantic inspection found a record-format issue
in one of them, which was corrected and tested with one further fresh-context
trial. All four responses pass the final contract grader; that fact alone does
not erase the semantic concern in the original response.

| Trial | Case | Observation |
| --- | --- | --- |
| 1 | case-16 | Assigned the four probes to direct promotion, minimization, a specialized suite, and archival; kept reported checks separate from execution. |
| 2 | case-17 | Deferred speculative implementation correctly, but used INFORMATIONAL severity to describe an unconfirmed finding whose consequences were unknown. |
| 3 | case-19 | Preserved the original verdict and distinguished the repaired candidate from the unchanged subject branch. |
| 4 | case-17, targeted repeat | Used HYPOTHESIS status and UNKNOWN severity, and deferred implementation pending evidence. |

The second trial exposed a limitation in the available severity vocabulary and
in what the contract grader measures. The final v2 skill and record format now
include UNKNOWN and explicitly distinguish uncertainty from low consequence.
The original answer, correction, and targeted repeat remain on record.

Raw responses, task packets, manifests, contract results, and skill/reference
digests are under `evals/recorded-smoke/2026-10-31-v2/`. The v1 validation record
and its original trials remain preserved separately. Initial v2 trials used
the pre-correction skill; the targeted repeat used the final revision. Do not
represent all four trials as runs of identical prompt bytes.

## Limits

These were selected documentary tasks, one trial each except the targeted
repeat. They did not run complete investigations, actual probe promotion,
repair branches, cherry-picks, or remote publication. All other v2 cases have
synthetic grader controls but no v2 agent run recorded here.

The semantic assessment above was made by the author-agent, not an independent
human reviewer. The grader retains PENDING_HUMAN_REVIEW. Fresh contexts were
used, but filesystem separation was instruction-based on a shared host; host
tool traces, exact model version, sampling parameters, and costs were not
exported. No baseline or controlled voice comparison was run, and the targeted
repeat does not establish generalization or causal improvement.
