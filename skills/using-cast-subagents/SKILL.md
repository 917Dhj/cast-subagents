---
name: using-cast-subagents
description: Use when starting any conversation or before any Codex response, action, file read, command, analysis, or clarifying question - establishes the always-on cast-subagents gate so Codex can decide whether to recommend a subagent lineup or stay silent.
---

# Using Cast Subagents

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill and complete only the assigned task.
</SUBAGENT-STOP>

## Mission

Before any response or action, decide whether the user would benefit from a subagent suggestion.

This is an always-on gatekeeper skill. It makes the cast-subagents rules visible before work begins, but it never spawns subagents.

## Always-On Gate

Before any response, clarifying question, file read, command, analysis, or task answer, read and apply this gate.

The purpose of this gate is not to force delegation. The purpose is to decide whether to suggest a lineup or stay silent.

## Decision Rule

If the task is subagent-friendly, output the suggestion contract first and stop. Do not answer task content until the user approves or declines.

If the task is not subagent-friendly, say nothing about subagents and continue normally.

## Suggest When

Suggest a lineup when the task has independent lanes such as:
- multi-axis branch or PR review
- read-heavy codebase mapping
- codepath plus docs/API verification
- option research and tradeoff synthesis
- regression-risk evidence gathering
- broad planning that can split into independent subtasks

## Silent Cases

Do not mention subagents when the task is:
- trivial or single-domain
- single-lane
- tightly coupled same-file work
- ambiguous and needs clarification first
- blocked on one immediate fact lookup
- wording-only
- explicitly opted out of subagents

## Minimum Lineups

Use `cast-subagents` for the full contract when available. This entry skill still has enough mapping to suggest directly when needed.

| Task shape | Recommended lineup | Work mode |
| --- | --- | --- |
| Branch or PR review across bugs, security, tests, docs, maintainability, or risk | `reviewer + code-mapper + docs-researcher` | read-only |
| Codepath plus docs/API verification | `code-mapper + docs-researcher` | read-only |
| Option research or tradeoff synthesis | `search-specialist + knowledge-synthesizer` | read-only |
| Codepath plus docs/API when `docs-researcher` is unavailable | `code-mapper + explorer` | read-only |
| Mixed codepath, docs/API verification, and regression-risk review | `code-mapper + docs-researcher + reviewer` | read-only |

Use only existing roles. If a preferred role is unavailable, say so and use `explorer` for read-heavy fallback. Never recommend more than 4 roles.

## Suggestion Contract

When suggesting, output exactly these four sections:

```text
Recommended lineup: <1-4 existing roles from the mapping>
Why this fits: <one task-specific sentence>
Work mode: <read-only | mixed | write-capable>
Permission question: <direct approval question>
```

Then stop. Do not spawn subagents or imply delegation has started.

## Approval Outcome

If the user rejects the suggestion, continue in the main thread and do not immediately re-suggest.

If the user approves, keep read-heavy work read-only first. Use write-capable agents only for bounded scopes, and serialize them unless their write areas are clearly disjoint.
