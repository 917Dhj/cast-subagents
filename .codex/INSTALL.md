# Installing cast-subagents for Codex

Advisory subagent lineup suggestions for Codex — suggests one lineup before complex tasks, then waits for approval.

## Prerequisites

- Node.js/npm (`npx`)
- Python 3

## Installation

**1. Install the skill for Codex with npx Skills:**

```bash
npx skills add 917Dhj/cast-subagents -a codex
CAST_SUBAGENTS_HOME="${AGENTS_HOME:-$HOME/.agents}/skills/cast-subagents"
```

If the command opens an interactive prompt, the agent may complete the normal install prompts for you: choose Codex as the target agent and confirm the install. If the prompt asks for anything else, pause and ask the user.

If `npx` fails, use the Codex skill-installer fallback instead:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo 917Dhj/cast-subagents \
  --path . \
  --name cast-subagents

CAST_SUBAGENTS_HOME="${CODEX_HOME:-$HOME/.codex}/skills/cast-subagents"
```

**2. Install the advisory gate** (adds a trigger block to AGENTS.md so Codex knows when to invoke the skill):

Default: install globally. This is the recommended setup because cast-subagents is meant to advise Codex across workspaces, before non-trivial tasks begin. It writes to `${CODEX_HOME:-$HOME/.codex}/AGENTS.md`.

```bash
python3 "$CAST_SUBAGENTS_HOME/scripts/install-agents-gate.py" --scope global
```

Use project-only install only when the user explicitly wants cast-subagents enabled for one repository:

```bash
python3 "$CAST_SUBAGENTS_HOME/scripts/install-agents-gate.py" \
  --scope project \
  --path /path/to/repo
```

**3. (Optional) Install bundled agent roles** — copies 7 specialized role definitions to your Codex agents directory:

Global:

```bash
python3 "$CAST_SUBAGENTS_HOME/scripts/install-agent-roles.py" --scope global
```

Project-only:

```bash
python3 "$CAST_SUBAGENTS_HOME/scripts/install-agent-roles.py" \
  --scope project \
  --path /path/to/repo
```

Without the bundled roles, cast-subagents still works — it will suggest lineups using whatever roles are already available in the Codex environment.

**4. Tell the user to restart Codex** so the skill and AGENTS rules are loaded.

## Verify

If this is a new shell, set `CAST_SUBAGENTS_HOME` to the install path first. For the default `npx` install, use `${AGENTS_HOME:-$HOME/.agents}/skills/cast-subagents`. For the Codex skill-installer fallback, use `${CODEX_HOME:-$HOME/.codex}/skills/cast-subagents`.

Check that the gate block was added:

```bash
grep -c "cast-subagents:start" "${CODEX_HOME:-$HOME/.codex}/AGENTS.md"
```

Expected output: `1`

Check that the skill directory exists:

```bash
ls "$CAST_SUBAGENTS_HOME/SKILL.md"
```

## Updating

Run the npx install command again:

```bash
npx skills add 917Dhj/cast-subagents -a codex
CAST_SUBAGENTS_HOME="${AGENTS_HOME:-$HOME/.agents}/skills/cast-subagents"
```

If you used the Codex skill-installer fallback, re-run that fallback command instead and keep `CAST_SUBAGENTS_HOME` pointed at `${CODEX_HOME:-$HOME/.codex}/skills/cast-subagents`.

Re-run the gate installer to update the AGENTS block (the installer is idempotent — it updates in place):

```bash
python3 "$CAST_SUBAGENTS_HOME/scripts/install-agents-gate.py" --scope global
```

## Uninstalling

Set `CAST_SUBAGENTS_HOME` to the install path before uninstalling.

Remove the advisory gate block from AGENTS.md:

```bash
python3 "$CAST_SUBAGENTS_HOME/scripts/install-agents-gate.py" --scope global --remove
```

Remove the skill directory:

```bash
rm -rf "$CAST_SUBAGENTS_HOME"
```
