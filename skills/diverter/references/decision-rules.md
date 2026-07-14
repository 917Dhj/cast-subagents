# Decision Rules

Use this table to decide whether a task should trigger delegation.

| Task shape | Main signal | Suggest subagents? | Capability archetype | Notes |
| --- | --- | --- | --- | --- |
| Multi-axis PR review | several review dimensions on one diff | Yes | code review + code mapping, optionally docs/API verification | Best when the user wants evidence from several angles in parallel. |
| Read-heavy codebase exploration | several paths or layers must be mapped | Yes | code mapping + search | Keep this read-only. |
| Docs/API verification | behavior must be checked against docs plus code | Yes | docs/API verification + code mapping | Use only if both code and docs matter. |
| Parallelizable research | independent questions can be explored separately | Yes | search + synthesis | Add code mapping only if a codebase path must also be traced. |
| Independent planning subtasks | one broad goal with separable investigations | Yes | planning + code mapping or search | Suggest only if the subtasks are truly independent. |
| Exploration before test coverage | read-heavy discovery first, then bounded regression coverage | Yes | code mapping + code review + test automation | Mark as `mixed`; do not let test edits start before discovery is done. |
| Security-sensitive review | mentions auth, authorization, session, token, secrets, user input, webhook, SSRF, prompt injection, tool permission, or multi-tenant data | Yes | security audit + code mapping, optionally code review | Use `security-auditor`; do not rely only on generic `reviewer` when security is central. |
| Test strategy / coverage analysis | asks what tests are missing, whether tests are enough, or how to prove a bug fix | Yes | test strategy + code mapping | Use read-only `test-engineer`; do not jump to `test-automator`. |
| Targeted test implementation | asks to add or update tests for a known bug or risk | Yes | test strategy + test automation, optionally code mapping | Use `mixed` unless scope is already clear and bounded. |
| Web performance audit | mentions Lighthouse, Core Web Vitals, LCP, INP, CLS, frontend route, rendering, loading, bundle, caching, images, fonts, or network behavior | Yes | Web performance audit + code mapping | Use only for Web projects or Web-facing components. |
| Pre-ship quality gate | asks for release readiness across code quality, tests, security, and risk | Yes | code review + security audit + test strategy, optionally code mapping | Keep read-only unless the user explicitly asks to fix. |
| LLM / agent safety review | mentions prompt injection, tool permissions, agent delegation, secrets in context, cross-tenant context, or destructive tools | Yes | security audit + code mapping + docs/API verification | Treat as security-sensitive. |
| Trivial single-domain task | one small change, one obvious lane | No | none | Suggesting subagents adds friction. |
| Tightly coupled write-heavy work | same files, same logic, same edit surface | No | none | Parallel write work is more likely to conflict than help. |
| Ambiguous request | unclear objective or missing success criteria | No | none | Clarify first. |
| Immediate critical-path fact lookup | one answer blocks everything else | No | none | Get the answer first, then reassess. |
| Explicit user opt-out | user says not to use subagents | No | none | Treat as a hard constraint. |
| Delegated subagent handoff | current task message explicitly says this is a delegated subagent task or includes `delegation_context: delegated-subagent` | No | none | Execute the assigned handoff instead of recursing into the Delegation Gate. |
| Style-only wording tweak | no specialist view or parallel lane is needed | No | none | Stay in the main thread. |
| Generic small PR review | only asks for one narrow bug, one small file, or style-only review | No | none | Avoid over-triggering multiple roles. |
| Non-Web performance task | CLI, backend algorithm, database performance, compiler/runtime issue without Web UI | Maybe, but not `web-performance-auditor` | code mapping + code review | Use `code-mapper + reviewer` only if task is multi-lane. |
| Test code writing without clear behavior | asks to add tests but target behavior is ambiguous | No | none | Clarify first; after the behavior boundary is known, use `test-engineer` before `test-automator`. |
| Security buzzword only | user says "make it secure" with no artifact, flow, or trust boundary | No | none | Clarify first. |

Practical tie-breakers:

| Tie-breaker | Preferred decision | Why |
| --- | --- | --- |
| The task is mostly read-heavy | Lean toward suggesting | Read-heavy delegation is safer and more predictable. |
| The task is mostly write-heavy | Lean toward not suggesting | Delegation overhead and merge risk increase quickly. |
| The task needs both docs and code verification | Lean toward suggesting | Those lanes parallelize cleanly. |
| The task needs clarification first | Do not suggest yet | The lineup will be low quality until intent is clear. |
| A good capability split would need more than 4 roles | Compress or do not suggest | v1 explicitly caps the role lineup at 4. |
| No relevant role is available for the needed capability | Stay silent unless the user asked about setup | Do not recommend role names that are not present. |
| Specialist role would not add an independent viewpoint | Do not add it | Specialist names should reduce ambiguity, not decorate the lineup. |
| Security boundary is central | Prefer `security-auditor` over generic `reviewer` | Deep security review needs a focused threat model. |
| Test strategy is central | Prefer `test-engineer` over generic `reviewer` | Coverage planning is different from PR review. |
| Web performance is central | Prefer `web-performance-auditor` over generic `reviewer` | Web metrics require measured-vs-potential discipline. |
