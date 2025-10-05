UV := uv
VENV := .venv
REDIS_CONTAINER := seedr-redis
REDIS_IMAGE := redis:7
REDIS_CONFIG := $(CURDIR)/redis/redis.conf
REDIS_DATA := $(CURDIR)/.redis-data

.PHONY: setup install run test lint format teardown clean redis-up redis-down redis-logs

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

redis-up:
	mkdir -p $(REDIS_DATA)
	docker rm -f $(REDIS_CONTAINER) >/dev/null 2>&1 || true
	docker run -d \
		--name $(REDIS_CONTAINER) \
		-p 6379:6379 \
		-v $(REDIS_CONFIG):/usr/local/etc/redis/redis.conf:ro \
		-v $(REDIS_DATA):/data \
		$(REDIS_IMAGE) redis-server /usr/local/etc/redis/redis.conf

redis-down: 
	docker stop $(REDIS_CONTAINER) >/dev/null 2>&1 || true

redis-logs:
	docker logs -f $(REDIS_CONTAINER)

teardown:
	rm -rf $(VENV)

clean:
	$(UV) cache clean