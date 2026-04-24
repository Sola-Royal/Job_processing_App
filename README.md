# hng14-stage2-devops
# HNG14 Stage 2 — Job Processing System

A containerised job processing system built with FastAPI, Node.js, Redis, and Docker.

## Architecture

User → Frontend (Node.js :3000)
↓
API (FastAPI :8000)
↓
Redis (internal only)
↓
Worker (Python)

## Prerequisites

- Docker >= 24.0
- Docker Compose >= 2.0
- Git

## Quick Start

### 1. Clone the repository
```bash
git clone <your-fork-url>
cd hng14-stage2-devops
```

### 2. Create your environment file
```bash
cp .env.example .env
```

Edit `.env` and set a strong Redis password:

REDIS_PASSWORD=your_strong_password_here
APP_ENV=production
FRONTEND_PORT=3000

### 3. Start the stack
```bash
docker compose up --build
```

### 4. Verify it is running
Open your browser and go to:

http://localhost:3000

You should see the Job Processor Dashboard.

### 5. Test the full flow
- Click **Submit New Job**
- A job ID appears immediately with status `queued`
- After ~2 seconds the status changes to `completed`

## What a Successful Startup Looks Like

✔ Container redis     — healthy
✔ Container api       — healthy
✔ Container worker    — started
✔ Container frontend  — healthy

All four containers running, frontend accessible at `http://localhost:3000`.

## Stopping the Stack
```bash
docker compose down
```

To also remove volumes:
```bash
docker compose down -v
```

## CI/CD Pipeline

The pipeline runs automatically on every push via GitHub Actions:

| Stage | Tool | Description |
|-------|------|-------------|
| Lint | flake8, eslint, hadolint | Code and Dockerfile quality |
| Test | pytest | Unit tests with Redis mocked |
| Build | Docker Buildx | Build and push all 3 images |
| Security | Trivy | Scan for CRITICAL vulnerabilities |
| Integration | docker compose | Full stack end-to-end test |
| Deploy | Rolling update | Zero-downtime deploy to main |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_HOST` | Redis hostname | `redis` |
| `REDIS_PORT` | Redis port | `6379` |
| `REDIS_PASSWORD` | Redis password | — |
| `API_URL` | API base URL for frontend | `http://api:8000` |
| `APP_ENV` | Application environment | `production` |
| `FRONTEND_PORT` | Host port for frontend | `3000` |
