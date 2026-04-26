---
name: using-cast-subagents
description: "Use when deciding whether to suggest Codex subagents or parallel agents before multi-lane work: branch/PR review for bugs, security, tests, maintainability, docs, or regression risk; codepath tracing plus docs/API verification; option research with tradeoff synthesis; auth/codebase mapping before risk assessment or planning. Stay silent for trivial single-file fixes, wording-only edits, one fact lookup, unclear requests, or explicit opt-out."
---

# Using Cast Subagents

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill and complete only the assigned task.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
Before any Codex response, action, file read, command, analysis, implementation, review, planning step, or clarifying question, you MUST read and apply this gate.

This does not mean you should mention subagents every time. It means you must check whether a subagent suggestion is warranted.

If the task is not subagent-friendly, stay completely silent about subagents and continue normally.
</EXTREMELY-IMPORTANT>

## Mission

Before any response or action, decide whether the user would benefit from a subagent suggestion.

This is an always-on gatekeeper skill. It makes the cast-subagents rules visible before work begins, but it never spawns subagents.

## Always-On Gate

Before any response, clarifying question, file read, command, analysis, implementation, review, planning step, or task answer, read and apply this gate.

The purpose of this gate is not to force delegation. The purpose is to decide whether to suggest a lineup or stay silent.

This is a two-stage process:

1. Stage 1: internally check whether the task is subagent-friendly.
2. Stage 2: only if Stage 1 says yes, output a visible subagent suggestion.

Most checks should produce no visible output. If the task does not warrant a suggestion, do not mention this gate, this skill, subagents, or delegation.

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

## Red Flags

These thoughts mean you are about to skip the gate. Stop and apply it first.

| Thought | Reality |
| --- | --- |
| "This is probably simple." | Simple tasks still get the silent gate check. |
| "I should inspect files first." | The gate comes before file reads or commands. |
| "The user did not mention subagents." | The gate decides whether to suggest them. |
| "Another skill applies." | Apply this gate before or alongside other process skills. |
| "I can answer quickly." | Quick answers still start with the silent gate check. |
| "Mentioning subagents would be annoying." | If the task is not a fit, stay silent after checking. |

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

When suggesting, write a short, conversational message. Do not use fixed section labels.

The message must convey these four pieces in order:
1. why this task could benefit from subagents
2. one recommended lineup of 1-4 exact role names, with task-specific reasons
3. the work mode, stated exactly as `read-only`, `mixed`, or `write-capable`
4. a direct permission question that matches the work mode

End with a question, then stop. Do not spawn subagents, answer task content, imply delegation has started, or use a stale template.

## Approval Outcome

If the user rejects the suggestion, continue in the main thread and do not immediately re-suggest.

If the user approves, keep read-heavy work read-only first. Use write-capable agents only for bounded scopes, and serialize them unless their write areas are clearly disjoint.
