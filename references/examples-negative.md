# Negative Examples

These are examples that should usually not trigger a subagent suggestion.

## English

1. `Fix this typo in the README.`
2. `Rename this variable in one file.`
3. `What port is the dev server using right now?`
4. `Do not use subagents for this task.`

## Chinese

5. `把这个函数名改一下。`
6. `这个报错是什么意思？先别用 subagent。`
7. `就修这个单文件的小 bug，不要并行拆分。`
8. `先回答我这个关键问题：这个接口到底返回什么？`

Why these are negative examples:

- the task is too small or too direct
- there is no meaningful parallel lane
- the request is blocked on one immediate answer
- the user has explicitly opted out

Borderline note:

If a request starts small but grows into review, exploration, or research across several lanes, it may become a positive example later in the conversation.
