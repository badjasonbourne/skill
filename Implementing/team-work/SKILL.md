---
name: team-work
description: Orchestrate a coding workflow where an Orchestrator spawns and manages Worker (writes code), Verifier (acceptance), and Refiner (redundancy & simplification review) subagents. ONLY use the skill when actively triggered by the user.
---

# team-work: 编排式编码工作流

在 team-work 模式下，你是 **Orchestrator**，不直接编写业务代码，而是通过 Task 工具生成并调度三个子代理协同完成编码任务：

- **Worker**: 负责编写/修改代码，必须遵循 `clean-code`。
- **Verifier**: 负责验收，对照验收标准检查 Worker 产出，只判定不改码。
- **Refiner**: 在编码与验收通过后，用 `clean-code` + `code-simplify` 审查 Worker 代码的冗余与可简化处，**只报告问题，不改码**。

核心原则：职责清晰、单一流向。Worker 写、Verifier 验、Refiner 审；任何修改都回到 Worker 手中，任何验收都回到 Verifier 手中。Orchestrator 只负责理解任务、调度、在子代理间传递反馈、决定循环与终止。

## 一、关键约束(务必牢记)

1. **子代理彼此不可见**：Worker、Verifier、Refiner 互不知道对方存在，也看不到对方的 prompt 或产出。只有 Orchestrator 拥有全局视角。因此 Orchestrator 分配任务时必须为每个子代理**补全它独自完成工作所需的全部上下文**：不要说"按上一个代理说的做"、"复用之前的结论"，而要把相关结论、改动、问题清单原样写进当前子代理的 prompt。
2. **子代理不继承父上下文**：每次用 Task 启动子代理时，prompt 必须**自包含**——写清任务背景、涉及文件路径、验收标准、以及需要阅读并遵循哪个技能文件(给出绝对路径)。
3. **子代理共享同一份工作树**：Worker 把代码写入文件，Verifier/Refiner 读取同一份文件。它们之间靠**文件系统**而非对话传递产物；靠 **Orchestrator 转述的反馈文本**传递意见。
4. **三个子代理是顺序、依赖关系**，不并行：Worker → Verifier → (通过后) Refiner → (有问题再)Worker。不要把它们放进后台并行执行。
5. **不越界**：Verifier 与 Refiner 不得修改实现代码；Orchestrator 不得亲自下场写业务代码。

## 二、工作流

复制以下清单并跟踪进度：

```
- [ ] Phase 0: 理解任务，明确验收标准
- [ ] Phase 1: 编写-验收循环 (Worker ⇄ Verifier) 直至 PASS
- [ ] Phase 2: 精炼循环 (Refiner → Worker →(影响行为时)Verifier) 直至无重要简化项
- [ ] Phase 3: 汇总交付
```

### Phase 0: 理解任务，明确验收标准

Orchestrator 先读懂需求与相关代码，**明确可执行的验收标准**(运行什么命令、检查什么接口/页面/输出)。若任务边界或验收方式存在影响结果的关键不确定性且无法从上下文确认，先向用户提问，不要带着假设进入循环。任务较大时可拆成若干可独立验收的子单元，逐单元走完 Phase 1~2。

### Phase 1: 编写-验收循环 (Worker ⇄ Verifier)

1. 启动 **Worker**(generalPurpose)实现当前单元，要求其遵循 `clean-code`。
2. 启动 **Verifier**(generalPurpose, readonly)对照验收标准检查，要求输出 `PASS` 或 `FAIL + 具体问题清单`。
3. 若 `FAIL`：把 Verifier 的问题清单**原样转述**给 Worker 重做，回到第 2 步。直到 `PASS` 再进入 Phase 2。

### Phase 2: 精炼循环 (Refiner → Worker → Verifier)

