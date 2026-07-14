import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODE_CLI = ROOT / "scripts" / "diverter-mode.py"


class DiverterModeTest(unittest.TestCase):
    def test_init_creates_ask_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / "codex-home"
            result = subprocess.run(
                [sys.executable, MODE_CLI, "init"],
                env={**os.environ, "CODEX_HOME": str(codex_home)},
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                json.loads(result.stdout),
                {"ok": True, "delegation_policy": "ask", "created": True},
            )
            self.assertEqual(
                json.loads(
                    (codex_home / "diverter" / "config.json").read_text()
                ),
                {"delegation_policy": "ask"},
            )

    def test_init_preserves_existing_valid_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / "codex-home"
            config = codex_home / "diverter" / "config.json"
            config.parent.mkdir(parents=True)
            config.write_text('{"delegation_policy": "auto"}\n')

            result = subprocess.run(
                [sys.executable, MODE_CLI, "init"],
                env={**os.environ, "CODEX_HOME": str(codex_home)},
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                json.loads(result.stdout),
                {"ok": True, "delegation_policy": "auto", "created": False},
            )
            self.assertEqual(config.read_text(), '{"delegation_policy": "auto"}\n')

    def test_init_rejects_invalid_configuration_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / "codex-home"
            config = codex_home / "diverter" / "config.json"
            config.parent.mkdir(parents=True)
            config.write_text("not json\n")

            result = subprocess.run(
                [sys.executable, MODE_CLI, "init"],
                env={**os.environ, "CODEX_HOME": str(codex_home)},
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertEqual(
                json.loads(result.stdout),
                {
                    "ok": False,
                    "error": "invalid_config",
                    "fallback_policy": "ask",
                },
            )
            self.assertEqual(config.read_text(), "not json\n")

    def test_status_reports_default_ask_without_creating_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / "codex-home"
            result = subprocess.run(
                [sys.executable, MODE_CLI, "status"],
                env={**os.environ, "CODEX_HOME": str(codex_home)},
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                json.loads(result.stdout),
                {"ok": True, "delegation_policy": "ask", "source": "default"},
            )
            self.assertFalse((codex_home / "diverter" / "config.json").exists())

    def test_status_reports_persisted_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / "codex-home"
            config = codex_home / "diverter" / "config.json"
            config.parent.mkdir(parents=True)
            config.write_text('{"delegation_policy": "auto"}\n')

            result = subprocess.run(
                [sys.executable, MODE_CLI, "status"],
                env={**os.environ, "CODEX_HOME": str(codex_home)},
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                json.loads(result.stdout),
                {"ok": True, "delegation_policy": "auto", "source": "config"},
            )

    def test_status_surfaces_invalid_configuration_and_falls_back_to_ask(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / "codex-home"
            config = codex_home / "diverter" / "config.json"
            config.parent.mkdir(parents=True)
            config.write_text('{"delegation_policy": "fast"}\n')

            result = subprocess.run(
                [sys.executable, MODE_CLI, "status"],
                env={**os.environ, "CODEX_HOME": str(codex_home)},
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                json.loads(result.stdout),
                {
                    "ok": True,
                    "delegation_policy": "ask",
                    "source": "fallback",
                    "warning": "invalid_config",
                },
            )
            self.assertEqual(config.read_text(), '{"delegation_policy": "fast"}\n')

    def test_set_persists_supported_policy(self) -> None:
        for policy in ("ask", "auto"):
            with self.subTest(policy=policy), tempfile.TemporaryDirectory() as temp_dir:
                codex_home = Path(temp_dir) / "codex-home"
                result = subprocess.run(
                    [sys.executable, MODE_CLI, policy],
                    env={**os.environ, "CODEX_HOME": str(codex_home)},
                    text=True,
                    capture_output=True,
                )

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(
                    json.loads(result.stdout),
                    {"ok": True, "delegation_policy": policy},
                )
                config = codex_home / "diverter" / "config.json"
                self.assertEqual(
                    json.loads(config.read_text()),
                    {"delegation_policy": policy},
                )
                self.assertEqual(list(config.parent.iterdir()), [config])

    def test_set_replaces_invalid_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / "codex-home"
            config = codex_home / "diverter" / "config.json"
            config.parent.mkdir(parents=True)
            config.write_text("not json\n")

            result = subprocess.run(
                [sys.executable, MODE_CLI, "auto"],
                env={**os.environ, "CODEX_HOME": str(codex_home)},
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(config.read_text()), {"delegation_policy": "auto"})

    def test_rejects_unsupported_operation_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / "codex-home"
            result = subprocess.run(
                [sys.executable, MODE_CLI, "fast"],
                env={**os.environ, "CODEX_HOME": str(codex_home)},
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 2)
            self.assertEqual(
                json.loads(result.stdout),
                {"ok": False, "error": "unsupported_operation"},
            )
            self.assertFalse((codex_home / "diverter" / "config.json").exists())


if __name__ == "__main__":
    unittest.main()
