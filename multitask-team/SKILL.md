---
name: multitask-team
description: ONLY use the skill when actively triggered by the user.
---

在Codex中利用Thread管理机制完成多任务并行开发，按照如下步骤：
1. **任务准备、分支创建与Thread创建**：分析当前的多个开发任务，为每个任务基于当前分支下创建一个新分支，然后为每个任务创建一个 Codex 子线程。每个子线程必须基于刚刚创建的对应新分支启动独立的 Git Worktree。每个thread的模型默认是gpt 5.5 medium。
2. **任务执行与并行管理**: 将任务分配给各子thread，**并要求它们直接阅读linear issue，而非由主线程进行二手信息复述**。子线程并行处理任务时，主线程进入等待状态 (sleep 3分钟，期间不干任何事情，也不用去监听子thread)，然后确认所有子线程的任务是否均已全部完成。
3. **功能分支提交与验收**: 子线程全部完成后，主线程采用串行方式，将worktree的变更合并到主工作区的对应分支，并在主工作对应分支进行验收，验收通过则进行git提交。若验收不通过，修复问题后重新验收。若存在复杂问题或不明确情况，立即停止并通知用户，不擅自处理。
4. **分支合并验证**: 所有功能分支均验收通过后，新建一个合并验证分支，将各功能分支的内容合并到合并验证分支，检查是否有冲突。如有冲突，请尝试在各功能分支上进行修复，然后再在合并验证分支进行验收，只到无冲突。
5. **Git提交规范**: 提交信息采用行业标准的总分结构，例如 `feat: xxx` 开头，随后列出关键点。遣词直白、减少术语黑话，默认中文提交。若项目为 `noesis-ui` 或 `noesis-api`，则使用英文。

示例流程如下：
<example>
当前所在分支是`make_something`，需要完成3个linear issue。
1. 第一步：阅读每个linear issue，然后为每个issue基于make_something创建一个分支，比如feature/credit-system, fix/fix-login-bug. 为每个 Issue 创建 Thread 并分配独立 Git Worktree，每个 Worktree 基于对应新分支创建（如 Issue-1 → feature/credit-system → Worktree-1）。在创建thread时，提示词应该保持简洁，直接让其用linear mcp阅读issue，而不是你复述开发任务。
2. 第二步：主线程开始sleep 180s, 不需要干任何事。
3. 第三步：每个Worktree内容已完成，将其变更合并到对应分支（如worktree-1合并到feature/credit-system），然后在主线程基于该分支验收，通过则git提交，否则修复问题。每次只合并一个worktree并验收，例如先合并验收worktree-1，再合并验收worktree-2。
4. 第四步：新建integrate/xxx分支，合并feature/credit-system、fix/fix-login-bug等分支，用于检查冲突。冲突则修改对应分支代码，再验证合并，直到没有冲突，且能验收通过。
</example>

注意事项：
- 每个分支的名称都要符合直觉的反应内容，而不是与linear id挂钩，比如feature/credit-system, 而不是feature/opc-1, fix/issue-123
- **在合并验证分支验收完成后，请不要合并到主分支或其他分支，停在此等待用户的处理**
