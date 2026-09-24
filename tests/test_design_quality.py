"""Static regressions for proportionate design-quality guidance."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class DesignQualityTests(unittest.TestCase):
    def test_spring_skill_links_design_quality(self):
        text = (ROOT / ".claude/skills/spring-backend/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("design-quality.md", text)

    def test_design_quality_rejects_dogmatic_abstraction(self):
        text = (ROOT / ".claude/skills/spring-backend/references/design-quality.md").read_text(encoding="utf-8").lower()
        self.assertIn("solid", text)
        self.assertTrue("yagni" in text or "kiss" in text)
        self.assertTrue("interface" in text)

if __name__ == "__main__":
    unittest.main()
