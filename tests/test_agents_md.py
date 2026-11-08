from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

def agents_text():
    return ' '.join((ROOT/'AGENTS.md').read_text(encoding='utf-8').split())

class AgentsMdTests(unittest.TestCase):
    def test_commit_rule_allows_one_coherent_commit_for_shared_fix(self):
        # charter.md: "Make coherent commits mapping to R-IDs ... Do not require one commit per ID."
        text=agents_text()
        self.assertNotIn('Commit that finding alone',text)
        self.assertNotIn('Do not batch several findings into one commit',text)
        self.assertIn("When one fix resolves several findings, or code and its tests must land together, make one coherent commit and record each finding's RED and GREEN in it.",text)

    def test_green_gate_does_not_depend_on_required_status(self):
        # main has no branch protection and no required status checks, so "required" is vacuous.
        text=agents_text()
        self.assertNotIn('every required CI check passes',text)

    def test_ready_gate_cannot_be_reached_by_rerunning_reviews(self):
        # records.md: "Do not repeat reviews to reach a target decision."
        text=agents_text()
        self.assertIn('no earlier case on that head left a required repair or investigation unresolved',text)

    def test_posted_report_is_a_concise_summary_without_private_evidence(self):
        # SKILL.md: "A concise public summary links the full case"; charter: never expose private artifacts.
        text=agents_text()
        self.assertIn('Post a concise decision summary',text)
        self.assertIn('Put the full case file in a collapsed section. Never push private evidence to make a link work.',text)

    def test_red_green_covers_skill_text_and_untestable_prose(self):
        text=agents_text()
        self.assertIn('**Rule text in `SKILL.md`, `references/` or `roles/`:**',text)
        self.assertIn('**A pull-request body or changelog:**',text)
        self.assertIn('This applies to every valid finding, including follow-ups',text)

    def test_review_uses_the_rules_on_main(self):
        text=agents_text()
        self.assertIn("Review with the rules on `main`. When the pull request changes Baker Street's own rules, those changes are the target of the review, not its authority.",text)

    def test_same_head_review_allowed_for_off_head_repairs_and_investigations(self):
        # records.md: completing repairs and investigation obligations is the path to READY.
        text=agents_text()
        self.assertNotIn('Do not run another review on an unchanged head to change its decision.',text)

    def test_green_gate_needs_ci_success_and_treats_other_results_as_failing(self):
        # A gate over "every check" is vacuous before any check runs; cancelled and timed out must count.
        text=agents_text()
        self.assertIn('every CI check on that head has completed. The `test` jobs from the CI workflow must have reported success, and every other check must have finished as success, skipped or neutral. Any other result, including cancelled or timed out, counts as failing. No checks at all is not green.',text)

    def test_accepted_and_withdrawn_findings_are_exempt(self):
        # records.md: ACCEPTED needs explicit user acceptance; WITHDRAWN retains no obligation.
        self.assertIn('This applies to every valid finding, including follow-ups, except a finding the user has explicitly accepted (ACCEPTED) or that was withdrawn (WITHDRAWN). For each one:',agents_text())

    def test_posted_case_is_redacted(self):
        # core.md: redact secrets and record redactions; charter: never expose private artifacts.
        self.assertIn('Redact secrets and private material first. Put the full case file in a collapsed section.',agents_text())

    def test_same_head_case_allowed_when_something_material_changed(self):
        # records.md: acceptance and evidenced dispute are Referral answers; neither changes the head.
        text=agents_text()
        self.assertIn("Do not repeat a review on an unchanged head merely to reach a different decision. A new case on an unchanged head is allowed when something material has changed since the last case: a repair that does not change the head, such as a pull-request body fix; a completed investigation; or the user's explicit acceptance of, or evidenced dispute with, a named finding. The new case states what changed.",text)

    def test_clean_gate_covers_findings_posted_anywhere(self):
        # Baker Street cases are comments, not review threads; criterion 2: no unresolved issues.
        self.assertIn('Every finding raised on the pull request, wherever it was posted (a review thread, a review body, a pull-request or issue comment, or a Baker Street case), has been fixed under the rule above, is ACCEPTED or WITHDRAWN, or was answered as not valid with evidence.',agents_text())

    def test_untestable_fix_evidence_goes_where_the_finding_was_posted(self):
        # A Baker Street finding has no review thread.
        self.assertIn('Put both in the reply to the review thread, or in the thread where the finding was posted.',agents_text())

    def test_case_validity_covers_head_body_and_base(self):
        # SKILL.md: valid only for the recorded artifacts; reassess affected claims when these change.
        self.assertIn('When one of them changes, reassess the affected claims in a new case before merge.',agents_text())

    def test_baker_street_gate_requires_latest_case_ready(self):
        # CodeRabbit 4507405353: no test pinned the READY requirement itself.
        self.assertIn('- **Baker Street passes:** the latest case for that head has the decision `READY`,',agents_text())

    def test_clean_gate_requires_no_unresolved_reviews(self):
        # CodeRabbit 4507405357: no test pinned the thread and reviewer-state conditions.
        self.assertIn('- **Clean:** no review thread is unresolved, and no reviewer still has changes requested or a review in progress, whether a person or a bot.',agents_text())

    def test_case_validity_follows_skill_md(self):
        # SKILL.md: valid only for the recorded artifacts, environment, and examined scope.
        self.assertIn('A case is valid only for the artifacts, environment and scope it recorded, including the head, the pull-request body and the base.',agents_text())

if __name__=='__main__': unittest.main()
