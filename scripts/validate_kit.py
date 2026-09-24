#!/usr/bin/env python3
"""Lint this kit's controlled metadata subset, links and safety configuration.

Python 3.10+, standard library only. This is NOT a Claude Code runtime validator,
a generic YAML parser, a security sandbox, or a behavioral model evaluation.
Frontmatter uses JSON-form scalar/list values, which are also valid YAML.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
READ_ONLY = {"code-reviewer", "security-reviewer", "platform-reviewer", "frontend-reviewer"}
KNOWN_TOOLS = {"Read", "Glob", "Grep", "Edit", "Write", "Bash"}
AGENT_KEYS = {"name", "description", "tools", "model", "permissionMode", "maxTurns", "skills"}
SKILL_KEYS = {"name", "description"}
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"\[[^\]\n]+\]\(([^\s)]+)\)")


# Required Markdown routes only; not semantic or model-behavior validation.
QUALITY_ROUTES = (
    ('.claude/agents/implementer.md', '.claude/skills/spring-backend/SKILL.md'),
    ('.claude/agents/code-reviewer.md', '.claude/skills/spring-backend/SKILL.md'),
    ('.claude/skills/evidence-review/SKILL.md', '.claude/skills/spring-backend/SKILL.md'),
    ('.claude/skills/spring-backend/SKILL.md', '.claude/skills/spring-backend/references/design-quality.md'),
    ('.claude/skills/spring-backend/SKILL.md', '.claude/skills/spring-backend/references/quality-verification.md'),
    ('.claude/skills/test-verification/SKILL.md', '.claude/skills/spring-backend/references/quality-verification.md'),
    ('docs/tasks/000-bootstrap.md', '.claude/skills/spring-backend/references/quality-verification.md'),
    ('docs/tasks/002-received-payments.md', '.claude/skills/spring-backend/references/quality-verification.md'),
    ('docs/tasks/003-first-calculation.md', '.claude/skills/spring-backend/references/quality-verification.md'),
)


# Presence of these links is NOT security enforcement or behavioral evaluation.
SECURITY_ROUTES = (
    ('.claude/agents/implementer.md', '.claude/skills/application-security/SKILL.md'),
    ('.claude/agents/code-reviewer.md', '.claude/skills/application-security/SKILL.md'),
    ('.claude/agents/security-reviewer.md', '.claude/skills/application-security/SKILL.md'),
    ('.claude/agents/test-engineer.md', '.claude/skills/application-security/references/security-verification.md'),
    ('.claude/skills/spring-backend/SKILL.md', '.claude/skills/application-security/SKILL.md'),
    ('.claude/skills/application-security/SKILL.md', '.claude/skills/application-security/references/spring-security.md'),
    ('.claude/skills/application-security/SKILL.md', '.claude/skills/application-security/references/browser-csrf-cors.md'),
    ('.claude/skills/application-security/SKILL.md', '.claude/skills/application-security/references/bff-keycloak.md'),
    ('.claude/skills/application-security/SKILL.md', '.claude/skills/application-security/references/resource-server.md'),
    ('.claude/skills/application-security/SKILL.md', '.claude/skills/application-security/references/authorization-data.md'),
    ('.claude/skills/application-security/SKILL.md', '.claude/skills/application-security/references/abuse-deployment.md'),
    ('.claude/skills/application-security/SKILL.md', '.claude/skills/application-security/references/security-verification.md'),
    ('.claude/skills/test-verification/SKILL.md', '.claude/skills/application-security/references/security-verification.md'),
    ('.claude/skills/evidence-review/SKILL.md', '.claude/skills/application-security/SKILL.md'),
    ('.claude/skills/react-typescript/SKILL.md', '.claude/skills/application-security/references/browser-csrf-cors.md'),
    ('.claude/skills/delivery-operations/SKILL.md', '.claude/skills/application-security/references/abuse-deployment.md'),
    ('docs/tasks/000-bootstrap.md', '.claude/skills/application-security/references/spring-security.md'),
    ('docs/tasks/001-bff-identity.md', '.claude/skills/application-security/references/security-verification.md'),
    ('docs/tasks/001-bff-identity.md', 'docs/security-profile.md'),
    ('docs/tasks/002-received-payments.md', '.claude/skills/application-security/references/security-verification.md'),
    ('docs/tasks/003-first-calculation.md', '.claude/skills/application-security/references/security-verification.md'),
    ('docs/security-profile.md', '.claude/skills/application-security/references/security-verification.md'),
)




PLATFORM_ROUTES = (
    ('.claude/agents/implementer.md', '.claude/skills/postgresql-migrations/SKILL.md'),
    ('.claude/agents/implementer.md', '.claude/skills/delivery-operations/SKILL.md'),
    ('.claude/agents/platform-reviewer.md', '.claude/skills/delivery-operations/SKILL.md'),
    ('.claude/agents/platform-reviewer.md', '.claude/skills/postgresql-migrations/SKILL.md'),
    ('.claude/agents/platform-reviewer.md', '.claude/skills/application-security/SKILL.md'),
    ('.claude/skills/postgresql-migrations/SKILL.md', '.claude/skills/postgresql-migrations/references/normalization.md'),
    ('.claude/skills/postgresql-migrations/SKILL.md', '.claude/skills/postgresql-migrations/references/flyway-safety.md'),
    ('.claude/skills/delivery-operations/SKILL.md', '.claude/skills/delivery-operations/references/docker-containers.md'),
    ('.claude/skills/delivery-operations/SKILL.md', '.claude/skills/delivery-operations/references/observability-stack.md'),
    ('docs/tasks/000-bootstrap.md', '.claude/skills/postgresql-migrations/references/normalization.md'),
    ('docs/tasks/000-bootstrap.md', '.claude/skills/delivery-operations/references/docker-containers.md'),
)



FRONTEND_ROUTES = (
    ('.claude/agents/implementer.md', '.claude/skills/react-typescript/SKILL.md'),
    ('.claude/agents/code-reviewer.md', '.claude/skills/react-typescript/SKILL.md'),
    ('.claude/agents/frontend-reviewer.md', '.claude/skills/react-typescript/SKILL.md'),
    ('.claude/agents/frontend-reviewer.md', '.claude/skills/application-security/SKILL.md'),
    ('.claude/skills/react-typescript/SKILL.md', '.claude/skills/react-typescript/references/server-state-api.md'),
    ('.claude/skills/react-typescript/SKILL.md', '.claude/skills/react-typescript/references/forms-state.md'),
    ('.claude/skills/react-typescript/SKILL.md', '.claude/skills/react-typescript/references/architecture-routing.md'),
    ('.claude/skills/react-typescript/SKILL.md', '.claude/skills/react-typescript/references/testing-accessibility.md'),
    ('.claude/skills/react-typescript/SKILL.md', '.claude/skills/application-security/references/browser-csrf-cors.md'),
    ('.claude/skills/react-typescript/SKILL.md', '.claude/skills/application-security/references/bff-keycloak.md'),
    ('.claude/skills/test-verification/SKILL.md', '.claude/skills/react-typescript/references/testing-accessibility.md'),
)

COMMUNITY_ROUTES = (('.claude/skills/spring-backend/SKILL.md', '.claude/skills/spring-backend/references/null-safety.md'), ('.claude/skills/spring-backend/SKILL.md', '.claude/skills/spring-backend/references/idempotent-commands.md'), ('.claude/skills/spring-backend/SKILL.md', '.claude/skills/spring-backend/references/transaction-failure-patterns.md'), ('.claude/skills/spring-backend/SKILL.md', '.claude/skills/postgresql-migrations/SKILL.md'), ('.claude/skills/postgresql-migrations/SKILL.md', '.claude/skills/postgresql-migrations/references/jpa-modeling.md'), ('.claude/skills/postgresql-migrations/SKILL.md', '.claude/skills/spring-backend/references/idempotent-commands.md'), ('.claude/skills/postgresql-migrations/SKILL.md', '.claude/skills/spring-backend/references/transaction-failure-patterns.md'), ('.claude/skills/postgresql-migrations/SKILL.md', '.claude/skills/test-verification/references/spring-data-evidence.md'), ('.claude/skills/test-verification/SKILL.md', '.claude/skills/test-verification/references/spring-data-evidence.md'), ('.claude/skills/test-verification/SKILL.md', '.claude/skills/postgresql-migrations/references/jpa-modeling.md'), ('.claude/skills/test-verification/SKILL.md', '.claude/skills/spring-backend/references/null-safety.md'), ('.claude/skills/test-verification/SKILL.md', '.claude/skills/spring-backend/references/idempotent-commands.md'), ('.claude/skills/test-verification/SKILL.md', '.claude/skills/spring-backend/references/transaction-failure-patterns.md'), ('.claude/skills/spring-backend/references/idempotent-commands.md', '.claude/skills/spring-backend/assets/idempotency/request-results.sql'), ('.claude/skills/spring-backend/references/idempotent-commands.md', '.claude/skills/spring-backend/assets/idempotency/CommandFingerprint.java'), ('.claude/skills/spring-backend/references/idempotent-commands.md', '.claude/skills/spring-backend/assets/idempotency/CommandFingerprintTest.java'), ('.claude/skills/spring-backend/references/idempotent-commands.md', '.claude/skills/spring-backend/scripts/verify_java_examples.py'), ('docs/tasks/000-bootstrap.md', '.claude/skills/spring-backend/references/null-safety.md'), ('docs/tasks/002-received-payments.md', '.claude/skills/postgresql-migrations/references/jpa-modeling.md'), ('docs/tasks/002-received-payments.md', '.claude/skills/spring-backend/references/idempotent-commands.md'), ('docs/tasks/003-first-calculation.md', '.claude/skills/spring-backend/references/null-safety.md'))

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
        try:
            result[key] = json.loads(value.strip())
        except json.JSONDecodeError as exc:
            raise ValueError(f"{key}: use a JSON-form quoted scalar/list in this kit") from exc
    return result


def validate(root: Path) -> dict[str, Any]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    counts: dict[str, int] = {"agents": 0, "skills": 0, "local_links": 0, "design_routes": 0, "security_routes": 0, "community_routes": 0, "platform_routes": 0, "frontend_routes": 0}

    def fail(path: Path | str, message: str) -> None:
        label = str(path.relative_to(root)) if isinstance(path, Path) else path
        errors.append(f"{label}: {message}")

    try:
        manifest = json.loads((root / "kit-manifest.json").read_text(encoding="utf-8"))
        if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
            raise ValueError("Expected manifest schema_version 1")
        expected_agents = manifest["agents"]
        expected_skills = manifest["skills"]
        required_files = manifest["required_files"]
        for key, values in (("agents", expected_agents), ("skills", expected_skills), ("required_files", required_files)):
            if not isinstance(values, list) or not values or not all(isinstance(x, str) for x in values):
                raise ValueError(f"{key} must be a nonempty string list")
            if len(values) != len(set(values)):
                raise ValueError(f"{key} contains duplicates")
        if not READ_ONLY.issubset(expected_agents):
            raise ValueError("Required independent reviewer roles are missing")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return {"status": "FAIL", "counts": counts, "errors": [f"kit-manifest.json: {exc}"], "warnings": []}

    for value in required_files:
        path = (root / value).resolve()
        if not path.is_relative_to(root):
            fail("kit-manifest.json", f"path escapes root: {value}")
        elif not path.is_file():
            fail(value, "required file is missing")

    skills_root = root / ".claude" / "skills"
    skill_paths = sorted(skills_root.glob("*/SKILL.md"))
    actual_skills = {path.parent.name for path in skill_paths}
    if actual_skills != set(expected_skills):
        fail("skills", f"manifest mismatch; missing={sorted(set(expected_skills)-actual_skills)}, extra={sorted(actual_skills-set(expected_skills))}")
    counts["skills"] = len(skill_paths)
    for path in skill_paths:
        try:
            data = frontmatter(path.read_text(encoding="utf-8"))
            if set(data) != SKILL_KEYS:
                raise ValueError("Skill metadata must have only name and description")
            if data["name"] != path.parent.name or not NAME.fullmatch(data["name"]):
                raise ValueError("Skill name must match directory and use lowercase hyphens")
            if not isinstance(data["description"], str) or not 20 <= len(data["description"]) <= 1024:
                raise ValueError("Description length must be 20..1024 characters")
            if len(path.read_text(encoding="utf-8").splitlines()) >= 500:
                raise ValueError("Entrypoint is too large for this kit")
        except (OSError, ValueError, TypeError, KeyError) as exc:
            fail(path, str(exc))

    agents_root = root / ".claude" / "agents"
    agent_paths = sorted(agents_root.glob("*.md"))
    actual_agents = {path.stem for path in agent_paths}
    if actual_agents != set(expected_agents):
        fail("agents", "Agent names do not match manifest")
    counts["agents"] = len(agent_paths)
    for path in agent_paths:
        try:
            data = frontmatter(path.read_text(encoding="utf-8"))
            required = AGENT_KEYS - {"skills"}
            if not required.issubset(data) or not set(data).issubset(AGENT_KEYS):
                raise ValueError("Unexpected or missing agent metadata keys")
            if data["name"] != path.stem or not NAME.fullmatch(data["name"]):
                raise ValueError("Agent name mismatch")
            if not isinstance(data["description"], str) or len(data["description"]) < 20:
                raise ValueError("Agent description is missing or too short")
            tools = data["tools"]
            if not isinstance(tools, list) or not tools or not all(isinstance(t, str) for t in tools):
                raise ValueError("Explicit nonempty tool list required")
            if len(tools) != len(set(tools)) or not set(tools).issubset(KNOWN_TOOLS):
                raise ValueError("Unexpected, duplicate, delegated or external-action tools")
            if path.stem in READ_ONLY and set(tools) != {"Read", "Glob", "Grep"}:
                raise ValueError("Independent reviewers must have only Read/Glob/Grep")
            if data["permissionMode"] != "default":
                raise ValueError("Kit agent permissionMode must remain default/manual")
            if not isinstance(data["model"], str) or not data["model"]:
                raise ValueError("Explicit model selection required")
            if type(data["maxTurns"]) is not int or not 1 <= data["maxTurns"] <= 50:
                raise ValueError("maxTurns must be an integer from 1 to 50")
            preloads = data.get("skills", [])
            if not isinstance(preloads, list) or not all(isinstance(s, str) for s in preloads):
                raise ValueError("skills must be a name list")
            if not set(preloads).issubset(actual_skills):
                raise ValueError("Preloaded skill is missing")
            if len(preloads) > 1:
                raise ValueError("This lean kit permits at most one preloaded skill per role")
        except (OSError, ValueError, TypeError, KeyError) as exc:
            fail(path, str(exc))

    settings_path = root / ".claude" / "settings.json"
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        permissions = settings["permissions"]
        if permissions.get("defaultMode") != "default":
            raise ValueError("Main session must use default/manual permissions")
        if permissions.get("allow"):
            raise ValueError("No blanket or automatic allow rules are shipped in this kit")
        required_denies = {"Read(**/.env)", "Read(**/.env.*)", "Read(/secrets/**)", "Edit(/.claude/settings.json)", "Bash(git push *)", "Bash(git commit *)", "Bash(git reset *)", "Bash(git clean *)"}
        denies = permissions.get("deny", [])
        if not isinstance(denies, list) or not all(isinstance(x, str) for x in denies):
            raise ValueError("deny must be a string list")
        if not required_denies.issubset(denies):
            raise ValueError("Required safety guardrail missing")
        if "hooks" in settings or "mcpServers" in settings:
            raise ValueError("No automatic hooks or external servers are shipped")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        fail(settings_path, str(exc))

    markdown = [root / "README.md", root / "CLAUDE.md", root / "THIRD_PARTY_NOTICES.md"]
    for dirname in (".claude", "docs", "evals", "verification"):
        markdown.extend((root / dirname).rglob("*.md"))
    for path in markdown:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            if urlparse(target).scheme or target.startswith("#"):
                continue
            target = unquote(target.split("#", 1)[0])
            linked = (path.parent / target).resolve()
            if not linked.is_relative_to(root):
                fail(path, "local link escapes kit root")
            elif not linked.exists():
                fail(path, f"broken local link: {target}")
            else:
                counts["local_links"] += 1
    for source, target in QUALITY_ROUTES:
        path = root / source
        try:
            targets = {
                (path.parent / unquote(link.split("#", 1)[0])).resolve()
                for link in LINK.findall(path.read_text(encoding="utf-8"))
                if not urlparse(link).scheme and not link.startswith("#")
            }
            if (root / target).resolve() not in targets:
                fail(source, f"required design-quality route missing: {target}")
            else:
                counts["design_routes"] += 1
        except OSError as exc:
            fail(source, f"cannot inspect design-quality route: {exc}")

    for source, target in SECURITY_ROUTES:
        path = root / source
        try:
            targets = {
                (path.parent / unquote(link.split("#", 1)[0])).resolve()
                for link in LINK.findall(path.read_text(encoding="utf-8"))
                if not urlparse(link).scheme and not link.startswith("#")
            }
            if (root / target).resolve() not in targets:
                fail(source, f"required security route missing: {target}")
            else:
                counts["security_routes"] += 1
        except OSError as exc:
            fail(source, f"cannot inspect security route: {exc}")

    for source, target in COMMUNITY_ROUTES:
        path = root / source
        try:
            targets = {
                (path.parent / unquote(link.split("#", 1)[0])).resolve()
                for link in LINK.findall(path.read_text(encoding="utf-8"))
                if not urlparse(link).scheme and not link.startswith("#")
            }
            if (root / target).resolve() not in targets:
                fail(source, f"required community route missing: {target}")
            else:
                counts["community_routes"] += 1
        except OSError as exc:
            fail(source, f"cannot inspect community route: {exc}")


    for source, target in PLATFORM_ROUTES:
        path = root / source
        try:
            targets = {
                (path.parent / unquote(link.split("#", 1)[0])).resolve()
                for link in LINK.findall(path.read_text(encoding="utf-8"))
                if not urlparse(link).scheme and not link.startswith("#")
            }
            if (root / target).resolve() not in targets:
                fail(source, f"required platform/database route missing: {target}")
            else:
                counts["platform_routes"] += 1
        except OSError as exc:
            fail(source, f"cannot inspect platform/database route: {exc}")

    for source, target in FRONTEND_ROUTES:
        path = root / source
        try:
            targets = {
                (path.parent / unquote(link.split("#", 1)[0])).resolve()
                for link in LINK.findall(path.read_text(encoding="utf-8"))
                if not urlparse(link).scheme and not link.startswith("#")
            }
            if (root / target).resolve() not in targets:
                fail(source, f"required frontend route missing: {target}")
            else:
                counts["frontend_routes"] += 1
        except OSError as exc:
            fail(source, f"cannot inspect frontend route: {exc}")

    try:
        provenance = json.loads((root / "docs/upstream-sources.json").read_text(encoding="utf-8"))
        if provenance.get("repository") != "rrezartprebreza/spring-boot-skills":
            raise ValueError("unexpected source repository")
        if not re.fullmatch(r"[0-9a-f]{40}", provenance.get("commit", "")):
            raise ValueError("upstream must be pinned to a full commit")
        if provenance.get("license") != "MIT" or len(provenance.get("files", [])) != 8:
            raise ValueError("expected inspected source inventory and MIT license")
        for item in provenance["files"]:
            if not re.fullmatch(r"[0-9a-f]{40}", item.get("git_blob_sha", "")):
                raise ValueError("missing source blob identity")
            expected_url = ("https://github.com/" + provenance["repository"] + "/blob/"
                            + provenance["commit"] + "/" + item["path"])
            if item.get("url") != expected_url:
                raise ValueError("source URL is not pinned to recorded commit/path")
            for destination in item["destinations"]:
                path = (root / destination).resolve()
                if not path.is_relative_to(root) or not path.is_file():
                    raise ValueError("missing or unsafe adapted destination")
        for name in ("spring-backend", "postgresql-migrations", "test-verification"):
            license_path = root / ".claude/skills" / name / "LICENSE-UPSTREAM.txt"
            data = license_path.read_bytes()
            git_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            if git_blob != "a58973b12dc7bebee056cb617d8ff7839e6692ae":
                raise ValueError("upstream MIT notice must remain complete")
    except (OSError, KeyError, TypeError, ValueError) as exc:
        fail("docs/upstream-sources.json", f"community provenance invalid: {exc}")

    policy = root / ".claude" / "policies" / "core.md"
    try:
        if "@.claude/policies/core.md" not in (root / "CLAUDE.md").read_text(encoding="utf-8") or not policy.is_file():
            fail("CLAUDE.md", "Missing shared policy reference")
    except OSError as exc:
        fail("CLAUDE.md", str(exc))
    warnings.append("Static kit checks only: Claude Code runtime, model behavior and application tests are NOT_RUN here.")
    return {"status": "FAIL" if errors else "PASS", "counts": counts, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable report")
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
