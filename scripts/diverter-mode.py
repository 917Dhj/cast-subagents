#!/usr/bin/env python3
"""Manage Diverter's user-level Delegation Policy."""

import json
import os
from pathlib import Path
import sys
import tempfile


def config_path() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return codex_home / "diverter" / "config.json"


def read_policy(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    policy = data.get("delegation_policy") if isinstance(data, dict) else None
    if policy not in {"ask", "auto"}:
        raise ValueError("invalid delegation_policy")
    return policy


def write_policy(path: Path, policy: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, delete=False
        ) as temp_file:
            json.dump({"delegation_policy": policy}, temp_file)
            temp_file.write("\n")
            temp_path = Path(temp_file.name)
        os.replace(temp_path, path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"init", "status", "ask", "auto"}:
        print(json.dumps({"ok": False, "error": "unsupported_operation"}))
        return 2

    path = config_path()
    if sys.argv[1] in {"ask", "auto"}:
        write_policy(path, sys.argv[1])
        print(json.dumps({"ok": True, "delegation_policy": sys.argv[1]}))
        return 0

    if sys.argv[1] == "status" and not path.exists():
        print(
            json.dumps(
                {"ok": True, "delegation_policy": "ask", "source": "default"}
            )
        )
        return 0

    if not path.exists():
        write_policy(path, "ask")
        policy = "ask"
        created = True
    else:
        try:
            policy = read_policy(path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError):
            if sys.argv[1] == "status":
                print(
                    json.dumps(
                        {
                            "ok": True,
                            "delegation_policy": "ask",
                            "source": "fallback",
                            "warning": "invalid_config",
                        }
                    )
                )
                return 0
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": "invalid_config",
                        "fallback_policy": "ask",
                    }
                )
            )
            return 1
        created = False
    if sys.argv[1] == "status":
        print(
            json.dumps(
                {"ok": True, "delegation_policy": policy, "source": "config"}
            )
        )
        return 0
    print(json.dumps({"ok": True, "delegation_policy": policy, "created": created}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
