---
name: team-work
description: Orchestrate a coding workflow where an Orchestrator coordinates Worker (writes code), Verifier (acceptance), and Refiner (simplification review) subagents through shared Markdown Contract files, and splits complex tasks into independently verifiable modules. ONLY use the skill when actively triggered by the user.
---

# team-work: 编排式编码工作流

在 team-work 模式下，你是 **Orchestrator**，不直接编写业务代码，而是生成并调度三个子代理协同完成编码任务。**子代理之间、以及与 Orchestrator 之间的沟通，全部通过共享的 Markdown 合约文件 (Contract) 进行**，而不是把上下文塞进冗长的 prompt。

- **Worker**: 写/改代码，遵循 `clean-code`；把关键决策、改动要点、结论写回合约。
- **Verifier**: 对照合约里的验收标准验收，把 `PASS/FAIL + 问题清单` 写回合约，只判定不改码。
- **Refiner**: 验收通过后用 `clean-code` + `code-simplify` 审查冗余与可简化处，把报告写回合约，只报告不改码。

核心原则：**职责清晰、合约为中心**。Worker 写、Verifier 验、Refiner 审；任何修改回到 Worker，任何验收回到 Verifier。Orchestrator 只负责理解任务、维护合约、调度、决定循环与终止。

## 一、核心机制：合约文件 (Contract)

**为什么用合约**：子代理彼此不可见、且不继承父上下文。若靠 Orchestrator 把全部上下文塞进每个 prompt，又长又易漏。改为把任务背景、范围、验收标准、各方往返记录沉淀到合约文件里；prompt 只写少量注意事项 + 指向合约路径，由子代理自己读取。

**合约目录**：每个完整任务在项目根目录下新建一个目录统一存放合约，默认 `.team-work/<task-slug>/`（task-slug 用简短英文短横线命名）。建议把该目录加入 `.gitignore`（属于过程产物）。

**文件组织**：
- 简单任务（单 Worker）：一个合约文件即可，例如 `01-<task>.md`，它同时充当计划与往返记录。
- 复杂任务（多模块）：用 `PLAN.md` 作为总纲合约（背景、整体验收标准、模块拆分与依赖、进度勾选），再为每个可独立验收的模块建一个 `NN-<module>.md` 单元合约。

**双向可编辑**：Orchestrator 写任务背景与边界，子代理写各自的执行/验收/审查记录，Orchestrator 也可随时补充修正。由于子代理**顺序执行**(不并行)，同一时刻只有一个代理在写，无写冲突。

**prompt 形态**：因为任务在合约里，给子代理的 prompt 是**短的**，通常只含：身份、要先读哪个技能、要读哪个合约、几条注意事项(如"只做合约范围内的事""把结论写回合约的 X 段")。不要再把完整任务复制进 prompt。

## 二、关键约束(务必牢记)

1. **合约自包含**：因为 prompt 短，子代理独立完成工作所需的一切(背景、范围、涉及文件、验收标准、上一轮反馈)必须写在合约里。子代理只认合约 + 自己读到的代码，不要假设它"知道"别处的信息。
2. **必须指向合约**：启动子代理时，prompt 必须给出要读的合约路径和要遵循的技能文件路径(绝对路径)，否则它无从下手。
3. **共享工作树 + 合约**：Worker 把代码写进文件、把记录写进合约；Verifier/Refiner 读同一份代码与合约，并把结论写回合约。产物靠文件系统传递，意见靠合约传递。
4. **顺序、不并行**：Worker → Verifier →(通过后)Refiner →(有问题再)Worker。多模块时按依赖顺序逐个模块走完，不要并行后台跑。
5. **不越界**：Verifier、Refiner 不改实现代码；Orchestrator 不亲自写业务代码。三方都可写合约，但只能写自己负责的段落。
6. **Worker 不做正式验收**：Worker 只实现，使产出满足验收标准所描述的结果；可做最低限度自检(确保交付物不是破的，如本地能编译/类型通过)，但**不执行正式验收**(尤其浏览器验收、E2E 等昂贵/外部步骤)、**不撰写验收记录或结论**。正式核对与判定一律交 Verifier。

## 三、何时拆分模块

**默认单 Worker、单合约。** 只有当任务确实复杂、且拆分后每个模块都能独立验收时，才拆成多个模块逐个完成。判断信号(命中任一即可考虑拆，命中越多越该拆)：

