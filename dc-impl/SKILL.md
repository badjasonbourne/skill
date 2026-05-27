---
name: dc-impl
description: Implement a divide & conquer style development plan from dc-spec. ONLY use the skill when actively triggered by the user.
---

# dc-impl: 分而治之任务实施

在 dc-impl 模式下，目标是基于 spec/PLAN.md 和 spec/task.json 逐步完成任务，并持续维护 spec/progress.txt。你需要严格遵循既有规划，但以当前项目事实为准；若发现规划与项目实际不一致，应先修正 spec/PLAN.md 或 spec/task.json，再继续实施。

dc-impl 一次只实施一个任务。每个任务都必须经历：选择任务 → 实施变更 → 执行验收 → 记录进度 → 标记 passed → 再选择下一个任务。除非遇到外部阻塞，不要在完成单个任务后停止，应持续推进直到所有任务完成。

## 一、前置条件

开始前，确认以下文件存在：
- spec/PLAN.md
- spec/task.json
- spec/progress.txt

若任一文件不存在，停止并告知用户先使用 dc-spec 模式生成规划。不要自行凭空创建实施计划。

开始实施前，先阅读 spec/PLAN.md 理解整体目标与策略，再阅读 spec/task.json 和 spec/progress.txt，确认任务清单、依赖关系、已完成内容和后续任务需要继承的上下文。

## 二、任务选择

从 spec/task.json 中选择一个 `passed: false` 的任务执行。若 T0 尚未完成，应先执行 T0；T0 只用于阅读需求、定位关键文件、理解项目结构与实现入口，不修改业务代码：
- 选择非 T0 任务时，应结合 task.json 的 passed 状态、progress.txt 的记录和当前项目状态，确认其前置依赖已经满足。
- 一次只选择一个任务，不要批量实施多个任务。若存在未完成任务，但没有任何任务的前置条件满足，停止并向用户说明阻塞原因。

## 三、实施要求

实施时只处理当前任务 description 中定义的范围，不要顺手实现相邻功能，也不要把后续任务提前完成。若遇到外部阻塞，例如缺少依赖、密钥、环境服务、账号登录态、第三方服务不可用等，立即停止并报告用户；不要绕过验收，也不要把未通过的任务标记为完成。

## 四、进度维护

每完成一个任务并通过验收后，立即更新 spec/progress.txt，并将 spec/task.json 中对应任务的 `passed` 标记为 `true`。progress.txt 重点写清楚做了什么、如何验收、以及后续任务需要知道的信息。

progress.txt 按以下格式追加：
```txt
# Progress

## Task 0: 熟悉任务上下文
{记录重要 findings}

## Task 1: {task name}
### Done:
- {改了什么}

### Verified:
- {执行了什么验收，结果如何}

### Notes:
- {后续任务需要知道的信息；没有则省略本节}
```