# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_CACHE_DIR=/root/.cache/pip

# Install system dependencies
RUN apt-get update --yes \
    && apt-get install --yes --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

FROM base AS builder

# Copy only requirements for dependency install
COPY --link requirements.txt ./

# Create venv and install dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv .venv \
    && .venv/bin/pip install --upgrade pip \
    && .venv/bin/pip install -r requirements.txt

# Copy application code
COPY --link . .

FROM base AS final

# Create non-root user
RUN useradd -m appuser
USER appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
# Copy application code from builder
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
