#!/usr/bin/env python3
"""Static validation for the reusable Claude Code full-stack kit.

Python 3.10+, standard library only. This validates repository structure,
metadata, local Markdown links and selected safety invariants. It does not
execute Claude Code, prove agent behavior, or prove application security.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
READ_ONLY_REVIEWERS = {
    "code-reviewer",
    "security-reviewer",
    "platform-reviewer",
    "frontend-reviewer",
}
KNOWN_TOOLS = {"Read", "Glob", "Grep", "Edit", "Write", "Bash"}
AGENT_KEYS = {
    "name",
    "description",
    "tools",
    "model",
    "permissionMode",
    "maxTurns",
    "skills",
}
SKILL_KEYS = {"name", "description"}
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"\[[^\]\n]+\]\(([^\s)]+)\)")


def frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("Missing opening frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("Missing closing frontmatter delimiter") from exc

    result: dict[str, Any] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep or not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", key):
            raise ValueError("Unsupported metadata key syntax")
        if key in result:
            raise ValueError(f"Duplicate metadata key: {key}")
        raw = value.strip()
        if not raw:
            parsed: Any = ""
        else:
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Metadata value for {key} must use JSON-compatible YAML") from exc
        result[key] = parsed
    return result


def _local_markdown_files(root: Path) -> list[Path]:
    files = list((root / ".claude").rglob("*.md"))
    for relative in (
        "README.md",
        "THIRD_PARTY_NOTICES.md",
        "evals/README.md",
        "verification/README.md",
        "templates/CLAUDE.md",
        "templates/project-profile.md",
    ):
        path = root / relative
        if path.is_file():
            files.append(path)
    return files


def _validate_local_links(root: Path, errors: list[str]) -> int:
    checked = 0
    for path in _local_markdown_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{path.relative_to(root)}: cannot read Markdown: {exc}")
            continue
        for raw in LINK.findall(text):
            if raw.startswith("#") or urlparse(raw).scheme:
                continue
            relative = unquote(raw.split("#", 1)[0])
            if not relative:
                continue
            target = (path.parent / relative).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                errors.append(
                    f"{path.relative_to(root)}: local link escapes repository root: {raw}"
                )
                continue
            if not target.exists():
                errors.append(
                    f"{path.relative_to(root)}: broken local link: {raw}"
                )
            checked += 1
    return checked


def _schema_errors(value: Any, schema: dict[str, Any], where: str) -> list[str]:
    """Validate only the JSON Schema keywords used by evals/schema.json.

    This is deliberately not a general JSON Schema implementation. Fail closed
    if the shipped schema starts using unsupported keywords or types.
    """
    supported = {"$schema", "title", "type", "const", "properties", "required",
                 "additionalProperties", "items", "minItems", "minLength", "pattern"}
    if set(schema) - supported:
        raise ValueError(f"unsupported schema keywords: {sorted(set(schema) - supported)}")
    types = {"object": dict, "array": list, "string": str, "integer": int}
    kind = schema.get("type")
    if kind not in types:
        raise ValueError(f"unsupported schema type: {kind}")
    if type(value) is not types[kind]:
        return [f"{where}: expected {kind}"]
    errors = []
    if "const" in schema and value != schema["const"]:
        errors.append(f"{where}: must equal {schema['const']!r}")
    if kind == "object":
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{where}: missing required field {key}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in sorted(set(value) - set(properties)):
                errors.append(f"{where}: unexpected field {key}")
        for key, child in properties.items():
            if key in value:
                errors.extend(_schema_errors(value[key], child, f"{where}.{key}"))
    elif kind == "array":
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{where}: too few items")
        for index, item in enumerate(value):
            errors.extend(_schema_errors(item, schema["items"], f"{where}[{index}]"))
    elif kind == "string":
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{where}: string too short")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{where}: string does not match required pattern")
    return errors


def _validate_evals(root: Path, errors: list[str]) -> tuple[int, int]:
    schema_path = root / "evals/schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"evals/schema.json: {exc}")
        return 0, 0
    suites = cases = 0
    seen: dict[str, str] = {}
    for path in sorted((root / "evals").glob("*.json")):
        if path == schema_path:
            continue
        where = str(path.relative_to(root))
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            problems = _schema_errors(data, schema, where)
        except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
            errors.append(f"{where}: invalid eval or schema: {exc}")
            continue
        errors.extend(problems)
        if problems:
            continue
        suites += 1
        for case in data["cases"]:
            cases += 1
            case_id = case["id"]
            if case_id in seen:
                errors.append(f"{where}: duplicate eval ID {case_id!r}; first in {seen[case_id]}")
            else:
                seen[case_id] = where
    if not suites:
        errors.append("evals: no valid suites found")
    return suites, cases


def _validate_skill_paths(root: Path, errors: list[str]) -> None:
    paths = list((root / ".claude/agents").glob("*.md"))
    paths.append(root / ".claude/policies/core.md")
    for path in paths:
        if not path.is_file():
            continue
        for relative in re.findall(r"`(\.claude/skills/[^`]+)`", path.read_text(encoding="utf-8")):
            target = (root / relative).resolve()
            if not target.is_relative_to((root / ".claude/skills").resolve()) or not target.is_file():
                errors.append(f"{path.relative_to(root)}: invalid repository-root skill path: {relative}")


def validate(root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    counts = {
        "agents": 0,
        "skills": 0,
        "local_links": 0,
    }

    def fail(where: str, message: str) -> None:
        errors.append(f"{where}: {message}")

    manifest_path = root / "kit-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "status": "FAIL",
            "counts": counts,
            "errors": [f"kit-manifest.json: {exc}"],
            "warnings": warnings,
        }

    if manifest.get("schema_version") != 1:
        fail("kit-manifest.json", "schema_version must be 1")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("kit_version", ""))):
        fail("kit-manifest.json", "kit_version must be semantic x.y.z")

    agents = manifest.get("agents")
    skills = manifest.get("skills")
    required = manifest.get("required_files")
    if not isinstance(agents, list) or not all(isinstance(x, str) for x in agents):
        fail("kit-manifest.json", "agents must be a string list")
        agents = []
    if not isinstance(skills, list) or not all(isinstance(x, str) for x in skills):
        fail("kit-manifest.json", "skills must be a string list")
        skills = []
    if not isinstance(required, list) or not all(isinstance(x, str) for x in required):
        fail("kit-manifest.json", "required_files must be a string list")
        required = []

    for relative in required:
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            fail("kit-manifest.json", f"required file escapes repository: {relative}")
            continue
        if not path.is_file():
            fail("kit-manifest.json", f"missing required file: {relative}")

    agent_dir = root / ".claude" / "agents"
    actual_agents = sorted(p.stem for p in agent_dir.glob("*.md"))
    if sorted(agents) != actual_agents:
        fail(
            ".claude/agents",
            f"manifest mismatch: manifest={sorted(agents)} actual={actual_agents}",
        )

    for name in actual_agents:
        path = agent_dir / f"{name}.md"
        try:
            data = frontmatter(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            fail(str(path.relative_to(root)), str(exc))
            continue
        unexpected = set(data) - AGENT_KEYS
        if unexpected:
            fail(str(path.relative_to(root)), f"unexpected metadata keys: {sorted(unexpected)}")
        if data.get("name") != name or not NAME.fullmatch(name):
            fail(str(path.relative_to(root)), "agent name must match filename")
        tools = data.get("tools")
        if not isinstance(tools, list) or not tools or len(tools) != len(set(tools)):
            fail(str(path.relative_to(root)), "tools must be a non-empty unique list")
            tools = []
        unknown = set(tools) - KNOWN_TOOLS
        if unknown:
            fail(str(path.relative_to(root)), f"unexpected tools: {sorted(unknown)}")
        if "Agent" in tools:
            fail(str(path.relative_to(root)), "nested Agent delegation is not allowed")
        if name in READ_ONLY_REVIEWERS and set(tools) != {"Read", "Glob", "Grep"}:
            fail(str(path.relative_to(root)), "reviewers must be read-only: Read/Glob/Grep")
        if data.get("permissionMode") == "bypassPermissions":
            fail(str(path.relative_to(root)), "bypassPermissions is forbidden")
        preloads = data.get("skills", [])
        if not isinstance(preloads, list) or not all(isinstance(x, str) for x in preloads):
            fail(str(path.relative_to(root)), "skills preload must be a string list")
        else:
            for preload in preloads:
                if preload not in skills:
                    fail(str(path.relative_to(root)), f"preloaded skill not in manifest: {preload}")
        counts["agents"] += 1

    skill_dir = root / ".claude" / "skills"
    actual_skills = sorted(p.name for p in skill_dir.iterdir() if p.is_dir()) if skill_dir.is_dir() else []
    if sorted(skills) != actual_skills:
        fail(
            ".claude/skills",
            f"manifest mismatch: manifest={sorted(skills)} actual={actual_skills}",
        )

    for name in actual_skills:
        path = skill_dir / name / "SKILL.md"
        if not path.is_file():
            fail(str((skill_dir / name).relative_to(root)), "missing SKILL.md")
            continue
        try:
            data = frontmatter(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            fail(str(path.relative_to(root)), str(exc))
            continue
        unexpected = set(data) - SKILL_KEYS
        if unexpected:
            fail(str(path.relative_to(root)), f"unexpected metadata keys: {sorted(unexpected)}")
        if data.get("name") != name or not NAME.fullmatch(name):
            fail(str(path.relative_to(root)), "skill name must match directory")
        if not isinstance(data.get("description"), str) or not data["description"].strip():
            fail(str(path.relative_to(root)), "skill description must be non-empty")
        counts["skills"] += 1

    openai_metadata = list(skill_dir.glob("*/agents/openai.yaml"))
    if openai_metadata:
        fail(".claude/skills", "Claude Code-only kit must not ship agents/openai.yaml")

    if (root / ".claude" / "settings.local.json").exists():
        fail(".claude/settings.local.json", "local Claude settings must not be committed")

    settings_path = root / ".claude" / "settings.json"
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        permissions = settings.get("permissions", {})
        if permissions.get("defaultMode") == "bypassPermissions":
            fail(".claude/settings.json", "bypassPermissions is forbidden")
        allow = permissions.get("allow", [])
        if any(x in {"Bash(*)", "Read(**)", "Edit(**)", "Write(**)"} for x in allow):
            fail(".claude/settings.json", "blanket allow rules are forbidden")
        deny = permissions.get("deny", [])
        for required_deny in ("Bash(git push *)", "Bash(git reset *)", "Read(**/.env)"):
            if required_deny not in deny:
                fail(".claude/settings.json", f"missing safety deny rule: {required_deny}")
    except (OSError, json.JSONDecodeError, AttributeError) as exc:
        fail(".claude/settings.json", f"invalid settings JSON: {exc}")

    for skill in ("spring-backend", "postgresql-migrations", "test-verification"):
        license_path = skill_dir / skill / "LICENSE-UPSTREAM.txt"
        if not license_path.is_file():
            fail(str(license_path.relative_to(root)), "missing upstream license notice")
        else:
            text = license_path.read_text(encoding="utf-8", errors="replace")
            if "MIT License" not in text:
                fail(str(license_path.relative_to(root)), "upstream MIT notice appears incomplete")

    notice = root / "THIRD_PARTY_NOTICES.md"
    if notice.is_file():
        text = notice.read_text(encoding="utf-8", errors="replace")
        if "rrezartprebreza/spring-boot-skills" not in text:
            fail("THIRD_PARTY_NOTICES.md", "missing recorded upstream attribution")

    counts["eval_suites"], counts["eval_cases"] = _validate_evals(root, errors)
    _validate_skill_paths(root, errors)
    counts["local_links"] = _validate_local_links(root, errors)

    warnings.append(
        "Static repository checks only: Claude Code runtime, model behavior and application tests are NOT_RUN."
    )
    return {
        "status": "FAIL" if errors else "PASS",
        "counts": counts,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()
    report = validate(args.root)
    if args.json:
        print(json.dumps(report, ensure_ascii=True, indent=2))
    else:
        print(f"Kit lint: {report['status']}; counts={report['counts']}")
        for message in report["errors"]:
            print("ERROR: " + message)
        for message in report["warnings"]:
            print("NOTE: " + message)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
