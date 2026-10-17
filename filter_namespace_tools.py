"""LiteLLM pre-call hook for removing unsupported namespace tools.

Some OpenAI-compatible upstreams only accept top-level tools whose type is
`"function"`. Newer clients can send grouped tools whose type is `"namespace"`.
This hook removes those unsupported namespace entries before LiteLLM forwards
the request upstream, while preserving standard function tools.
"""

from typing import Any

from litellm.integrations.custom_logger import CustomLogger


def filter_namespace_tools_payload(data: dict[str, Any]) -> dict[str, Any]:
    """Remove top-level namespace tools from a LiteLLM request payload.

    The input mapping is modified in place and returned for LiteLLM hook
    compatibility.

    If every tool is removed, ``tools`` and ``tool_choice`` are removed
    together so the upstream does not receive a tool choice without tools.
    """

    tools = data.get("tools")
    if not isinstance(tools, list):
        return data

    filtered_tools = [
        tool
        for tool in tools
        if not (isinstance(tool, dict) and tool.get("type") == "namespace")
    ]

    if filtered_tools:
        data["tools"] = filtered_tools
    else:
        data.pop("tools", None)
        data.pop("tool_choice", None)

    return data


class NamespaceToolFilter(CustomLogger):
    """LiteLLM proxy callback that filters unsupported namespace tools."""

    async def async_pre_call_hook(
        self,
        user_api_key_dict: Any,
        cache: Any,
        data: dict[str, Any],
        call_type: Any,
    ) -> dict[str, Any]:
        return filter_namespace_tools_payload(data)


namespace_tool_filter = NamespaceToolFilter()
