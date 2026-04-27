# Role Lineups

Choose capabilities first. Then keep only the roles that are available in the current Codex environment.

## Capability Map

| Capability | Preferred bundled role | Use when | Missing-role behavior |
| --- | --- | --- | --- |
| code mapping | `code-mapper` | tracing code paths, ownership, or execution flow | Drop the capability or handle mapping in the main thread after approval. |
| risk review | `reviewer` | finding correctness, security, test, or regression risks | Drop the capability if another role still covers a useful lane. |
| docs/API verification | `docs-researcher` | verifying documented API/framework behavior | Mention that docs verification is not delegated; do not substitute an unknown role. |
| search | `search-specialist` | gathering high-signal codebase or external evidence | Drop if code mapping or docs verification already covers the task. |
| synthesis | `knowledge-synthesizer` | consolidating multiple research outputs | Synthesize in the main thread after other agents return. |
| planning | `task-distributor` | decomposing broad work into bounded subtasks | Plan in the main thread if no planning role is available. |
| test automation | `test-automator` | adding or updating targeted regression coverage | Do not suggest write-capable delegation unless this role or another explicit test role is available. |

## Common Capability Lineups

| Scenario | Capability lineup | Preferred roles when available | Work mode |
| --- | --- | --- | --- |
| Multi-axis PR review | risk review + code mapping + docs/API verification | `reviewer` + `code-mapper` + `docs-researcher` | read-only |
| Read-heavy repo exploration | code mapping + search | `code-mapper` + `search-specialist` | read-only |
| Docs + codepath verification | docs/API verification + code mapping | `docs-researcher` + `code-mapper` | read-only |
| Research + synthesis | search + synthesis | `search-specialist` + `knowledge-synthesizer` | read-only |
| Planning a broad change | planning + code mapping | `task-distributor` + `code-mapper` | read-only |
| Exploration before test coverage | code mapping + risk review + test automation | `code-mapper` + `reviewer` + `test-automator` | mixed |
| Coverage-focused follow-up | risk review + test automation | `reviewer` + `test-automator` | write-capable |

## Compression Rules

- Recommend exactly one lineup made only of available roles.
- Prefer 2 roles over 3 when the task can still be answered well.
- If one unavailable capability is non-essential, drop it and keep the remaining useful lineup.
- If a missing capability is important, mention that the main thread can cover it after approval.
- If no relevant roles are available, stay silent during implicit checks and continue normally.
- Never recommend 4 roles only to sound thorough.

## Write-Safety Rules

- `test-automator` is write-capable because it may edit tests.
- Mixed lineups should start with read-only work and pause before `test-automator` writes.
- Do not suggest write-capable implementation work unless an explicit write-capable role for that work is available.
