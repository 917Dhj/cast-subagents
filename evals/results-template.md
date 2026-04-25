# Evaluation Results Template

## Run Metadata

- Date:
- Plugin revision:
- Evaluator:
- Surface:
- Suite: `smoke` / `extended` / `desktop`
- Arm: `baseline` / `plugin`
- Installation mode: `plugin` / `$CODEX_HOME/skills` / `symlink` / `legacy root skill`
- Raw output directory:

## Discovery

| Check | Result | Pass? |
| --- | --- | --- |
| `using-cast-subagents` visible |  |  |
| `cast-subagents` visible |  |  |
| No skill load errors |  |  |

## Summary

| Metric | Result | Pass? |
| --- | --- | --- |
| Positive/edge suggestion rate |  |  |
| Negative-case false positive rate |  |  |
| Approval-gate violations |  |  |
| `>4` role violations |  |  |
| Fallback correctness rate |  |  |

## Prompt-by-Prompt Results

| ID | Suite | Score / 5 | Suggested? | Roles used | Permission question present? | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| pos-01 | smoke |  |  |  |  |  |
| pos-02 | smoke |  |  |  |  |  |
| pos-03 | smoke |  |  |  |  |  |
| pos-04 | extended |  |  |  |  |  |
| pos-05 | extended |  |  |  |  |  |
| pos-06 | extended |  |  |  |  |  |
| neg-01 | smoke |  |  |  |  |  |
| neg-02 | extended |  |  |  |  |  |
| neg-03 | smoke |  |  |  |  |  |
| neg-04 | extended |  |  |  |  |  |
| neg-05 | smoke |  |  |  |  |  |
| neg-06 | extended |  |  |  |  |  |
| edge-01 | extended |  |  |  |  |  |
| edge-02 | smoke |  |  |  |  |  |
| edge-03 | extended |  |  |  |  |  |
| edge-04 | extended |  |  |  |  |  |
| edge-05 | extended |  |  |  |  |  |
| edge-06 | smoke |  |  |  |  |  |

## Failure Patterns

- 
- 
- 

## Subagent Evaluator Notes

- Runner:
- Reviewer:
- Synthesizer:

## Recommended Revisions

- Files to revise:
- Why:
- Expected effect:

## Go / No-Go

- Decision:
- Reason:
