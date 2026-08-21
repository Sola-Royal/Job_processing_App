# FIXES.md — Bug Report & Fixes

## Bug 1 — `.env` file committed to repository
- **File:** `api/.env`
- **Problem:** A real `.env` file containing `REDIS_PASSWORD=supersecretpassword123` was committed to the repository. This exposes secrets in git history and violates security best practices.
- **Fix:** Deleted `api/.env`, added `.env` to `.gitignore`, created `.env.example` with placeholder values.

## Bug 2 — API hardcodes Redis host as `localhost`
- **File:** `api/main.py`, line 8
- **Problem:** `redis.Redis(host="localhost")` — inside Docker, services cannot reach each other via `localhost`. This causes the API to fail to connect to Redis entirely.
- **Fix:** Changed to `host=os.environ.get("REDIS_HOST", "redis")` so the host is read from environment variables.

## Bug 3 — Worker hardcodes Redis host as `localhost`
- **File:** `worker/worker.py`, line 5
- **Problem:** Same issue as Bug 2 — `redis.Redis(host="localhost")` fails inside Docker containers.
- **Fix:** Changed to `host=os.environ.get("REDIS_HOST", "redis")`.

## Bug 4 — Redis password not passed to connection
- **File:** `api/main.py` line 8, `worker/worker.py` line 5
- **Problem:** The `.env` file defined `REDIS_PASSWORD` but neither the API nor the Worker passed it to the Redis connection. This causes `NOAUTH Authentication required` errors when Redis has a password set.
- **Fix:** Added `password=os.environ.get("REDIS_PASSWORD", None)` to the Redis constructor in both files.

## Bug 5 — Frontend hardcodes API URL as `localhost`
- **File:** `frontend/app.js`, line 5
- **Problem:** `const API_URL = "http://localhost:8000"` — inside Docker, the frontend container cannot reach the API container via `localhost`.
- **Fix:** Changed to `const API_URL = process.env.API_URL || "http://api:8000"` so the URL is read from environment variables.

## Bug 6 — Redis queue key mismatch between API and Worker
- **File:** `api/main.py` line 12, `worker/worker.py` line 13
- **Problem:** The API pushed jobs to a queue named `"job"` (singular) while the worker was reading from `"jobs"` (plural). Jobs were pushed but never picked up by the worker.
- **Fix:** Standardised both to use `"jobs"` as the queue key.

## Bug 7 — No decode_responses on Redis connection
- **File:** `api/main.py`, `worker/worker.py`
- **Problem:** Without `decode_responses=True`,
