# Handoff Schema

Every delegated task should use the same minimum payload shape.

| Field | Required content | Why it exists | Good example |
| --- | --- | --- | --- |
| `delegation_context` | the explicit delegated-subagent bypass | prevents recursive advisory gates | `delegated-subagent; parent approval already completed; do not invoke cast-subagents or request another delegation approval; execute this handoff only` |
| `goal` | the exact sub-problem the agent owns | prevents scope drift | `Map the auth failure path for the save-settings flow.` |
| `success_criteria` | what counts as done | keeps the result verifiable | `Return the real call path, owning files, and likely failure boundary.` |
| `scope_in` | what is in scope | defines ownership | `settings modal save path, client mutation, API handler` |
| `scope_out` | what is explicitly out of scope | prevents adjacent work | `do not edit code, do not review unrelated forms` |
| `relevant_paths` | files, folders, symbols, or entrypoints to inspect | speeds up grounding | `src/settings/, app/api/settings/, useSettingsForm` |
| `constraints` | process or safety constraints | preserves parent intent | `read-only only; cite concrete files and symbols` |
| `deliverable` | exact output expected from the subagent | makes integration easier | `3-5 bullet summary with file references` |
| `verification` | how the parent will check the result | improves quality | `must include at least one concrete code path and one likely failure point` |
| `write_policy` | read-only, mixed, or write-capable policy | avoids unsafe delegation | `read-only` |
| `open_questions` | unresolved unknowns the agent should keep visible | prevents silent guessing | `whether the API uses optimistic updates before the save completes` |

Recommended Markdown template:

```md
delegation_context: delegated-subagent; parent approval already completed; do not invoke cast-subagents or request another delegation approval; execute this handoff only
goal: Map the affected code path for the settings save failure.
success_criteria: Identify the real execution path, likely failure boundary, and the files that own the behavior.
scope_in: settings modal, client mutation, API route, response handling
scope_out: unrelated settings pages, styling, copy updates
relevant_paths: src/settings/, app/api/settings/, useSettingsForm
constraints: read-only; no code edits; cite concrete files and symbols
deliverable: concise summary with file references and one likely root cause candidate
verification: parent can trace the same path from your references
write_policy: read-only
open_questions: whether retries or optimistic state updates affect the failure mode
```

Delegation context is the recursion guard. A child agent should bypass cast-subagents only when the current task message explicitly says this is a delegated subagent task or includes `delegation_context: delegated-subagent`; then it should execute the assigned handoff directly instead of suggesting another subagent lineup.

## Spawn Context Policy

Write each handoff as if the child agent starts fresh, with no useful chat history. The parent thread should put task-critical context directly in the handoff: goal, scope, file paths, URLs, IDs, constraints, deliverable, and verification method.

Default spawn shape:

```text
agent_type: docs-researcher
fork_context: false
prompt: <structured handoff with delegation_context>
```

Avoid combining role-specific spawning with full-history fork:

```text
bad: agent_type: docs-researcher + fork_context: true
good: agent_type: docs-researcher + delegation_context + structured handoff
```

Use `fork_context` only when exact conversation history matters more than role specialization. In that case, do not specify `agent_type`; the child inherits the parent agent type.

Write-policy meanings:

| Value | Meaning |
| --- | --- |
| `read-only` | the agent must not edit files |
| `mixed` | the parent expects read-first work before any writes |
| `write-capable` | the agent may edit, but only within the stated scope |

v1 rule:
- if a handoff would be weak without several open questions answered first, do not delegate yet
