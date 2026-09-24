"""Static kit route/metadata regressions, NOT Spring/Keycloak security tests."""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_security_routes", ROOT / "scripts/validate_kit.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class SecurityRoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "kit"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    def tearDown(self):
        self.temp.cleanup()

    def assert_route_fails_without_link(self, source, target):
        path = self.root / source
        original = path.read_text(encoding="utf-8")
        destination = (self.root / target).resolve()
        matches = [x for x in MOD.LINK.findall(original)
                   if not urlparse(x).scheme and not x.startswith("#")
                   and (path.parent / unquote(x.split("#", 1)[0])).resolve() == destination]
        self.assertTrue(matches, (source, target))
        altered = original
        for link in matches:
            altered = altered.replace("](" + link + ")", "] route deliberately removed")
        path.write_text(altered, encoding="utf-8")
        try:
            report = MOD.validate(self.root)
            self.assertEqual(report["status"], "FAIL", report)
            self.assertTrue(any("required security route missing" in x for x in report["errors"]), report)
        finally:
            path.write_text(original, encoding="utf-8")

    def test_security_routes_all_present_and_unique(self):
        report = MOD.validate(self.root)
        self.assertEqual(report["status"], "PASS", report)
        self.assertEqual(len(MOD.SECURITY_ROUTES), 22)
        self.assertEqual(len(set(MOD.SECURITY_ROUTES)), 22)
        self.assertEqual(report["counts"]["security_routes"], 22)

    def test_each_required_security_route_has_negative_regression(self):
        for source, target in MOD.SECURITY_ROUTES:
            with self.subTest(source=source, target=target):
                self.assert_route_fails_without_link(source, target)

    def test_each_new_reference_is_required_and_missing_file_fails(self):
        manifest = json.loads((self.root / "kit-manifest.json").read_text())
        for name in ("spring-security", "browser-csrf-cors", "resource-server", "security-verification"):
            relative = ".claude/skills/application-security/references/" + name + ".md"
            with self.subTest(reference=name):
                self.assertIn(relative, manifest["required_files"])
                path = self.root / relative
                original = path.read_bytes()
                path.unlink()
                try:
                    report = MOD.validate(self.root)
                    self.assertEqual(report["status"], "FAIL", report)
                    self.assertTrue(any(name + ".md" in x for x in report["errors"]), report)
                finally:
                    path.write_bytes(original)

    def test_security_profile_is_required(self):
        (self.root / "docs/security-profile.md").unlink()
        report = MOD.validate(self.root)
        self.assertEqual(report["status"], "FAIL", report)
        self.assertTrue(any("security-profile.md" in x for x in report["errors"]), report)

    def test_original_design_routes_remain_present(self):
        report = MOD.validate(self.root)
        self.assertEqual(report["counts"]["design_routes"], 9)

    def test_security_update_preserved_with_platform_and_frontend_reviewers(self):
        report = MOD.validate(self.root)
        self.assertEqual(report["counts"]["agents"], 6)
        self.assertEqual(report["counts"]["skills"], 9)
        self.assertTrue((self.root / ".claude/agents/platform-reviewer.md").is_file())
        self.assertTrue((self.root / ".claude/agents/frontend-reviewer.md").is_file())

    def test_both_reviewers_remain_read_only(self):
        for role in ("code-reviewer", "security-reviewer"):
            data = MOD.frontmatter((self.root / ".claude/agents" / (role + ".md")).read_text())
            self.assertEqual(set(data["tools"]), {"Read", "Glob", "Grep"})
            self.assertEqual(data["permissionMode"], "default")

    def test_no_preload_expansion(self):
        for path in (self.root / ".claude/agents").glob("*.md"):
            data = MOD.frontmatter(path.read_text())
            self.assertLessEqual(len(data.get("skills", [])), 1)
            self.assertNotIn("Agent", data["tools"])

    def test_manual_security_cases_unique_and_unexecuted(self):
        suite = json.loads((self.root / "evals/security-rules.json").read_text())
        self.assertEqual(suite["status"], "NOT_RUN_IN_CLAUDE_CODE")
        self.assertEqual(len(suite["cases"]), 24)
        self.assertEqual(len({x["id"] for x in suite["cases"]}), 24)
        self.assertTrue(all(x["status"] == "NOT_RUN" and x["input"] and x["expected"] for x in suite["cases"]))

    def test_security_definition_not_confused_with_model_execution(self):
        text = (self.root / "tests/test_security_rules.py").read_text()
        self.assertIn("NOT Spring/Keycloak security tests", text)
        report = MOD.validate(self.root)
        self.assertTrue(any("NOT_RUN" in x for x in report["warnings"]))

    def test_shared_security_entrypoint_stays_small(self):
        text = (self.root / ".claude/skills/application-security/SKILL.md").read_text()
        self.assertLess(len(text.splitlines()), 80)
        self.assertEqual(set(MOD.frontmatter(text)), {"name", "description"})

    def test_portable_skill_reference_links_are_internal(self):
        root = (self.root / ".claude/skills/application-security").resolve()
        for path in root.rglob("*.md"):
            for link in MOD.LINK.findall(path.read_text()):
                if urlparse(link).scheme or link.startswith("#"):
                    continue
                target = (path.parent / unquote(link.split("#", 1)[0])).resolve()
                self.assertTrue(target.is_relative_to(root), (path, link))
                self.assertTrue(target.is_file(), (path, link))


if __name__ == "__main__":
    unittest.main()
