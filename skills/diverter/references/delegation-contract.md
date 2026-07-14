# Delegation Contract

Every Diverter message uses one shared structure and one Delegation Policy ending.

## Shared Information

Convey these three pieces in order:

1. Why the task benefits from delegation.
2. Exactly one lineup of 1-4 available roles, with a task-specific assignment for each role.
3. The Work Mode: exactly one of `read-only`, `mixed`, or `write-capable`.

Keep the message conversational, under roughly 4-6 short sentences, and in the user's language when natural. Keep role names and Work Mode labels exact.

Shared hard rules:

- Never list several equal-weight lineups.
- Never invent a role or exceed four roles.
- Mention an important dropped capability when its role is unavailable.
- Add specialists only for concrete independent signals.
- Do not describe results that do not exist.
- Do not imply dispatch happened before the message.

## `ask` Ending

End with a direct permission question matched to the Work Mode, then stop.

- `read-only`: invite evidence gathering before the user decides.
- `mixed`: offer to start with read-only exploration and pause before writes.
- `write-capable`: flag write risk and allow a read-only alternative.

Do not inspect, run, search, summarize, spawn, or implement before approval.

Example:

> This splits cleanly. `code-mapper` can trace where the retry logic runs, while `docs-researcher` verifies the API's idempotency guarantee. Work Mode is `read-only`. Should I have them gather the evidence first?

## `auto` Ending

End with a declarative Dispatch Announcement, then dispatch in the same turn regardless of Work Mode.

- State that the selected roles are starting now.
- State that the Root Session will collect and synthesize their results.
- Do not ask a question or pause for approval.
- Do not weaken sandbox or permission controls.

Example:

> This splits cleanly. `code-mapper` will trace where the retry logic runs, while `docs-researcher` verifies the API's idempotency guarantee. Work Mode is `read-only`. I'm dispatching them now and will synthesize their findings here.

## Failure Cases

Avoid:

- unnamed "agents" instead of exact roles
- more than four roles
- alternative lineup menus
- an `ask` message without a permission question
- an `auto` message that asks a question or stops
- task work before Dispatch Authorization
- redispatching a lineup already announced or executed for the current task
- suggesting another lineup for a delegated-subagent handoff
