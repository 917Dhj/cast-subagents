import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install-agent-roles.py"


class RoleInstallerTest(unittest.TestCase):
    def test_installs_only_selected_roles_into_global_codex_home(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / "codex-home"
            agents = codex_home / "agents"
            agents.mkdir(parents=True)
            untouched = agents / "custom.toml"
            untouched.write_text("name = 'custom'\n")

            result = subprocess.run(
                [
                    sys.executable,
                    INSTALLER,
                    "--overwrite",
                    "--role",
                    "code-mapper",
                ],
                env={**os.environ, "CODEX_HOME": str(codex_home)},
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((agents / "code-mapper.toml").is_file())
            self.assertFalse((agents / "reviewer.toml").exists())
            self.assertEqual(untouched.read_text(), "name = 'custom'\n")

            help_result = subprocess.run(
                [sys.executable, INSTALLER, "--help"],
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertNotIn("--scope", help_result.stdout)
            self.assertNotIn("--path", help_result.stdout)

    def test_dry_run_does_not_create_agent_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / "codex-home"
            result = subprocess.run(
                [sys.executable, INSTALLER, "--dry-run", "--role", "reviewer"],
                env={**os.environ, "CODEX_HOME": str(codex_home)},
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("installed:", result.stdout)
            self.assertFalse((codex_home / "agents").exists())

    def test_unknown_role_fails_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / "codex-home"
            result = subprocess.run(
                [sys.executable, INSTALLER, "--role", "not-a-role"],
                env={**os.environ, "CODEX_HOME": str(codex_home)},
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("Unknown role", result.stderr)
            self.assertFalse((codex_home / "agents").exists())


if __name__ == "__main__":
    unittest.main()
