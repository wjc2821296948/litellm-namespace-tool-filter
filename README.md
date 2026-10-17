# LiteLLM Namespace Tool Filter

[![Tests](https://github.com/wjc2821296948/litellm-namespace-tool-filter/actions/workflows/tests.yml/badge.svg)](https://github.com/wjc2821296948/litellm-namespace-tool-filter/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

[English](README.en.md) | [中文](README.md)

一个轻量的 LiteLLM pre-call hook：过滤上游不支持的顶层 `namespace` 工具，同时保留标准 `function` 工具。

它适用于 OpenAI Codex 这类客户端已经开始发送分组工具定义，而上游 OpenAI 兼容提供商仍只接受传统 function tools 的场景。

## 问题背景

客户端请求可能包含：

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

部分严格校验工具结构的 NVIDIA NIM / vLLM 部署会在模型实际收到请求之前直接拒绝第二项：

```text
Input should be 'function'
input: 'namespace'
```

典型调用链：

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

这个 hook 只处理顶层工具列表：

```text
function     -> 保留
namespace    -> 删除
其他类型     -> 保留
```

如果过滤后一个工具都不剩，会同时移除 `tool_choice`，避免向上游发送“指定工具但没有 tools”的请求。

## 安装

把 `filter_namespace_tools.py` 放到 LiteLLM 能导入的位置。

Docker 部署可以同时挂载 hook 与 LiteLLM 配置：

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

然后在 `config.yaml` 中启用 callback：

```yaml
litellm_settings:
  drop_params: true
  callbacks:
    - filter_namespace_tools.namespace_tool_filter
```

修改后重启 LiteLLM。

完整示例见 [examples](examples/) 目录。

## NVIDIA NIM 示例

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

API Key 建议通过环境变量提供，不要直接提交到仓库：

```bash
export NVIDIA_API_KEY="..."
```

## 会过滤哪些内容？

这个过滤器**不会全局禁用 tool calling**。普通 function tools 仍然会被保留。

它只删除顶层结构为：

```json
{
  "type": "namespace"
}
```

的工具对象。

在当前 Codex 构建中，常见例子包括：

- `multi_agent_v1`：子 Agent 管理工具组，例如创建、发送消息、等待、恢复和关闭 Agent。
- `mcp__node_repl`：JavaScript / Node REPL 工具组。

这些 namespace 被过滤后，上游模型暂时无法使用对应的分组能力，但标准顶层 function tools 仍可正常使用。

## 重要限制

本项目是**兼容性过滤器**，不是 namespace-to-function 转换器。

它会主动丢弃不兼容的 namespace 工具组，不会：

- 把 namespace 内的函数展开成独立 function；
- 把上游的 tool call 再映射回客户端期望的 namespace 调用格式。

未来可以通过“双向 namespace 展平 + tool-call 反向映射”保留这些能力，但这已经超出单纯请求过滤的范围。

## 适用范围

适用于以下 LiteLLM Proxy 场景：

1. 客户端发送 `type: "namespace"` 工具；
2. 上游只接受 `type: "function"` 工具；
3. 与其让整个请求直接 400，不如暂时舍弃 namespace 工具组。

本项目不绑定某一个模型。

## 测试

仓库包含过滤行为的单元测试：

```bash
python -m pip install pytest
pytest -q
```

测试不需要正在运行的 LiteLLM Proxy，也不需要 NVIDIA API Key。

## 安全

不要提交 Provider API Key、LiteLLM master key、数据库密码或包含真实密钥的生产 `config.yaml`。

示例配置刻意使用环境变量引用。

## 许可证

Apache License 2.0，详见 [LICENSE](LICENSE)。