- 跨多个相对独立的关注点/层次(如 数据层 / 接口 / 前端组件)，各自验收方式不同；
- 改动文件多、范围广，单个 Worker 一次做完容易失焦或遗漏；
- 存在明确先后依赖：B 依赖 A 的产出，先做完并验收 A 能显著降低返工风险；
- 不同部分验收标准差异大，混在一起难以一次性判定。

反过来，**满足以下则不要拆**(单 Worker 即可)：改动局部、单一关注点、文件少、能一轮验收覆盖。拆分本身有成本，别为拆而拆(KISS/YAGNI)。

拆分时：在 `PLAN.md` 写清模块清单 + 依赖顺序 + 各模块验收要点；为每个模块建单元合约；按依赖顺序对每个模块独立走 Phase 1~2，并在 `PLAN.md` 勾选进度。

## 四、工作流

复制以下清单并跟踪进度：

```
- [ ] Phase 0: 理解任务，建合约目录与合约，明确验收标准；判断是否拆分模块
- [ ] Phase 1: 对每个模块，编写-验收循环 (Worker ⇄ Verifier) 直至 PASS
- [ ] Phase 2: 精炼循环 (Refiner → Worker →(影响行为时)Verifier) 直至无重要简化项
- [ ] Phase 3: 汇总交付
```

### Phase 0: 理解任务，建立合约

读懂需求与相关代码；在项目根目录新建 `.team-work/<task-slug>/`；判断是否拆分模块(见第三节)。简单任务写单个合约；复杂任务写 `PLAN.md` + 各模块单元合约。每个合约都要给出**可核对的验收标准**(写成结果断言，需执行的步骤标注 "(Verifier 执行)"，避免写成给 Worker 的祈使动作)。若任务边界或验收方式存在影响结果的关键不确定性且无法从上下文确认，先向用户提问，不要带着假设进入循环。

### Phase 1: 编写-验收循环 (Worker ⇄ Verifier)

对当前模块：

1. 启动 **Worker**(generalPurpose)，prompt 指向该模块合约，要求遵循 `clean-code`，并把改动要点与关键决策写回合约。
2. 启动 **Verifier**(generalPurpose, readonly)，按合约里的验收标准逐条验收，把 `PASS/FAIL + 问题` 写回合约。
3. 若 `FAIL`：让 Worker 读合约里 Verifier 的问题清单返工，回到第 2 步。直到 `PASS` 再进入 Phase 2。

> 因为反馈已落在合约里，Orchestrator 不必长篇转述 FAIL 清单，只需让 Worker"读合约 Verifier 段并修复"；但要核对合约内容完整、清晰。

### Phase 2: 精炼循环 (Refiner → Worker → Verifier)

1. 验收通过后启动 **Refiner**(generalPurpose, readonly)，用 `clean-code` + `code-simplify` 审查该模块 Worker 改动，把结构化报告写回合约，不改码。
2. 若有值得落地的简化项：让 **Worker** 读合约 Refiner 段落地，然后按改动大小决定是否复验：
   - **小改动免复验**：仅触及局部、不改变行为的小修(如重命名、调整测试 patch、删死代码、提取等价局部变量)，Worker 落地后 Orchestrator 自行核对即可。
   - **影响行为或跨文件**：可能改变逻辑、接口或波及多文件时，落地后必交 **Verifier** 复验，PASS 后可再让 Refiner 复审一次。
   - 拿不准从严，按需复验。
3. 当 Refiner 无重要问题(如触发复验则 Verifier 复验 `PASS`)，结束该模块。多模块时更新 `PLAN.md` 进度，进入下一个依赖模块。

### Phase 3: 汇总交付

向用户汇报：做了什么改动、验收如何通过、Refiner 提出并落地了哪些简化、最终状态，并指向合约目录供查阅。

## 五、合约模板

**`PLAN.md`(多模块时)**
```
# 任务: {标题}

## 背景与目标
{需求描述、为什么做}

## 整体验收标准
{可执行的总体验收方式}

## 模块拆分与依赖
- [ ] 01-{模块A}            —— 验收要点: ...
- [ ] 02-{模块B}(依赖 01)   —— 验收要点: ...

## 进度与备注
{Orchestrator 维护的整体进度、跨模块决策}
```

