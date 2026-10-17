# Security

## Secrets

Do not commit production LiteLLM configuration files if they contain secrets.

Keep provider API keys, LiteLLM master keys, database credentials, and other tokens in environment variables or a dedicated secret manager.

The files under `examples/` intentionally reference environment variables instead of real credentials.

## Reporting a vulnerability

If you find a security issue in this repository, please avoid posting credentials, tokens, private request payloads, or other sensitive data in a public issue.

Open an issue containing only the minimum non-sensitive reproduction details needed to describe the problem.
