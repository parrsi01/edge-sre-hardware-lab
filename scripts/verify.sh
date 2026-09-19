#!/usr/bin/env bash
set -euo pipefail

docker compose config --quiet
docker compose build
docker compose run --rm --no-deps control-api pytest -q
docker compose run --rm --no-deps device --self-test
docker compose up -d
./scripts/wait-ready.sh
curl -fsS http://localhost:8000/api/status | jq -e '.connected == true' >/dev/null
curl -fsS http://localhost:9090/-/ready >/dev/null
curl -fsS http://localhost:3000/api/health | jq -e '.database == "ok"' >/dev/null
echo "All local verification checks passed."
