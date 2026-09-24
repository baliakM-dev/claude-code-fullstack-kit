"""Static regressions for test-evidence efficiency and isolation."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class TestVerificationRulesTests(unittest.TestCase):
    def test_external_mutable_state_must_be_repeatable(self):
        text = (ROOT / ".claude/skills/test-verification/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("immediately repeatable", text)
        self.assertIn("guaranteed cleanup/reset", text)

    def test_evidence_is_deduplicated_across_layers(self):
        text = (ROOT / ".claude/skills/test-verification/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Prove one material behavior once", text)
        self.assertIn("distinct mechanism", text)

    def test_test_engineer_prioritizes_must_should_later(self):
        text = (ROOT / ".claude/agents/test-engineer.md").read_text(encoding="utf-8")
        self.assertIn("MUST", text)
        self.assertIn("SHOULD", text)
        self.assertIn("LATER", text)

if __name__ == "__main__":
    unittest.main()