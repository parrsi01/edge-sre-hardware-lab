.PHONY: setup up down demo test status logs clean

setup:
	./scripts/macos-setup.sh

up:
	docker compose up --build -d
	./scripts/wait-ready.sh

down:
	docker compose down

demo:
	./scripts/demo.sh

test:
	docker compose build
	docker compose run --rm --no-deps control-api pytest -q
	docker compose run --rm --no-deps device /app/device-simulator --self-test

status:
	docker compose ps
	@curl -fsS http://localhost:8000/api/status | jq .

logs:
	docker compose logs -f --tail=100

clean:
	docker compose down --volumes --remove-orphans

