"""Regression tests for the reusable kit validator."""
from __future__ import annotations
import importlib.util
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_kit", ROOT / "scripts" / "validate_kit.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "kit"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    def tearDown(self):
        self.temp.cleanup()

    def validate(self):
        return MOD.validate(self.root)

    def test_delivered_kit_passes(self):
        result = self.validate()
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(result["counts"]["agents"], 7)
        self.assertEqual(result["counts"]["skills"], 9)

    def test_missing_manifest_fails(self):
        (self.root / "kit-manifest.json").unlink()
        self.assertEqual(self.validate()["status"], "FAIL")

    def test_invalid_settings_json_fails(self):
        (self.root / ".claude/settings.json").write_text("{", encoding="utf-8")
        self.assertEqual(self.validate()["status"], "FAIL")

    def test_reviewer_write_access_fails(self):
        p = self.root / ".claude/agents/code-reviewer.md"
        text = p.read_text(encoding="utf-8").replace(
            'tools: ["Read", "Glob", "Grep"]',
            'tools: ["Read", "Glob", "Grep", "Write"]',
        )
        p.write_text(text, encoding="utf-8")
        self.assertEqual(self.validate()["status"], "FAIL")

    def test_missing_skill_fails(self):
        shutil.rmtree(self.root / ".claude/skills/react-typescript")
        self.assertEqual(self.validate()["status"], "FAIL")

    def test_openai_metadata_fails(self):
        d = self.root / ".claude/skills/react-typescript/agents"
        d.mkdir()
        (d / "openai.yaml").write_text("interface: {}", encoding="utf-8")
        self.assertEqual(self.validate()["status"], "FAIL")

    def test_local_settings_fails(self):
        (self.root / ".claude/settings.local.json").write_text("{}", encoding="utf-8")
        self.assertEqual(self.validate()["status"], "FAIL")

    def test_broken_local_link_fails(self):
        p = self.root / ".claude/skills/react-typescript/SKILL.md"
        p.write_text(p.read_text(encoding="utf-8") + "\n[broken](references/nope.md)\n", encoding="utf-8")
        self.assertEqual(self.validate()["status"], "FAIL")

    def write_suite(self, data, name="cases.json"):
        (self.root / "evals" / name).write_text(json.dumps(data), encoding="utf-8")

    def suite(self, name="cases.json"):
        return json.loads((self.root / "evals" / name).read_text(encoding="utf-8"))

    def test_eval_required_fields_cannot_be_removed(self):
        original = self.suite()
        for level, keys in (("suite", ("schema_version", "suite", "status", "cases")),
                            ("case", ("id", "input", "expected", "status"))):
            for key in keys:
                with self.subTest(level=level, key=key):
                    data = json.loads(json.dumps(original))
                    del (data if level == "suite" else data["cases"][0])[key]
                    self.write_suite(data)
                    result = self.validate()
                    self.assertEqual(result["status"], "FAIL", result)
                    self.assertTrue(any(f"missing required field {key}" in e for e in result["errors"]))

    def test_duplicate_ids_within_and_across_suites_fail(self):
        original = self.suite()
        for other in ("cases.json", "design-quality.json"):
            with self.subTest(other=other):
                data = json.loads(json.dumps(original))
                data["cases"][0]["id"] = self.suite(other)["cases"][1]["id"]
                self.write_suite(data)
                result = self.validate()
                self.assertEqual(result["status"], "FAIL", result)
                self.assertTrue(any("duplicate eval ID" in e for e in result["errors"]))

    def test_invalid_eval_values_fail_without_crashing(self):
        original = self.suite()
        mutations = [("schema_version", True), ("schema_version", 2),
                     ("suite", "  "), ("status", "PASS"), ("cases", []), ("cases", {})]
        for key, value in mutations:
            with self.subTest(key=key, value=value):
                data = json.loads(json.dumps(original)); data[key] = value
                self.write_suite(data)
                self.assertEqual(self.validate()["status"], "FAIL")
        for key, value in (("id", []), ("id", ""), ("input", " "),
                           ("expected", []), ("expected", "old format"),
                           ("expected", [""]), ("expected", [None]), ("status", "PASS"),
                           ("prompt", "legacy field")):
            with self.subTest(key=key, value=value):
                data = json.loads(json.dumps(original)); data["cases"][0][key] = value
                self.write_suite(data)
                self.assertEqual(self.validate()["status"], "FAIL")
        for data in (None, [], {"cases": [None]}):
            self.write_suite(data)
            self.assertEqual(self.validate()["status"], "FAIL")

    def test_missing_or_malformed_eval_suite_fails(self):
        path = self.root / "evals/cases.json"
        path.write_text("{", encoding="utf-8")
        self.assertEqual(self.validate()["status"], "FAIL")
        path.unlink()
        self.assertEqual(self.validate()["status"], "FAIL")

    def test_results_are_separate_from_unexecuted_definitions(self):
        directory = self.root / "evals/results"
        directory.mkdir()
        (directory / "run.json").write_text('{"status": "PASS"}', encoding="utf-8")
        result = self.validate()
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(result["counts"]["eval_suites"], 6)
        self.assertEqual(result["counts"]["eval_cases"], 103)

    def test_schema_is_used_and_unsupported_keywords_fail_closed(self):
        path = self.root / "evals/schema.json"
        original = json.loads(path.read_text(encoding="utf-8"))
        changed = dict(original, required=original["required"] + ["new_field"])
        path.write_text(json.dumps(changed), encoding="utf-8")
        self.assertEqual(self.validate()["status"], "FAIL")
        path.write_text(json.dumps(dict(original, allOf=[])), encoding="utf-8")
        self.assertEqual(self.validate()["status"], "FAIL")
        path.write_text("{", encoding="utf-8")
        self.assertEqual(self.validate()["status"], "FAIL")
        path.unlink()
        self.assertEqual(self.validate()["status"], "FAIL")

    def test_broken_and_escaping_repo_root_skill_paths_fail(self):
        path = self.root / ".claude/agents/implementer.md"
        original = path.read_text(encoding="utf-8")
        for target in ("missing/SKILL.md", "../../kit-manifest.json"):
            with self.subTest(target=target):
                path.write_text(original + f"\nRead `.claude/skills/{target}`.\n", encoding="utf-8")
                result = self.validate()
                self.assertEqual(result["status"], "FAIL", result)
                self.assertTrue(any("invalid repository-root skill path" in e for e in result["errors"]))

    def test_financial_and_planning_routes_resolve_to_declared_skills(self):
        manifest = json.loads((self.root / "kit-manifest.json").read_text(encoding="utf-8"))
        for source, skill in (("agents/implementer.md", "financial-calculations"),
                              ("agents/test-engineer.md", "financial-calculations"),
                              ("policies/core.md", "change-planning")):
            with self.subTest(source=source):
                text = (self.root / ".claude" / source).read_text(encoding="utf-8")
                targets = re.findall(r"`(\.claude/skills/[^`]+/SKILL.md)`", text)
                self.assertIn(f".claude/skills/{skill}/SKILL.md", targets)
                for target in targets:
                    metadata = MOD.frontmatter((self.root / target).read_text(encoding="utf-8"))
                    self.assertIn(metadata["name"], manifest["skills"])
                    self.assertEqual(metadata["name"], Path(target).parent.name)

    def test_agent_capabilities_and_selective_preloads(self):
        readonly = MOD.READ_ONLY_REVIEWERS | {"implementation-explainer"}
        for path in (self.root / ".claude/agents").glob("*.md"):
            data = MOD.frontmatter(path.read_text(encoding="utf-8"))
            with self.subTest(agent=path.stem):
                expected = {"Read", "Glob", "Grep"}
                if path.stem not in readonly:
                    expected |= {"Edit", "Write", "Bash"}
                self.assertEqual(set(data["tools"]), expected)
                self.assertNotIn("financial-calculations", data.get("skills", []))
                self.assertNotIn("change-planning", data.get("skills", []))
                self.assertNotIn("effort", data)


class FrontmatterTests(unittest.TestCase):
    def test_frontmatter_parses_json_compatible_yaml(self):
        value = MOD.frontmatter('---\nname: "x"\ntools: ["Read"]\n---\nbody')
        self.assertEqual(value["name"], "x")
        self.assertEqual(value["tools"], ["Read"])

    def test_duplicate_key_rejected(self):
        with self.assertRaises(ValueError):
            MOD.frontmatter('---\nname: "a"\nname: "b"\n---')

if __name__ == "__main__":
    unittest.main()