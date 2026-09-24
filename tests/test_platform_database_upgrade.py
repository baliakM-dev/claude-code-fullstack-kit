from __future__ import annotations
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_kit_platform", ROOT / "scripts" / "validate_kit.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

class PlatformDatabaseUpgradeTests(unittest.TestCase):
    def test_new_references_exist(self):
        for rel in (
            '.claude/skills/postgresql-migrations/references/normalization.md',
            '.claude/skills/postgresql-migrations/references/flyway-safety.md',
            '.claude/skills/delivery-operations/references/docker-containers.md',
            '.claude/skills/delivery-operations/references/observability-stack.md',
        ):
            self.assertTrue((ROOT/rel).is_file(), rel)

    def test_platform_reviewer_is_read_only(self):
        data = MOD.frontmatter((ROOT/'.claude/agents/platform-reviewer.md').read_text())
        self.assertEqual(set(data['tools']), {'Read','Glob','Grep'})
        self.assertEqual(data.get('skills'), ['delivery-operations'])

    def test_manifest_preserves_platform_reviewer_with_six_agents_nine_skills(self):
        data = json.loads((ROOT/'kit-manifest.json').read_text())
        self.assertEqual(len(data['agents']), 6)
        self.assertEqual(len(data['skills']), 9)
        self.assertIn('platform-reviewer', data['agents'])

    def test_routes_are_all_present(self):
        result = MOD.validate(ROOT)
        self.assertEqual(result['status'], 'PASS', result)
        self.assertEqual(result['counts']['platform_routes'], len(MOD.PLATFORM_ROUTES))

    def test_normalization_is_not_bcnf_dogma(self):
        text = (ROOT/'.claude/skills/postgresql-migrations/references/normalization.md').read_text()
        self.assertIn('Check 1NF/2NF/3NF', text)
        self.assertIn('BCNF', text)
        self.assertIn('Do not decompose blindly', text)
        self.assertIn('Deliberate denormalization', text)

    def test_flyway_applied_migration_is_immutable(self):
        text = (ROOT/'.claude/skills/postgresql-migrations/references/flyway-safety.md').read_text()
        self.assertIn('Do not edit a versioned migration', text)
        self.assertIn('Expand / migrate / contract', text)
        self.assertIn('real-PostgreSQL execution is NOT_RUN', text)

    def test_observability_blocks_high_cardinality_labels(self):
        text = (ROOT/'.claude/skills/delivery-operations/references/observability-stack.md').read_text()
        self.assertIn('Never put user ID, email, trace ID', text)
        self.assertIn('Do not use trace ID, request ID, user ID', text)
        self.assertIn('OpenTelemetry Collector or Grafana Alloy', text)

    def test_eval_definitions_are_not_claimed_run(self):
        cases = json.loads((ROOT/'evals/platform-database.json').read_text())
        self.assertGreaterEqual(len(cases), 12)
        self.assertTrue(all(c['status']=='NOT_RUN' for c in cases))
        self.assertTrue(all(len(c['criteria']) >= 3 for c in cases))

    def test_removing_platform_route_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            clone = Path(tmp)/'kit'
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            path = clone/'.claude/skills/delivery-operations/SKILL.md'
            text = path.read_text()
            text = text.replace('[observability-stack.md](references/observability-stack.md)', 'observability-stack.md')
            path.write_text(text)
            result = MOD.validate(clone)
            self.assertEqual(result['status'], 'FAIL')
            self.assertTrue(any('platform/database route missing' in e for e in result['errors']))

if __name__ == '__main__':
    unittest.main()
