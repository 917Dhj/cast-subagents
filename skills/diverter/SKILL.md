---
name: diverter
description: "Use when suggesting exactly one Codex subagent lineup before work begins for multi-lane tasks: branch/PR review across bugs, security, tests, maintainability, docs, or regression risk; codepath tracing plus docs/API verification; option research with tradeoff synthesis; auth/codebase mapping before risk assessment or planning. Advisory only; no auto-spawn; approval required. Do not use for delegated subagent handoffs, trivial single-file fixes, wording-only edits, one fact lookup, unclear requests, or explicit opt-out."
---

<NATIVE-PROACTIVE-DELEGATION-STOP>
If higher-priority session instructions explicitly state that proactive multi-agent delegation is active, skip this skill, even when explicitly invoked. Do not mention Diverter or its disablement, suggest a lineup, request delegation approval, or start an Execution Backend. Continue the current task under the native policy.

Without that explicit signal, continue with the normal decision process below.
</NATIVE-PROACTIVE-DELEGATION-STOP>

<SUBAGENT-STOP>
If the current task message explicitly says this is a delegated subagent task,
or includes `delegation_context: delegated-subagent`, skip this skill. Do not
suggest another lineup or ask for delegation approval. Execute only the assigned
handoff within its constraints.
</SUBAGENT-STOP>

# Diverter

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
- security-sensitive code review involving auth, authorization, secrets, user input, webhooks, dependencies, or LLM/tool permissions
- test coverage analysis, test strategy, or regression test planning
- targeted test implementation that should start with read-only behavior mapping
- Web performance audit for frontend routes, Core Web Vitals, Lighthouse, LCP, INP, CLS, loading, rendering, or network behavior
- pre-ship quality gate across review, tests, security, and release risk

Typical request shapes:
- "review this PR for bugs, security, maintainability, and tests"
- "trace the code path and verify the docs/API behavior"
- "research several options and summarize the tradeoffs"
- "map the codebase before we change anything"

## Do Not Use This Skill When

Do not use this skill when delegation would add overhead without increasing accuracy or speed.

Hard stop cases:
- current task messages that explicitly say this is a delegated subagent task
- handoffs with `delegation_context: delegated-subagent`
- trivial single-domain tasks
- tightly coupled write-heavy work in the same files
- ambiguous requests that need clarification first
- tasks blocked on one immediate critical-path answer
- wording-only edits
- explicit user opt-out from subagents
- generic small PR review or style-only review that does not need specialist lanes
- Web performance specialist work for non-Web performance tasks
- write-capable test automation when the target behavior is ambiguous
- vague security requests without a concrete artifact, flow, or trust boundary

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

1. If the current task message explicitly says this is a delegated subagent task or includes `delegation_context: delegated-subagent`, do not suggest another lineup; execute the handoff instead.
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
| code review | `reviewer` | read-only |
| security audit | `security-auditor` | read-only |
| docs/API verification | `docs-researcher` | read-only |
| search | `search-specialist` | read-only |
| synthesis | `knowledge-synthesizer` | read-only |
| planning | `task-distributor` | read-only |
| test strategy | `test-engineer` | read-only |
| test automation | `test-automator` | write-capable |
| Web performance audit | `web-performance-auditor` | read-only |

Availability rules:
- for the Native Subagent Backend, recommend roles exposed by the current Codex session
- when native role metadata is hidden, treat bundled roles installed by the Role Installer as available to the CLI Worker Backend unless the user says installation was skipped or the runner reports a missing role
- do not invent role names
- do not assume generic fallback roles exist
- if a capability has no available role, drop that role from the lineup
- if the dropped capability is important, say the main thread can cover it after approval
- if no relevant role is available, stay silent during implicit checks and continue normally
- if the user explicitly asks why no lineup is available, tell them to install the bundled agent pack

Selection guidance:

