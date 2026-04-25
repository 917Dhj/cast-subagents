# Cast Subagents Skill v1 Plan

## Goal

Build a Codex skill that improves delegation behavior without requiring users to merge or replace their existing `AGENTS.md`.

The skill should make Codex better at one narrow workflow:

1. decide whether the current task is subagent-friendly
2. recommend one lineup of 1-4 existing roles
3. explain why the lineup fits
4. label the work mode
5. ask for permission before any subagent is spawned

This is a `suggest-only` capability. It is not an automatic delegation engine.

## Product Shape

- repository type: skill-first
- directory name: `cast-subagents`
- v1 scope: instruction-only skill
- primary target: Codex
- non-goals:
  - plugin packaging
  - custom project agents
  - mandatory `AGENTS.md` snippets
  - runtime scripts or external dependencies

## Root Files

- `SKILL.md`
  - contains the core decision policy
  - must be strong enough for implicit triggering
- `agents/openai.yaml`
  - carries Codex-facing display and default prompt metadata
- `README.md`
  - explains scope, installation, and evaluation
- `LICENSE`
  - default `MIT`
- `.gitignore`
  - ignore only routine local artifacts

## Reference Files

- `references/decision-rules.md`
  - task classification and suggest/no-suggest table
- `references/role-lineups.md`
  - scenario-to-lineup mapping
- `references/handoff-schema.md`
  - minimum handoff payload contract
- `references/examples-positive.md`
  - positive trigger examples
- `references/examples-negative.md`
  - negative trigger examples
- `references/suggestion-contract.md`
  - user-facing wording and templates

## Evaluation Files

- `evals/prompts.yaml`
  - fixed 18-case prompt suite
- `evals/rubric.md`
  - 5-point binary rubric
- `evals/scenarios.md`
  - baseline, treatment, desktop, and two-step approval scenarios
- `evals/results-template.md`
  - reusable round log

## Behavioral Contract

The skill must enforce all of these:

- only suggest when the task materially benefits from delegation
- do not mention subagents on negative cases
- recommend one lineup only
- keep the lineup size between 1 and 4
- use existing roles only
- explicitly mention role fallback when needed
- ask for approval before any spawn
- after approval, prefer read-only exploration first
- serialize write-capable agents unless write scopes are clearly disjoint
- summarize results back in the main thread

## Whitelist

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

## Trigger Rules

Positive trigger classes:

- multi-axis review
- read-heavy exploration
- docs or API verification
- parallelizable research
- independent planning subtasks

Negative trigger classes:

- trivial single-domain tasks
- tightly coupled write-heavy work
- ambiguous requests needing clarification
- tasks blocked on one immediate critical-path answer
- explicit user opt-out

## Evaluation Plan

Two arms:

- `baseline`
- `skill-only`

Two surfaces:

- CLI for reproducibility
- Desktop for experience validation

Success gates:

- positive-case suggestion rate `>= 80%`
- negative-case false positive rate `<= 15%`
- approval-gate violations `= 0`
- lineup size above 4 `= 0`
- fallback correctness rate `>= 90%`

## Next Session Work Order

1. inspect the scaffold and confirm no missing required files
2. tighten `SKILL.md` wording if implicit trigger quality is weak
3. run CLI baseline on the fixed prompt set
4. run CLI treatment on the same prompt set
5. compare results with the rubric
6. run the representative desktop prompt subset
7. if needed, revise only:
   - `SKILL.md`
   - `agents/openai.yaml`
   - `references/examples-positive.md`
   - `references/examples-negative.md`
   - `references/suggestion-contract.md`
8. do not add scripts, tests, plugins, or custom agents in v1 unless the evaluation clearly proves the instruction-only approach is insufficient
