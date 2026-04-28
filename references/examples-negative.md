# Negative Examples

These are examples that should usually not trigger a subagent suggestion.

## English

1. `Fix this typo in the README.`
2. `Rename this variable in one file.`
3. `What port is the dev server using right now?`
4. `Do not use subagents for this task.`
5. `delegation_context: delegated-subagent; parent approval already completed; goal: Extract candidate papers from this source list.`

## Chinese

6. `把这个函数名改一下。`
7. `这个报错是什么意思？先别用 subagent。`
8. `就修这个单文件的小 bug，不要并行拆分。`
9. `先回答我这个关键问题：这个接口到底返回什么？`
10. `delegation_context: delegated-subagent; parent approval already completed; goal: 按这个 handoff 抽取候选文献。`

Why these are negative examples:

- the task is too small or too direct
- there is no meaningful parallel lane
- the request is blocked on one immediate answer
- the user has explicitly opted out
- delegated subagent handoffs already passed parent approval and should execute, not suggest another lineup

Borderline note:

If a request starts small but grows into review, exploration, or research across several lanes, it may become a positive example later in the conversation.
