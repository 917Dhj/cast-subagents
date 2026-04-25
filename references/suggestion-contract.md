# Suggestion Contract

Every subagent suggestion must follow the same user-facing contract.

Required section order:

1. `Recommended lineup`
2. `Why this fits`
3. `Work mode`
4. `Permission question`

Required behavior:

- recommend one lineup only
- keep the lineup between 1 and 4 roles
- use existing roles only
- mention fallback substitutions explicitly
- ask for permission before any spawn

## Template 1: Read-Only Review

```text
Recommended lineup: reviewer + code-mapper + docs-researcher
Why this fits: reviewer can look for correctness and test risks, code-mapper can trace the real execution path, and docs-researcher can verify the API or framework assumptions in parallel.
Work mode: read-only
Permission question: Want me to use these subagents for this review?
```

Use this when:
- the task is a multi-axis review
- code, docs, and risk assessment can be separated cleanly

## Template 2: Docs + Codepath Verification

```text
Recommended lineup: docs-researcher + code-mapper
Why this fits: docs-researcher can confirm the documented behavior while code-mapper traces the implementation path that depends on it.
Work mode: read-only
Permission question: Want me to use these subagents before we decide on a fix?
```

Use this when:
- the main uncertainty is "what should happen" versus "what the code actually does"

## Template 3: Mixed Exploration + Implementation

```text
Recommended lineup: code-mapper + reviewer + worker
Why this fits: code-mapper can locate the real failure path, reviewer can pressure-test the likely fix, and worker can apply the smallest bounded change once the issue is understood.
Work mode: mixed
Permission question: Want me to use these subagents, with read-only exploration first and implementation only after that?
```

Use this when:
- one bounded implementation step follows a read-heavy investigation
- the write scope can be kept small and delayed until the issue is understood

## Failure Cases To Avoid

Do not do these:

- `I can spin up a few agents if you want.` without naming the lineup
- listing 5 or more roles
- offering three equally weighted lineups with no recommendation
- saying or implying that delegation already started
- asking a vague question like `Should I use subagents?` without showing the proposed lineup
