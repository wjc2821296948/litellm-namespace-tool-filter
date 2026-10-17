# Security Policy

[English](SECURITY_en.md) | [中文](SECURITY.md)

## Supported versions

Security fixes are provided for the latest version on the `main` branch.

| Version | Supported |
|---|---|
| `main` | Yes |
| Older revisions | No |

## Reporting a vulnerability

Please **do not** disclose suspected vulnerabilities, credentials, provider tokens, private request payloads, or production configuration in a public issue or pull request.

Preferred reporting path:

1. Open the repository **Security** tab.
2. Choose **Report a vulnerability**.
3. Provide the minimum information needed to reproduce and assess the issue.

If private vulnerability reporting is unavailable, contact the maintainer at `admin@lrate.top`.

## Sensitive data

This project is designed to transform request metadata in LiteLLM. Reports may therefore involve request bodies or provider configuration. Before sharing logs or examples:

- remove API keys and bearer tokens;
- remove LiteLLM master keys;
- remove database credentials;
- remove private hostnames and internal addresses when they are not required;
- minimize request payloads to the smallest safe reproduction.

## Security expectations

The hook should:

- avoid logging request bodies or secrets;
- preserve unrelated tool definitions;
- avoid executing tool content;
- avoid fetching remote code or data;
- make only the minimum request mutation required for compatibility.

## Disclosure

Please allow maintainers reasonable time to investigate and prepare a fix before public disclosure.

## Thanks

Thank you to everyone who reports security issues responsibly.
