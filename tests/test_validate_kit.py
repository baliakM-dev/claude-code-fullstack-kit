"""Regression tests for the static kit validator, not AI-agent behavior tests."""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_kit", ROOT / "scripts" / "validate_kit.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class MetadataTests(unittest.TestCase):
    def test_json_yaml_subset(self):
        result = MOD.frontmatter('---\nname: "sample"\ntools: ["Read", "Grep"]\nmaxTurns: 18\n---\nBody')
        self.assertEqual(result["tools"], ["Read", "Grep"])
        self.assertEqual(result["maxTurns"], 18)

    def test_missing_open_delimiter(self):
        with self.assertRaises(ValueError): MOD.frontmatter('name: "sample"')

    def test_missing_close_delimiter(self):
        with self.assertRaises(ValueError): MOD.frontmatter('---\nname: "sample"')

    def test_duplicate_key_rejected(self):
        with self.assertRaises(ValueError): MOD.frontmatter('---\nname: "a"\nname: "b"\n---')

    def test_malformed_list_rejected(self):
        with self.assertRaises(ValueError): MOD.frontmatter('---\ntools: ["Read"\n---')

    def test_unicode_description(self):
        result = MOD.frontmatter('---\ndescription: "Overenie \\u00faprav"\n---')
        self.assertEqual(result["description"], "Overenie \u00faprav")


class KitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "kit"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))

    def tearDown(self):
        self.temp.cleanup()

    def edit(self, relative, old, new):
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def failed(self, fragment):
        report = MOD.validate(self.root)
        self.assertEqual(report["status"], "FAIL", report)
        self.assertTrue(any(fragment in e for e in report["errors"]), report)

    def test_delivered_kit_passes(self):
        result = MOD.validate(self.root)
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(result["counts"]["agents"], 6)
        self.assertEqual(result["counts"]["skills"], 9)

    def test_missing_manifest_fails(self):
        (self.root / "kit-manifest.json").unlink()
        self.failed("kit-manifest.json")

    def test_invalid_settings_json_fails(self):
        (self.root / ".claude/settings.json").write_text('{', encoding="utf-8")
        self.failed("settings.json")

    def test_reviewer_shell_rejected(self):
        self.edit('.claude/agents/code-reviewer.md', '["Read", "Glob", "Grep"]', '["Read", "Glob", "Grep", "Bash"]')
        self.failed("reviewers must")

    def test_security_reviewer_write_rejected(self):
        self.edit('.claude/agents/security-reviewer.md', '["Read", "Glob", "Grep"]', '["Read", "Glob", "Grep", "Write"]')
        self.failed("reviewers must")

    def test_nested_delegation_rejected(self):
        self.edit('.claude/agents/implementer.md', '"Write", "Bash"]', '"Write", "Bash", "Agent"]')
        self.failed("Unexpected, duplicate")

    def test_bypass_mode_rejected(self):
        self.edit('.claude/agents/implementer.md', 'permissionMode: "default"', 'permissionMode: "bypassPermissions"')
        self.failed("permissionMode")

    def test_missing_preload_rejected(self):
        self.edit('.claude/agents/code-reviewer.md', 'skills: ["evidence-review"]', 'skills: ["nonexistent"]')
        self.failed("Preloaded skill")

    def test_skill_name_mismatch_rejected(self):
        self.edit('.claude/skills/react-typescript/SKILL.md', 'name: "react-typescript"', 'name: "wrong-name"')
        self.failed("Skill name")

    def test_missing_skill_rejected(self):
        shutil.rmtree(self.root / '.claude/skills/react-typescript')
        self.failed("manifest mismatch")

    def test_missing_reference_rejected(self):
        (self.root / '.claude/skills/application-security/references/bff-keycloak.md').unlink()
        self.failed("broken local link")

    def test_external_link_not_treated_as_file(self):
        with (self.root/'README.md').open('a',encoding='utf-8') as f:
            f.write('\n[External](https://example.invalid/not-fetched)\n')
        self.assertEqual(MOD.validate(self.root)["status"], "PASS")

    def test_local_path_escape_rejected(self):
        with (self.root/'README.md').open('a',encoding='utf-8') as f:
            f.write('\n[Bad](../../outside.md)\n')
        self.failed("escapes kit root")

    def test_allow_rule_rejected(self):
        path = self.root/'.claude/settings.json'
        value = json.loads(path.read_text())
        value['permissions']['allow'] = ['Bash(*)']
        path.write_text(json.dumps(value), encoding='utf-8')
        self.failed("No blanket")

    def test_secret_guardrail_required(self):
        path = self.root/'.claude/settings.json'
        value = json.loads(path.read_text())
        value['permissions']['deny'].remove('Read(**/.env)')
        path.write_text(json.dumps(value), encoding='utf-8')
        self.failed("guardrail missing")

    def test_automatic_hook_rejected(self):
        path = self.root/'.claude/settings.json'
        value = json.loads(path.read_text())
        value['hooks'] = {}
        path.write_text(json.dumps(value), encoding='utf-8')
        self.failed("No automatic hooks")

    def test_unbounded_turns_rejected(self):
        self.edit('.claude/agents/implementer.md','maxTurns: 35','maxTurns: 1000')
        self.failed("maxTurns")

    def test_policy_reference_required(self):
        self.edit('CLAUDE.md','@.claude/policies/core.md','a policy elsewhere')
        self.failed("Missing shared policy")

    def test_oversized_skill_rejected(self):
        path = self.root/'.claude/skills/react-typescript/SKILL.md'
        with path.open('a',encoding='utf-8') as f: f.write('\n' * 500)
        self.failed("too large")

    def test_manifest_path_escape_rejected(self):
        path = self.root/'kit-manifest.json'
        value = json.loads(path.read_text())
        value['required_files'].append('../outside.md')
        path.write_text(json.dumps(value),encoding='utf-8')
        self.failed("path escapes root")


if __name__ == '__main__':
    unittest.main()
