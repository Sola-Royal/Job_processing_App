# ── Build stage ──────────────────────────────────────────────
FROM python:3.11-alpine AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip==26.2.1 setuptools==84.0.0 wheel==0.48.0 && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Final stage ──────────────────────────────────────────────
FROM python:3.11-alpine

RUN addgroup -S -g 1000 appgroup && adduser -S -u 1000 appuser -G appgroup

WORKDIR /app

COPY --from=builder /install /usr/local

COPY worker.py .

RUN chown -R appuser:appgroup /app

USER 1000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD ["sh", "-c", "python -c \"import os; os.kill(1, 0)\" || exit 1"]

CMD ["python", "worker.py"]
