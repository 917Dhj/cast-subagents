#!/usr/bin/env python3
"""Install bundled Cast Subagents role definitions."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def source_roles() -> dict[str, Path]:
    role_root = skill_root() / "agents" / "categories"
    roles = {}
    for path in sorted(role_root.glob("*/*.toml")):
        roles[path.stem] = path
    return roles


def target_dir(scope: str, path: str | None) -> Path:
    if scope == "global":
        if path:
            raise ValueError("--path is only valid with --scope project")
        return codex_home() / "agents"

    project_root = Path(path or os.getcwd()).expanduser()
    return project_root / ".codex" / "agents"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scope",
        choices=("global", "project"),
        default="global",
        help="Install globally to CODEX_HOME/agents or to a project's .codex/agents.",
    )
    parser.add_argument(
        "--path",
        help="Project root when using --scope project. Defaults to the current directory.",
    )
    parser.add_argument(
        "--role",
        action="append",
        help="Role name to install. Repeat to install multiple roles. Defaults to all bundled roles.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing.")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing role files.")
    return parser.parse_args(argv)


def selected_roles(all_roles: dict[str, Path], requested: list[str] | None) -> dict[str, Path]:
    if not requested:
        return all_roles

    unknown = sorted(set(requested) - set(all_roles))
    if unknown:
        available = ", ".join(sorted(all_roles))
        raise ValueError(f"Unknown role(s): {', '.join(unknown)}. Available roles: {available}")

    return {name: all_roles[name] for name in requested}


def install_roles(roles: dict[str, Path], dest_root: Path, dry_run: bool, overwrite: bool) -> list[str]:
    actions = []
    for name, src in sorted(roles.items()):
        dest = dest_root / f"{name}.toml"
        if dest.exists() and not overwrite:
            actions.append(f"skipped existing: {dest}")
            continue

        action = "updated" if dest.exists() else "installed"
        actions.append(f"{action}: {dest}")
        if dry_run:
            continue

        dest_root.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    return actions


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        roles = selected_roles(source_roles(), args.role)
        dest = target_dir(args.scope, args.path)
        actions = install_roles(roles, dest, args.dry_run, args.overwrite)
    except OSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    for action in actions:
        print(action)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
