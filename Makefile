.PHONY: up down logs seed test restart ps clean

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

seed:
	docker compose exec backend python -m app.scripts.seed

test:
	docker compose exec backend pytest -q

restart:
	docker compose restart backend worker frontend

ps:
	docker compose ps

clean:
	docker compose down -v