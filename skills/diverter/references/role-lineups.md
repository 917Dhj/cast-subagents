# Role Lineups

Choose capabilities first. Then keep only the roles that are available in the current Codex environment.

## Capability Map

| Capability | Preferred bundled role | Use when | Missing-role behavior |
| --- | --- | --- | --- |
| code mapping | `code-mapper` | tracing code paths, ownership, or execution flow | Drop the capability or handle mapping in the main thread after Dispatch Authorization. |
| code review | `reviewer` | general PR review, correctness, maintainability, contracts, regressions, and light security/test risk | Handle in the main thread or use another explicit review role if one is available. |
| security audit | `security-auditor` | auth, authorization, secrets, user input, webhooks, SSRF, dependencies, LLM/tool permissions, or exploitable vulnerability risk | Mention that security audit is not delegated; do not substitute a generic reviewer when security is central. |
| docs/API verification | `docs-researcher` | verifying documented API/framework behavior | Mention that docs verification is not delegated; do not substitute an unknown role. |
| search | `search-specialist` | gathering high-signal codebase or external evidence | Drop if code mapping or docs verification already covers the task. |
| synthesis | `knowledge-synthesizer` | consolidating multiple research outputs | Synthesize in the main thread after other agents return. |
| planning | `task-distributor` | decomposing broad work into bounded subtasks | Plan in the main thread if no planning role is available. |
| test strategy | `test-engineer` | coverage gaps, test plan, test level choice, or Prove-It regression planning | Handle test strategy in the main thread; do not jump directly to write-capable test automation. |
| test automation | `test-automator` | writing or updating targeted tests after scope is clear | Do not suggest write-capable testing if unavailable. |
| Web performance audit | `web-performance-auditor` | Core Web Vitals, Lighthouse, frontend route/component performance, loading, rendering, network, caching, images, fonts, or bundle risks | Handle in the main thread or skip the specialist if the task is not Web-specific. |

## Common Capability Lineups

| Scenario | Capability lineup | Preferred roles when available | Work mode |
| --- | --- | --- | --- |
| General PR review | code review + code mapping | `reviewer` + `code-mapper` | read-only |
| Multi-axis PR review with docs/API assumptions | code review + code mapping + docs/API verification | `reviewer` + `code-mapper` + `docs-researcher` | read-only |
| Security-sensitive review | security audit + code mapping + code review | `security-auditor` + `code-mapper` + `reviewer` | read-only |
| Auth / permission / token flow review | security audit + code mapping | `security-auditor` + `code-mapper` | read-only |
| LLM / agent tool safety review | security audit + code mapping + docs/API verification | `security-auditor` + `code-mapper` + `docs-researcher` | read-only |
| Test coverage analysis | test strategy + code mapping | `test-engineer` + `code-mapper` | read-only |
| Add targeted regression tests | test strategy + test automation + code mapping | `test-engineer` + `test-automator` + `code-mapper` | mixed |
| Web performance source audit | Web performance audit + code mapping | `web-performance-auditor` + `code-mapper` | read-only |
| Web performance audit with artifacts | Web performance audit | `web-performance-auditor` | read-only |
| Read-heavy repo exploration | code mapping + search | `code-mapper` + `search-specialist` | read-only |
| Docs + codepath verification | docs/API verification + code mapping | `docs-researcher` + `code-mapper` | read-only |
| Research + synthesis | search + synthesis | `search-specialist` + `knowledge-synthesizer` | read-only |
| Planning a broad change | planning + code mapping | `task-distributor` + `code-mapper` | read-only |
| Coverage-focused follow-up | code review + test automation | `reviewer` + `test-automator` | write-capable |
| Pre-ship quality gate | code review + security audit + test strategy + code mapping | `reviewer` + `security-auditor` + `test-engineer` + `code-mapper` | read-only |

## Compression Rules

- Recommend exactly one lineup made only of available roles.
- Prefer 2 roles over 3 when the task can still be answered well.
- If one unavailable capability is non-essential, drop it and keep the remaining useful lineup.
- If a missing capability is important, mention that the main thread can cover it after Dispatch Authorization.
- If no relevant roles are available, stay silent during implicit checks and continue normally.
- Never recommend 4 roles only to sound thorough.
- Ordinary PR review defaults to `reviewer + code-mapper`; do not add every quality specialist.
- Add `security-auditor` only for concrete security boundaries or explicit security audit requests.
- Add `test-engineer` only for test strategy, coverage gaps, proof, or regression planning.
- Add `test-automator` only when the user explicitly asks for test writes and the behavior scope is clear.
- Add `web-performance-auditor` only for Web-facing performance work.
- For non-Web performance, use `code-mapper + reviewer` only if the task is multi-lane.
- If more than 4 roles are triggered, keep the central specialist and `code-mapper`; drop non-core roles.

## Write-Safety Rules

- `test-automator` is write-capable because it may edit tests.
- Mixed lineups should start with read-only work. Under `ask`, pause before `test-automator` writes unless the user authorized the full mixed sequence; under `auto`, continue once the read-only scope is clear.
- Do not suggest write-capable implementation work unless an explicit write-capable role for that work is available.
