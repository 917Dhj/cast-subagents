# Cast Subagents

Cast Subagents is a Codex plugin that helps Codex decide when a task is worth delegating to subagents and how to suggest that delegation without taking control away from the user.

The plugin is intentionally narrow. It does not create custom agents, replace Codex orchestration, or force automatic delegation. Instead, it gives Codex a reusable workflow for:

- recognizing delegation-worthy tasks
- recommending one clear lineup of 1-4 existing roles
- explaining why that lineup fits
- labeling the work as read-only, mixed, or write-capable
- asking for permission before any subagent is spawned

## What It Does

The v1 plugin uses two instruction-only skills:

- `using-cast-subagents`: the broad entry skill that checks whether a coding, review, research, planning, or verification task should trigger a subagent suggestion
- `cast-subagents`: the detailed policy skill that defines role selection, fallback behavior, approval gates, and after-approval handoff expectations

The entry skill is designed to be loaded early for broad task categories, then stay silent when delegation would add overhead.

## What It Does Not Do

This plugin does not:

- spawn subagents automatically
- define project-local custom agents
- require users to replace or merge their existing `AGENTS.md`
- install scripts, runtimes, or external dependencies
- add runtime tools or test harnesses

If the task is too small, too ambiguous, or too tightly coupled, the correct behavior is to stay in the main thread and continue normally.

## Installation

After this repository is published, add it as a Codex marketplace:

```bash
codex plugin marketplace add 917Dhj/cast-subagents
```

Then open the Codex plugin directory:

```text
/plugins
```

Select the `Cast Subagents` marketplace and install the `cast-subagents` plugin. Start a new Codex thread after installation so the bundled skills are loaded.

This local repository has been prepared for that GitHub marketplace flow, but this change set does not publish, push, tag, or create a GitHub release.

## Updating

After new versions are published, refresh the marketplace:

```bash
codex plugin marketplace upgrade cast-subagents-marketplace
```

Then reinstall or refresh the plugin from the Codex plugin directory if needed, and start a new thread.

## Uninstalling

Open `/plugins`, select the installed plugin, and choose uninstall.

To remove the marketplace:

```bash
codex plugin marketplace remove cast-subagents-marketplace
```

## Usage

Example prompts that should usually trigger a suggestion:

- `Review this branch against main for bugs, test gaps, security risks, and maintainability.`
- `Map the affected code path, verify the docs/API behavior, and then tell me whether the patch is safe.`
- `Research three approaches and summarize the tradeoffs before we implement anything.`
- `先帮我查代码路径，再核对文档，再给我一份风险判断。`

Example prompts that should usually not trigger a suggestion:

- `Fix this typo.`
- `Rename this variable in one file.`
- `Don't use subagents for this task.`
- `这个函数是做什么的？`

When a suggestion is appropriate, Codex should recommend one lineup, explain why it fits, state the work mode, and ask for permission before spawning any subagent.
The suggestion should read like a short natural message, not a fixed set of labeled fields.

## Development

The plugin entry point is:

```text
.codex-plugin/plugin.json
```

The manifest points Codex at:

```text
skills/
```

The `agents/openai.yaml` file is experimental/internal metadata and is not required for Codex plugin installation.

To validate the marketplace locally before publishing, add the local repository as a marketplace:

```bash
codex plugin marketplace add /Users/dinghongjing/Documents/Playground/cast-subagents
```

Then open `/plugins`, choose the `Cast Subagents` marketplace, and install the plugin. This command changes the user's Codex marketplace configuration, so it is documented here rather than run as part of routine file validation.

For CLI evaluation without changing the normal Codex home, use a temporary `CODEX_HOME` and copy or symlink the plugin skills into that home:

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

## Evaluation

The first evaluation gate is a reduced smoke suite. The full prompt suite is retained as an extended pressure test after smoke passes.

Evaluation materials live under [evals/](evals/):

- [evals/prompts.yaml](evals/prompts.yaml)
- [evals/rubric.md](evals/rubric.md)
- [evals/scenarios.md](evals/scenarios.md)
- [evals/results-template.md](evals/results-template.md)

Evaluation stages:

1. Discovery: confirm both skills are visible in model input.
2. CLI smoke: run the prompts marked `smoke: true`.
3. Desktop manual: run representative prompts in a new Desktop session.
4. Extended suite: run the full prompt set only after smoke passes.

## Release Process

Before publishing:

1. Confirm `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` are valid JSON.
2. Confirm the marketplace URL points to the public GitHub repository.
3. Run the local marketplace install test.
4. Push to GitHub.
5. Run the remote marketplace install test with `codex plugin marketplace add 917Dhj/cast-subagents`.
6. Update `CHANGELOG.md`, tag the release, and create a GitHub release.

Early releases use `ref: main` in `.agents/plugins/marketplace.json` so users get the latest published plugin. After the plugin stabilizes, consider pinning the marketplace entry to a release tag.

## Current Limitations

- Trigger quality still depends on Codex's implicit skill selection behavior.
- Role availability depends on the local Codex role catalog.
- CLI and Desktop use the same `skills/` content, but their installation/discovery paths differ.
- This v1 intentionally avoids scripts, tests, custom agents, and automated packaging.
- Assets are not included yet; `plugin.json` does not reference `composerIcon` or `logo`.

## Repository Layout

```text
cast-subagents/
├─ .codex-plugin/plugin.json
├─ .agents/plugins/marketplace.json
├─ skills/
│  ├─ using-cast-subagents/
│  └─ cast-subagents/
├─ references/
├─ evals/
├─ agents/openai.yaml        # experimental/internal metadata
├─ CHANGELOG.md
├─ SECURITY.md
├─ PRIVACY.md
└─ LICENSE
```

## License

MIT. See [LICENSE](LICENSE).
