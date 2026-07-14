import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PluginContractTest(unittest.TestCase):
    def test_plugin_package_and_session_start_hook_are_discoverable(self) -> None:
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        marketplace = json.loads(
            (ROOT / ".agents" / "plugins" / "marketplace.json").read_text()
        )
        hooks = json.loads((ROOT / "hooks" / "hooks.json").read_text())

        self.assertEqual(manifest["name"], "cast-subagents")
        self.assertEqual(manifest["version"], "0.1.0")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertNotIn("hooks", manifest)

        self.assertEqual(marketplace["name"], "cast-subagents")
        entry = marketplace["plugins"]
        self.assertEqual(len(entry), 1)
        self.assertEqual(entry[0]["name"], "cast-subagents")
        self.assertEqual(entry[0]["source"]["source"], "url")
        self.assertEqual(
            entry[0]["source"]["url"],
            "https://github.com/917Dhj/cast-subagents.git",
        )
        self.assertEqual(entry[0]["source"]["ref"], "main")
        self.assertEqual(entry[0]["policy"]["installation"], "AVAILABLE")
        self.assertEqual(entry[0]["policy"]["authentication"], "ON_INSTALL")

        self.assertEqual(set(hooks["hooks"]), {"SessionStart"})
        group = hooks["hooks"]["SessionStart"][0]
        self.assertEqual(group["matcher"], "startup|resume|clear|compact")
        handler = group["hooks"][0]
        self.assertEqual(handler["type"], "command")
        self.assertIn("${PLUGIN_ROOT}/hooks/session_start.py", handler["command"])
        self.assertIn("$env:PLUGIN_ROOT", handler["commandWindows"])
        self.assertEqual(handler["timeout"], 5)

        result = subprocess.run(
            [sys.executable, ROOT / "hooks" / "session_start.py"],
            input='{"source":"startup"}',
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("Subagent Advisory Gate", result.stdout)
        self.assertIn("delegation_context: delegated-subagent", result.stdout)
        self.assertIn("invoke `$cast-subagents` first", result.stdout)

    def test_bundled_skill_is_the_only_skill_entry_and_selects_a_backend(self) -> None:
        skill_path = ROOT / "skills" / "cast-subagents" / "SKILL.md"
        skill = skill_path.read_text()

        self.assertTrue(skill_path.is_file())
        self.assertFalse((ROOT / "SKILL.md").exists())
        for name in (
            "decision-rules.md",
            "role-lineups.md",
            "handoff-schema.md",
            "suggestion-contract.md",
            "examples-positive.md",
            "examples-negative.md",
        ):
            self.assertTrue((skill_path.parent / "references" / name).is_file(), name)

        self.assertIn("Backend Capability Check", skill)
        self.assertIn("Native Subagent Backend", skill)
        self.assertIn("CLI Worker Backend", skill)
        self.assertIn("agent_type", skill)
        self.assertIn("model", skill)
        self.assertIn("reasoning_effort", skill)
        self.assertIn("scripts/run-cli-agent.py", skill)
        self.assertIn("delegation_context: delegated-subagent", skill)

    def test_install_guide_has_one_plugin_only_flow(self) -> None:
        guide = (ROOT / ".codex" / "INSTALL.md").read_text()

        self.assertIn("codex plugin marketplace add 917Dhj/cast-subagents", guide)
        self.assertIn("codex plugin add cast-subagents@cast-subagents", guide)
        self.assertIn("/hooks", guide)
        self.assertIn("install-agent-roles.py", guide)
        self.assertIn("Python 3.11", guide)
        self.assertNotIn("npx skills", guide)
        self.assertNotIn("install-agents-gate.py", guide)
        self.assertNotIn("--scope", guide)

        install_order = (
            "### 2. Install the plugin",
            "### 3. Choose the global Bundled Subagents",
            "### 4. Run the Role Installer for the user",
            "### 5. Trust the SessionStart Hook",
            "### 6. Verify and restart",
        )
        positions = [guide.index(heading) for heading in install_order]
        self.assertEqual(positions, sorted(positions))

        updating = guide.split("## Updating", 1)[1]
        self.assertLess(updating.index("Role Installer"), updating.index("/hooks"))

        for readme_name in ("README.md", "README.zh.md"):
            readme = (ROOT / readme_name).read_text()
            self.assertNotIn("npx skills", readme, readme_name)
            self.assertNotIn("install-agents-gate.py", readme, readme_name)
            self.assertNotIn("AGENTS.md gate", readme, readme_name)

        self.assertFalse((ROOT / "scripts" / "install-agents-gate.py").exists())


if __name__ == "__main__":
    unittest.main()
