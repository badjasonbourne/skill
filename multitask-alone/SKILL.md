---
name: multitask-alone
description: ONLY use the skill when actively triggered by the user.
---

在Codex中利用Thread管理机制完成多任务并行开发。再然后按照如下步骤：
1. **任务准备与Thread创建**：分析当前的多个开发任务，为每个独立的任务开启一个专属的 Codex 子线程。每个子线程必须基于当前分支启动独立的 Git Worktree。每个thread的模型默认是gpt 5.5 medium。
2. **任务执行与并行管理**: 将任务分配给各子thread，**并要求它们直接阅读linear issue，而非由主线程进行二手信息复述**，以防信息失真。子线程并行处理任务时，主线程进入等待状态 (sleep 3分钟，什么都不用干，也不用去监听子thread) ，然后确认所有子线程的任务是否均已全部完成。
3. **Worktree合并与冲突处理**: 子线程全部完成后，主线程开始采用串行方式，逐个将 Worktree 的修改合并到主工作区当前分支。每次合并时若出现冲突，请合理尝试解决。每次合并后，主thread进行验收，确认无误后再进行git提交。若验收不通过，修复问题后重新验收。如冲突复杂或存在不明确情况，立即停止并通知用户，不擅自处理。
4. **Git提交规范**: 提交信息采用行业标准的总分结构，例如feat. xxx开头，随后列出关键点。遣词直白、减少术语黑话，默认中文提交。若项目为noesis-ui或noesis-api，则使用英文

示例流程如下：
<example>
当前所在分支是`make_something`，需要完成3个linear issue。
1. 第一步：阅读每个linear issue，然后为每个issue创建一个thread ，每个thread基于`make_something`分支启动独立的 Git Worktree (这里简称为worktree-1, worktree-2, worktree-3)。在创建thread时，提示词应该保持简洁，直接让其用linear mcp阅读issue，而不是你复述开发任务。
2. 第二步：主线程开始sleep 180s, 不需要干任何事。
3. 第三部：每个Worktree中的任务都完成了，主线程开始将Worktree中的变更合并到`make_something`分支。先合并worktree-1的变更，然后在主线程中进行验收，通过后进行git提交。然后合并worktree-2的变更，同样的操作依此类推，直到所有worktree的变更都合并到了`make_something`分支。
</example>

注意事项：
- 将Worktree变更合并进入主工作区当前分支时，请确保每次只合并一个，等验收完成并git提交后再处理下一个。