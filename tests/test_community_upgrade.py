"""Regression checks for retained third-party attribution."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class CommunityAttributionTests(unittest.TestCase):
    def test_notice_names_upstream_repository(self):
        text = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
        self.assertIn("rrezartprebreza/spring-boot-skills", text)

    def test_adapted_skills_keep_mit_notice(self):
        for name in ("spring-backend", "postgresql-migrations", "test-verification"):
            with self.subTest(skill=name):
                path = ROOT / ".claude/skills" / name / "LICENSE-UPSTREAM.txt"
                self.assertTrue(path.is_file())
                self.assertIn("MIT License", path.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
