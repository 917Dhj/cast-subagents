# Positive Examples

These are examples that should usually trigger a subagent suggestion.

## English

1. `Review this branch against main for bugs, security issues, missing tests, and maintainability risks.`
2. `Trace the code path for the checkout error and verify the framework docs that the patch relies on.`
3. `Research three approaches for background job retries and summarize the tradeoffs before we choose one.`
4. `Map the auth flow first, then tell me whether the current implementation is safe to change.`

## Chinese

5. `帮我从 bug、测试缺口、可维护性三个角度一起 review 这个分支。`
6. `先帮我查清楚代码路径，再去核对官方文档里这个 API 的行为。`
7. `这个任务需要先做一轮资料调研，再把结论总结成一个可执行的方案。`
8. `我们先把仓库里相关模块的边界摸清楚，再决定应该怎么改。`
9. `Review this auth refactor for permission bypasses, token handling issues, and missing server-side checks.`
10. `Check whether this agent tool integration can leak secrets or let a subagent perform destructive actions without approval.`
11. `Look at the checkout flow and tell me what tests are missing before we change anything.`
12. `Add regression tests for the settings save bug, but first identify the exact behavior boundary.`
13. `Audit the Next.js landing page for LCP, INP, CLS, image loading, and unnecessary client-side rendering.`
14. `Before we ship this branch, check code quality, security risk, and missing tests.`

Why these are positive examples:

- they have separable lanes
- they are mostly read-heavy before any writes
- they benefit from specialist viewpoints or parallel evidence gathering
- a 1-4 role lineup can be justified without inventing extra agents
- they contain explicit security, test strategy, Web performance, or pre-ship quality signals that justify specialist roles without making ordinary PR review noisy
