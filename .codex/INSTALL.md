# Installing cast-subagents for Codex

Advisory subagent lineup suggestions for Codex — suggests one lineup before complex tasks, then waits for approval.

## Prerequisites

- Node.js/npm (`npx`)
- Python 3

## Installation

**1. Install the skill for Codex with npx Skills:**

```bash
npx skills add 917Dhj/cast-subagents -a codex
```

If the command opens an interactive prompt, choose Codex as the target agent.

**2. Install the advisory gate** (adds a trigger block to AGENTS.md so Codex knows when to invoke the skill):

Global install — applies to all Codex workspaces:

```bash
python3 "${AGENTS_HOME:-$HOME/.agents}/skills/cast-subagents/scripts/install-agents-gate.py" --scope global
```

Project-only install — applies to one repository:

```bash
python3 "${AGENTS_HOME:-$HOME/.agents}/skills/cast-subagents/scripts/install-agents-gate.py" \
  --scope project \
  --path /path/to/repo
```

**3. (Optional) Install bundled agent roles** — copies 7 specialized role definitions to your Codex agents directory:

Global:

```bash
python3 "${AGENTS_HOME:-$HOME/.agents}/skills/cast-subagents/scripts/install-agent-roles.py" --scope global
```

Project-only:

```bash
python3 "${AGENTS_HOME:-$HOME/.agents}/skills/cast-subagents/scripts/install-agent-roles.py" \
  --scope project \
  --path /path/to/repo
```

Without the bundled roles, cast-subagents still works — it will suggest lineups using whatever roles are already available in the Codex environment.

**4. Tell the user to restart Codex** so the skill and AGENTS rules are loaded.

## Verify

Check that the gate block was added:

```bash
grep -c "cast-subagents:start" "${CODEX_HOME:-$HOME/.codex}/AGENTS.md"
```

Expected output: `1`

Check that the skill directory exists:

```bash
ls "${AGENTS_HOME:-$HOME/.agents}/skills/cast-subagents/SKILL.md"
```

## Updating

Run the npx install command again:

```bash
npx skills add 917Dhj/cast-subagents -a codex
```

Re-run the gate installer to update the AGENTS block (the installer is idempotent — it updates in place):

```bash
python3 "${AGENTS_HOME:-$HOME/.agents}/skills/cast-subagents/scripts/install-agents-gate.py" --scope global
```

## Uninstalling

Remove the advisory gate block from AGENTS.md:

```bash
python3 "${AGENTS_HOME:-$HOME/.agents}/skills/cast-subagents/scripts/install-agents-gate.py" --scope global --remove
```

Remove the skill directory:

```bash
rm -rf "${AGENTS_HOME:-$HOME/.agents}/skills/cast-subagents"
```
