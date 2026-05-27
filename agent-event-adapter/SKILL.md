---
name: agent-event-ui-adapter
description: Correctly designs provider-agnostic agent event adapter for UI consumption.
disable-model-invocation: true
---

# Agent Event Adapter

将 Agent SDK 的流式事件**重命名 + 裁字段**后透传给前端。

## 适配器只做两件事

1. **重命名**：SDK 事件名晦涩（如 `PartStartEvent`、`FunctionToolCallEvent`），改为前端渲染直觉的名称（如 `text_start`、`tool_execution_start`）
2. **裁字段**：SDK 事件载荷字段多而杂，只透传 UI 需要的字段

**不做**事件聚合、重组、拆分、转换、业务逻辑注入。适配器中的事件与 SDK 事件**一一对应**，只是名字不同、字段更少。

## 事件语义（命名习惯 `{语义}_{phase}`）

### 文本与推理

| 事件 | 含义 |
|------|------|
| `text_start` | 助手回复文本块开始 |
| `text_delta` | 回复文本增量 |
| `text_end` | 回复文本块结束 |
| `reasoning_start` | 模型思考/推理块开始 |
| `reasoning_delta` | 思考内容增量 |
| `reasoning_end` | 思考块结束 |

### 工具调用（参数流）

模型在生成工具调用参数时的流式片段（尚未执行）。

| 事件 | 含义 |
|------|------|
| `toolcall_start` | 普通工具调用参数块开始 |
| `toolcall_delta` | 工具名/参数 JSON 增量 |
| `toolcall_end` | 普通工具调用参数块结束 |
| `native_toolcall_start` | 内置/原生工具调用参数块开始 |
| `native_toolcall_delta` | 原生工具调用参数增量 |
| `native_toolcall_end` | 原生工具调用参数块结束 |

### 工具执行与结果

实际执行工具或收到返回时发出（与上面的参数流阶段区分）。

| 事件 | 含义 |
|------|------|
| `tool_execution_start` | 开始执行 function 类工具 |
| `tool_execution_end` | function 工具执行结束 |
| `tool_result_start` | output 类工具调用开始 |
| `tool_result_end` | output 类工具结果就绪 |
| `native_tool_execution_start` | 开始执行内置工具 |
| `native_tool_execution_end` | 内置工具执行结束 |
| `native_toolresult_start` | 原生工具返回块开始 |
| `native_toolresult_end` | 原生工具返回块结束 |

### 附件与其它块

| 事件 | 含义 |
|------|------|
| `file_start` / `file_end` | 文件类内容块的开始与结束 |
| `compaction_start` / `compaction_end` | 上下文压缩/摘要块的开始与结束 |
| `final_result_ready` | 结构化最终结果已就绪（尚非整轮结束） |

### 运行生命周期

| 事件 | 含义 |
|------|------|
| `run_completed` | 本轮 Agent 运行成功结束 |
| `run_failed` | 本轮运行失败 |

## 设计原则

- 与 SDK 事件**一一对应**，不合并、不拆分、不派生新事件
- 未知 SDK 事件应显式失败，勿静默丢弃
- 适配层零业务逻辑

## 参考实现

可参考 [reference/agent_ui_adapter.py](reference/agent_ui_adapter.py)。但请注意，该文件是 **PydanticAI** 的 UI 适配器示例，展示事件重命名与字段裁剪的写法。开发时请按**具体 Agent SDK** 自行实现映射（如 Google ADK、LangChain），不要照搬其中的 `isinstance` 分支与 import。
