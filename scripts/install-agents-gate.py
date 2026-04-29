#!/usr/bin/env python3
"""Install or remove the Cast Subagents AGENTS.md advisory gate."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys


START_MARKER = "<!-- cast-subagents:start -->"
END_MARKER = "<!-- cast-subagents:end -->"

GATE_BLOCK = f"""{START_MARKER}
## Subagent Advisory Gate

This gate applies only to the main/frontline Codex agent before starting a user-level task.

If the current task message explicitly says this is a delegated subagent task, or includes `delegation_context: delegated-subagent`, do not invoke `$cast-subagents`, do not suggest another lineup, and do not wait for delegation approval. Parent approval has already completed; execute only the assigned handoff within its constraints.

Before starting any non-trivial coding, review, research, planning, codebase-mapping, docs/API-verification, or regression-risk task, check whether it matches the cast-subagents trigger patterns.

If it matches, invoke `$cast-subagents` first, suggest exactly one lineup, and stop before inspecting files, running commands, searching docs, summarizing findings, or starting implementation.

If it does not match, continue normally and do not mention subagents.
{END_MARKER}
"""


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()


def target_file(scope: str, path: str | None) -> Path:
    if scope == "global":
        if path:
            raise ValueError("--path is only valid with --scope project")
        return codex_home() / "AGENTS.md"

    project_root = Path(path or os.getcwd()).expanduser()
    return project_root / "AGENTS.md"


def marker_counts(text: str) -> tuple[int, int]:
    return text.count(START_MARKER), text.count(END_MARKER)


def validate_markers(text: str) -> None:
    start_count, end_count = marker_counts(text)
    if start_count != end_count:
        raise ValueError("Found only one cast-subagents marker. Fix AGENTS.md manually before running this script.")
    if start_count > 1:
        raise ValueError("Found multiple cast-subagents blocks. Keep one block before running this script.")
    if start_count == 1 and text.index(START_MARKER) > text.index(END_MARKER):
        raise ValueError("Found cast-subagents markers in the wrong order.")


def install_block(text: str) -> tuple[str, str]:
    validate_markers(text)
    start_count, _ = marker_counts(text)

    if start_count == 0:
        if text.strip():
            return text.rstrip() + "\n\n" + GATE_BLOCK, "installed"
        return GATE_BLOCK, "installed"

    start = text.index(START_MARKER)
    end = text.index(END_MARKER) + len(END_MARKER)
    return text[:start] + GATE_BLOCK.rstrip() + text[end:], "updated"


def remove_block(text: str) -> tuple[str, str]:
    validate_markers(text)
    start_count, _ = marker_counts(text)
    if start_count == 0:
        return text, "unchanged"

    start = text.index(START_MARKER)
    end = text.index(END_MARKER) + len(END_MARKER)
    before = text[:start].rstrip()
    after = text[end:].lstrip("\n")
    if before and after:
        return before + "\n\n" + after, "removed"
    if before:
        return before + "\n", "removed"
    return after, "removed"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scope",
        choices=("global", "project"),
        default="global",
        help="Install globally to CODEX_HOME/AGENTS.md or to a project AGENTS.md.",
    )
    parser.add_argument(
        "--path",
        help="Project root when using --scope project. Defaults to the current directory.",
    )
    parser.add_argument("--remove", action="store_true", help="Remove the managed block.")
    parser.add_argument("--dry-run", action="store_true", help="Print the action without writing.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        target = target_file(args.scope, args.path)
        text = target.read_text(encoding="utf-8") if target.exists() else ""
        new_text, action = remove_block(text) if args.remove else install_block(text)
    except OSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(f"{action}: {target}")
    if args.dry_run:
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(new_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
