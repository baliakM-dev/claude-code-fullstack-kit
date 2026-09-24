"""Static regressions for platform and database guidance."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class PlatformDatabaseTests(unittest.TestCase):
    def test_platform_reviewer_is_read_only(self):
        text = (ROOT / ".claude/agents/platform-reviewer.md").read_text(encoding="utf-8")
        self.assertIn('tools: ["Read", "Glob", "Grep"]', text)
        self.assertIn('skills: ["delivery-operations"]', text)

    def test_database_references_exist(self):
        base = ROOT / ".claude/skills/postgresql-migrations/references"
        self.assertTrue((base / "normalization.md").is_file())
        self.assertTrue((base / "flyway-safety.md").is_file())

    def test_normalization_is_not_bcnf_dogma(self):
        text = (ROOT / ".claude/skills/postgresql-migrations/references/normalization.md").read_text(encoding="utf-8")
        self.assertIn("BCNF", text)
        self.assertIn("Do not decompose blindly", text)

    def test_observability_warns_about_cardinality(self):
        text = (ROOT / ".claude/skills/delivery-operations/references/observability-stack.md").read_text(encoding="utf-8").lower()
        self.assertIn("cardinality", text)

if __name__ == "__main__":
    unittest.main()
