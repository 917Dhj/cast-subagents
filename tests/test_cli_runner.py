import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run-cli-agent.py"


class CliRunnerTest(unittest.TestCase):
    def test_runs_ephemeral_leaf_worker_with_role_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            codex_home = temp / "codex-home"
            agents = codex_home / "agents"
            agents.mkdir(parents=True)
            (agents / "code-mapper.toml").write_text(
                '''name = "code-mapper"
model = "gpt-5.6-terra"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
web_search = "live"
developer_instructions = """
Map the requested code path.
"""
'''
            )

            bin_dir = temp / "bin"
            bin_dir.mkdir()
            fake_codex = bin_dir / "codex"
            fake_codex.write_text(
                f"""#!{sys.executable}
import json
import os
from pathlib import Path
import sys

Path(os.environ["FAKE_CODEX_CAPTURE"]).write_text(json.dumps({{
    "argv": sys.argv[1:],
    "stdin": sys.stdin.read(),
}}))
print("worker stdout")
"""
            )
            fake_codex.chmod(0o755)

            capture = temp / "capture.json"
            workspace = temp / "workspace"
            workspace.mkdir()
            extra_one = temp / "extra-one"
            extra_two = temp / "extra-two"
            extra_one.mkdir()
            extra_two.mkdir()
            handoff = "goal: Trace the settings save path.\nwrite_policy: read-only\n"
            env = {
                **os.environ,
                "CODEX_HOME": str(codex_home),
                "FAKE_CODEX_CAPTURE": str(capture),
                "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            }

            result = subprocess.run(
                [
                    sys.executable,
                    RUNNER,
                    "code-mapper",
                    "-C",
                    workspace,
                    "--add-dir",
                    extra_one,
                    "--add-dir",
                    extra_two,
                ],
                input=handoff,
                env=env,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "worker stdout\n")
            call = json.loads(capture.read_text())
            self.assertEqual(
                call["argv"],
                [
                    "-a",
                    "never",
                    "--search",
                    "--disable",
                    "multi_agent",
                    "--disable",
                    "multi_agent_v2",
                    "exec",
                    "--ephemeral",
                    "-m",
                    "gpt-5.6-terra",
                    "-c",
                    'model_reasoning_effort="high"',
                    "-s",
                    "read-only",
                    "-C",
                    str(workspace),
                    "--add-dir",
                    str(extra_one),
                    "--add-dir",
                    str(extra_two),
                    "-",
                ],
            )
            self.assertIn("Map the requested code path.", call["stdin"])
            self.assertIn("delegation_context: delegated-subagent", call["stdin"])
            self.assertIn("do not invoke cast-subagents", call["stdin"].lower())
            self.assertIn(handoff, call["stdin"])

    def test_propagates_worker_failure_and_stderr(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            agents = temp / "codex-home" / "agents"
            agents.mkdir(parents=True)
            (agents / "reviewer.toml").write_text(
                '''model = "gpt-5.6-sol"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
developer_instructions = "Review the change."
'''
            )
            bin_dir = temp / "bin"
            bin_dir.mkdir()
            fake_codex = bin_dir / "codex"
            fake_codex.write_text(
                f"#!{sys.executable}\nimport sys\nprint('partial result')\nprint('worker failed', file=sys.stderr)\nraise SystemExit(7)\n"
            )
            fake_codex.chmod(0o755)

            result = subprocess.run(
                [sys.executable, RUNNER, "reviewer"],
                input="goal: Review one diff.\n",
                env={
                    **os.environ,
                    "CODEX_HOME": str(temp / "codex-home"),
                    "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
                },
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 7)
            self.assertEqual(result.stdout, "partial result\n")
            self.assertEqual(result.stderr, "worker failed\n")

    def test_rejects_invalid_role_name_before_running_codex(self) -> None:
        result = subprocess.run(
            [sys.executable, RUNNER, "../reviewer"],
            input="goal: Review one diff.\n",
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("Invalid role name", result.stderr)

    def test_rejects_unsupported_reasoning_effort(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / "codex-home"
            agents = codex_home / "agents"
            agents.mkdir(parents=True)
            (agents / "reviewer.toml").write_text(
                '''model = "gpt-5.6-sol"
model_reasoning_effort = "maximum"
sandbox_mode = "read-only"
developer_instructions = "Review the change."
'''
            )
            result = subprocess.run(
                [sys.executable, RUNNER, "reviewer"],
                input="goal: Review one diff.\n",
                env={**os.environ, "CODEX_HOME": str(codex_home)},
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("unsupported model_reasoning_effort", result.stderr)


if __name__ == "__main__":
    unittest.main()
