#!/usr/bin/env python3
"""Inject the Diverter Advisory Gate into a root Codex session."""

GATE = """## Subagent Advisory Gate

This gate applies only to the main/frontline Codex agent before starting a user-level task.

If the current task message explicitly says this is a delegated subagent task, or includes `delegation_context: delegated-subagent`, do not invoke `$diverter`, do not suggest another lineup, and do not wait for delegation approval. Parent approval has already completed; execute only the assigned handoff within its constraints.

Before starting any non-trivial coding, review, research, planning, codebase-mapping, docs/API-verification, or regression-risk task, check whether it matches the Diverter trigger patterns.

If it matches, invoke `$diverter` first, suggest exactly one lineup, and stop before inspecting files, running commands, searching docs, summarizing findings, or starting implementation.

If it does not match, continue normally and do not mention subagents.
"""


if __name__ == "__main__":
    print(GATE, end="")
