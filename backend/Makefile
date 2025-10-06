UV := uv
VENV := .venv
.PHONY: setup install run test lint format migrate teardown clean shell

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
