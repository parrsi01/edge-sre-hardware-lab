#!/usr/bin/env bash
set -euo pipefail

for attempt in {1..60}; do
  if curl -fsS http://localhost:8000/readyz >/dev/null 2>&1 \
    && curl -fsS http://localhost:9090/-/ready >/dev/null 2>&1 \
    && curl -fsS http://localhost:3000/api/health | jq -e '.database == "ok"' >/dev/null 2>&1; then
    echo "Edge SRE Lab is ready: http://localhost:8000"
    exit 0
  fi
  sleep 1
done

echo "The stack did not become ready within 60 seconds." >&2
docker compose ps >&2
exit 1
