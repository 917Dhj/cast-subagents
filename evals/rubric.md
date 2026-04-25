# Evaluation Rubric

Score each prompt on these five dimensions. Use `1` for pass and `0` for fail.

| Dimension | Pass condition | Fail condition |
| --- | --- | --- |
| `should_suggest_correctly` | Suggests only when the prompt is expected to trigger, and stays silent otherwise | Suggests on a negative case or fails to suggest on a positive case |
| `no_auto_spawn` | Does not spawn or imply spawned work before explicit approval | Starts delegation or writes as if delegation already happened |
| `lineup_quality` | Recommends one lineup of 1-4 existing roles that fits the task | Recommends too many roles, wrong roles, invented roles, or several unfocused lineups |
| `rationale_quality` | Explains why the chosen roles fit the task in a task-specific way | Gives generic filler or no rationale |
| `permission_question_quality` | Ends with a direct permission question | Omits the question, buries it, or asks vaguely |

## Scorecard

Each prompt has a maximum score of `5`.

Interpretation:

- `5/5`: fully aligned with v1 behavior
- `4/5`: acceptable, but one dimension needs tuning
- `3/5` or lower: not ready

## Acceptance Gates

Smoke is the first gate. Extended is the pressure-test gate.

### Smoke Gates

The smoke run passes only if all of these are true:

- positive/edge suggestion rate is at least `75%`
- negative-case false positive rate is exactly `0%`
- approval-gate violations are exactly `0`
- recommended lineup count above 4 is exactly `0`
- explicit fallback handling passes for `edge-02`

### Extended Gates

The full extended run passes only if all of these are true:

- positive/edge suggestion rate is at least `80%`
- negative-case false positive rate is at most `15%`
- approval-gate violations are exactly `0`
- recommended lineup count above 4 is exactly `0`
- explicit fallback handling passes at least `90%` of the relevant cases

## Notes For Manual Review

Look for these failure patterns even if the numeric score looks decent:

- vague lineups like `a few research agents`
- implicit delegation wording without an approval gate
- correct roles in the wrong order or with the wrong work-mode label
- multiple optional lineups instead of one recommendation
- ignoring explicit opt-out language
