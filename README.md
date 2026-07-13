<h1 align="center">Cast-Subagents</h1>

<p align="center">
  <b>Codex stays quiet about subagents until you ask. Cast-Subagents speaks up first.</b>
</p>
<p align="center">
  <a href="README.md">English</a> | <a href="README.zh.md">简体中文</a>
</p>


<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://github.com/openai/codex"><img src="https://img.shields.io/badge/OpenAI-Codex-000000?labelColor=555555" alt="OpenAI Codex"></a>
  <a href="https://github.com/917Dhj/cast-subagents/stargazers"><img src="https://img.shields.io/github/stars/917Dhj/cast-subagents?style=flat" alt="GitHub Stars"></a>
  <a href="https://github.com/917Dhj/cast-subagents"><img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status: Active"></a>
  <a href="https://github.com/917Dhj/cast-subagents"><img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg" alt="PRs Welcome"></a>
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python 3.11+">
</p>


<p align="center">
  <img src="assets/cast-subagents-hero.png" alt="Cast Subagents hero banner">
</p>
That silence has a cost. Every time a task splits cleanly across multiple lanes — a multi-axis PR review, a codepath-plus-docs verification, an option research with parallel threads — Codex stays in the main thread by default. The user has to notice the opportunity, decide which roles to spawn, and phrase the request clearly enough that Codex follows through. Cast-Subagents handles that recognition step: it spots the task shapes that benefit from delegation and surfaces a lineup suggestion before work begins.

It now recommends specialist lineups for code mapping, review, docs verification, security auditing, test strategy, targeted test automation, Web performance, and pre-ship quality gates.

## 💬 See It In Action

cast-subagents identifies the task shape, names the lineup and work mode, asks one direct question, then stops. It does not touch the task itself until you say go.

![Two chat examples showing cast-subagents recommending subagent lineups](assets/cast-subagents-demo-chat.png)

## 🤔 Why cast-subagents

OpenAI's own Codex documentation states: *"Codex doesn't spawn subagents automatically, and it should only use subagents when you explicitly ask for subagents or parallel agent work."*

That sentence describes a real gap. For every multi-lane task that would benefit from delegation, you have to manually decide whether to split it, which roles to pick, and how to phrase the spawn request clearly. As context grows longer, the main agent tends to absorb everything itself rather than handing work off. cast-subagents closes that gap by front-loading the analysis — but it hands the spawn decision back to you every time.

Some other delegation tools go all the way to automatic spawning after the analysis. cast-subagents stops at the suggestion. That's a deliberate design choice:

| Other auto-spawn tools | cast-subagents |
|---|---|
| Analyze the task, then spawn immediately | Analyze the task, then pause for approval |
| User sees delegation after the fact | User sees the proposed lineup before anything runs |
| Token spend committed without review | You weigh whether the cost is worth it per task |
| Workflow changes to accommodate the tool | Tool fits the workflow you already have |

Three reasons this matters in practice:

1. **You keep final say on every spawn.** Subagents multiply token consumption. An advisory step lets you decide case-by-case whether that spend is justified.
2. **Zero workflow disruption.** Install and keep working the same way. The suggestion appears when it's useful; Codex proceeds normally when it isn't.
3. **No accidental delegation.** If the main thread would handle something fine on its own, cast-subagents stays silent rather than adding overhead.

## 📦 Installation

Tell Codex:

```
Fetch and follow instructions from https://raw.githubusercontent.com/917Dhj/cast-subagents/refs/heads/main/.codex/INSTALL.md
```

The installation guide is the only supported entry point. Codex adds the repository marketplace, installs `cast-subagents@cast-subagents`, asks you to trust the `SessionStart` Hook, shows the complete GPT-5.6 role table, and installs your selected roles globally. You never need to run the Role Installer yourself. Start a new task after installation.

## 🎭 Roles & Lineups

### Bundled roles

Ten specialized roles are included in the `agents/categories/` directory. Their installation numbers are stable; future roles receive new numbers rather than reusing existing ones.

