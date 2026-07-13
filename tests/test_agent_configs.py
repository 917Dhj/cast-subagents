from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "code-mapper": ("gpt-5.6-terra", "high", "read-only"),
    "search-specialist": ("gpt-5.6-luna", "medium", "read-only"),
    "docs-researcher": ("gpt-5.6-luna", "high", "read-only"),
    "knowledge-synthesizer": ("gpt-5.6-luna", "high", "read-only"),
    "task-distributor": ("gpt-5.6-sol", "medium", "read-only"),
    "reviewer": ("gpt-5.6-sol", "medium", "read-only"),
    "security-auditor": ("gpt-5.6-sol", "high", "read-only"),
    "test-engineer": ("gpt-5.6-luna", "xhigh", "read-only"),
    "test-automator": ("gpt-5.6-terra", "xhigh", "workspace-write"),
    "web-performance-auditor": ("gpt-5.6-luna", "xhigh", "read-only"),
}


class AgentConfigTest(unittest.TestCase):
    def test_bundled_agents_use_the_release_mapping(self) -> None:
        paths = sorted((ROOT / "agents" / "categories").glob("*/*.toml"))
        configs = {path.stem: tomllib.loads(path.read_text()) for path in paths}

        self.assertEqual(set(configs), set(EXPECTED))
        for name, expected in EXPECTED.items():
            config = configs[name]
            actual = (
                config["model"],
                config["model_reasoning_effort"],
                config["sandbox_mode"],
            )
            self.assertEqual(actual, expected, name)
            self.assertEqual(config["web_search"], "live", name)


if __name__ == "__main__":
    unittest.main()
