---
name: pydanticai-ui-adapter
description: Correctly designs pydanticai agent event adapter for UI consumption. ONLY use the skill when actively triggered by the user.
---

# PydanticAI Agent UI Adapter

将 PydanticAI SDK 的流式事件**重命名 + 裁字段**后透传给前端。

## 适配器只做两件事

1. **重命名**：SDK 事件名晦涩（如 `PartStartEvent`、`FunctionToolCallEvent`），改为前端渲染直觉的名称（如 `text_start`、`tool_execution_start`）
2. **裁字段**：SDK 事件载荷字段多而杂，只透传 UI 需要的字段

**不做**事件聚合、重组、拆分、转换、业务逻辑注入。适配器中的事件与 SDK 事件**一一对应**，只是名字不同、字段更少。

## 事件语义（命名习惯 `{语义}_{phase}`）

### 文本与推理


| 事件                | 含义                  |
| ----------------- | ------------------- |
| `text_start`      | python 开始输出一段用户可见文本 |
| `text_delta`      | 输出增量的用户可见文本         |
| `text_end`        | 用户可见文本输出完毕             |
| `reasoning_start` | 开始输出一段Agent的推理文本          |
| `reasoning_delta` | 输出增量的Agent的推理文本              |
| `reasoning_end`   | Agent的推理文本输出完毕               |


### 工具调用（参数流）

模型在生成工具调用参数时的流式片段（尚未执行）。


| 事件               | 含义             |
| ---------------- | -------------- |
| `toolcall_start` | 开始输出一个工具调用的入参文本    |
| `toolcall_delta` | 输出增量的工具调用的入参文本 |
| `toolcall_end`   | 工具调用的入参输出完毕    |


### 工具执行与结果

实际执行工具或收到返回时发出（与上面的参数流阶段区分）。


| 事件                        | 含义          |
| ------------------------- | ----------- |
| `tool_execution_start`    | 开始执行工具函数函数体 |
| `tool_execution_end`      | 工具函数函数体执行完毕 |
| `structured_answer_start` | 结构化输出开始   |
| `structured_answer_end`   | 结构化输出完毕   |


### 附件与其它块


| 事件                                    | 含义              |
| ------------------------------------- | --------------- |
| `file_start` / `file_end`             | 文件类内容块的开始与结束    |
| `compaction_start` / `compaction_end` | 上下文压缩/摘要块的开始与结束 |
| `final_output_detected`               | 检测到当前是最终输出      |


### 运行生命周期


| 事件              | 含义              |
| --------------- | --------------- |
| `run_completed` | 本轮 Agent 运行成功结束 |
| `run_failed`    | 本轮运行失败          |


## 设计原则

- 与 SDK 事件**一一对应**，不合并、不拆分、不派生新事件
- 未知 SDK 事件应显式失败，勿静默丢弃
- 适配层零业务逻辑

## 参考实现

可参考 [reference/agent_ui_adapter.py](reference/agent_ui_adapter.py)。但请注意，该文件是 **PydanticAI** 的 UI 适配器示例，展示事件重命名与字段裁剪的写法。开发时请按**具体 Agent SDK** 自行实现映射（如 Google ADK、LangChain），不要照搬其中的 `isinstance` 分支与 import。