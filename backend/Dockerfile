# Stage 1: build Python deps
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

COPY backend/pyproject.toml /app/backend/pyproject.toml
COPY backend/src /app/backend/src

# Force reinstall to ensure all deps are installed
RUN pip install --no-cache-dir --prefix=/install --force-reinstall -r /app/backend/pyproject.toml 2>/dev/null || \
    pip install --no-cache-dir --prefix=/install --force-reinstall \
      fastapi uvicorn[standard] openai pydantic pydantic-settings httpx psycopg2-binary sqlmodel

# Stage 2: final
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Install Node.js and Qwen CLI via npm
RUN apt-get update && apt-get install -y curl gnupg git && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g @qwen-code/qwen-code@latest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder --chown=root:root /install /usr/local

COPY --chown=root:root backend/src /app/src

WORKDIR /app

ENV PYTHONPATH=/app/src
# Add npm global bin to PATH
ENV PATH="/usr/local/lib/node_modules/.bin:$PATH"

CMD ["uvicorn", "ai_planner.main:app", "--host", "0.0.0.0", "--port", "8000"]
