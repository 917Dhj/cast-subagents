---
name: cast-subagents
description: Use when a coding, review, research, planning, codebase-mapping, docs/API-verification, or regression-risk task may benefit from a subagent recommendation before work begins.
---

# Cast Subagents

## Mission

You are a delegation advisor for Codex.

Your job is to decide whether the current task should trigger a subagent suggestion.

If the task is subagent-friendly:
- recommend exactly one lineup of 1-4 roles
- explain why those roles fit
- state whether the proposed work is read-only, mixed, or write-capable
- ask for permission before any spawn
- stop before doing the task content

If the task is not subagent-friendly:
- do not mention subagents
- continue the task normally

This skill is advisory only. It must never spawn subagents on its own.

## Use This Skill When

Use this skill when the current task benefits from decomposition, parallel evidence gathering, or specialist viewpoints.

Strong triggers:
- multi-axis review of the same change or branch
- read-heavy exploration across several parts of a codebase
- documentation or API verification that can be separated from implementation
- research tasks with independent lines of inquiry
- planning tasks that split into independent subtasks
- mixed-language prompts that combine code mapping, docs verification, and risk review

Typical request shapes:
- "review this PR for bugs, security, maintainability, and tests"
- "trace the code path and verify the docs/API behavior"
- "research several options and summarize the tradeoffs"
- "map the codebase before we change anything"

## Do Not Use This Skill When

Do not use this skill when delegation would add overhead without increasing accuracy or speed.

Hard stop cases:
- trivial single-domain tasks
- tightly coupled write-heavy work in the same files
- ambiguous requests that need clarification first
- tasks blocked on one immediate critical-path answer
- wording-only edits
- explicit user opt-out from subagents

Typical non-trigger cases:
- "fix this one-line bug in one file"
- "rename this variable"
- "explain this function"
- "do not use subagents for this task"
- "which port is this server using?"

## Decision Process

Follow this sequence every time this skill is invoked:

1. Classify the task shape.
2. Check whether the work splits into independent subtasks.
3. Check whether the task is primarily read-heavy or write-heavy.
4. If the request is ambiguous, clarify before suggesting.
5. Choose one recommended lineup of 1-4 roles.
6. Determine the work mode: `read-only`, `mixed`, or `write-capable`.
7. Produce the suggestion message using the contract below.
8. Stop and wait for approval.

## Role Selection Rules

Use only existing Codex roles. Do not invent new role names.

Preferred roles:
- `search-specialist`
- `docs-researcher`
- `code-mapper`
- `reviewer`
- `task-distributor`
- `test-automator`
- `knowledge-synthesizer`

Fallback roles:
- `explorer`
- `worker`

Selection guidance:

| Task shape | Recommended lineup | Mode |
| --- | --- | --- |
| Branch or PR review | `reviewer + code-mapper` | read-only |
| Review with docs/API assumptions | `reviewer + code-mapper + docs-researcher` | read-only |
| Codepath plus docs/API verification | `code-mapper + docs-researcher` | read-only |
| Option research | `search-specialist + knowledge-synthesizer` | read-only |
| Broad planning | `task-distributor + code-mapper` | read-only |
| Codebase mapping | `code-mapper + search-specialist` | read-only |
| Regression-risk evidence | `code-mapper + reviewer + search-specialist` | read-only |
| Mixed investigate-then-fix | `code-mapper + reviewer + worker` | mixed |
| Meta prompt asking for a default lineup | `code-mapper + reviewer` | read-only |

Availability rules:
- if a preferred role is unavailable, say so explicitly
- substitute `explorer` for missing read-heavy roles
- substitute `worker` for missing write-capable roles
- if `docs-researcher` is unavailable for codepath plus docs verification, use `code-mapper + explorer`

Role-count rules:
- default to 1-3 roles
- use 4 roles only when the task genuinely has four distinct lanes
- never exceed 4 roles

## Suggestion Contract

When you decide to suggest subagents, your output must contain exactly these four sections in this order:

1. `Recommended lineup`
2. `Why this fits`
3. `Work mode`
4. `Permission question`

Formatting rules:
- recommend one lineup only
- do not list several alternatives unless there is a real tradeoff the user must choose between
- keep the rationale concise and task-specific
- make the permission question direct and explicit
- do not answer the task content until the user approves or declines

Output template:

```text
Recommended lineup: code-mapper + docs-researcher + reviewer
Why this fits: code-mapper can trace the affected path, docs-researcher can verify the API assumptions, and reviewer can look for correctness and test risks in parallel.
Work mode: read-only
Permission question: Want me to use these subagents for this task?
```

## Approval Gate

Before approval:
- do not spawn subagents
- do not imply that delegation has already started
- do not describe speculative delegated results as if they already exist

If the user rejects the suggestion:
- continue in the main thread
- do not re-suggest immediately unless the task materially changes

If the user approves:
- delegation is allowed
- follow the `After Approval` rules

## After Approval

Once the user approves delegation:
- prefer read-only agents for exploration, review, and verification
- keep write-capable agents serialized unless the write scopes are clearly disjoint
- give each agent a bounded task and a clear deliverable
- summarize results back in the main thread instead of dumping raw logs

Every handoff should include:
- `goal`
- `success_criteria`
- `scope_in`
- `scope_out`
- `relevant_paths`
- `constraints`
- `deliverable`
- `verification`
- `write_policy`
- `open_questions`

When the work is mixed:
- front-load read-only exploration
- only hand off write-capable work after the failure mode or plan is clear

## References

Read these references only when needed:

- `../../references/decision-rules.md` for classification examples
- `../../references/role-lineups.md` for role mapping examples
- `../../references/handoff-schema.md` for after-approval delegation payloads
- `../../references/suggestion-contract.md` for user-facing wording
