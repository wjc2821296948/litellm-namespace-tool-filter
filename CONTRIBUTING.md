# 贡献指南

[English](CONTRIBUTING_en.md) | [中文](CONTRIBUTING.md)

感谢您对 LiteLLM Namespace Tool Filter 的关注。

## 可以贡献什么

欢迎以下类型的贡献：

- Bug 修复
- LiteLLM / Provider 兼容性改进
- 测试用例
- 文档与示例
- namespace 展平或双向映射方案的设计讨论

## 开始之前

请先确认：

1. 已阅读 [README](README.md) 与 [行为准则](CODE_OF_CONDUCT.md)。
2. 不要提交真实 API Key、LiteLLM master key、数据库密码或生产配置。
3. 尽量保持改动小而集中，一个 PR 只解决一个主题。

## 本地开发

```bash
git clone https://github.com/wjc2821296948/litellm-namespace-tool-filter.git
cd litellm-namespace-tool-filter

python -m pip install pytest
pytest -q
```

当前测试不要求运行中的 LiteLLM 或真实 Provider Key。

## 分支命名

建议使用：

```text
feat/<name>
fix/<name>
docs/<name>
test/<name>
chore/<name>
```

## 提交信息

建议遵循 Conventional Commits：

```text
feat(filter): add provider-specific mode
fix(filter): remove tool_choice when tools are empty
docs(readme): clarify NVIDIA NIM setup
test(filter): cover mixed tool payloads
```

保持每次提交职责单一，方便审查与回滚。

## Pull Request

PR 描述建议包含：

- 改了什么
- 为什么需要修改
- 如何验证
- 是否改变现有过滤行为
- 是否影响普通 `function` tools
- 是否涉及安全或兼容性风险

提交前请运行：

```bash
pytest -q
python -m py_compile filter_namespace_tools.py
```

## 兼容性原则

默认目标是：

- 保留标准 `function` tools；
- 只处理明确不兼容的 `namespace` tools；
- 不静默改写未知工具类型；
- 不在过滤器中记录请求正文、Key 或其他敏感数据。

如果 PR 改变这些原则，请在描述中明确说明。

## 安全问题

安全问题请按照 [SECURITY.md](SECURITY.md) 私下报告，不要在公开 Issue 中发布密钥或敏感请求内容。

## 许可证

提交贡献即表示您同意相关贡献在 Apache License 2.0 下发布。
