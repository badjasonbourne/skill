---
name: create-linear-issue
description: When users want to create a linear issue, please use this skill.
---

创建一个标准且无歧义的linear issue，便于相关同事看到后能迅速接手开发。大致流程为: 检查环境中是否有linear MCP -> 与用户讨论需求中的模糊点，并达成共识 -> 创建issue，写入linear:

| 阶段 | 时机 | 动作 | 关键要求 |
| --- | --- | --- | --- |
| 环境检测 | 任务开始时 | 检查当前环境中是否存在 Linear MCP | 若不存在，立即停止任务并向用户汇报 |
| 需求澄清 | 环境正常后 | 阅读用户给定需求及相关上下文，指出 3 个最核心的不确定或模糊点 | 每个模糊点需同时给出可选解决策略与你的推荐，便于用户在不同取舍之间做决策 |
| 创建 Issue | 与用户讨论完毕，且用户表示没有其他问题或说 OK 时 | 写入 Linear | 包含Context、Expected Result。Expected Result 得从用户视角描述，比如用户期望如何操作、看到什么、点击什么会触发什么反应 |

此外，如果用户没有指定project，就不应该保存，应先询问用户想保存在哪个project。