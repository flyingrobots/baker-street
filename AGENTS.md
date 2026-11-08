# Agent working rules

## Fix review findings with RED→GREEN

Fix every issue raised in a pull-request review, whether by a person or a bot, with its own RED→GREEN evidence:

1. Write the test first. Run `make test` and record that it fails for the reason the finding names.
2. Make the smallest fix that resolves that finding.
3. Run `make test` again and record that every test passes.
4. Commit that finding alone. Put the RED and GREEN results in the commit message, and reply to the review thread with the commit.

This rule also applies to fixes that are not code:

- **Rule text in `references/` or `roles/`:** add a test that reads the file and checks for the rule. It must fail before the edit and pass after it.
- **A fix to a test:** show the gap with a deliberate mutation of the code under test. The mutant must pass the old test and fail the new one, and the real code must pass the new one.

If a finding is not valid, reply with the evidence and make no change. Do not batch several findings into one commit. Do not skip the RED step because a fix looks obvious.
