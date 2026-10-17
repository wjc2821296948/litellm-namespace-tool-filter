import importlib
import sys
import types


def _load_module():
    """Load the hook without installing LiteLLM by stubbing CustomLogger."""

    litellm = types.ModuleType("litellm")
    integrations = types.ModuleType("litellm.integrations")
    custom_logger = types.ModuleType("litellm.integrations.custom_logger")

    class CustomLogger:
        pass

    custom_logger.CustomLogger = CustomLogger

    sys.modules["litellm"] = litellm
    sys.modules["litellm.integrations"] = integrations
    sys.modules["litellm.integrations.custom_logger"] = custom_logger

    sys.modules.pop("filter_namespace_tools", None)
    return importlib.import_module("filter_namespace_tools")


def test_preserves_function_tools_and_removes_namespace_tools():
    module = _load_module()
    payload = {
        "tools": [
            {"type": "function", "name": "read_file"},
            {"type": "namespace", "name": "multi_agent_v1", "tools": []},
            {"type": "function", "name": "shell"},
        ]
    }

    result = module.filter_namespace_tools_payload(payload)

    assert result["tools"] == [
        {"type": "function", "name": "read_file"},
        {"type": "function", "name": "shell"},
    ]


def test_removes_tools_and_tool_choice_when_all_tools_are_namespaces():
    module = _load_module()
    payload = {
        "tools": [{"type": "namespace", "name": "mcp__node_repl", "tools": []}],
        "tool_choice": "auto",
    }

    result = module.filter_namespace_tools_payload(payload)

    assert "tools" not in result
    assert "tool_choice" not in result


def test_leaves_payload_without_list_tools_unchanged():
    module = _load_module()
    payload = {"tools": None, "model": "example"}

    result = module.filter_namespace_tools_payload(payload)

    assert result == {"tools": None, "model": "example"}


def test_preserves_unknown_non_namespace_tool_types():
    module = _load_module()
    payload = {"tools": [{"type": "custom", "name": "future_tool"}]}

    result = module.filter_namespace_tools_payload(payload)

    assert result["tools"] == [{"type": "custom", "name": "future_tool"}]
