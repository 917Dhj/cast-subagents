---
name: diverter-mode
description: "Explicitly view or change Diverter's persistent Delegation Policy. Use only when the user invokes `$diverter-mode`; never invoke implicitly."
---

# Diverter Mode

Manage Diverter's user-level Delegation Policy. This is an explicit control surface, not a delegation task.

Never invoke `$diverter`, evaluate a lineup, or spawn subagents while processing this skill.

## Accepted Operations

- `auto` — persist automatic dispatch for suitable tasks
- `ask` — persist approval-first delegation
- `status` — report the policy that the next `SessionStart` will load
- no argument — behave like `status` and also list the three operations above

Reject every other value without changing configuration. Do not guess aliases or accept configuration paths.

## Run Mode Control

Let `skill_file` be the fully expanded absolute path to this `SKILL.md`, compute `plugin_root = Path(skill_file).parents[2]`, and verify `${plugin_root}/.codex-plugin/plugin.json` exists.

Run exactly one of:

```bash
python3 "${plugin_root}/scripts/diverter-mode.py" auto
python3 "${plugin_root}/scripts/diverter-mode.py" ask
python3 "${plugin_root}/scripts/diverter-mode.py" status
```

Parse the JSON on stdout and require a zero exit status before reporting success.

## User Response

After a successful `auto` or `ask` operation, say exactly:

```text
Diverter mode changed to `<policy>`.
Restart or reopen the task to apply the new mode.
```

For `status`, report the returned policy as the configuration that the next `SessionStart` will load. If `source` is `default`, say that `ask` is the default because configuration is missing. If `warning` is `invalid_config`, say that configuration is invalid and Diverter will safely fall back to `ask`; do not repair it during a query.

Match any surrounding explanation to the user's language, while keeping policy names and commands exact. A mode change never updates the active Root Session directly.
