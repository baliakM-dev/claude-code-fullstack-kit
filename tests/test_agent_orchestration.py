"""Static regressions for risk-based agent orchestration."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class AgentOrchestrationTests(unittest.TestCase):
    def test_placeholder_agents_are_forbidden(self):
        text = (ROOT / ".claude/policies/core.md").read_text(encoding="utf-8")
        self.assertIn("Never spawn a placeholder", text)
        self.assertIn("independent value", text)

    def test_implementer_requires_version_clean_code(self):
        text = (ROOT / ".claude/agents/implementer.md").read_text(encoding="utf-8")
        self.assertIn("redundant checked exceptions", text)
        self.assertIn("unused imports", text)

    def test_code_reviewer_checks_framework_version_correctness(self):
        text = (ROOT / ".claude/agents/code-reviewer.md").read_text(encoding="utf-8")
        self.assertIn("resolved/project-selected version", text)
        self.assertIn("equivalent lambda vs method-reference", text)

if __name__ == "__main__":
    unittest.main()