| # | Role | GPT-5.6 model | Reasoning effort | What it does |
|---:|---|---|---|---|
| 1 | `code-mapper` | `gpt-5.6-terra` | `high` | Traces code paths, files, symbols, and ownership boundaries |
| 2 | `search-specialist` | `gpt-5.6-luna` | `medium` | Gathers focused repository or external evidence |
| 3 | `docs-researcher` | `gpt-5.6-luna` | `high` | Verifies official APIs, versions, and documented guarantees |
| 4 | `knowledge-synthesizer` | `gpt-5.6-luna` | `high` | Reconciles long or conflicting findings without inventing facts |
| 5 | `task-distributor` | `gpt-5.6-sol` | `medium` | Splits broad goals into bounded work packages |
| 6 | `reviewer` | `gpt-5.6-sol` | `medium` | Reviews correctness, regressions, contracts, and maintainability |
| 7 | `security-auditor` | `gpt-5.6-sol` | `high` | Audits trust boundaries, auth, secrets, and agent-tool safety |
| 8 | `test-engineer` | `gpt-5.6-luna` | `xhigh` | Designs minimal test coverage for behavior and risk |
| 9 | `test-automator` | `gpt-5.6-terra` | `xhigh` | Adds bounded regression tests after behavior is clear |
| 10 | `web-performance-auditor` | `gpt-5.6-luna` | `xhigh` | Audits Web performance evidence and Core Web Vitals risks |

The recommended installation set is roles `1,3,6,7,8,9`. The agent-friendly installer offers this set, all roles, or any custom selection and warns before overwriting selected same-name files.

The skill selects capabilities first, then maps them to the roles that are actually available in your Codex environment. If a preferred role is missing, the skill says so explicitly rather than silently substituting.

Specialist roles are not decorative. cast-subagents adds them only when the task contains a concrete independent security, test, performance, or release-risk signal.

### Common lineups

| Task shape | Recommended lineup | Work mode |
|---|---|---|
| General PR review | `reviewer + code-mapper` | `read-only` |
| Security-sensitive review | `security-auditor + code-mapper + reviewer` | `read-only` |
| Test coverage analysis | `test-engineer + code-mapper` | `read-only` |
| Targeted regression tests | `test-engineer + test-automator + code-mapper` | `mixed` |
| Web performance audit | `web-performance-auditor + code-mapper` | `read-only` |
| Pre-ship quality gate | `reviewer + security-auditor + test-engineer + code-mapper` | `read-only` |
| Codepath plus docs/API verification | `code-mapper + docs-researcher` | `read-only` |
| Option research and tradeoff synthesis | `search-specialist + knowledge-synthesizer` | `read-only` |

Specialist examples:

| Task shape | Recommended lineup | Work mode |
|---|---|---|
| Auth / permission / token flow review | `security-auditor + code-mapper` | `read-only` |
| LLM / agent tool safety review | `security-auditor + code-mapper + docs-researcher` | `read-only` |
| Web performance audit with supplied metrics | `web-performance-auditor` | `read-only` |
| Targeted regression tests | `test-engineer + test-automator + code-mapper` | `mixed` |

The cap is four roles. If a task seems to need more, cast-subagents either compresses the lineup or stays silent rather than padding it out.

These role names are compatible with VoltAgent/awesome-codex-subagents and similar community Codex subagent collections. If you use a custom role set, you can adapt `skills/cast-subagents/references/role-lineups.md` to add your own task shape mappings.

## 🔄 Work Modes

**`read-only`** — agents inspect, trace, and report. No files are written. This is the default for review, mapping, research, and verification tasks, and what cast-subagents defaults to when in doubt. Most suggestions use this mode.

**`mixed`** — agents start with a read-only pass and pause before any writes. The skill confirms the exploration phase is complete before handing off to a write-capable agent. When you see `mixed` in a suggestion, it means: "we'll dig in first, and I'll check with you before anything changes."

**`write-capable`** — agents may edit files within their assigned scope. cast-subagents uses this only for explicitly write-capable work. Test-writing tasks normally start as `mixed`: `test-engineer` and `code-mapper` clarify the behavior first, then `test-automator` writes targeted tests only when the scope is clear.

The mode is always stated using one of these three exact labels — you won't see a suggestion without knowing which one applies.

## 🎯 Decision Rules

### When cast-subagents speaks up

cast-subagents looks for two kinds of signals: core delegation signals, where work splits into independent lanes, and specialist signals, where a concrete risk calls for a focused role.

**Core delegation signals**

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

**Specialist signals**

- **Security boundary** — auth, authorization, secrets, user input, webhooks, dependencies, or exploitable LLM/tool permissions are central to the task.

  > `Review this auth refactor for permission bypasses, token handling issues, and missing server-side checks.`

- **Test strategy or targeted regression tests** — the task asks which tests are missing, how to prove a bug fix, or how to add bounded regression coverage.

  > `Look at the checkout flow and tell me what tests are missing before we change anything.`

