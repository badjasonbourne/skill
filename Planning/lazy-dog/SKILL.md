---
name: lazy-dog
description: When planning a development approach, proactively evaluate whether a mature library, third-party API, or SaaS can replace custom code to save the user's time. Assumes budget and machine performance are unlimited and the user's time is precious, but weighs integration/adaptation cost rather than adopting third parties blindly. Use when planning a development approach, designing a solution, choosing a tech stack, or deciding whether to build something yourself vs. use an existing library/API/service.
---

# Buy vs Build：能买就别造

## 核心立场

做开发计划/方案时，**默认优先用成熟的库 / 第三方 API / SaaS 来完成需求**，把自研当成需要论证的例外。

前提假设（默认成立，除非用户另说）：

- **预算无限**：花钱买 API、买算力、买服务都不心疼。
- **机器性能无限**：不为省内存/省 CPU 而牺牲开发效率。
- **用户时间宝贵**：用户是"懒狗"，要的是省时省力，不是炫技。

所以决策时**不要把"成本/性能"当主要约束**，要把"**少写代码、少踩坑、少维护、快上线**"当主要目标。

## 真正要权衡的成本

钱和算力不是成本，**真正的成本是"集成与适配的复杂度"**。引入一个三方之前，问这几个问题：

1. **适配代价**：接进来要改多少现有代码？前后端要不要按它的协议/格式大改？
2. **冗余度**：它的能力/协议里，我真正用到的有多少？是不是为了 10% 的功能背上 100% 的复杂度？
3. **控制权**：它的抽象是否绑死我？以后想改行为是顺手还是要绕开它？
4. **自研难度**：如果自己写，是不是一个薄薄的小模块？（注意：**代码反正是 AI 写的，纯逻辑型的小东西对 AI 不难**，这会大幅拉低"自研"的实际成本。）

## 决策规则

**该用三方（buy）**——当它能净减少总工作量：

- 它解决的是**通用的、有标准答案的脏活累活**（并发、OCR、PDF 解析、鉴权、支付、音视频转码、向量检索……）。
- 接入是"装个库 + 调几个函数"级别，适配面小。
- 自己造等于重新发明轮子，还得自己维护边界情况。

**该自研（build）**——当三方反而是负担：

- 它强加一套**重协议/重规范**，而我只用得上其中一小部分，适配却要全量遵守。
- 接它需要前后端做大量改造，改造量 ≥ 自己写一个薄适配层。
- 需求是项目特有的薄逻辑，AI 几下就能写好，且写出来更可控。

## 标尺示例（用户给定，照此对齐直觉）

- ✅ **并发/多线程**：用 `anyio` 而不是手搓原生 `threading`/`asyncio`。多装一个库换来简单轻松，值。
- ✅ **OCR 转 Markdown**：直接调 Mistral 的 OCR API，而不是自己拼 `opencv` + `markitdown`。预算多，省时间。
- ❌ **Agent 库的流式输出**：**不要**上 AGUI 这类协议库。它协议复杂、很多事件根本用不上，前后端却要严格按它适配改造——这种情况自己写一个轻量 `ui-adapter` 更划算（反正也是 AI 写，不难）。

## 在方案里怎么体现

输出开发计划/方案时：

1. 对每个**有现成解的子问题**，先点名 1 个推荐的成熟库/API/服务，并一句话说明"为什么它能帮用户省时间"。
2. 对决定**自研**的部分，明确说明"为什么不用三方"（通常是适配成本/冗余度/控制权的问题）。
3. 不必为每个三方列一堆备选；给一个默认选择即可，避免选择困难。
4. 牢记目标是**偷懒省时**，不是"为了用三方而用三方"——当自研明显更省事时，大方选自研。
