# Repository Context

## Project purpose

LiteLLM Namespace Tool Filter is a compatibility hook for LiteLLM Proxy. It removes unsupported top-level tools whose `type` is `namespace` before LiteLLM forwards a request to strict OpenAI-compatible upstream providers.

The project exists to keep requests working with providers such as NVIDIA NIM / vLLM deployments that accept classic top-level `function` tools but reject newer namespace tool groups.

## Core behavior

The hook lives in `filter_namespace_tools.py`.

Expected behavior:

- preserve standard `function` tools;
- remove top-level `namespace` tools;
- preserve unknown non-namespace tool types;
- if no tools remain, remove both `tools` and `tool_choice`;
- avoid logging or exposing request bodies and secrets.

## Important limitation

This is a filter, not a namespace translator. It does not flatten nested namespace functions and does not remap tool calls back to the client namespace format.

## Tests

Run:

```bash
pytest -q
python -m py_compile filter_namespace_tools.py
```

Tests must not require production credentials, a running LiteLLM proxy, or network access.

## Security

Never commit API keys, LiteLLM master keys, database credentials, production request payloads, or private provider configuration.

## Review priorities

PR reviews should prioritize:

1. preserving existing function-tool behavior;
2. request-shape compatibility;
3. accidental data loss from over-broad filtering;
4. secret leakage or logging;
5. tests for any behavior change;
6. keeping the hook small and provider-agnostic unless provider-specific behavior is explicitly justified.
