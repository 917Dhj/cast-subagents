# cast-subagents

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A Codex skill that suggests exactly one subagent lineup for complex tasks, then waits for your approval before any delegation starts.

Cast Subagents is intentionally advisory. It does not spawn agents by itself, inspect files before approval, or force delegation into small tasks. It speaks up only when a task has independent work lanes, such as multi-axis review, codebase mapping, docs/API verification, option research, or regression-risk analysis.

## How It Works

Cast Subagents uses two pieces:

1. `AGENTS.md` advisory gate: a short managed block that tells Codex when to invoke `$cast-subagents`.
2. `SKILL.md`: the full advisor that classifies the task, chooses one lineup, states the work mode, asks permission, and stops.

The AGENTS gate is the trigger. The skill is the playbook.

For trivial tasks, single-file edits, one immediate fact lookup, unclear requests, or explicit opt-out prompts, Codex should continue normally and never mention subagents.

## Example

```text
> Review this branch against main for bugs, security issues, missing tests,
  and maintainability risks.

I think this is a good fit for subagents. I'd put reviewer on correctness
and test risks, code-mapper on the affected paths, and docs-researcher on
the API assumptions in the diff, since those are separate angles they can
inspect in parallel. Work mode is read-only. Want me to send them in to take
a look before you decide?
```

The suggestion always includes:

- why the task could benefit from subagents
- one exact lineup with a reason for each role
- one work mode: `read-only`, `mixed`, or `write-capable`
- a direct permission question

## Installation

Install the skill into Codex:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo 917Dhj/cast-subagents \
  --path . \
  --name cast-subagents
```

If the repository is private, make sure your shell has GitHub access through existing git credentials, `GH_TOKEN`, or `GITHUB_TOKEN`.

Then install the AGENTS gate globally:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/cast-subagents/scripts/install-agents-gate.py" --scope global
```

Restart Codex after installation so the skill and AGENTS rules are loaded.

## AGENTS Gate Options

Global install is recommended because it applies to all Codex workspaces:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/cast-subagents/scripts/install-agents-gate.py" --scope global
```

Project-level install is useful when you only want this behavior in one repository:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/cast-subagents/scripts/install-agents-gate.py" \
  --scope project \
  --path /path/to/repo
```

The installer manages only this block:

```md
<!-- cast-subagents:start -->
## Subagent Advisory Gate

Before starting any non-trivial coding, review, research, planning, codebase-mapping, docs/API-verification, or regression-risk task, check whether it matches the cast-subagents trigger patterns.

If it matches, invoke `$cast-subagents` first, suggest exactly one lineup, and stop before inspecting files, running commands, searching docs, summarizing findings, or starting implementation.

If it does not match, continue normally and do not mention subagents.
<!-- cast-subagents:end -->
```

If `AGENTS.md` already exists, the installer preserves everything outside the managed block. Re-running the installer updates the block in place.

Remove the managed block with:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/cast-subagents/scripts/install-agents-gate.py" --scope global --remove
```

Preview without writing:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/cast-subagents/scripts/install-agents-gate.py" --scope global --dry-run
```

## Updating

Update the installed skill by removing the old copy and installing again:

```bash
rm -rf "${CODEX_HOME:-$HOME/.codex}/skills/cast-subagents"
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo 917Dhj/cast-subagents \
  --path . \
  --name cast-subagents
```

Then re-run the AGENTS gate installer. It is idempotent and only updates the managed block.

## Decision Rules

Cast Subagents should speak up for:

- multi-axis branch or PR review
- read-heavy codebase mapping
- codepath tracing plus docs/API verification
- option research and tradeoff synthesis
- regression-risk evidence gathering
- broad planning with separable subtasks

It should stay quiet for:

- trivial or single-domain tasks
- tightly coupled same-file work
- ambiguous requests that need clarification first
- one immediate fact lookup
- wording-only edits
- explicit opt-out from subagents

## Roles

Preferred role names:

- `search-specialist`
- `docs-researcher`
- `code-mapper`
- `reviewer`
- `task-distributor`
- `test-automator`
- `knowledge-synthesizer`

Fallback roles:

- `explorer`
- `worker`

The role names are coordination labels. They should match the subagent roles available in your Codex environment.

## Project Structure

```text
cast-subagents/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── decision-rules.md
│   ├── examples-negative.md
│   ├── examples-positive.md
│   ├── handoff-schema.md
│   ├── role-lineups.md
│   └── suggestion-contract.md
├── scripts/
│   └── install-agents-gate.py
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## License

This project is released under the [MIT License](LICENSE).
