.PHONY: build up down restart logs logs-api api-container migrate makemigrations createsuperuser shell celery celery-logs flower flower-logs clean prune

# ── Setup ─────────────────────────────────────────────────
build:
	docker compose build

# ── Start / Stop ──────────────────────────────────────────
up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

# ── Logs ──────────────────────────────────────────────────
logs:
	docker compose logs -f

logs-api:
	docker compose logs -f apis

api-container:
	docker compose exec -it apis /bin/bash

# ── Django management ─────────────────────────────────────
migrate:
	docker compose exec apis python manage.py migrate

makemigrations:
	docker compose exec apis python manage.py makemigrations

createsuperuser:
	docker compose exec apis python manage.py createsuperuser

shell:
	docker compose exec apis python manage.py shell_plus

# ── Celery ────────────────────────────────────────────────
celery:
	docker compose up -d celery_worker

celery-logs:
	docker compose logs -f celery_worker

flower:
	docker compose up -d flower

flower-logs:
	docker compose logs -f flower

# ── Cleanup ───────────────────────────────────────────────
clean:
	docker compose down -v --remove-orphans

prune:
	docker system prune -f
