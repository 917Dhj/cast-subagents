# Role Lineups

Use this table when choosing the single recommended lineup.

| Scenario | Recommended roles | Why these roles fit | Work mode | Fallback |
| --- | --- | --- | --- | --- |
| Multi-axis PR review | `reviewer` + `code-mapper` + `docs-researcher` | reviewer finds risks, code-mapper traces ownership, docs-researcher verifies assumptions | read-only | If `docs-researcher` is unavailable, use `explorer` for evidence gathering and say the docs specialist is unavailable. |
| Read-heavy repo exploration | `code-mapper` + `search-specialist` | code-mapper traces the real path, search-specialist gathers high-signal evidence fast | read-only | Replace missing role with `explorer`. |
| Docs + codepath verification | `docs-researcher` + `code-mapper` | the task splits naturally into docs truth and code truth | read-only | Replace either missing role with `explorer`, but mention the downgrade. |
| Research + synthesis | `search-specialist` + `knowledge-synthesizer` | one agent gathers, the other consolidates | read-only | If `knowledge-synthesizer` is unavailable, keep one research role and synthesize in the main thread. |
| Planning a broad change | `task-distributor` + `code-mapper` | task-distributor structures the work, code-mapper grounds it in the real repo | read-only | Replace missing read role with `explorer`. |
| Exploration before a bounded fix | `code-mapper` + `reviewer` + `worker` | first understand, then risk-check, then apply one targeted implementation | mixed | If `worker` is unavailable, fall back to main-thread implementation after read-only delegation. |
| Coverage-focused follow-up | `reviewer` + `test-automator` | reviewer finds risky gaps, test-automator adds the smallest regression coverage | write-capable | If `test-automator` is unavailable, use `worker` and state that test automation will be more general. |
| Unavailable preferred role in a review task | `reviewer` + `explorer` | explorer stands in for evidence gathering when a specialist is missing | read-only | Always state the missing preferred role explicitly. |

Compression rules:

- Prefer 2 roles over 3 when the task can still be answered well.
- Prefer 3 roles over 4 unless four independent lanes are clearly justified.
- Never recommend 4 roles only to sound thorough.
- If one role adds only marginal value, drop it.

Write-safety rules:

- Any lineup containing `worker` or `test-automator` is write-capable.
- Mixed lineups should still start with read-only work.
- When the task is same-file or same-scope implementation, do not suggest a write-capable lineup at all.
