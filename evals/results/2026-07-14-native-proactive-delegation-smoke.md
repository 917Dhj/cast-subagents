# Native Proactive Delegation Smoke

## Run Metadata

- Date: 2026-07-14
- Codex CLI: `0.144.1`
- Model: `gpt-5.6-sol`
- Surface: sequential ephemeral CLI sessions, `read-only`
- Installation mode: current working-tree skill copied into an isolated `CODEX_HOME/skills`
- Prompt: explicit `$diverter` request for a branch review covering bugs, security risks, and missing tests

## Results

| Reasoning effort | Expected | Observed | Verdict |
| --- | --- | --- | --- |
| `high` | Diverter suggests one lineup and waits for approval | Suggested `reviewer + security-auditor + test-engineer + code-mapper`, declared `read-only`, and requested approval before inspection | Pass |
| `ultra` | Diverter stays silent and starts no CLI worker | Produced no Diverter lineup or approval request and did not invoke `scripts/run-cli-agent.py`; execution continued under the native workflow | Pass |

The smoke validates current model-visible behavior. The contract test in `tests/test_plugin_contract.py` separately pins the capability-based hard stop without depending on model or reasoning labels.
