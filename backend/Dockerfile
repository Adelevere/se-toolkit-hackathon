# Stage 1: build
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

COPY backend/pyproject.toml /app/backend/pyproject.toml
COPY backend/src /app/backend/src

RUN pip install --no-cache-dir --prefix=/install -r /app/backend/pyproject.toml 2>/dev/null || \
    pip install --no-cache-dir --prefix=/install \
      fastapi uvicorn[standard] openai pydantic pydantic-settings httpx

# Stage 2: final
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

COPY --from=builder --chown=nonroot:nonroot /install /usr/local

COPY --chown=nonroot:nonroot backend/src /app/src

USER nonroot
WORKDIR /app

ENV PYTHONPATH=/app/src

CMD ["uvicorn", "ai_planner.main:app", "--host", "0.0.0.0", "--port", "8000"]
