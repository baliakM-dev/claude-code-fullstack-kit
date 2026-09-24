"""Regression checks specific to the Claude Code-only 1.5.1 packaging."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ClaudeCodeOnly151Tests(unittest.TestCase):
    def test_no_openai_skill_metadata_is_shipped(self):
        found = list((ROOT / '.claude' / 'skills').glob('*/agents/openai.yaml'))
        self.assertEqual(found, [])

    def test_manifest_marks_151_and_keeps_claude_assets(self):
        manifest = json.loads((ROOT / 'kit-manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['kit_version'], '1.5.1')
        self.assertEqual(len(manifest['agents']), 6)
        self.assertEqual(len(manifest['skills']), 9)
        for name in manifest['agents']:
            self.assertTrue((ROOT / '.claude' / 'agents' / f'{name}.md').is_file())
        for name in manifest['skills']:
            self.assertTrue((ROOT / '.claude' / 'skills' / name / 'SKILL.md').is_file())


if __name__ == '__main__':
    unittest.main()
