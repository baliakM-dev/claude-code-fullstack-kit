"""Static regressions for the read-only implementation explainer."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ImplementationExplainerTests(unittest.TestCase):
    def test_explainer_is_read_only_and_not_a_reviewer(self):
        text = (ROOT / ".claude/agents/implementation-explainer.md").read_text(encoding="utf-8")
        self.assertIn('tools: ["Read", "Glob", "Grep"]', text)
        self.assertIn("educator, not an implementer or reviewer", text)
        self.assertIn("Framework magic", text)
        self.assertIn("Mental model", text)

    def test_core_does_not_auto_append_explainer(self):
        text = (ROOT / ".claude/policies/core.md").read_text(encoding="utf-8")
        self.assertIn("Do not append it automatically", text)
        self.assertIn("implementation-explainer", text)

if __name__ == "__main__":
    unittest.main()
