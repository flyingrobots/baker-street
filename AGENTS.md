# Agent working rules

## Fix review findings with RED→GREEN

Fix every issue raised in a pull-request review, whether by a person or a bot, with its own RED→GREEN evidence. This applies to every valid finding, including follow-ups, except a finding the user has explicitly accepted (ACCEPTED) or that was withdrawn (WITHDRAWN). For each one:

1. Write the test first. Run `make test` and record that it fails for the reason the finding names.
2. Make the smallest fix that resolves that finding.
3. Run `make test` again and record that every test passes.
4. Commit each finding separately. When one fix resolves several findings, or code and its tests must land together, make one coherent commit and record each finding's RED and GREEN in it. Put the RED and GREEN results in the commit message, and reply to each review thread with the commit.

This rule also applies to fixes that are not code:

- **Rule text in `SKILL.md`, `references/` or `roles/`:** add a test that reads the file and checks for the rule. It must fail before the edit and pass after it.
- **A pull-request body or changelog:** no repository test can fail. RED is the reviewed text, quoted, shown to fail the finding. GREEN is the corrected text, checked against the same finding. Put both in the reply to the review thread.
- **A fix to a test:** show the gap with a deliberate mutation of the code under test. The mutant must pass the old test and fail the new one, and the real code must pass the new one.

If a finding is not valid, reply with the evidence and make no change. Do not batch unrelated findings into one commit. Do not skip the RED step because a fix looks obvious.

## Review every pull request with Baker Street before merge

Before you merge a pull request, review it with Baker Street, the skill in this repository:

1. Run Baker Street on the pull request at its current head. Choose the smallest tier that fits the risk. Review with the rules on `main`. When the pull request changes Baker Street's own rules, those changes are the target of the review, not its authority.
2. Post a concise decision summary to the GitHub thread of the linked issue. If no issue is linked, post it on the pull request. Put the full case file in a collapsed section. Never push private evidence to make a link work.
3. Follow the case. Carry out each required repair under the RED→GREEN rule above. Then review the repaired head again with Baker Street. A case is valid only for the head it reviewed.

Merge only when all of these are true at the same head:

- **Baker Street passes:** the latest case for that head has the decision `READY`, and no earlier case on that head left a required repair or investigation unresolved. A new case on an unchanged head is allowed only to review a repair that does not change the head, such as a pull-request body fix, or to complete a named investigation. Do not otherwise run another review to change a decision.
- **Clean:** no review thread is unresolved, and no reviewer still has changes requested or a review in progress, whether a person or a bot.
- **Green:** every CI check on that head has completed. The `test` jobs from the CI workflow must have reported success, and every other check must have finished as success, skipped or neutral. Any other result, including cancelled or timed out, counts as failing. No checks at all is not green.

If any condition fails, do not merge. Report which condition failed.
