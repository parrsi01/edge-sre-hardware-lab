#!/usr/bin/env bash
set -euo pipefail

base_url="http://localhost:8000"
curl -fsS "$base_url/readyz" >/dev/null

echo "1/4 Healthy system"
curl -fsS "$base_url/api/status" | jq '{connected, availability_percent, latest_sample}'

echo "2/4 Injecting a controlled device fault"
curl -fsS -X POST "$base_url/api/fault" -H 'Content-Type: application/json' -d '{"enabled":true}' | jq .
sleep 3
curl -fsS "$base_url/api/status" | jq '{connected, device_status, last_error}'

echo "3/4 Recovering the device"
curl -fsS -X POST "$base_url/api/fault" -H 'Content-Type: application/json' -d '{"enabled":false}' | jq .
sleep 3
curl -fsS "$base_url/readyz" | jq .

echo "4/4 Demonstration complete"
curl -fsS "$base_url/api/status" | jq '{connected, availability_percent, polls_successful, polls_total}'
echo "Dashboard: http://localhost:8000"
echo "Grafana:   http://localhost:3000/d/edge-sre-lab"

