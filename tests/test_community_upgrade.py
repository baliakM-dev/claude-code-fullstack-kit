"""Static integration/provenance regressions, not executed AI or Spring tests."""
import hashlib
import importlib.util
import json
import shutil
import struct
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('community_kit_validator', ROOT/'scripts/validate_kit.py')
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class CommunityUpgradeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)/'kit'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))

    def tearDown(self):
        self.temp.cleanup()

    def change_provenance(self, change):
        p = self.root/'docs/upstream-sources.json'
        data = json.loads(p.read_text()); change(data); p.write_text(json.dumps(data))
        report = MOD.validate(self.root)
        self.assertEqual(report['status'], 'FAIL', report)
        self.assertTrue(any('community provenance invalid' in x for x in report['errors']), report)

    def test_all_routes_present(self):
        report = MOD.validate(self.root)
        self.assertEqual(report['status'], 'PASS', report)
        self.assertEqual(report['counts']['community_routes'], 21)
        self.assertEqual(len(set(MOD.COMMUNITY_ROUTES)), 21)

    def test_each_route_required(self):
        for source, target in MOD.COMMUNITY_ROUTES:
            with self.subTest(source=source, target=target):
                p = self.root/source; text = p.read_text()
                matches = [x for x in MOD.LINK.findall(text)
                           if not urlparse(x).scheme and not x.startswith('#')
                           and (p.parent/unquote(x.split('#', 1)[0])).resolve() == (self.root/target).resolve()]
                self.assertTrue(matches)
                changed = text
                for match in matches: changed = changed.replace(']('+match+')', '] removed')
                p.write_text(changed)
                try:
                    result = MOD.validate(self.root)
                    self.assertEqual(result['status'], 'FAIL', result)
                    self.assertTrue(any('required community route missing' in e for e in result['errors']), result)
                finally: p.write_text(text)

    def test_new_reference_files_required(self):
        data = json.loads((self.root/'docs/upstream-sources.json').read_text())
        for item in data['files']:
            for name in item['destinations']:
                with self.subTest(name=name):
                    p = self.root/name; original = p.read_bytes(); p.unlink()
                    try: self.assertEqual(MOD.validate(self.root)['status'], 'FAIL')
                    finally: p.write_bytes(original)

    def test_commit_must_be_pinned(self):
        self.change_provenance(lambda d: d.update(commit='main'))

    def test_blob_identity_required(self):
        self.change_provenance(lambda d: d['files'][0].update(git_blob_sha='unknown'))

    def test_source_url_must_match_commit(self):
        self.change_provenance(lambda d: d['files'][0].update(url='https://github.com/example/tree/main'))

    def test_destination_cannot_escape(self):
        self.change_provenance(lambda d: d['files'][0].update(destinations=['../../outside']))

    def test_full_license_notice_required(self):
        for name in ('spring-backend', 'postgresql-migrations', 'test-verification'):
            with self.subTest(name=name):
                p = self.root/'.claude/skills'/name/'LICENSE-UPSTREAM.txt'
                original = p.read_bytes(); p.write_text('MIT License only')
                try:
                    result = MOD.validate(self.root)
                    self.assertEqual(result['status'], 'FAIL')
                    self.assertTrue(any('MIT notice' in x for x in result['errors']))
                finally: p.write_bytes(original)

    def test_example_known_vector_independently(self):
        fields = ['receipt:v1','EUR','12.30','2026-09-23','Consulting']
        binary = b''.join(struct.pack('>I',len(s.encode('utf-8')))+s.encode('utf-8') for s in fields)
        expected = hashlib.sha256(binary).hexdigest()
        test = (self.root/'.claude/skills/spring-backend/assets/idempotency/CommandFingerprintTest.java').read_text()
        self.assertIn('equal("'+expected+'", hash("12.30", "Consulting"))', test)

    def test_model_scenarios_are_unexecuted_definitions(self):
        d = json.loads((self.root/'evals/community-patterns.json').read_text())
        self.assertEqual(len(d['cases']), 16)
        self.assertEqual(len({c['id'] for c in d['cases']}), 16)
        self.assertTrue(all(c['status']=='NOT_RUN' and c['input'] and c['expected'] for c in d['cases']))

    def test_existing_preloads_preserved_with_platform_reviewer(self):
        d = json.loads((self.root/'kit-manifest.json').read_text())
        self.assertEqual(d['kit_version'], '1.5.1')
        self.assertEqual(len(d['agents']), 6); self.assertEqual(len(d['skills']), 9)
        for p in (self.root/'.claude/agents').glob('*.md'):
            meta = MOD.frontmatter(p.read_text())
            expected = {'code-reviewer': ['evidence-review'], 'security-reviewer': ['application-security'], 'test-engineer': ['test-verification'], 'platform-reviewer': ['delivery-operations'], 'frontend-reviewer': ['react-typescript']}
            self.assertEqual(meta.get('skills', []), expected.get(p.stem, []))
            self.assertNotIn('Agent', meta['tools'])

    def test_entrypoints_stay_small(self):
        for name in ('spring-backend','postgresql-migrations','test-verification'):
            text = (self.root/'.claude/skills'/name/'SKILL.md').read_text()
            self.assertLess(len(text.splitlines()), 100)


if __name__ == '__main__': unittest.main()
