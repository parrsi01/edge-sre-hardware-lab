#!/usr/bin/env bash
set -euo pipefail

required=(brew git docker cmake jq curl colima)
missing=()
for command_name in "${required[@]}"; do
  command -v "$command_name" >/dev/null 2>&1 || missing+=("$command_name")
done

if ((${#missing[@]})); then
  echo "Missing commands: ${missing[*]}"
  echo "Install Homebrew first, then: brew install git docker docker-compose cmake jq colima"
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  colima start --cpu 2 --memory 4 --vm-type=vz
fi

echo "Development tools ready. Docker context: $(docker context show)"
docker --version
docker compose version

