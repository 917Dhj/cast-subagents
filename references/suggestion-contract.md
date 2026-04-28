# Suggestion Contract

Every subagent suggestion must follow a structured intent contract, not a rigid output template.

## Required Information

Every suggestion must convey four pieces of information in this order:

1. A brief opening that signals why the task could benefit from subagents.
2. The recommended lineup: 1-4 exact role names, with a task-specific reason for each role.
3. The work mode: exactly one of `read-only`, `mixed`, or `write-capable`.
4. A direct permission question that matches the work mode.

If any of these pieces is missing, the suggestion is incomplete.

## Order and Tone

- Keep the required information in order, but do not use fixed section labels.
- Sound like a thoughtful collaborator, not a form.
- Vary the wording each time; do not reuse the same opener or closing question.
- Keep the whole message under roughly 4-6 short sentences.
- Speak in first person when natural, such as "I think" or "I'd suggest".
- Match the user's language when natural, but keep role names and work mode labels as exact English tokens.

## Hard Rules

- Recommend exactly one lineup.
- Do not list alternatives unless there is a real tradeoff the user must choose between.
- Keep the lineup between 1 and 4 roles.
- Use existing roles only.
- Mention every recommended role by its exact role name.
- If a capability was dropped because its role is unavailable, mention the gap briefly.
- State the work mode explicitly using one of: `read-only`, `mixed`, `write-capable`.
- End with a question, not a statement.
- Ask for permission before any spawn.
- Do not answer the task content before the user approves or declines.
- Do not describe results that do not exist yet.
- Do not imply that any subagent has already started.

## Permission Question by Work Mode

Match the closing question to the actual risk of the proposed work.

- `read-only`: invite the user to let the subagents investigate before deciding.
- `mixed`: offer to start with read-only exploration and pause before any writes.
- `write-capable`: flag the write risk explicitly and offer a read-only alternative if useful.

The exact wording is up to the model. The point is that the question should make the user feel the difference between "this is safe to try" and "this will change files."

## Examples for Tone, Not for Copying

Example 1: multi-axis PR review, read-only

> I think this is a good fit for subagents. I'd put reviewer on correctness and test risks, code-mapper on the affected paths, and docs-researcher on the API assumptions in the diff, since those are separate angles they can inspect in parallel. Work mode is read-only. Want me to send them in to take a look before you decide?

Example 2: codepath plus docs verification, read-only

> This one splits cleanly. code-mapper can trace where the payment retry logic actually runs, and docs-researcher can verify what the Stripe API guarantees about idempotency keys. Both stay read-only. Should I have them gather evidence first?

Example 3: mixed investigate-then-cover

> I'd handle this in two passes. First, code-mapper and reviewer dig into the failure mode without touching anything; once we know what is actually risky, test-automator can add bounded regression coverage. Mixed mode overall, and I would hold the writes until the read pass is done. Want me to start with the read-only exploration and pause before any test edits?

Example 4: option research, read-only

> Worth splitting this. search-specialist can pull candidate libraries and recent benchmarks, and knowledge-synthesizer can fold the findings into a short tradeoff summary. Read-only. Should I have them put together the options before we pick one?

Example 5: write-capable test coverage, with a read-only alternative

> This task involves write-capable delegation because test-automator would add or update regression tests. reviewer can identify the riskiest behavior first, but the coverage pass would change files. Want me to proceed in write-capable mode, or would you rather I start with reviewer alone in read-only and confirm the plan before any test edits?

## Failure Cases To Avoid

Do not do these:

- suggesting "a few agents" without naming the exact lineup
- listing 5 or more roles
- offering three equally weighted lineups with no recommendation
- saying or implying that delegation already started
- asking a vague approval question without showing the proposed lineup
- suggesting another lineup when the prompt is already a delegated subagent handoff
