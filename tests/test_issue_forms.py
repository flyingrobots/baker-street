"""Examine the written directions; these trials do not certify authors' conduct."""
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
FORMS = ('bug', 'decision', 'feature', 'investigation',
         'nine-section-card', 'research', 'spike')


class IssueFormTests(unittest.TestCase):
    def test_technical_names_keep_precision_without_modernising_the_prose(self):
        text = (ROOT / 'AGENTS.md').read_text()
        self.assertIn('necessary technical names, such as `mutation testing`', text)
        self.assertIn('Set these names apart as technical literals', text)
        self.assertIn('Examine the surrounding prose for period style', text)
        self.assertNotIn('Put modern technical terms in\n  the plain technical prose', text)

    def test_metadata_guidance_preserves_quoted_values(self):
        for name in FORMS:
            with self.subTest(form=name):
                text = (ROOT / '.github/ISSUE_TEMPLATE' / (name + '.md')).read_text()
                guidance = text.split('<!--', 1)[1].split('-->', 1)[0]
                self.assertIn('title, area, and source as valid YAML strings', guidance)
                self.assertIn('Escape embedded double quotes and backslashes', guidance)
                example = re.search(r'^Example: title: (.+)$', guidance, re.MULTILINE)
                self.assertIsNotNone(example, 'Supply a quoted-value example')
                self.assertEqual(json.loads(example.group(1)), 'Correct "none" in C:\\cases')
                self.assertIn('```yaml\n.dag: issue-dag/2', text)


if __name__ == '__main__':
    unittest.main()
