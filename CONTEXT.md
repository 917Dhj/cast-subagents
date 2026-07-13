# Cast Subagents

Cast Subagents recommends and supplies specialized subagents while leaving the parent Codex session under user control.

## Language

**Root Session**:
The user-controlled Codex session that evaluates a task, approves delegation, and integrates subagent results.
_Avoid_: Root agent configuration, managed root

**Bundled Subagent**:
A specialized agent definition shipped by Cast Subagents for delegated work. Cast Subagents owns its default model configuration, and every bundled role enables live web search without requiring it to be used.
_Avoid_: Root agent, parent agent

**Static Model Mapping**:
The release mapping from each Bundled Subagent role to a GPT-5.6 model and reasoning effort. It remains the default until later evaluations justify a revision, with no runtime routing or automatic fallback.
_Avoid_: Model router, model profile

| Bundled Subagent | Model | Reasoning effort |
| --- | --- | --- |
| `code-mapper` | `gpt-5.6-terra` | `high` |
| `search-specialist` | `gpt-5.6-luna` | `medium` |
| `docs-researcher` | `gpt-5.6-luna` | `high` |
| `knowledge-synthesizer` | `gpt-5.6-luna` | `high` |
| `task-distributor` | `gpt-5.6-sol` | `medium` |
| `reviewer` | `gpt-5.6-sol` | `medium` |
| `security-auditor` | `gpt-5.6-sol` | `high` |
| `test-engineer` | `gpt-5.6-luna` | `xhigh` |
| `test-automator` | `gpt-5.6-terra` | `xhigh` |
| `web-performance-auditor` | `gpt-5.6-luna` | `xhigh` |

**Recommended Role Set**:
The default installation selection for common Cast Subagents workflows: `code-mapper`, `docs-researcher`, `reviewer`, `security-auditor`, `test-engineer`, and `test-automator`.
_Avoid_: All roles, minimal roles

**Selected Role Set**:
The validated Bundled Subagents chosen through the `recommended`, `all`, or custom installation path. Only these roles are installed and overwritten.
_Avoid_: Lineup, active agents

**Role Installer**:
The plugin-provided script that installs the Selected Role Set into `${CODEX_HOME:-$HOME/.codex}/agents/` during the `.codex/INSTALL.md` flow. Codex runs it after installing the plugin; the user does not invoke it manually. It has no project-scoped mode and does not activate the Advisory Gate or modify instruction files.
_Avoid_: Gate installer, plugin installer

**Role Number**:
A stable numeric identifier used only to select a Bundled Subagent during installation. Existing numbers are never reassigned; new roles receive new numbers.
_Avoid_: Role order, priority

**Selection Intent**:
The set of Bundled Subagents the user means to install, interpreted by the Agent from structured or free-form input. The Agent asks again only when that intent is genuinely unclear; there is no user-facing input grammar.
_Avoid_: Selection syntax, parsed command

**Routing Smoke Test**:
The release check that starts one Terra, one Luna, and one Sol Bundled Subagent and confirms the requested model, reasoning effort, sandbox, and successful return.
_Avoid_: Quality evaluation, benchmark

**Execution Backend**:
The mechanism the Root Session uses after delegation approval to run a Bundled Subagent while preserving its Static Model Mapping, sandbox, and developer instructions.
_Avoid_: Model router, fallback model

**Native Subagent Backend**:
The preferred Execution Backend when the visible `spawn_agent` interface supports custom agent, model, and reasoning selectors.
_Avoid_: MultiAgent V1, default backend

**CLI Worker Backend**:
The compatibility Execution Backend that runs an independent `codex exec` process with the Bundled Subagent's explicit model, reasoning effort, sandbox, and instructions.
_Avoid_: Generic subagent mode, degraded mode

**CLI Worker Runner**:
The stateless, single-role Python 3.11+ plugin script that uses `tomllib` to read one installed Bundled Subagent TOML, accepts one delegated handoff on stdin, runs one `codex exec` worker, and returns its final output to the Root Session. Parallelism belongs to the Root Session, not the runner.
_Avoid_: Lineup orchestrator, worker daemon

**Backend Capability Check**:
The Root Session's inspection of the visible `spawn_agent` interface. Native Subagent Backend is selected only when the required selectors are exposed; otherwise CLI Worker Backend is selected without relying on the parent model name.
_Avoid_: Sol check, version check

**Advisory Gate**:
The Root Session checkpoint that decides whether a task merits a subagent recommendation before task work begins. It never starts subagents and always waits for user approval.
_Avoid_: Automatic spawning, delegation engine

**Advisory Gate Activation**:
The delivery of the Advisory Gate to a Root Session so that the checkpoint applies throughout that session.
_Avoid_: Automatic subagent trigger, AGENTS gate
