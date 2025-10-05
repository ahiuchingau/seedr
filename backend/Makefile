UV := uv
VENV := .venv
.PHONY: setup install run test lint format teardown clean

setup: install ## Create virtualenv and install dependencies

install: clean teardown
	$(UV) venv
	$(UV) pip install -e .[dev]

run:
	$(UV) run uvicorn app.main:app --reload

test:
	$(UV) run pytest

lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff format .

teardown:
	rm -rf $(VENV)

clean:
	$(UV) cache clean
