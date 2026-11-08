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
        self.assertIn('every CI check on that head has completed and passed; none is failing or pending.',text)

if __name__=='__main__': unittest.main()
