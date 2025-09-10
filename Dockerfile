# ---- Base image
FROM python:3.11-slim AS base

# Avoid interactive prompts, speed up pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---- Install Python deps first (better layer caching)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---- Copy app code
COPY app ./app

# ---- Runtime env (override in deploy)
ENV APP_ENV=prod \
    DATABASE_URL="" \
    JWT_SECRET="change-me"

# ---- Expose & default command (uvicorn, multi-worker)
EXPOSE 8000
# OLD
# CMD ["uvicorn", "app.main:app", \
#      "--host", "0.0.0.0", "--port", "8000", \
#      "--workers", "2", "--proxy-headers", "--forwarded-allow-ips", "*"]

# NEW (shell form so ${PORT} works; defaults to 8000)
CMD ["/bin/sh","-c","uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers ${UVICORN_WORKERS:-2} --proxy-headers --forwarded-allow-ips '*'"]
