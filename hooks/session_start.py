#!/usr/bin/env python3
"""Inject the Diverter Delegation Gate into a root Codex session."""

import json
import os
from pathlib import Path


def load_policy() -> str:
    codex_home = Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()
    path = codex_home / "diverter" / "config.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        policy = data.get("delegation_policy") if isinstance(data, dict) else None
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError):
        return "ask"
    return policy if policy in {"ask", "auto"} else "ask"


def build_gate(policy: str) -> str:
    return f"""## Diverter Delegation Gate

delegation_policy: {policy}

This gate applies only to the main/frontline Codex agent before starting a user-level task.

If the current user message explicitly invokes `$diverter-mode`, execute Mode Control directly. Do not invoke `$diverter`, evaluate delegation, or spawn subagents for that message.

If the current task message explicitly says this is a delegated subagent task, or includes `delegation_context: delegated-subagent`, do not invoke `$diverter`, suggest another lineup, or request Dispatch Authorization. Execute only the assigned handoff within its constraints.

Before starting any non-trivial coding, review, research, planning, codebase-mapping, docs/API-verification, or regression-risk task, check whether it matches the Diverter trigger patterns.

If it matches, invoke `$diverter` first and apply the loaded Delegation Policy. An explicit user instruction for the current task may override this policy without changing persistent configuration.

If it does not match, continue normally and do not mention subagents.
"""


if __name__ == "__main__":
    print(build_gate(load_policy()), end="")