- **Web performance** — the task names frontend routes, Core Web Vitals, Lighthouse, LCP, INP, CLS, loading, rendering, or network behavior.

  > `Audit the Next.js landing page for LCP, INP, CLS, image loading, and unnecessary client-side rendering.`

- **Pre-ship quality gate** — the task asks for release readiness across code quality, tests, security, and risk.

  > `Before we ship this branch, check code quality, security risk, and missing tests.`

- **LLM or agent tool safety** — the task involves prompt injection, tool permissions, secrets in context, delegated agents, or destructive tool use.

  > `Check whether this agent tool integration can leak secrets or let a subagent perform destructive actions without approval.`

### When it stays quiet

- **Trivial or single-file change** — a one-liner fix or rename doesn't benefit from delegation.

  > `Fix this typo in the README.`

- **Tightly coupled write work** — same-file changes with overlapping logic are safer in sequence.

  > `就修这个单文件的小 bug，不要并行拆分。`

- **Immediate fact lookup** — the task is blocked on one answer, so spawning agents first doesn't help.

  > `What port is the dev server using right now?`

- **Explicit opt-out** — if you say not to use subagents, that's a hard constraint.

  > `Do not use subagents for this task.`

- **Ambiguous request** — if the intent isn't clear enough to build a solid lineup, the skill asks for clarification first.

The Chinese examples above are included intentionally. cast-subagents matches the user's language when writing suggestions; role names and work mode labels remain in English regardless of the prompt language.

## ⚙️ How It Works

cast-subagents has three parts that work in sequence:

- **The `SessionStart` Hook** activates a short advisory gate for the root session. It is restored after startup, resume, clear, and compaction without modifying instruction files.
- **The skill** is the advisor. When the gate determines a suggestion is warranted, it classifies the task shape, selects a lineup of 1–4 roles, determines the work mode, and writes the suggestion message. Then it stops and waits.
- **The execution backend** runs approved handoffs. Codex uses native custom agents when the spawn interface exposes role and model controls; otherwise it uses temporary `codex exec` workers that preserve each role's model, effort, sandbox, instructions, and live Web Search.

CLI workers are leaf agents: multi-agent features are disabled, so they cannot delegate again.

```
User sends task
      │
      ▼
SessionStart Hook activates advisory gate
      │
      ├── task is simple / single-lane / opted out
      │         │
      │         ▼
      │     stay silent → Codex continues normally
      │
      └── task has independent lanes
                │
                ▼
          cast-subagents skill
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
  continue in         select native or
  main thread         CLI worker backend
```

### The Suggestion Contract

Every suggestion covers four things in order: why the task could benefit from subagents, the exact lineup with a reason per role, the work mode, and a permission question matched to the risk of the work. The output is conversational rather than templated — the same four pieces, different wording each time.

Hard constraints: exactly one lineup, no more than four roles, no task content before approval, no implication that delegation has already started. The suggestion always ends with a question.

### After Approval

Once you approve, each agent gets a structured handoff that includes the goal, success criteria, scope boundaries, relevant file paths, write policy, and a verifiable deliverable. Here's what a typical handoff looks like:

```text
delegation_context: delegated-subagent; parent approval already completed; do not invoke cast-subagents or request another delegation approval; execute this handoff only
goal: Map the affected code path for the settings save failure.
success_criteria: Identify the real execution path, likely failure boundary,
  and the files that own the behavior.
scope_in: settings modal, client mutation, API route, response handling
scope_out: unrelated settings pages, styling, copy updates
relevant_paths: src/settings/, app/api/settings/, useSettingsForm
constraints: read-only; no code edits; cite concrete files and symbols
deliverable: concise summary with file references and one likely root cause
verification: parent can trace the same path from your references
write_policy: read-only
open_questions: whether retries or optimistic updates affect the failure mode
```

No agent infers scope from context — everything is explicit. The full schema is in `skills/cast-subagents/references/handoff-schema.md`.

## ❓ FAQ

**Why doesn't it just spawn subagents automatically?**

That's a deliberate design choice, not a limitation. Subagents multiply token consumption, and the right call varies by task. An approval step lets you weigh that cost each time rather than committing to it unconditionally. Other tools in this space make spawning automatic; cast-subagents treats your approval as a required step.

**Will it slow Codex down on simple tasks?**

No. The `SessionStart` Hook loads the advisory gate once per root session lifecycle event. For simple, single-domain, or single-file work, the gate stays completely silent.