| Task shape | Capability lineup | Preferred role lineup when available | Mode |
| --- | --- | --- | --- |
| General branch or PR review | code review + code mapping | `reviewer + code-mapper` | read-only |
| Review with docs/API assumptions | code review + code mapping + docs/API verification | `reviewer + code-mapper + docs-researcher` | read-only |
| Security-sensitive review | security audit + code mapping + code review | `security-auditor + code-mapper + reviewer` | read-only |
| Auth / permission / token flow review | security audit + code mapping | `security-auditor + code-mapper` | read-only |
| LLM / agent tool safety review | security audit + code mapping + docs/API verification | `security-auditor + code-mapper + docs-researcher` | read-only |
| Test coverage analysis | test strategy + code mapping | `test-engineer + code-mapper` | read-only |
| Add targeted regression tests | test strategy + test automation + code mapping | `test-engineer + test-automator + code-mapper` | mixed |
| Web performance source audit | Web performance audit + code mapping | `web-performance-auditor + code-mapper` | read-only |
| Web performance audit with supplied metrics | Web performance audit | `web-performance-auditor` | read-only |
| Codepath plus docs/API verification | code mapping + docs/API verification | `code-mapper + docs-researcher` | read-only |
| Option research | search + synthesis | `search-specialist + knowledge-synthesizer` | read-only |
| Broad planning | planning + code mapping | `task-distributor + code-mapper` | read-only |
| Codebase mapping | code mapping + search | `code-mapper + search-specialist` | read-only |
| Regression-risk evidence | code mapping + code review + search | `code-mapper + reviewer + search-specialist` | read-only |
| Pre-ship quality gate | code review + security audit + test strategy + code mapping | `reviewer + security-auditor + test-engineer + code-mapper` | read-only |
| Meta prompt asking for a default lineup | code mapping + code review | `code-mapper + reviewer` | read-only |

Role-count rules:
- default to 1-3 roles
- use 4 roles only when the task genuinely has four distinct lanes and all four roles are available
- never exceed 4 roles

Specialist compression rules:
- ordinary PR review stays `reviewer + code-mapper`
- add `security-auditor` only when the task has a concrete security boundary or explicit security audit request
- add `test-engineer` only when the task asks about tests, coverage, proof, or test strategy
- add `test-automator` only when test writing or updating is explicitly requested and the scope is clear enough to be safe
- add `web-performance-auditor` only for Web apps, Web routes, Web pages, Web components, or Web performance artifacts
- if more than 4 roles are triggered, keep the central risk specialist and `code-mapper`, then drop non-core roles

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
- include an explicit delegated-subagent bypass so the child agent does not invoke diverter again
- summarize results back in the main thread instead of dumping raw logs

### Select the Execution Backend

Perform a Backend Capability Check against the visible `spawn_agent` interface after approval:

- If `agent_type`, `model`, and `reasoning_effort` are all exposed, use the Native Subagent Backend and follow the native spawn policy below.
- If any required selector is hidden, use the CLI Worker Backend. Do not treat `task_name` as an agent selector and do not use a generic native child when the role settings cannot be guaranteed.

For each approved CLI role, let `skill_file` be the fully expanded absolute path to this `SKILL.md`, compute `plugin_root = Path(skill_file).parents[2]`, verify `${plugin_root}/.codex-plugin/plugin.json` exists, and invoke `${plugin_root}/scripts/run-cli-agent.py` once. Do not derive the path from a catalog alias such as `r3`, a cache version, or the Skill directory itself. Pass the role name, the Root Session workspace with `-C`, and each required additional writable or readable directory with `--add-dir`. Send the complete delegated handoff on stdin and use the runner's stdout as that role's result. A non-zero exit and stderr are a visible worker failure; do not retry by removing the multi-agent disable flags.

The Root Session owns orchestration for both backends. Read-only roles may run concurrently. Write-capable roles run serially unless their write scopes are clearly disjoint. Mixed work completes its read-only phase before any write-capable role starts.

Spawn call policy:
- for the Native Subagent Backend, default to role-specific spawning: specify the target `agent_type`, do not set `fork_context`, and pass a self-contained handoff as the child prompt
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

`delegated-subagent; parent approval already completed; do not invoke diverter or request another delegation approval; execute this handoff only`

When the work is mixed:
- front-load read-only exploration
- only hand off write-capable work after the failure mode or plan is clear

## References

Read these references only when needed:

- `references/decision-rules.md` for classification examples
- `references/role-lineups.md` for role mapping examples
- `references/handoff-schema.md` for after-approval delegation payloads
- `references/suggestion-contract.md` for user-facing wording
