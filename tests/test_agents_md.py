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

if __name__=='__main__': unittest.main()
