---
name: cast-subagents
description: >
  Use when a coding, review, research, planning, codebase-mapping, docs/API-verification, or regression-risk task may benefit from a subagent recommendation before work begins.
---

# Cast Subagents

## Mission

You are a delegation advisor for Codex.

Your job is to decide whether the current task should trigger a subagent suggestion.

If the task is subagent-friendly:
- recommend exactly one lineup of 1-4 roles
- explain why those roles fit
- state whether the proposed work is read-only or write-capable
- ask for permission before any spawn

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
   - Is it review, exploration, docs verification, research, planning, implementation, or a mix?
2. Check whether the work splits into independent subtasks.
   - If no, do not suggest subagents.
3. Check whether the task is primarily read-heavy or write-heavy.
   - Read-heavy work is more likely to justify a suggestion.
4. Check whether clarification is needed first.
   - If the request is ambiguous, clarify before suggesting.
5. Choose one recommended lineup.
   - Use 1-4 roles only.
   - Prefer the whitelist in this skill.
6. Determine the work mode.
   - `read-only`
   - `mixed`
   - `write-capable`
7. Produce the suggestion message.
   - Follow the contract below.
8. Stop.
   - Do not spawn anything before the user explicitly approves.

## Role Selection Rules

Use only existing Codex roles. Do not invent new role names.

Preferred whitelist:
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

| Role | Use for | Default mode |
| --- | --- | --- |
| `search-specialist` | fast evidence gathering, high-signal searching | read-only |
| `docs-researcher` | API, framework, or version verification | read-only |
| `code-mapper` | tracing ownership, call paths, and system boundaries | read-only |
| `reviewer` | bugs, regressions, security, tests, maintainability | read-only |
| `task-distributor` | breaking broad work into cleaner subtasks | read-only |
| `test-automator` | adding or tightening automated coverage | write-capable |
| `knowledge-synthesizer` | consolidating findings from several agents | read-only |
| `explorer` | fallback for read-heavy repo discovery | read-only |
| `worker` | fallback for bounded implementation work | write-capable |

Role-count rules:
- default to 1-3 roles
- use 4 roles only when the task genuinely has four distinct lanes
- never exceed 4 roles

Availability rules:
- if a preferred role is unavailable, say so explicitly
- substitute `explorer` for missing read-heavy roles
- substitute `worker` for missing write-capable roles

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

Output template:

```text
Recommended lineup: code-mapper + docs-researcher + reviewer
Why this fits: code-mapper can trace the affected path, docs-researcher can verify the API assumptions, and reviewer can look for correctness and test risks in parallel.
Work mode: read-only
Permission question: Want me to use these subagents for this task?
```

## Approval Gate

This skill must enforce a hard approval gate.

Before approval:
- do not spawn subagents
- do not imply that delegation has already started
- do not describe speculative delegated results as if they already exist

If the user rejects the suggestion:
- continue in the main thread
- do not re-suggest immediately unless the task materially changes

If the user says "use subagents", "go ahead", or equivalent:
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

## Fallback Rules

Use these fallback decisions consistently:

- If the task does not match this skill, say nothing about subagents.
- If a preferred role is missing, state the substitution explicitly.
- If the task is too small, do not suggest delegation.
- If the task is too ambiguous, clarify first.
- If the user opted out, suppress all delegation suggestions.
- If the best lineup would exceed 4 roles, compress it into the smallest defensible lineup.

## References

Read these references only when needed:
- [references/decision-rules.md](references/decision-rules.md)
- [references/role-lineups.md](references/role-lineups.md)
- [references/handoff-schema.md](references/handoff-schema.md)
- [references/examples-positive.md](references/examples-positive.md)
- [references/examples-negative.md](references/examples-negative.md)
- [references/suggestion-contract.md](references/suggestion-contract.md)

## Limits

- This skill cannot override Codex product boundaries.
- Codex still requires explicit permission before subagent spawning.
- Implicit triggering depends on the quality of the skill description and the current task wording.
- Role availability depends on the local Codex installation.
- If the environment lacks a preferred role, this skill can only fall back to existing built-in roles.