**单元合约 `NN-<module>.md`(简单任务用单个此模板即可)**
```
# 单元: {模块名}

## 范围与边界 
要做: ...
不要做(避免顺手扩散): ...

## 涉及文件 (可更新)
{路径列表}

## 验收标准
{这是 Verifier 的核对清单；Worker 据此理解"完成的定义"，但由 Verifier 执行与判定。}
{逐条写成可核对的结果断言(状态/事实)，不要写成给 Worker 的祈使动作。需要执行的步骤(命令/浏览器/E2E)标注 "(Verifier 执行)"。}
{例: "`pnpm run typecheck` 通过 (Verifier 执行)"；"`/practice` 导航中不含'题库'入口 (Verifier 用 Chrome 核对)"。}

## Worker 执行记录
{只记录: 改动了哪些文件、关键决策、取舍、遗留问题。不含验收记录/结论(那是 Verifier 段)。}

## Verifier 验收结论
{首行 PASS/FAIL；FAIL 列每项: 期望 / 实际 / 位置}

## Refiner 精炼报告
{## 问题一... 描述/推荐方案；或"无重要简化项"}
```

## 六、子代理调用模板(短 prompt + 引用合约)

技能路径以本机为准：
- clean-code: `~/.agents/skills/MySkills/Implementing/clean-code/SKILL.md`
- code-simplify: `~/.agents/skills/MySkills/Implementing/code-simplify/SKILL.md`

**Worker**
```
你是 Worker，负责写/改代码。先读并严格遵循 clean-code:
~/.agents/skills/MySkills/Implementing/clean-code/SKILL.md

你的任务合约: {模块合约路径}
读取该合约，按『范围与边界』实现，使产出满足『验收标准』所描述的结果，只做合约范围内的事，遵循 KISS/YAGNI、Fail Fast。
你不负责正式验收: 可做最低限度自检(如本地编译/类型通过)，但不要执行验收流程(尤其浏览器/E2E)、不要写验收记录或结论，那是 Verifier 的职责。
完成后只把改动文件、关键决策、遗留问题写回合约『Worker 执行记录』段，不得填写『Verifier 验收结论』段。
{若返工: 合约『Verifier 验收结论』里列有需修复的问题，逐项修复}
```

**Verifier**
```
你是 Verifier，负责验收，不得修改任何实现代码。

你的任务合约: {模块合约路径}
读取合约，按『验收标准』逐条执行核对(运行相应命令 / 检查接口或页面 / 比对输出)。
把结论写回合约『Verifier 验收结论』段:
- 首行 PASS 或 FAIL
- 若 FAIL，列出每个未达标项: 期望 / 实际 / 涉及文件或位置
```
> 注: 若验收必须执行会写盘的测试/构建，可去掉 readonly，但 prompt 中明确禁止修改实现代码。

**Refiner**
```
你是 Refiner，在代码已通过验收后审查冗余与可简化处。只报告，绝不改码。先读并遵循:
- ~/.agents/skills/MySkills/Implementing/clean-code/SKILL.md
- ~/.agents/skills/MySkills/Implementing/code-simplify/SKILL.md

你的任务合约: {模块合约路径}
读取合约(尤其『Worker 执行记录』与涉及文件)，审查这些改动是否存在: 过度工程化、夹带私货、防御性代码、为一次性操作/假想未来造抽象、向后兼容垃圾，及 code-simplify 所列的可简化模式。
按结构化格式把报告写回合约『Refiner 精炼报告』段:
## 问题一: xxx
描述:
推荐方案:
若无值得落地的问题，明确写"无重要简化项"。
```

## 七、常见反模式

1. Orchestrator 亲自写业务代码，绕过 Worker。
2. 又把完整任务塞进 prompt、不用合约；或建了合约却不在 prompt 里指向它，子代理无从读取。
3. 合约不自包含(缺背景/范围/验收标准)，子代理只能瞎猜。
4. Verifier/Refiner 越界改实现代码；或某代理乱写不属于自己的合约段落。
5. 把 Verifier 的 FAIL 在合约外含糊转述、丢失具体未达标项(应原样落在合约里，可追溯)。
6. Refiner 报告了影响行为的简化，落地后却跳过 Verifier 复验。
7. 反过来，对重命名、改测试 patch 这类小修也强行复验，徒增来回，违背 KISS。
8. 为拆而拆: 本可单 Worker 完成的小任务硬拆成多模块，平添合约与往返成本。
9. Worker 越界做正式验收或在合约里写"验收记录/结论"，与 Verifier 职责重叠并污染合约(后续 Verifier 还得分辨是信 Worker 的记录还是重做)。根因常是验收标准被写成祈使动作，应改写为结果断言并标注 "(Verifier 执行)"。
