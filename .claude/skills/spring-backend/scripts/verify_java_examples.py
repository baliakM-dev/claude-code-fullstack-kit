#!/usr/bin/env python3
"""Compile the shipped Java helper and run its scenarios. No network or database.

Requires Python 3.10+ and JDK 17+. Uses --release 17, not the application's toolchain.
Exit 0 = helper scenarios passed; 1 = verification failed; 2 = prerequisite missing.
This is not a Spring, JPA, Keycloak, NullAway or PostgreSQL test runner.
"""
from __future__ import annotations
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]


def execute(javac: str | None = None, java: str | None = None) -> int:
    compiler = javac or shutil.which("javac")
    runtime = java or shutil.which("java")
    if not compiler or not runtime:
        print("NOT_RUN: Java helper needs both java and javac on PATH.")
        return 2
    sources = [SKILL / "assets/idempotency" / name for name in
               ("CommandFingerprint.java", "CommandFingerprintTest.java")]
    if any(not p.is_file() or not p.resolve().is_relative_to(SKILL) for p in sources):
        print("FAIL: expected shipped Java sources missing or outside skill.")
        return 1
    try:
        with tempfile.TemporaryDirectory(prefix="kit-java-helper-") as directory:
            commands = [
                [compiler, "--release", "17", "-encoding", "UTF-8", "-Xlint:all", "-Werror",
                 "-d", directory, *(str(p) for p in sources)],
                [runtime, "-cp", directory, "kit.examples.idempotency.CommandFingerprintTest"],
            ]
            for command in commands:
                result = subprocess.run(command, capture_output=True, text=True,
                                        encoding="utf-8", errors="replace", timeout=40, check=False)
                if result.returncode != 0:
                    print("FAIL: Java compile/scenario command exited", result.returncode)
                    print((result.stdout + result.stderr)[-8000:])
                    return 1
            output = result.stdout
            print(output.strip())
            match = re.search(r"(?m)^JAVA_HELPER_SCENARIOS_PASS=(\d+)$", output)
            if not match or int(match.group(1)) != 20:
                print("FAIL: scenario completion marker missing or incomplete.")
                return 1
            return 0
    except (OSError, subprocess.TimeoutExpired) as error:
        print("FAIL:", type(error).__name__, "during local Java example verification")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    return execute()


if __name__ == "__main__":
    sys.exit(main())
