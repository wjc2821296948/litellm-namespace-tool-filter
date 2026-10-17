FROM docker.litellm.ai/berriai/litellm:main-stable

LABEL org.opencontainers.image.source="https://github.com/wjc2821296948/litellm-namespace-tool-filter"
LABEL org.opencontainers.image.description="LiteLLM with the namespace tool compatibility hook preinstalled"
LABEL org.opencontainers.image.licenses="Apache-2.0"

COPY filter_namespace_tools.py /app/filter_namespace_tools.py
