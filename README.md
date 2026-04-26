# cast-subagents

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Codex Compatible](https://img.shields.io/badge/Codex-compatible-green.svg)](https://github.com/917Dhj/cast-subagents)

A Codex plugin that recommends the right subagent lineup for complex tasks — and waits for you to approve before anyone moves.

---

Every time a Codex task is large enough to benefit from parallel agents, you face the same manual overhead: decide whether to split, figure out which roles to send, then write the spawn instructions clearly enough that the main thread actually follows through. cast-subagents handles the first two steps automatically — it analyzes the task, picks a lineup, and surfaces the suggestion before work begins. What it never does is spawn on its own: the final call is always yours.

The plugin is two skills working in sequence: an always-on internal gate that should be read before every Codex task, and an advisor that does the detailed lineup selection when the gate decides a suggestion is warranted. Most gate reads produce no visible output. Between the two, the heavy coordination work happens before the task starts — not after Codex has already committed to an approach.

## 💬 See It In Action

The two examples below show the full interaction pattern: cast-subagents identifies the task shape, names the lineup and work mode, asks one direct question, then stops. It doesn't answer the task itself until you approve.

Here's what cast-subagents looks like when it triggers on a real task:

```text
> Review this branch against main for bugs, security issues, missing tests,
  and maintainability risks.

I think this is a good fit for subagents. I'd put reviewer on correctness
and test risks, code-mapper on the affected paths, and docs-researcher on
the API assumptions in the diff — those are separate angles they can cover
in parallel. Work mode is read-only. Want me to send them in to take a look
before you decide?

> yes

Understood. Delegating now to reviewer, code-mapper, and docs-researcher.
Each agent will report back independently before any changes are made.
```

And here's an example where the task splits along two distinct lines:

```text
> Trace the code path for the checkout error and verify the framework docs
  that the patch relies on.

This one splits cleanly. code-mapper can trace where the checkout error
actually runs, and docs-researcher can verify what the framework guarantees
about that behavior. Both stay read-only. Should I have them gather evidence
first?

> go ahead

Starting with read-only delegation to code-mapper and docs-researcher.
```

## 🤔 Why cast-subagents

OpenAI's own Codex documentation states: *"Codex doesn't spawn subagents automatically, and it should only use subagents when you explicitly ask for subagents or parallel agent work."*

That sentence describes a real gap. For every task that would benefit from delegation, you need to manually decide whether to split it, which roles to pick, and how to phrase the spawn request clearly. As context grows longer, the main agent tends to absorb everything itself rather than handing work off. cast-subagents closes that gap by front-loading the analysis — but it keeps the spawn decision squarely in your hands.

Some other delegation tools take the analysis all the way to automatic spawning. cast-subagents stops at the suggestion, and that's a deliberate design choice rather than a missing feature:

| Other auto-spawn tools | cast-subagents |
|---|---|
| Analyze the task, then spawn immediately | Analyze the task, then pause for your approval |
| User sees delegation after the fact | User sees the proposed lineup before anything runs |
| Token spend is committed without review | You can weigh whether the cost is worth it each time |
| Workflow changes to accommodate the tool | Tool fits into whatever workflow you already have |

Three reasons this matters in practice:

1. **You keep final say on every spawn.** Subagents multiply token consumption quickly. An advisory step lets you decide case-by-case whether that cost is justified.
2. **Zero workflow disruption.** There's nothing to reconfigure. Install the plugin, keep working the same way, and the suggestion appears when it's useful.
3. **No accidental delegation.** If the main thread would have handled something fine on its own, cast-subagents stays silent rather than adding overhead.

## ⚙️ How It Works

cast-subagents is made up of two skills that work in sequence:

- **using-cast-subagents** is the always-on internal gate. It should be read before every Codex response, action, file read, command, analysis, implementation, review, planning step, or clarifying question. It makes the coarse call: does this task warrant a visible suggestion, or should Codex proceed quietly?
- **cast-subagents** is the advisor. When the gate decides a suggestion is warranted, this skill does the detailed work: classifies the task shape, selects a lineup of 1–4 roles, determines the work mode, and writes the suggestion message. Then it stops and waits.

Think of them as front-of-house and back-of-house: the gate decides whether to escalate, the advisor decides what to recommend.

The important distinction is internal versus visible behavior: `using-cast-subagents` should run almost all the time, but cast-subagents should only speak when a task has independent lanes that make delegation worth considering. For simple, single-lane, or opted-out tasks, the gate stays completely silent.

### The Suggestion Contract

When cast-subagents does speak, it follows a consistent structure called the suggestion contract. Every suggestion must cover four things in order: why the task could benefit from subagents, the exact lineup with a reason for each role, the work mode, and a permission question that matches the risk of the proposed work. The output is conversational rather than a fixed template — the same four pieces, different wording each time.

The contract also has hard constraints: exactly one lineup, no more than four roles, no task content before approval, and no implication that delegation has already started. The closing question is always a question, not a statement.

```
User sends task
      │
      ▼
using-cast-subagents gate
      │
      ├── task is simple / single-lane / opted out
      │         │
      │         ▼
      │     stay silent → Codex continues normally
      │
      └── task has independent lanes
                │
                ▼
          cast-subagents advisor
                │
                ▼
          classify task shape
          select lineup (1–4 roles)
          choose work mode
          write suggestion message
                │
                ▼
          STOP — wait for approval
                │
      ┌─────────┴──────────┐
      │                    │
   declined             approved
      │                    │
      ▼                    ▼
  continue in         delegate with
  main thread         handoff schema
```

Once you approve, each agent receives a structured handoff payload that includes the goal, success criteria, scope boundaries, relevant file paths, write policy, and a verifiable deliverable. The structure ensures each agent knows exactly what it owns and what it must leave alone. No agent infers scope from context; everything is explicit.

Here's what a typical handoff looks like after you approve a `code-mapper` delegation:

```text
goal: Map the affected code path for the settings save failure.
success_criteria: Identify the real execution path, likely failure boundary,
  and the files that own the behavior.
scope_in: settings modal, client mutation, API route, response handling
scope_out: unrelated settings pages, styling, copy updates
relevant_paths: src/settings/, app/api/settings/, useSettingsForm
constraints: read-only; no code edits; cite concrete files and symbols
deliverable: concise summary with file references and one likely root cause
write_policy: read-only
open_questions: whether retries or optimistic state updates affect the failure mode
```

This format is defined in `references/handoff-schema.md` and applies to every delegated agent regardless of role or work mode.

## 🎯 Decision Rules

### When cast-subagents speaks up

- **Multi-axis review** — the task asks for several independent review angles on the same diff or branch.

  > `Review this branch against main for bugs, security issues, missing tests, and maintainability risks.`

- **Read-heavy codebase mapping** — the task requires tracing multiple paths or layers before any changes.

  > `Map the auth flow first, then tell me whether the current implementation is safe to change.`

- **Codepath plus docs/API verification** — the task needs both a code trace and a documentation check, and those can run in parallel.

  > `先帮我查清楚代码路径，再去核对官方文档里这个 API 的行为。`

- **Parallelizable research** — the task involves independent questions that don't block each other.

  > `Research three approaches for background job retries and summarize the tradeoffs before we choose one.`

- **Broad planning with separable subtasks** — the task is a high-level goal with clearly independent investigation lanes.

  > `Map the relevant module boundaries first, then decide how to approach the change.`

### When it stays quiet

- **Trivial or single-file change** — a one-liner fix or rename doesn't benefit from delegation.

  > `Fix this typo in the README.`

- **Tightly coupled write work** — changes in the same files with overlapping logic are safer to do in sequence.

  > `就修这个单文件的小 bug，不要并行拆分。`

- **Immediate fact lookup** — the task is blocked on one answer, so spawning agents doesn't help yet.

  > `What port is the dev server using right now?`

- **Explicit opt-out** — if you say not to use subagents, that's a hard constraint.

  > `Do not use subagents for this task.`

- **Ambiguous request** — if the intent isn't clear enough to build a solid lineup, cast-subagents asks for clarification instead.

The Chinese examples above are included intentionally. cast-subagents matches the user's language when writing the suggestion, and role names and work mode labels remain in English regardless of the prompt language. You can find the full set of positive and negative examples in `references/examples-positive.md` and `references/examples-negative.md`.

## 🎭 Roles & Lineups

### The nine roles

**Preferred roles** — used whenever the task fits their specialty:

| Role | What it does |
|---|---|
| `search-specialist` | Gathers high-signal evidence across the codebase or external sources |
| `docs-researcher` | Verifies API guarantees and documentation assumptions |
| `code-mapper` | Traces execution paths and maps ownership across files |
| `reviewer` | Identifies correctness, test, and security risks in a change |
| `task-distributor` | Structures a broad goal into bounded, independent subtasks |
| `test-automator` | Adds minimal regression coverage for identified risk areas |
| `knowledge-synthesizer` | Consolidates research findings into a concise, actionable summary |

**Fallback roles** — substituted when a preferred role isn't available:

| Role | When it's used |
|---|---|
| `explorer` | Replaces any unavailable read-heavy preferred role |
| `worker` | Replaces any unavailable write-capable preferred role |

When a fallback is used, cast-subagents says so explicitly rather than silently substituting. For example: "docs-researcher isn't available, so I'd use explorer for evidence gathering instead — the coverage will be more general."

### Common lineups

| Task shape | Recommended lineup | Work mode |
|---|---|---|
| Multi-axis PR review | `reviewer + code-mapper + docs-researcher` | read-only |
| Codepath plus docs/API verification | `code-mapper + docs-researcher` | read-only |
| Option research and tradeoff synthesis | `search-specialist + knowledge-synthesizer` | read-only |
| Read-heavy codebase exploration | `code-mapper + search-specialist` | read-only |
| Exploration before a bounded fix | `code-mapper + reviewer + worker` | mixed |
| Coverage-focused follow-up | `reviewer + test-automator` | write-capable |

These role names are compatible with VoltAgent/awesome-codex-subagents and similar community Codex subagent collections. If you use a custom collection, you can adapt `references/role-lineups.md` to add your own task shape mappings.

A few things to keep in mind when reading the table:

- cast-subagents recommends one lineup per suggestion, not a menu of options. If the task clearly fits one pattern, that's the one you'll see.
- The cap is four roles. If a task seems to need more, cast-subagents either compresses the lineup or stays silent rather than padding it out.
- Roles serve as coordination labels, not implementations. Whether your `reviewer` agent is a lightweight script or a full-featured code auditor is up to your setup.

## 🔄 Work Modes

**`read-only`** — agents inspect, trace, and report. No files are written. This is the default for review, mapping, research, and verification tasks. It's the safest delegation path, and cast-subagents defaults here when in doubt. Most suggestions fall into this mode.

**`mixed`** — agents start with a read-only pass and pause before any writes. cast-subagents confirms the exploration phase is complete before handing off to a write-capable agent. When you see `mixed` in a suggestion, it means: "we'll dig in first, and I'll check with you before anything changes." Writes don't happen silently.

**`write-capable`** — agents may edit files within their assigned scope. cast-subagents flags this mode explicitly in the suggestion and, where the tradeoff is worth surfacing, offers to start in read-only mode instead. You always see this label before you approve. Any lineup that includes `worker` or `test-automator` uses this mode.

The mode is always stated using one of these three exact labels — you won't see a suggestion without knowing which one applies.

## 📦 Installation

Add this repository as a Codex plugin marketplace:

```bash
codex plugin marketplace add 917Dhj/cast-subagents
```

Then open `/plugins`, choose the `Cast Subagents` marketplace, and install the `cast-subagents` plugin. Start a new Codex thread after installation so the bundled skills are loaded.

If this repository is private, your GitHub credentials must have access to `917Dhj/cast-subagents` before adding or upgrading the marketplace.

## Updating

After changes are pushed to GitHub, refresh the marketplace:

```bash
codex plugin marketplace upgrade cast-subagents-marketplace
```

Then use `/plugins` to refresh or reinstall `cast-subagents` if the installed plugin cache has not updated automatically.

## ❓ FAQ

Common questions about behavior, customization, and scope.

**Why doesn't it just spawn subagents automatically?**

That's a deliberate design choice. Subagents multiply token consumption, and the right call varies by task. An approval step means you can weigh that cost each time rather than committing to it unconditionally. Other tools in this space make spawning automatic; cast-subagents treats your approval as a required step, not an optional one.

**Will it slow Codex down on simple tasks?**

No. The always-on gate (`using-cast-subagents`) evaluates every task before responding, but for simple, single-domain, or single-file work it stays completely silent. You won't see a suggestion for tasks that don't warrant one.

**What if I want to skip the suggestion just this once?**

Include a phrase like "do not use subagents" or "no subagents" in your prompt. The gate treats explicit opt-outs as a hard constraint and silences itself for that task. You can also just decline the suggestion when it appears — cast-subagents will continue in the main thread without re-suggesting unless the task materially changes.

**Does it work with custom subagent collections?**

The preferred role names (`search-specialist`, `docs-researcher`, `code-mapper`, etc.) are compatible with collections like VoltAgent/awesome-codex-subagents. If you use a custom set of roles, you can edit `references/role-lineups.md` to add your own mappings and task shapes. cast-subagents will use whatever roles are available and say explicitly when a preferred role is missing.

**Does it edit my code?**

No. cast-subagents only produces a suggestion and waits. Even after you approve, the spawn itself is handled by Codex's main thread — cast-subagents doesn't touch your files at any point.

**Does it support non-English prompts?**

Yes. cast-subagents matches your language when writing the suggestion. Role names and work mode labels remain in English as exact tokens, but the surrounding message follows the language of your prompt. Chinese is supported out of the box; other languages follow naturally from how Codex handles multilingual input.

**Can I customize which task shapes trigger a suggestion?**

Yes — `references/decision-rules.md` is the source of truth for task shape classification. If you want to add, remove, or adjust trigger conditions, edit that file. Similarly, `references/role-lineups.md` controls the lineup recommendations. Both files are plain Markdown tables, so there's no configuration language to learn.

**What if the suggested lineup is almost right but not quite?**

Decline the suggestion and tell Codex what you'd change. For example: "use code-mapper and reviewer, but skip docs-researcher for this one." cast-subagents won't re-suggest unless the task changes; it continues with the main thread and follows your direction.

---

## 🗂 Project Structure

```text
cast-subagents/
├── skills/
│   ├── cast-subagents/
│   │   └── SKILL.md              # Core advisor skill
│   └── using-cast-subagents/
│       └── SKILL.md              # Always-on gate skill
├── references/                   # Reference files loaded by the skills at runtime
│   ├── decision-rules.md         # Task shape → suggest/silent mapping
│   ├── role-lineups.md           # Task shape → lineup recommendations
│   ├── suggestion-contract.md    # Output format and tone rules
│   ├── handoff-schema.md         # Post-approval delegation payload
│   ├── examples-positive.md      # Tasks that should trigger a suggestion
│   └── examples-negative.md      # Tasks that should stay silent
├── .agents/
│   └── plugins/marketplace.json  # Git-backed Codex marketplace entry
├── agents/
│   └── openai.yaml
├── .codex-plugin/
│   └── plugin.json               # Plugin manifest
└── CHANGELOG.md
```

The `references/` directory is the main place to make substantive changes. The `skills/` SKILL.md files load these references at runtime, so you can tune decision rules, lineup tables, and wording without touching the skill logic itself.

---

## 🛣 Roadmap

The following are directions under consideration. Nothing here is committed.

- May expand the task shape library to cover more mixed-mode patterns, especially investigation-before-refactor flows where the exploration and the implementation have different risk profiles.
- Could add explicit support for additional prompt languages beyond Chinese and English — the suggestion contract already follows user language naturally, but some language-specific phrasing patterns may warrant tuning.
- Considering a configurable "default silent" mode for users who prefer to opt in per-task rather than receiving automatic suggestions across all tasks.
- May expose role availability as a configuration option so teams can restrict the recommended lineups to only the roles they actually have deployed in their Codex environment.
- Could add lightweight eval tooling to help contributors verify that new decision rules don't break existing silent cases — currently the eval setup requires manual review against the rubric.
- May introduce a lightweight changelog format for `references/` files so it's easier to see what rules changed between versions.

## 🤝 Contributing & License

Issues and pull requests are welcome. The most useful contributions are:

- New task shapes in `references/decision-rules.md`, with a matching lineup in `references/role-lineups.md`
- Positive and negative examples in `references/examples-positive.md` and `references/examples-negative.md` that ground the new rule in real prompts

When adding decision rules, the useful test is: can you write a prompt that should trigger the rule, and a similar-looking prompt that should stay silent? If both are in the example files, the rule is well-scoped. If you can only write the positive case, the silent boundary isn't clear yet.

This project is released under the [MIT License](LICENSE).
