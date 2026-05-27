from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, ConfigDict
from pydantic_ai import AgentRunResultEvent
from pydantic_ai.messages import (
    BuiltinToolCallEvent,
    BuiltinToolResultEvent,
    CompactionPart,
    FilePart,
    FinalResultEvent,
    FunctionToolCallEvent,
    FunctionToolResultEvent,
    NativeToolCallPart,
    NativeToolReturnPart,
    OutputToolCallEvent,
    OutputToolResultEvent,
    PartDeltaEvent,
    PartEndEvent,
    PartStartEvent,
    TextPart,
    TextPartDelta,
    ThinkingPart,
    ThinkingPartDelta,
    ToolCallPart,
    ToolCallPartDelta,
)


AgentAdapterEventType = Literal[
    "text_start",
    "text_delta",
    "text_end",
    "reasoning_start",
    "reasoning_delta",
    "reasoning_end",
    "toolcall_start",
    "toolcall_delta",
    "toolcall_end",
    "native_toolcall_start",
    "native_toolcall_delta",
    "native_toolcall_end",
    "native_toolresult_start",
    "native_toolresult_end",
    "file_start",
    "file_end",
    "compaction_start",
    "compaction_end",
    "final_result_ready",
    "tool_execution_start",
    "tool_execution_end",
    "tool_result_start",
    "tool_result_end",
    "native_tool_execution_start",
    "native_tool_execution_end",
    "run_completed",
    "run_failed",
]


