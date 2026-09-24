"""Static routing/packaging regressions; these do not run an AI or a Spring app."""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_quality_routes", ROOT / "scripts/validate_kit.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class DesignQualityRoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "kit"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))

    def tearDown(self):
        self.temp.cleanup()

    def remove_link(self, relative, target):
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        old = f"]({target})"
        self.assertIn(old, text)
        path.write_text(text.replace(old, "] - reference removed", 1), encoding="utf-8")
        report = MOD.validate(self.root)
        self.assertEqual(report["status"], "FAIL", report)
        self.assertTrue(any("required design-quality route missing" in e for e in report["errors"]), report)

    def test_all_nine_design_routes_present(self):
        report = MOD.validate(self.root)
        self.assertEqual(report["status"], "PASS", report)
        self.assertEqual(report["counts"]["design_routes"], 9)

    def test_implementer_must_reach_standard(self):
        self.remove_link('.claude/agents/implementer.md', '../skills/spring-backend/SKILL.md')

    def test_reviewer_must_reach_same_standard(self):
        self.remove_link('.claude/agents/code-reviewer.md', '../skills/spring-backend/SKILL.md')

    def test_evidence_review_must_reach_standard(self):
        self.remove_link('.claude/skills/evidence-review/SKILL.md', '../spring-backend/SKILL.md')

    def test_backend_requires_design_reference(self):
        self.remove_link('.claude/skills/spring-backend/SKILL.md', 'references/design-quality.md')

    def test_backend_requires_verification_reference(self):
        self.remove_link('.claude/skills/spring-backend/SKILL.md', 'references/quality-verification.md')

    def test_test_skill_must_reach_verification(self):
        self.remove_link('.claude/skills/test-verification/SKILL.md', '../spring-backend/references/quality-verification.md')

    def test_bootstrap_routes_quality_checks(self):
        self.remove_link('docs/tasks/000-bootstrap.md', '../../.claude/skills/spring-backend/references/quality-verification.md')

    def test_payment_module_activates_boundary_check(self):
        self.remove_link('docs/tasks/002-received-payments.md', '../../.claude/skills/spring-backend/references/quality-verification.md')

    def test_calculator_activates_pure_core_check(self):
        self.remove_link('docs/tasks/003-first-calculation.md', '../../.claude/skills/spring-backend/references/quality-verification.md')

    def test_missing_quality_files_fail(self):
        for name in ('design-quality.md', 'quality-verification.md'):
            with self.subTest(name=name):
                path = self.root / '.claude/skills/spring-backend/references' / name
                data = path.read_bytes()
                path.unlink()
                report = MOD.validate(self.root)
                self.assertEqual(report['status'], 'FAIL', report)
                self.assertTrue(any(name in e for e in report['errors']), report)
                path.write_bytes(data)

    def test_manual_cases_unique_and_not_reported_run(self):
        value = json.loads((self.root/'evals/design-quality.json').read_text(encoding='utf-8'))
        cases = value['cases']
        self.assertEqual(len(cases), 12)
        self.assertEqual(len({case['id'] for case in cases}), len(cases))
        self.assertTrue(all(case['status'] == 'NOT_RUN' for case in cases))
        self.assertTrue(all(case['input'] and case['expected'] for case in cases))


if __name__ == '__main__':
    unittest.main()
