"""Static regressions for React/TypeScript guidance."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class FrontendRulesTests(unittest.TestCase):
    def test_frontend_reviewer_is_read_only(self):
        text = (ROOT / ".claude/agents/frontend-reviewer.md").read_text(encoding="utf-8")
        self.assertIn('tools: ["Read", "Glob", "Grep"]', text)
        self.assertIn('skills: ["react-typescript"]', text)

    def test_react_skill_links_expected_references(self):
        base = ROOT / ".claude/skills/react-typescript"
        text = (base / "SKILL.md").read_text(encoding="utf-8")
        for name in ("server-state-api.md", "forms-state.md", "architecture-routing.md", "testing-accessibility.md"):
            self.assertIn(name, text)
            self.assertTrue((base / "references" / name).is_file())

    def test_server_state_guidance_mentions_query_and_token_boundary(self):
        text = (ROOT / ".claude/skills/react-typescript/references/server-state-api.md").read_text(encoding="utf-8").lower()
        self.assertIn("tanstack query", text)
        self.assertIn("access or refresh tokens", text)

if __name__ == "__main__":
    unittest.main()