class AgentAdapterEvent(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: AgentAdapterEventType
    part_index: Optional[int] = None
    text: Optional[str] = None
    text_delta: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_name: Optional[str] = None
    tool_name_delta: Optional[str] = None
    args: Optional[Any] = None
    args_delta: Optional[Any] = None
    content: Optional[Any] = None
    args_valid: Optional[bool] = None
    output: Optional[Any] = None
    message: Optional[str] = None
    message_history_json: Optional[str] = None


def adapt_agent_event(event: object) -> AgentAdapterEvent:
    if isinstance(event, PartStartEvent):
        return _adapt_part_start_event(event=event)
    if isinstance(event, PartDeltaEvent):
        return _adapt_part_delta_event(event=event)
    if isinstance(event, PartEndEvent):
        return _adapt_part_end_event(event=event)
    if isinstance(event, FinalResultEvent):
        return AgentAdapterEvent(
            type="final_result_ready",
            tool_call_id=event.tool_call_id,
            tool_name=event.tool_name,
        )
    if isinstance(event, FunctionToolCallEvent):
        return AgentAdapterEvent(
            type="tool_execution_start",
            tool_call_id=event.tool_call_id,
            tool_name=event.part.tool_name,
            args=event.part.args,
            args_valid=event.args_valid,
        )
    if isinstance(event, FunctionToolResultEvent):
        return AgentAdapterEvent(
            type="tool_execution_end",
            tool_call_id=event.tool_call_id,
            tool_name=getattr(event.part, "tool_name", None),
            content=getattr(event.part, "content", None),
        )
    if isinstance(event, OutputToolCallEvent):
        return AgentAdapterEvent(
            type="tool_result_start",
            tool_call_id=event.tool_call_id,
            tool_name=event.part.tool_name,
            args=event.part.args,
            args_valid=event.args_valid,
        )
    if isinstance(event, OutputToolResultEvent):
        return AgentAdapterEvent(
            type="tool_result_end",
            tool_call_id=event.tool_call_id,
            tool_name=getattr(event.part, "tool_name", None),
            content=getattr(event.part, "content", None),
        )
    if isinstance(event, BuiltinToolCallEvent):
        return AgentAdapterEvent(
            type="native_tool_execution_start",
            tool_call_id=event.part.tool_call_id,
            tool_name=event.part.tool_name,
            args=event.part.args,
        )
    if isinstance(event, BuiltinToolResultEvent):
        return AgentAdapterEvent(
            type="native_tool_execution_end",
            tool_call_id=event.result.tool_call_id,
            tool_name=event.result.tool_name,
            content=event.result.content,
        )
    if isinstance(event, AgentRunResultEvent):
        raw_message_history_json = event.result.all_messages_json()
        return AgentAdapterEvent(
            type="run_completed",
            output=event.result.output,
            message_history_json=raw_message_history_json.decode()
            if isinstance(raw_message_history_json, bytes)
            else raw_message_history_json,
        )
    raise TypeError(f"Unsupported agent event: {type(event).__name__}")


def adapt_agent_error(error: BaseException) -> AgentAdapterEvent:
    return AgentAdapterEvent(
        type="run_failed",
        message=str(error),
    )


def _adapt_part_start_event(event: PartStartEvent) -> AgentAdapterEvent:
    part = event.part
    if isinstance(part, TextPart):
        return AgentAdapterEvent(type="text_start", part_index=event.index, text=part.content)
    if isinstance(part, ThinkingPart):
        return AgentAdapterEvent(type="reasoning_start", part_index=event.index, text=part.content)
    if isinstance(part, NativeToolCallPart):
        return AgentAdapterEvent(
            type="native_toolcall_start",
            part_index=event.index,
            tool_call_id=part.tool_call_id,
            tool_name=part.tool_name,
            args=part.args,
        )
    if isinstance(part, ToolCallPart):
        return AgentAdapterEvent(
            type="toolcall_start",
            part_index=event.index,
            tool_call_id=part.tool_call_id,
            tool_name=part.tool_name,
            args=part.args,
        )
    if isinstance(part, NativeToolReturnPart):
        return AgentAdapterEvent(
            type="native_toolresult_start",
            part_index=event.index,
            tool_call_id=part.tool_call_id,
            tool_name=part.tool_name,
            content=part.content,
        )
    if isinstance(part, FilePart):
        return AgentAdapterEvent(type="file_start", part_index=event.index, content=part.content)
    if isinstance(part, CompactionPart):
        return AgentAdapterEvent(type="compaction_start", part_index=event.index, text=part.content)
    raise TypeError(f"Unsupported part start event: {type(part).__name__}")


def _adapt_part_delta_event(event: PartDeltaEvent) -> AgentAdapterEvent:
    delta = event.delta
    if isinstance(delta, TextPartDelta):
        return AgentAdapterEvent(type="text_delta", part_index=event.index, text_delta=delta.content_delta)
    if isinstance(delta, ThinkingPartDelta):
        return AgentAdapterEvent(type="reasoning_delta", part_index=event.index, text_delta=delta.content_delta)
    if isinstance(delta, ToolCallPartDelta):
        return AgentAdapterEvent(
            type="toolcall_delta",
            part_index=event.index,
            tool_call_id=delta.tool_call_id,
            tool_name_delta=delta.tool_name_delta,
            args_delta=delta.args_delta,
        )
    raise TypeError(f"Unsupported part delta event: {type(delta).__name__}")


def _adapt_part_end_event(event: PartEndEvent) -> AgentAdapterEvent:
    part = event.part
    if isinstance(part, TextPart):
        return AgentAdapterEvent(type="text_end", part_index=event.index, text=part.content)
    if isinstance(part, ThinkingPart):
        return AgentAdapterEvent(type="reasoning_end", part_index=event.index, text=part.content)
    if isinstance(part, NativeToolCallPart):
        return AgentAdapterEvent(
            type="native_toolcall_end",
            part_index=event.index,
            tool_call_id=part.tool_call_id,
            tool_name=part.tool_name,
            args=part.args,
        )
    if isinstance(part, ToolCallPart):
        return AgentAdapterEvent(
            type="toolcall_end",
            part_index=event.index,
            tool_call_id=part.tool_call_id,
            tool_name=part.tool_name,
            args=part.args,
        )
    if isinstance(part, NativeToolReturnPart):
        return AgentAdapterEvent(
            type="native_toolresult_end",
            part_index=event.index,
            tool_call_id=part.tool_call_id,
            tool_name=part.tool_name,
            content=part.content,
        )
    if isinstance(part, FilePart):
        return AgentAdapterEvent(type="file_end", part_index=event.index, content=part.content)
    if isinstance(part, CompactionPart):
        return AgentAdapterEvent(type="compaction_end", part_index=event.index, text=part.content)
    raise TypeError(f"Unsupported part end event: {type(part).__name__}")
