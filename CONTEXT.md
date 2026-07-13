# Cast Subagents

Cast Subagents recommends and supplies specialized subagents while leaving the parent Codex session under user control.

## Language

**Root Session**:
The user-controlled Codex session that evaluates a task, approves delegation, and integrates subagent results.
_Avoid_: Root agent configuration, managed root

**Bundled Subagent**:
A specialized agent definition shipped by Cast Subagents for delegated work. Cast Subagents owns its default model configuration.
_Avoid_: Root agent, parent agent

**Static Model Mapping**:
The release mapping from each Bundled Subagent role to a GPT-5.6 model and reasoning effort. It remains the default until later evaluations justify a revision, with no runtime routing or automatic fallback.
_Avoid_: Model router, model profile

**Recommended Role Set**:
The default installation selection for common Cast Subagents workflows: `code-mapper`, `docs-researcher`, `reviewer`, `security-auditor`, `test-engineer`, and `test-automator`.
_Avoid_: All roles, minimal roles

**Selected Role Set**:
The validated Bundled Subagents chosen through the `recommended`, `all`, or custom installation path. Only these roles are installed and overwritten.
_Avoid_: Lineup, active agents

**Role Number**:
A stable numeric identifier used only to select a Bundled Subagent during installation. Existing numbers are never reassigned; new roles receive new numbers.
_Avoid_: Role order, priority

**Selection Intent**:
The set of Bundled Subagents the user means to install, interpreted by the Agent from structured or free-form input. The Agent asks again only when that intent is genuinely unclear; there is no user-facing input grammar.
_Avoid_: Selection syntax, parsed command
