# Evaluation Scenarios

This repository now evaluates the plugin shape, not only a single skill.

There are two prompt suites:

- `smoke`: the reduced first gate, marked with `smoke: true` in [prompts.yaml](prompts.yaml)
- `extended`: the full 18-prompt pressure suite, run only after smoke passes

CLI is the reproducible surface. Desktop is the manual experience surface.

## Discovery Check

Use an isolated home and copy the plugin skills into it:

```bash
rm -rf /tmp/codex-subagent-eval/skill
mkdir -p /tmp/codex-subagent-eval/skill/skills
cp -R skills/* /tmp/codex-subagent-eval/skill/skills/
```

Confirm both skills are visible:

```bash
CODEX_HOME=/tmp/codex-subagent-eval/skill \
codex debug prompt-input | rg "using-cast-subagents|cast-subagents"
```

Pass condition:

- `using-cast-subagents` appears
- `cast-subagents` appears
- no `failed to load skill` error appears

## CLI Baseline

Create an isolated home without plugin skills:

```bash
rm -rf /tmp/codex-subagent-eval/baseline
mkdir -p /tmp/codex-subagent-eval/baseline
```

Run the prompts marked `smoke: true` first:

```bash
CODEX_HOME=/tmp/codex-subagent-eval/baseline \
codex exec -s read-only "REPLACE_WITH_PROMPT"
```

Record raw output and score it with [rubric.md](rubric.md).

## CLI Plugin Smoke

Use the discovered skill home from the discovery check:

```bash
CODEX_HOME=/tmp/codex-subagent-eval/skill \
codex exec -s read-only "REPLACE_WITH_PROMPT"
```

Run only prompts marked `smoke: true`.

Smoke pass gates:

- positive/edge trigger rate is at least `75%`
- negative false positive rate is exactly `0%`
- approval-gate violations are exactly `0`
- recommended lineup count above 4 is exactly `0`
- explicit fallback handling passes for `edge-02`

## CLI Extended Suite

Run the full 18-prompt suite only after smoke passes.

Extended pass gates remain stricter:

- positive/edge trigger rate is at least `80%`
- negative false positive rate is at most `15%`
- approval-gate violations are exactly `0`
- recommended lineup count above 4 is exactly `0`
- explicit fallback handling passes at least `90%` of relevant cases

## Desktop Manual Validation

Desktop validation is a smoke test for:

- plugin visibility
- entry skill implicit triggering
- user-facing wording
- approval-gate behavior
- negative-case silence

Recommended prompt subset:

- `pos-01`
- `pos-03`
- `neg-03`
- `edge-06`

Manual setup:

1. Enable this repository as a Codex plugin.
2. Confirm the plugin manifest points at `skills/`.
3. Start a new Codex Desktop session.
4. Verify that `using-cast-subagents` and `cast-subagents` are visible in the available skills list.
5. Run the prompt subset.
6. Verify that wording matches [../references/suggestion-contract.md](../references/suggestion-contract.md).

## Two-Step Approval-Gate Checks

Use these follow-up turns after the first smoke pass.

### Reject Path

1. Run `edge-03`.
2. Confirm that Codex suggests a lineup and asks permission.
3. Reply:

   ```text
   No, continue without subagents.
   ```

4. Pass condition:
   - Codex continues in the main thread
   - Codex does not immediately re-suggest

### Approval Path

1. Run `edge-04`.
2. Confirm that Codex suggests a lineup and asks permission.
3. Reply:

   ```text
   Yes, use those subagents.
   ```

4. Pass condition:
   - delegated exploration stays read-first
   - write-capable work stays bounded
   - the main thread summarizes results instead of dumping raw logs

## Subagent-Assisted Evaluation

Subagents may help evaluate, but should not edit repository files.

Recommended split:

- `test-automator` or `worker`: run CLI smoke shards only when each runner has an independent authenticated `CODEX_HOME`
- `reviewer`: independently score outputs against [rubric.md](rubric.md)
- `knowledge-synthesizer`: summarize failure patterns across evaluator notes

Do not copy the same `auth.json` into multiple parallel `CODEX_HOME` directories for concurrent `codex exec` runs. Parallel refreshes can invalidate or reuse the same token. If only one authenticated home is available, run CLI prompts sequentially and use subagents only for read-only scoring of completed raw outputs.

The main thread owns final judgment and writes result files.

## Recording Results

Use [results-template.md](results-template.md) for each evaluation round.

Recommended naming:

- `evals/results/round-01.md`
- `evals/results/round-02.md`

Record the suite (`smoke` or `extended`) and installation mode (`plugin`, `$CODEX_HOME/skills`, symlink, or legacy root skill). Do not change the prompt set during a round. If you revise the plugin or skills, start a new results file.
