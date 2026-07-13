#!/usr/bin/env python3
"""Run one installed Cast Subagents role as an ephemeral Codex CLI worker."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib


ROLE_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SANDBOX_MODES = {"read-only", "workspace-write"}
REASONING_EFFORTS = {"low", "medium", "high", "xhigh"}


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("role", help="Installed role name.")
    parser.add_argument("-C", "--cd", default=os.getcwd(), help="Worker workspace.")
    parser.add_argument(
        "--add-dir",
        action="append",
        default=[],
        help="Additional directory available to the worker. Repeat as needed.",
    )
    return parser.parse_args(argv)


def load_role(name: str) -> dict[str, str]:
    if ROLE_NAME.fullmatch(name) is None:
        raise ValueError(f"Invalid role name: {name}")

    path = codex_home() / "agents" / f"{name}.toml"
    config = tomllib.loads(path.read_text(encoding="utf-8"))
    required = ("model", "model_reasoning_effort", "sandbox_mode", "developer_instructions")
    for key in required:
        if not isinstance(config.get(key), str) or not config[key].strip():
            raise ValueError(f"Role {name} has invalid {key}")
    if config["sandbox_mode"] not in SANDBOX_MODES:
        raise ValueError(f"Role {name} has unsupported sandbox_mode: {config['sandbox_mode']}")
    if config["model_reasoning_effort"] not in REASONING_EFFORTS:
        raise ValueError(
            f"Role {name} has unsupported model_reasoning_effort: "
            f"{config['model_reasoning_effort']}"
        )
    return config


def worker_prompt(instructions: str, handoff: str) -> str:
    if not handoff.strip():
        raise ValueError("Delegated handoff is empty")
    return f"""Role developer instructions:
{instructions.strip()}

Delegation constraints:
delegation_context: delegated-subagent
- Parent approval already completed. Execute only this handoff.
- Do not invoke cast-subagents or request another delegation approval.
- Do not delegate, spawn subagents, or create child workers.

Delegated handoff:
{handoff}
"""


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        role = load_role(args.role)
        prompt = worker_prompt(role["developer_instructions"], sys.stdin.read())
    except (OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    command = [
        "codex",
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
        role["model"],
        "-c",
        f'model_reasoning_effort="{role["model_reasoning_effort"]}"',
        "-s",
        role["sandbox_mode"],
        "-C",
        str(Path(args.cd).expanduser()),
    ]
    for path in args.add_dir:
        command.extend(("--add-dir", str(Path(path).expanduser())))
    command.append("-")

    try:
        result = subprocess.run(command, input=prompt, text=True, capture_output=True)
    except OSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    sys.stdout.write(result.stdout)
    if result.returncode:
        sys.stderr.write(result.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
