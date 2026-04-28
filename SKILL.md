---
name: cast-subagents
description: "Use when suggesting exactly one Codex subagent lineup before work begins for multi-lane tasks: branch/PR review across bugs, security, tests, maintainability, docs, or regression risk; codepath tracing plus docs/API verification; option research with tradeoff synthesis; auth/codebase mapping before risk assessment or planning. Advisory only; no auto-spawn; approval required. Do not use for delegated subagent handoffs, trivial single-file fixes, wording-only edits, one fact lookup, unclear requests, or explicit opt-out."
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
- do not inspect files, run commands, search docs, summarize findings, or start implementation before approval
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
- delegated subagent handoffs where parent approval already completed
- trivial single-domain tasks
- tightly coupled write-heavy work in the same files
- ambiguous requests that need clarification first
- tasks blocked on one immediate critical-path answer
- wording-only edits
- explicit user opt-out from subagents

Typical non-trigger cases:
- "delegation_context: delegated-subagent"
- "parent approval already completed; execute this handoff only"
- "fix this one-line bug in one file"
- "rename this variable"
- "explain this function"
- "do not use subagents for this task"
- "which port is this server using?"

## Decision Process

Follow this sequence every time this skill is invoked:

1. If the current prompt is a delegated subagent handoff, do not suggest another lineup; execute the handoff instead.
2. Classify the task shape.
3. Check whether the work splits into independent subtasks.
4. Check whether the task is primarily read-heavy or write-heavy.
5. If the request is ambiguous, clarify before suggesting.
6. Choose one recommended lineup of 1-4 roles.
7. Determine the work mode: `read-only`, `mixed`, or `write-capable`.
8. Produce the suggestion message using the contract below.
9. Stop and wait for approval.

## Capability Selection Rules

Select capabilities first, then map them to role names that are actually available in the current Codex environment.

Bundled capability map:

| Capability | Preferred bundled role | Work mode |
| --- | --- | --- |
| code mapping | `code-mapper` | read-only |
| risk review | `reviewer` | read-only |
| docs/API verification | `docs-researcher` | read-only |
| search | `search-specialist` | read-only |
| synthesis | `knowledge-synthesizer` | read-only |
| planning | `task-distributor` | read-only |
| test automation | `test-automator` | write-capable |

Availability rules:
- recommend only roles that are explicitly available in the current Codex session
- do not invent role names
- do not assume generic fallback roles exist
- if a capability has no available role, drop that role from the lineup
- if the dropped capability is important, say the main thread can cover it after approval
- if no relevant role is available, stay silent during implicit checks and continue normally
- if the user explicitly asks why no lineup is available, tell them to install the bundled agent pack

Selection guidance:

| Task shape | Capability lineup | Preferred role lineup when available | Mode |
| --- | --- | --- | --- |
| Branch or PR review | risk review + code mapping | `reviewer + code-mapper` | read-only |
| Review with docs/API assumptions | risk review + code mapping + docs/API verification | `reviewer + code-mapper + docs-researcher` | read-only |
| Codepath plus docs/API verification | code mapping + docs/API verification | `code-mapper + docs-researcher` | read-only |
| Option research | search + synthesis | `search-specialist + knowledge-synthesizer` | read-only |
| Broad planning | planning + code mapping | `task-distributor + code-mapper` | read-only |
| Codebase mapping | code mapping + search | `code-mapper + search-specialist` | read-only |
| Regression-risk evidence | code mapping + risk review + search | `code-mapper + reviewer + search-specialist` | read-only |
| Exploration before test coverage | code mapping + risk review + test automation | `code-mapper + reviewer + test-automator` | mixed |
| Meta prompt asking for a default lineup | code mapping + risk review | `code-mapper + reviewer` | read-only |

Role-count rules:
- default to 1-3 roles
- use 4 roles only when the task genuinely has four distinct lanes and all four roles are available
- never exceed 4 roles

## Suggestion Contract

When you decide to suggest subagents, write a short, conversational message using structured intent instead of a rigid template. The message must convey these four pieces of information in this order:

1. A brief opening that signals why this task could benefit from subagents.
2. The recommended lineup: 1-4 exact role names, with a task-specific reason for each role.
3. The work mode: exactly one of `read-only`, `mixed`, or `write-capable`.
4. A direct permission question that matches the work mode.

Tone rules:
- sound like a thoughtful collaborator, not a form
- vary the wording each time; do not reuse the same opener or closing question
- keep the whole suggestion under roughly 4-6 short sentences
- speak in first person when natural, such as "I think" or "I'd suggest"
- match the user's language when natural, but keep role names and work mode labels as exact English tokens

Hard rules:
- recommend exactly one lineup
- do not list alternatives unless there is a real tradeoff the user must choose between
- mention every recommended role by its exact role name
- state the work mode explicitly using one of: `read-only`, `mixed`, `write-capable`
- End with a question, not a statement
- do not answer the task content until the user approves or declines
- do not describe results that do not exist yet
- do not imply that any subagent has already started

For `read-only` mode, the closing question should invite the user to let the subagents investigate before deciding. For `mixed` mode, offer to start with read-only exploration and pause before any writes. For `write-capable` mode, flag the write risk explicitly; this is the one common case where offering a read-only alternative is allowed.

## Approval Gate

Before approval:
- do not spawn subagents
- do not inspect files, run commands, search docs, summarize findings, or start implementation
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
- include an explicit delegated-subagent bypass so the child agent does not invoke cast-subagents again
- summarize results back in the main thread instead of dumping raw logs

Spawn call policy:
- default to role-specific spawning: specify the target `agent_type`, do not set `fork_context`, and pass a self-contained handoff as the child prompt
- treat the handoff as the context carrier; do not rely on inherited chat history for task-critical context
- use `fork_context` only when exact conversation history matters more than role specialization
- when using `fork_context`, do not specify `agent_type`; accept that the child inherits the parent agent type
- if a spawn attempt fails because `fork_context` and `agent_type` were combined, retry once with the same `agent_type`, no `fork_context`, and the self-contained handoff

Every handoff should include:
- `delegation_context`
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

Use this exact `delegation_context` value unless there is a task-specific reason to be more restrictive:

`delegated-subagent; parent approval already completed; do not invoke cast-subagents or request another delegation approval; execute this handoff only`

When the work is mixed:
- front-load read-only exploration
- only hand off write-capable work after the failure mode or plan is clear

## References

Read these references only when needed:

- `references/decision-rules.md` for classification examples
- `references/role-lineups.md` for role mapping examples
- `references/handoff-schema.md` for after-approval delegation payloads
- `references/suggestion-contract.md` for user-facing wording
