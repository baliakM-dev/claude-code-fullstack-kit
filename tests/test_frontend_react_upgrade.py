import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_kit", ROOT / "scripts/validate_kit.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class FrontendReactUpgradeTest(unittest.TestCase):
    def test_frontend_reviewer_is_read_only_and_preloads_only_react(self):
        data = MOD.frontmatter((ROOT / '.claude/agents/frontend-reviewer.md').read_text())
        self.assertEqual(set(data['tools']), {'Read', 'Glob', 'Grep'})
        self.assertEqual(data.get('skills'), ['react-typescript'])
        self.assertEqual(data['permissionMode'], 'default')

    def test_react_skill_routes_progressively(self):
        text = (ROOT / '.claude/skills/react-typescript/SKILL.md').read_text()
        for target in ('server-state-api.md', 'forms-state.md', 'architecture-routing.md', 'testing-accessibility.md'):
            self.assertIn(target, text)
        self.assertIn('bff-keycloak', text)
        self.assertIn('do not load all frontend references by default', text.lower())

    def test_server_state_rules_protect_bff_and_cache_scope(self):
        text = (ROOT / '.claude/skills/react-typescript/references/server-state-api.md').read_text().lower()
        self.assertIn('never read/store access or refresh tokens', text)
        self.assertIn('principal-scoped', text)
        self.assertIn('do not automatically retry authentication/authorization failures', text)
        self.assertIn('abortsignal', text)

    def test_forms_rules_separate_state_ownership(self):
        text = (ROOT / '.claude/skills/react-typescript/references/forms-state.md').read_text().lower()
        self.assertIn('server state -> tanstack query', text)
        self.assertIn('form state -> react hook form', text)
        self.assertIn('local ephemeral ui state', text)
        self.assertIn('server validation authoritative', text)

    def test_architecture_rules_reject_blanket_memoization_and_route_auth(self):
        text = (ROOT / '.claude/skills/react-typescript/references/architecture-routing.md').read_text().lower()
        self.assertIn('backend authorization remains mandatory', text)
        self.assertIn('do not add `usememo`, `usecallback` or `react.memo` everywhere', text)
        self.assertIn('do not force this exact tree', text)

    def test_test_reference_separates_mock_and_real_oidc(self):
        text = (ROOT / '.claude/skills/react-typescript/references/testing-accessibility.md').read_text().lower()
        self.assertIn('react testing library', text)
        self.assertIn('msw', text)
        self.assertIn('playwright', text)
        self.assertIn('do not prove real oidc', text)

    def test_frontend_eval_cases_are_not_claimed_run(self):
        cases = json.loads((ROOT / 'evals/frontend-react.json').read_text())
        self.assertGreaterEqual(len(cases), 10)
        self.assertTrue(all(c['status'] == 'NOT_RUN' for c in cases))
        self.assertTrue(all(len(c['criteria']) >= 3 for c in cases))

    def test_frontend_route_removal_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            clone = Path(tmp) / 'kit'
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            p = clone / '.claude/skills/react-typescript/SKILL.md'
            text = p.read_text().replace('[server-state-api.md](references/server-state-api.md)', 'server-state-api.md')
            p.write_text(text)
            result = MOD.validate(clone)
            self.assertEqual(result['status'], 'FAIL')
            self.assertTrue(any('required frontend route missing' in e for e in result['errors']))

    def test_manifest_version_and_agent_count(self):
        manifest = json.loads((ROOT / 'kit-manifest.json').read_text())
        self.assertEqual(manifest['kit_version'], '1.5.1')
        self.assertIn('frontend-reviewer', manifest['agents'])
        self.assertEqual(len(manifest['agents']), 6)
        self.assertEqual(len(manifest['skills']), 9)


if __name__ == '__main__':
    unittest.main()
