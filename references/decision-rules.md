# Decision Rules

Use this table to decide whether a task should trigger a subagent suggestion.

| Task shape | Main signal | Suggest subagents? | Capability archetype | Notes |
| --- | --- | --- | --- | --- |
| Multi-axis PR review | several review dimensions on one diff | Yes | risk review + code mapping, optionally docs/API verification | Best when the user wants evidence from several angles in parallel. |
| Read-heavy codebase exploration | several paths or layers must be mapped | Yes | code mapping + search | Keep this read-only. |
| Docs/API verification | behavior must be checked against docs plus code | Yes | docs/API verification + code mapping | Use only if both code and docs matter. |
| Parallelizable research | independent questions can be explored separately | Yes | search + synthesis | Add code mapping only if a codebase path must also be traced. |
| Independent planning subtasks | one broad goal with separable investigations | Yes | planning + code mapping or search | Suggest only if the subtasks are truly independent. |
| Exploration before test coverage | read-heavy discovery first, then bounded regression coverage | Yes | code mapping + risk review + test automation | Mark as `mixed`; do not let test edits start before discovery is done. |
| Trivial single-domain task | one small change, one obvious lane | No | none | Suggesting subagents adds friction. |
| Tightly coupled write-heavy work | same files, same logic, same edit surface | No | none | Parallel write work is more likely to conflict than help. |
| Ambiguous request | unclear objective or missing success criteria | No | none | Clarify first. |
| Immediate critical-path fact lookup | one answer blocks everything else | No | none | Get the answer first, then reassess. |
| Explicit user opt-out | user says not to use subagents | No | none | Treat as a hard constraint. |
| Delegated subagent handoff | `delegation_context: delegated-subagent` or parent approval already completed | No | none | Execute the assigned handoff instead of recursing into advisory mode. |
| Style-only wording tweak | no specialist view or parallel lane is needed | No | none | Stay in the main thread. |

Practical tie-breakers:

| Tie-breaker | Preferred decision | Why |
| --- | --- | --- |
| The task is mostly read-heavy | Lean toward suggesting | Read-heavy delegation is safer and more predictable. |
| The task is mostly write-heavy | Lean toward not suggesting | Delegation overhead and merge risk increase quickly. |
| The task needs both docs and code verification | Lean toward suggesting | Those lanes parallelize cleanly. |
| The task needs clarification first | Do not suggest yet | The lineup will be low quality until intent is clear. |
| A good capability split would need more than 4 roles | Compress or do not suggest | v1 explicitly caps the role lineup at 4. |
| No relevant role is available for the needed capability | Stay silent unless the user asked about setup | Do not recommend role names that are not present. |
