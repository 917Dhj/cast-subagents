# Cast Subagents

Cast Subagents is a Codex plugin that helps Codex decide when a task is worth delegating to subagents and how to suggest that delegation without taking control away from the user.

The plugin is intentionally narrow. It does not create custom agents, replace Codex orchestration, or force automatic delegation. Instead, it gives Codex a reusable workflow for:

- recognizing delegation-worthy tasks
- recommending one clear lineup of 1-4 existing roles
- explaining why that lineup fits
- labeling the work as read-only, mixed, or write-capable
- asking for permission before any subagent is spawned

## Plugin Shape

The v1 plugin uses two instruction-only skills:

- `using-cast-subagents`: the broad entry skill that checks whether a coding, review, research, planning, or verification task should trigger a subagent suggestion
- `cast-subagents`: the detailed policy skill that defines role selection, fallback behavior, approval gates, and after-approval handoff expectations

The entry skill follows the Superpowers-style pattern: it is loaded early for broad task categories, then stays silent when delegation would add overhead.

## What This Plugin Does Not Do

This plugin does not:

- spawn subagents automatically
- define project-local custom agents
- require users to replace or merge their existing `AGENTS.md`
- install scripts, runtimes, or external dependencies
- add runtime tools or test harnesses

If the task is too small, too ambiguous, or too tightly coupled, the correct behavior is to stay in the main thread and continue normally.

## Installation During Development

For Desktop validation, install or enable this repository as a Codex plugin. The plugin manifest is:

```text
.codex-plugin/plugin.json
```

The manifest points Codex at:

```text
skills/
```

For CLI evaluation, use a temporary `CODEX_HOME` and copy or symlink the plugin skills into that home:

```bash
mkdir -p /tmp/codex-subagent-eval/skill/skills
cp -R skills/* /tmp/codex-subagent-eval/skill/skills/
```

Then verify discovery:

```bash
CODEX_HOME=/tmp/codex-subagent-eval/skill \
codex debug prompt-input | rg "using-cast-subagents|cast-subagents"
```

Avoid relying on `[[skills.config]]` for the current evaluation path unless you have confirmed the local Codex build loads it.

## Example Prompts

Example prompts that should usually trigger a suggestion:

- `Review this branch against main for bugs, test gaps, security risks, and maintainability.`
- `Map the affected code path, verify the API docs, and then tell me whether the patch is safe.`
- `Research three approaches and summarize the tradeoffs before we implement anything.`
- `先帮我查代码路径，再核对文档，再给我一份风险判断。`

Example prompts that should usually not trigger a suggestion:

- `Fix this typo.`
- `Rename this variable in one file.`
- `Don't use subagents for this task.`
- `这个函数是做什么的？`

## Evaluation Workflow

The first evaluation gate is a reduced smoke suite. The full 18-prompt suite is retained as an extended pressure test after smoke passes.

Evaluation materials live under [evals/](evals/):

- [evals/prompts.yaml](evals/prompts.yaml)
- [evals/rubric.md](evals/rubric.md)
- [evals/scenarios.md](evals/scenarios.md)
- [evals/results-template.md](evals/results-template.md)

Evaluation stages:

1. Discovery: confirm both skills are visible in model input.
2. CLI smoke: run the prompts marked `smoke: true`.
3. Desktop manual: run the representative prompts in a new Desktop session.
4. Extended suite: run the full prompt set only after smoke passes.

## Current Limitations

- Trigger quality still depends on Codex's implicit skill selection behavior.
- Role availability depends on the local Codex role catalog.
- CLI and Desktop use the same `skills/` content, but their installation/discovery paths differ.
- This v1 intentionally avoids scripts, tests, custom agents, and automated packaging.

## Repository Layout

```text
cast-subagents/
├─ .codex-plugin/plugin.json
├─ skills/
│  ├─ using-cast-subagents/
│  └─ cast-subagents/
├─ SKILL.md                  # legacy skill entry for repo-root installs
├─ agents/openai.yaml
├─ references/
├─ evals/
└─ .agent-work/
```
