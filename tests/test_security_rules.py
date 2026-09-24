"""Static regressions for shared security guidance."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class SecurityRulesTests(unittest.TestCase):
    def test_security_skill_has_core_references(self):
        base = ROOT / ".claude/skills/application-security"
        text = (base / "SKILL.md").read_text(encoding="utf-8")
        for name in (
            "spring-security.md",
            "browser-csrf-cors.md",
            "bff-keycloak.md",
            "resource-server.md",
            "authorization-data.md",
            "abuse-deployment.md",
            "security-verification.md",
        ):
            self.assertIn(name, text)
            self.assertTrue((base / "references" / name).is_file())

    def test_security_reviewer_is_read_only(self):
        text = (ROOT / ".claude/agents/security-reviewer.md").read_text(encoding="utf-8")
        self.assertIn('tools: ["Read", "Glob", "Grep"]', text)
        self.assertIn('skills: ["application-security"]', text)

    def test_bff_guidance_keeps_tokens_server_side(self):
        text = (ROOT / ".claude/skills/application-security/references/bff-keycloak.md").read_text(encoding="utf-8").lower()
        self.assertIn("access token", text)
        self.assertIn("refresh token", text)
        self.assertIn("csrf", text)

    def test_spa_csrf_guidance_prefers_current_spring7_idiom_without_false_deprecation(self):
        text = (ROOT / ".claude/skills/application-security/references/browser-csrf-cors.md").read_text(encoding="utf-8")
        self.assertIn(".csrf(CsrfConfigurer::spa)", text)
        self.assertIn(".csrf(csrf -> csrf.spa())", text)
        self.assertIn("equivalent and not a defect", text)

    def test_spring_security_guidance_rejects_redundant_historical_throws(self):
        text = (ROOT / ".claude/skills/application-security/references/spring-security.md").read_text(encoding="utf-8")
        self.assertIn("do not keep `throws Exception`", text)
        self.assertIn("resolved Spring Security version", text)

if __name__ == "__main__":
    unittest.main()