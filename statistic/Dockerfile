FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
LABEL authors="Dmitry"

RUN apt-get update && \
    apt-get install -y \
    bash \
    nano \
    curl

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ENV UV_TOOL_BIN_DIR=/usr/local/bin

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY .. /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT []

CMD ["granian", "statistic_app.main:app", "--interface", "asgi", "--port", "8003", "--host", "0.0.0.0", "--reload"]