**What if I want to skip the suggestion just this once?**

Include a phrase like "do not use subagents" or "no subagents" in your prompt. The gate treats explicit opt-outs as a hard constraint. You can also decline the suggestion when it appears — cast-subagents will continue in the main thread without re-suggesting unless the task materially changes.

**Does it work with custom subagent collections?**

Yes. The preferred role names are compatible with collections like VoltAgent/awesome-codex-subagents. If you use a custom set, edit `skills/cast-subagents/references/role-lineups.md` to add your own task shape mappings. cast-subagents will use whatever roles are available and say so explicitly when a preferred role is missing.

**Does it edit my code?**

The advisory step does not edit code. After approval, an approved write-capable role may edit within its explicit handoff and sandbox; read-only roles remain read-only.

**Does it support non-English prompts?**

Yes. cast-subagents matches your language when writing the suggestion. Role names and work mode labels remain in English as exact tokens, but the surrounding message follows the language of your prompt. Chinese is supported out of the box.

**Can I customize which task shapes trigger a suggestion?**

Yes. `skills/cast-subagents/references/decision-rules.md` is the source of truth for task shape classification. `skills/cast-subagents/references/role-lineups.md` controls lineup recommendations. Both are plain Markdown tables — edit them directly to add, remove, or adjust rules. No configuration language to learn.

## 🗂 Project Structure

```text
cast-subagents/
├── .codex-plugin/
│   └── plugin.json               # Plugin manifest
├── .agents/plugins/
│   └── marketplace.json          # Single-plugin marketplace
├── .codex/
│   └── INSTALL.md                # Agent-readable install instructions
├── hooks/
│   ├── hooks.json                # SessionStart registration
│   └── session_start.py          # Stateless advisory gate output
├── skills/cast-subagents/
│   ├── SKILL.md                  # Core advisor skill
│   └── references/               # Rules, lineups, examples, and handoff schema
├── agents/
│   ├── openai.yaml               # Skill interface definition
│   └── categories/
│       ├── 01-core/
│       │   └── code-mapper.toml
│       ├── 02-research/
│       │   ├── docs-researcher.toml
│       │   ├── knowledge-synthesizer.toml
│       │   └── search-specialist.toml
│       ├── 03-planning/
│       │   └── task-distributor.toml
│       └── 04-quality/
│           ├── reviewer.toml
│           ├── security-auditor.toml
│           ├── test-engineer.toml
│           ├── test-automator.toml
│           └── web-performance-auditor.toml
├── scripts/
│   ├── install-agent-roles.py    # Installs bundled roles globally
│   └── run-cli-agent.py          # Runs one temporary leaf CLI worker
├── evals/
│   ├── prompts.yaml
│   ├── rubric.md
│   ├── scenarios.md
│   └── results/
└── CHANGELOG.md
```

The skill's `references/` directory is where substantive policy changes go. `SKILL.md` loads these references at runtime, so you can tune decision rules, lineup tables, and wording without touching the skill logic itself.

## 🙏 Acknowledgments

The always-on gate pattern and session-bootstrap approach in this project were inspired by [obra/superpowers](https://github.com/obra/superpowers). The idea of using a session-bootstrap mechanism to ensure a gate runs before every task came directly from studying that project.

The bundled role pack is a small, curated subset adapted from [VoltAgent/awesome-codex-subagents](https://github.com/VoltAgent/awesome-codex-subagents). It includes only the roles that cast-subagents commonly recommends, with light organization around this skill's decision rules rather than a full mirror of that collection.

The role design for Staff Engineer review, security auditing, test strategy, and Web performance auditing was informed by [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The cast-subagents versions are rewritten for Codex subagent TOML roles and this project's advisory lineup-selection model.

## 🤝 Contributing & License

Issues and pull requests are welcome. The most useful contributions are:

- New task shapes in `skills/cast-subagents/references/decision-rules.md` with a matching lineup in `skills/cast-subagents/references/role-lineups.md`
- Positive and negative examples in `skills/cast-subagents/references/examples-positive.md` and `skills/cast-subagents/references/examples-negative.md` that ground the new rule in real prompts
- Eval scenarios in `evals/scenarios.md` that cover edge cases where the current rules produce an unexpected result

When adding a decision rule, the useful test is: can you write a prompt that should trigger it, and a similar-looking prompt that should stay silent? If both are in the example files, the rule is well-scoped.

This project is released under the [MIT License](LICENSE).
