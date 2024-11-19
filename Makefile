build:
	docker compose -f local.yml up --build -d --remove-orphans
up:
	docker compose -f local.yml up -d
up-no-d:
	docker compose -f local.yml up
down:
	docker compose -f local.yml down
down-v:
	docker compose -f local.yml down -v
show-logs:
	docker compose -f local.yml logs -f

show-logs-api:
	docker compose -f local.yml logs -f api

migrations:
	docker compose -f local.yml run --rm api python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm api python manage.py migrate

collect-static:
	docker compose -f local.yml run --rm api python manage.py collectstatic --not-input --clear

superuser:
	docker compose -f local.yml run --rm api python manage.py createsuperuser

db-volume:
	docker volume inspect django_estate_postgres_data

mail-volume:
	docker volume inspect django_estate_mailpit_data

estate-db:
	docker compose -f local.yml exec postgres psql --username=postgres --dbname=estate