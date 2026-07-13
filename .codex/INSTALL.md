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

**3. Choose and install bundled agent roles.**

Show this complete table before asking the user which roles to install. Role numbers are stable and must not be reassigned.

| # | Role | GPT-5.6 model | Reasoning effort | Description |
|---:|---|---|---|---|
| 1 | `code-mapper` | `gpt-5.6-terra` | `medium` | Trace code paths, files, symbols, and ownership boundaries. |
| 2 | `search-specialist` | `gpt-5.6-luna` | `medium` | Gather focused evidence from repositories or external sources. |
| 3 | `docs-researcher` | `gpt-5.6-luna` | `high` | Verify official APIs, versions, and documented guarantees. |
| 4 | `knowledge-synthesizer` | `gpt-5.6-luna` | `high` | Reconcile long or conflicting findings without inventing facts. |
| 5 | `task-distributor` | `gpt-5.6-sol` | `medium` | Split broad goals into bounded work packages. |
| 6 | `reviewer` | `gpt-5.6-sol` | `medium` | Review correctness, regressions, contracts, and maintainability. |
| 7 | `security-auditor` | `gpt-5.6-sol` | `high` | Audit trust boundaries, auth, secrets, and agent-tool safety. |
| 8 | `test-engineer` | `gpt-5.6-luna` | `high` | Design minimal test coverage for behavior and risk. |
| 9 | `test-automator` | `gpt-5.6-terra` | `xhigh` | Add bounded regression tests after behavior is clear. |
| 10 | `web-performance-auditor` | `gpt-5.6-luna` | `high` | Audit Web performance evidence and Core Web Vitals risks. |

Warn the user that every selected role will overwrite any existing same-name agent file. Unselected roles remain untouched.

If `request_user_input` is available, ask exactly one structured question with these two explicit options; let the client provide its automatic `Other` free-text input:

- `Install recommended set (Recommended)` — installs and overwrites roles 1, 3, 6, 7, 8, and 9.
- `Install all roles` — installs and overwrites all 10 roles.

If `request_user_input` is unavailable, ask the user to reply with `recommended`, `all`, or describe the roles they want, such as `1,2,3`, then wait for the reply.

Interpret the user's selection naturally rather than enforcing a formal input grammar. Deduplicate the resulting roles and map only to roles in the table. If the selection intent is unclear or requests an unavailable role, ask one concise follow-up and do not run the installer yet.

Expand `recommended` to roles 1, 3, 6, 7, 8, and 9. Expand `all` to roles 1 through 10. Once the selection is clear, call the existing installer with `--overwrite` and one `--role` argument per selected role. Use the global or project scope already chosen by the user. For example, the recommended global install is:

```bash
python3 "$CAST_SUBAGENTS_HOME/scripts/install-agent-roles.py" --scope global --overwrite \
  --role code-mapper \
  --role docs-researcher \
  --role reviewer \
  --role security-auditor \
  --role test-engineer \
  --role test-automator
```

If the user declines bundled roles, continue without running the role installer. cast-subagents can still use available roles, but preferred lineups may degrade when roles are missing.

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

Repeat the role selection in step 3 to migrate selected bundled roles to the current release. Selected same-name files are overwritten.

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
