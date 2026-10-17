# LiteLLM Namespace Tool Filter

[![Tests](https://github.com/wjc2821296948/litellm-namespace-tool-filter/actions/workflows/tests.yml/badge.svg)](https://github.com/wjc2821296948/litellm-namespace-tool-filter/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

[English](README.en.md) | [中文](README.md)

A small LiteLLM pre-call hook that removes unsupported top-level `namespace` tools while preserving standard `function` tools.

It is useful when a client such as OpenAI Codex sends newer grouped tool definitions, but the upstream OpenAI-compatible provider accepts only classic function tools.

## Codex with LiteLLM and NVIDIA NIM

This project was originally created to solve a tool-schema compatibility problem in the **OpenAI Codex -> LiteLLM -> NVIDIA NIM** request path.

When Codex uses LiteLLM as a custom OpenAI-compatible endpoint and LiteLLM forwards the model request to NVIDIA NIM / vLLM, Codex may send grouped tools with `type: "namespace"`, such as `multi_agent_v1` or `mcp__node_repl`. Some NVIDIA NIM / vLLM endpoints accept only classic `type: "function"` tools, so the forwarded request can fail with errors such as:

```text
litellm.BadRequestError: Nvidia_nimException
Input should be 'function'
Field required: function
```

With this pre-call hook enabled, LiteLLM removes incompatible namespace tools before the request reaches NVIDIA NIM while preserving ordinary function tools. This allows Codex to continue using the upstream model instead of failing the entire request.

Typical path:

```text
Codex
  -> LiteLLM /v1/responses
  -> LiteLLM conversion and forwarding
  -> NVIDIA NIM / vLLM /v1/chat/completions
```

If Codex works through LiteLLM but NVIDIA NIM returns `Nvidia_nimException`, `Input should be 'function'`, or `input: 'namespace'`, this filter directly targets that compatibility issue.

## The problem

A request may contain tools like:

```json
{
  "tools": [
    {
      "type": "function",
      "name": "read_file"
    },
    {
      "type": "namespace",
      "name": "multi_agent_v1",
      "tools": [
        {
          "type": "function",
          "name": "spawn_agent"
        }
      ]
    }
  ]
}
```

Strict upstreams such as some NVIDIA NIM / vLLM deployments can reject the second entry before the model is called:

```text
Input should be 'function'
input: 'namespace'
```

Typical request path:

```text
OpenAI Codex
    |
    v
LiteLLM
    |
    v
NVIDIA NIM / vLLM
    |
    X 400 validation error
```

This hook changes only the top-level tool list:

```text
function     -> preserved
namespace    -> removed
other values -> preserved
```

If all tools are removed, the hook also removes `tool_choice` so LiteLLM does not forward a tool selection without any tools.

## Installation

Copy `filter_namespace_tools.py` somewhere LiteLLM can import it.

For a Docker deployment, mount both the hook and your LiteLLM config:

```yaml
services:
  litellm:
    image: docker.litellm.ai/berriai/litellm:main-stable
    volumes:
      - ./config.yaml:/app/config.yaml:ro
      - ./filter_namespace_tools.py:/app/filter_namespace_tools.py:ro
    command:
      - "--config=/app/config.yaml"
```

Then enable the callback in `config.yaml`:

```yaml
litellm_settings:
  drop_params: true
  callbacks:
    - filter_namespace_tools.namespace_tool_filter
```

Restart LiteLLM after changing the configuration.

A complete example is available in the [examples](examples/) directory.

## Example with NVIDIA NIM

```yaml
model_list:
  - model_name: gpt-oss-20b
    litellm_params:
      model: nvidia_nim/openai/gpt-oss-20b
      api_base: https://integrate.api.nvidia.com/v1
      api_key: os.environ/NVIDIA_API_KEY

litellm_settings:
  drop_params: true
  callbacks:
    - filter_namespace_tools.namespace_tool_filter
```

Store the API key in an environment variable instead of committing it:

```bash
export NVIDIA_API_KEY="..."
```

## What is filtered?

The filter does **not** disable tool calling globally. Standard function tools remain available.

It removes only top-level objects whose schema contains:

```json
{
  "type": "namespace"
}
```

In current Codex builds, examples can include grouped tool namespaces such as:

- `multi_agent_v1` — sub-agent management tools such as spawning, messaging, waiting for, resuming, and closing agents.
- `mcp__node_repl` — grouped JavaScript / Node REPL tools.

Those grouped capabilities are unavailable to the upstream model after filtering, while normal top-level function tools can still be used.

## Important limitation

This project is a compatibility filter, not a namespace-to-function translator.

It deliberately **drops** unsupported namespace groups. It does not flatten nested functions and it does not translate tool calls back into the namespace format expected by the client.

A future compatibility layer could preserve those capabilities by implementing bidirectional namespace flattening and tool-call remapping, but that requires more than a request-side filter.

## Scope

This hook is designed for LiteLLM Proxy deployments where:

1. the client sends `type: "namespace"` tool definitions;
2. the upstream only accepts `type: "function"` tool definitions; and
3. dropping grouped namespace tools is preferable to rejecting the entire request.

It is not specific to a single model.

## Testing

The repository includes unit tests for the filtering behavior:

```bash
python -m pip install pytest
pytest -q
```

The tests do not require a running LiteLLM proxy or an NVIDIA API key.

## Security

Do not commit provider API keys, LiteLLM master keys, database credentials, or production `config.yaml` files.

The example configuration uses environment-variable references intentionally.

## License

Apache License 2.0. See [LICENSE](LICENSE).
