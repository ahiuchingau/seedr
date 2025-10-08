UV := uv
VENV := .venv
.PHONY: setup install run test lint format migrate teardown clean shell docker-build docker-up docker-down docker-logs docker-shell docker-migrate docker-makemigrations

setup: install ## Create virtualenv and install dependencies

install: clean teardown
	$(UV) venv
	$(UV) pip install -e .[dev]

run:
	$(UV) run python manage.py runserver

shell:
	$(UV) run python manage.py shell

test:
	$(UV) run pytest

lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff format .

migrate:
	$(UV) run python manage.py migrate

teardown:
	rm -rf $(VENV)

clean:
	$(UV) cache clean

# Docker targets
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-shell:
	docker-compose exec web python manage.py shell

docker-migrate:
	docker-compose exec web python manage.py migrate

docker-makemigrations:
	docker-compose exec web python manage.py makemigrations
