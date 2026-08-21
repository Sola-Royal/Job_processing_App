#!/bin/bash
set -e

TIMEOUT=60
POLL_INTERVAL=2
FRONTEND_URL="http://localhost:3000"

echo "Submitting job..."
RESPONSE=$(curl -sf --max-time 10 -X POST "${FRONTEND_URL}/submit")
echo "Response: $RESPONSE"

JOB_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "Job ID: $JOB_ID"

echo "Polling for completion (timeout: ${TIMEOUT}s)..."
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT ]; do
  STATUS=$(curl -sf --max-time 10 \
    "${FRONTEND_URL}/status/${JOB_ID}" | \
    python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "Status: $STATUS (${ELAPSED}s elapsed)"

  if [ "$STATUS" = "completed" ]; then
    echo "Job completed successfully!"
    exit 0
  fi

  sleep $POLL_INTERVAL
  ELAPSED=$((ELAPSED + POLL_INTERVAL))
done

echo "ERROR: Job did not complete within ${TIMEOUT}s"
exit 1