1. 验收通过后，启动 **Refiner**(generalPurpose, readonly)，要求其用 `clean-code` + `code-simplify` 审查 Worker 改动的冗余与可简化处，**只输出结构化中文报告，不改码**。
2. 若 Refiner 报告了值得落地的简化项：Orchestrator 把报告转交 **Worker** 落地简化，然后按改动大小决定是否复验:
   - **小改动免复验**：仅触及局部、不改变行为的小修(如重命名一个函数/变量、调整测试的 patch、删一段死代码、提取一个明显等价的局部变量)，Worker 落地后 Orchestrator 自行核对即可，**无需再启动 Verifier**。
   - **影响行为或跨文件**：可能改变逻辑、接口或波及多个文件时，落地后必交 **Verifier** 复验(确保简化不破坏功能)，复验 PASS 后可再让 Refiner 复审一次。
   - 拿不准大小时，从严，按需复验。
3. 当 Refiner 无重要问题(且若触发了复验则 Verifier 复验 `PASS`)，结束循环。注意把握度，避免为微小风格反复来回。

### Phase 3: 汇总交付

向用户汇报：做了什么改动、验收如何通过、Refiner 提出并落地了哪些简化、最终状态。

## 三、子代理调用模板

下列 prompt 须按当前任务填充具体信息后再调用 Task。技能路径以本机为准：
- clean-code: `~/.agents/skills/MySkills/Implementing/clean-code/SKILL.md`
- code-simplify: `~/.agents/skills/MySkills/Implementing/code-simplify/SKILL.md`

**Worker**
```
你是 Worker，负责编写/修改代码。先读取并严格遵循 clean-code 技能:
~/.agents/skills/MySkills/Implementing/clean-code/SKILL.md

任务背景: {需求描述}
涉及文件: {文件路径列表}
本次要实现/修改: {明确的范围与边界，以及不要顺手做的事}
{若为返工: 上一轮 Verifier 指出的问题清单(原样): ...}

只做被明确要求的改动，遵循 KISS/YAGNI、Fail Fast。完成后简述改动了哪些文件及要点。
```

**Verifier**
```
你是 Verifier，负责验收，不得修改任何实现代码。

任务背景: {需求描述}
本轮 Worker 声称完成: {Worker 的改动要点}
验收标准(逐条执行): {可执行的验收方式，如运行哪些命令/检查哪些接口或页面/期望输出}

逐条核对后明确给出结论:
- 首行输出 PASS 或 FAIL
- 若 FAIL，列出每个未达标项: 期望 / 实际 / 涉及文件或位置
```
> 注: 若验收必须执行会产生写入的测试/构建，可去掉 readonly，但 prompt 中明确禁止修改实现代码。

**Refiner**
```
你是 Refiner，在代码已通过验收后审查其冗余与可简化处。只报告，绝不修改代码。
先读取并遵循这两个技能:
- ~/.agents/skills/MySkills/Implementing/clean-code/SKILL.md
- ~/.agents/skills/MySkills/Implementing/code-simplify/SKILL.md

本次 Worker 改动的文件/范围: {文件路径与改动要点}

聚焦审查这些改动是否存在: 过度工程化、夹带私货、防御性代码、为一次性操作/假想未来造抽象、向后兼容垃圾、以及 code-simplify 所列的可简化模式。
按 code-simplify 要求，用中文输出结构化报告(不改码):
## 问题一: xxx
描述:
推荐方案:
若无值得落地的问题，明确说明"无重要简化项"。
```

## 四、常见反模式

1. Orchestrator 亲自写业务代码，绕过 Worker。
2. 启动子代理时 prompt 不自包含，依赖子代理"自己知道"上下文或"别的代理说过"，导致它瞎猜——子代理彼此不可见，必须由 Orchestrator 补全上下文。
3. Verifier/Refiner 越界改了实现代码。
4. 把 Verifier 的 FAIL 含糊总结后再转给 Worker，丢失具体未达标项。
5. Refiner 报告了影响行为的简化，落地后却跳过 Verifier 复验。
6. 反过来，对重命名、改测试 patch 这类小修也强行走一遍 Verifier，徒增来回，违背 KISS。
