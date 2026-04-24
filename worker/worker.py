import redis
import time
import os

r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    password=os.environ.get("REDIS_PASSWORD", None),
    decode_responses=True,
)


def process_job(job_id):
    print(f"Processing job {job_id}", flush=True)
    time.sleep(2)  # simulate work
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}", flush=True)


def main():
    print("Worker started, waiting for jobs...", flush=True)
    while True:
        job = r.brpop("jobs", timeout=5)
        if job:
            _, job_id = job
            process_job(job_id)


if __name__ == "__main__":
    main()
