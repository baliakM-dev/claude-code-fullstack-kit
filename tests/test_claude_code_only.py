"""Claude Code-only packaging regressions."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ClaudeCodeOnlyTests(unittest.TestCase):
    def test_no_openai_metadata(self):
        self.assertEqual(list((ROOT / ".claude/skills").glob("*/agents/openai.yaml")), [])

    def test_manifest_counts(self):
        manifest = json.loads((ROOT / "kit-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["kit_version"], "1.5.2")
        self.assertEqual(len(manifest["agents"]), 6)
        self.assertEqual(len(manifest["skills"]), 9)

    def test_local_settings_not_committed(self):
        self.assertFalse((ROOT / ".claude/settings.local.json").exists())

if __name__ == "__main__":
    unittest.main()
