"""Mock-based runner error-handling tests; Java behavior runs separately."""
import contextlib
import importlib.util
import io
import subprocess
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'.claude/skills/spring-backend/scripts/verify_java_examples.py'
SPEC=importlib.util.spec_from_file_location('java_example_runner', PATH)
MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)

def result(code=0, out=''):
    return SimpleNamespace(returncode=code,stdout=out,stderr='')

class JavaRunnerTests(unittest.TestCase):
    def invoke(self, outputs):
        with patch.object(MOD.subprocess,'run', side_effect=outputs) as run:
            with contextlib.redirect_stdout(io.StringIO()):
                value=MOD.execute('checked-javac','checked-java')
            calls=run.call_args_list
        return value,calls

    def test_missing_jdk_not_run(self):
        with patch.object(MOD.shutil,'which',return_value=None), patch.object(MOD.subprocess,'run') as run:
            with contextlib.redirect_stdout(io.StringIO()): self.assertEqual(MOD.execute(),2)
            run.assert_not_called()

    def test_compiler_failure_is_not_pass(self):
        value,calls=self.invoke([result(1,'compile failed')]);self.assertEqual(value,1);self.assertEqual(len(calls),1)

    def test_runtime_failure_is_not_pass(self):
        value,_=self.invoke([result(),result(1,'assertion failed')]);self.assertEqual(value,1)

    def test_no_scenarios_marker_is_not_pass(self):
        value,_=self.invoke([result(),result(0,'success')]);self.assertEqual(value,1)

    def test_incomplete_count_is_not_pass(self):
        value,_=self.invoke([result(),result(0,'JAVA_HELPER_SCENARIOS_PASS=0\n')]);self.assertEqual(value,1)

    def test_success_requires_complete_marker(self):
        value,_=self.invoke([result(),result(0,'JAVA_HELPER_SCENARIOS_PASS=20\n')]);self.assertEqual(value,0)

    def test_timeout_is_failure(self):
        value,_=self.invoke(subprocess.TimeoutExpired(['java'],40));self.assertEqual(value,1)

    def test_compiles_actual_shipped_sources_in_removed_temporary_directory(self):
        value,calls=self.invoke([result(),result(0,'JAVA_HELPER_SCENARIOS_PASS=20\n')])
        self.assertEqual(value,0)
        command=calls[0].args[0]
        self.assertIn(str(MOD.SKILL/'assets/idempotency/CommandFingerprint.java'),command)
        self.assertIn(str(MOD.SKILL/'assets/idempotency/CommandFingerprintTest.java'),command)
        temporary=Path(command[command.index('-d')+1]);self.assertFalse(temporary.exists())
        self.assertNotIn('shell',calls[0].kwargs)
        self.assertIn('--release',command)

if __name__ == '__main__': unittest.main()
