# Contributing Guide

[English](CONTRIBUTING_en.md) | [中文](CONTRIBUTING.md)

Thank you for your interest in LiteLLM Namespace Tool Filter.

## Ways to contribute

Contributions are welcome in areas such as:

- Bug fixes
- LiteLLM or provider compatibility improvements
- Tests
- Documentation and examples
- Design work for namespace flattening or bidirectional tool-call mapping

## Before you start

Please:

1. Read the [README](README.en.md) and [Code of Conduct](CODE_OF_CONDUCT.md).
2. Never commit real API keys, LiteLLM master keys, database credentials, or production configuration.
3. Keep each pull request focused on one topic whenever possible.

## Local development

```bash
git clone https://github.com/wjc2821296948/litellm-namespace-tool-filter.git
cd litellm-namespace-tool-filter

python -m pip install pytest
pytest -q
```

The current test suite does not require a running LiteLLM proxy or real provider credentials.

## Branch naming

Recommended patterns:

```text
feat/<name>
fix/<name>
docs/<name>
test/<name>
chore/<name>
```

## Commit messages

Conventional Commits are recommended:

```text
feat(filter): add provider-specific mode
fix(filter): remove tool_choice when tools are empty
docs(readme): clarify NVIDIA NIM setup
test(filter): cover mixed tool payloads
```

Keep commits small and single-purpose to make review and rollback easier.

## Pull requests

A useful PR description should explain:

- What changed
- Why the change is needed
- How it was verified
- Whether filtering behavior changes
- Whether standard `function` tools are affected
- Any security or compatibility risk

Before submitting, run:

```bash
pytest -q
python -m py_compile filter_namespace_tools.py
```

## Compatibility principles

The default goals are to:

- Preserve standard `function` tools.
- Handle only explicitly incompatible `namespace` tools.
- Avoid silently rewriting unknown tool types.
- Avoid logging request bodies, credentials, or other sensitive data.

If a pull request changes these principles, call it out clearly in the PR description.

## Security issues

Follow [SECURITY_en.md](SECURITY_en.md) for private security reporting. Do not post credentials or sensitive request payloads in public issues.

## License

By contributing, you agree that your contribution may be distributed under the Apache License 2.0.
