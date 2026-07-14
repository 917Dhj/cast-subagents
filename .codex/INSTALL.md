# Installing Cast Subagents for Codex

Cast Subagents is a Codex plugin that suggests one specialist lineup before complex work, waits for approval, and preserves bundled role settings across native and CLI execution backends.

This file is the only supported installation entry. Follow it as one agent-led flow; do not ask the user to run the role installer manually.

## Prerequisites

- Codex with plugin and Hook support
- Python 3.11+

## Installation

### 1. Add the repository marketplace

```bash
codex plugin marketplace add 917Dhj/cast-subagents
```

### 2. Install the plugin

```bash
codex plugin add cast-subagents@cast-subagents --json
```

Keep the returned `installedPath`; use that exact absolute path as `CAST_SUBAGENTS_PLUGIN` below. Do not infer a versioned cache directory because Git-backed marketplace plugins may use `local` as their cache version.

### 3. Choose the global Bundled Subagents

Show this complete table before asking which roles to install. Role numbers are stable and must not be reassigned.

| # | Role | GPT-5.6 model | Reasoning effort | Description |
|---:|---|---|---|---|
| 1 | `code-mapper` | `gpt-5.6-terra` | `high` | Trace code paths, files, symbols, and ownership boundaries. |
| 2 | `search-specialist` | `gpt-5.6-luna` | `medium` | Gather focused evidence from repositories or external sources. |
| 3 | `docs-researcher` | `gpt-5.6-luna` | `high` | Verify official APIs, versions, and documented guarantees. |
| 4 | `knowledge-synthesizer` | `gpt-5.6-luna` | `high` | Reconcile long or conflicting findings without inventing facts. |
| 5 | `task-distributor` | `gpt-5.6-sol` | `medium` | Split broad goals into bounded work packages. |
| 6 | `reviewer` | `gpt-5.6-sol` | `medium` | Review correctness, regressions, contracts, and maintainability. |
| 7 | `security-auditor` | `gpt-5.6-sol` | `high` | Audit trust boundaries, auth, secrets, and agent-tool safety. |
| 8 | `test-engineer` | `gpt-5.6-luna` | `xhigh` | Design minimal test coverage for behavior and risk. |
| 9 | `test-automator` | `gpt-5.6-terra` | `xhigh` | Add bounded regression tests after behavior is clear. |
| 10 | `web-performance-auditor` | `gpt-5.6-luna` | `xhigh` | Audit Web performance evidence and Core Web Vitals risks. |

Warn that each selected role overwrites an existing same-name global Agent file; unselected files remain untouched.

If `request_user_input` is available, ask one structured question with these options and allow the client's free-form choice:

- `Install recommended set (Recommended)` — roles 1, 3, 6, 7, 8, and 9.
- `Install all roles` — all ten roles.

Otherwise ask for `recommended`, `all`, or a custom role selection. Interpret the choice naturally, deduplicate it, and ask one concise follow-up only when the selection is unclear.

### 4. Run the Role Installer for the user

Set `CAST_SUBAGENTS_PLUGIN` to the exact `installedPath` returned in step 2. For example:

```bash
CAST_SUBAGENTS_PLUGIN="/absolute/path/from/the-installedPath-field"
```

Run the installer with `--overwrite` and one `--role` per selected role. For the recommended set:

```bash
python3 "$CAST_SUBAGENTS_PLUGIN/scripts/install-agent-roles.py" --overwrite \
  --role code-mapper \
  --role docs-researcher \
  --role reviewer \
  --role security-auditor \
  --role test-engineer \
  --role test-automator
```

The installer writes only to the global Agent directory under the effective Codex home.

### 5. Trust the SessionStart Hook

After the selected roles are installed, tell the user to open `/hooks`, review the Cast Subagents `SessionStart` command, and trust it before starting a new Codex task. Do not pause role installation while waiting for Hook trust. Codex's normal warning and fail-open behavior applies when the Hook is untrusted, skipped, times out, or fails.

### 6. Verify and restart

Verify the plugin and selected roles:

```bash
test -f "$CAST_SUBAGENTS_PLUGIN/skills/cast-subagents/SKILL.md"
test -f "${CODEX_HOME:-$HOME/.codex}/agents/code-mapper.toml"
```

Tell the user to start a new Codex task. The trusted `SessionStart` Hook and newly installed roles are loaded in the new task.

## Updating

Refresh the marketplace and reinstall the plugin:

```bash
codex plugin marketplace upgrade cast-subagents
codex plugin add cast-subagents@cast-subagents --json
```

Use the newly returned `installedPath`. Repeat the role selection and run the current release's Role Installer so selected global roles receive the new definitions. After the roles are installed, if Codex marks the changed Hook for review, ask the user to repeat `/hooks` trust before starting a new task.
