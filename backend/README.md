# Seedr Backend

FastAPI service that manages hydroponic scheduling data using SQLite as the primary datastore.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) for dependency and virtualenv management

## Setup

```bash
cd backend
make setup
```

`make setup` provisions a `.venv` via `uv` and installs runtime plus developer dependencies. The application will create the SQLite database file on first use.

## Running the API

```bash
make run
```

The API will boot with a health endpoint at `GET /api/v1/health`.

## Maintenance Commands

- `make test` — run the pytest suite.
- `make lint` — execute Ruff checks.
- `make format` — apply Ruff formatting.
- `make teardown` — remove the virtual environment.
- `make clean` — delete Python cache directories.

## Configuration

Environment variables can be placed in a `.env` file in the `backend` directory.

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `APP_ENV` | `development` | Identifies deployment environment |
| `APP_NAME` | `Seedr Hydroponics Scheduler` | Display name for the service |
| `API_V1_PREFIX` | `/api/v1` | Prefix for versioned API routes |
| `SQLITE_DB_PATH` | `seedr.db` | Path to the SQLite database file |
| `SCHEDULER_TIMEZONE` | `UTC` | Default timezone for scheduled tasks |
| `REMINDER_LEAD_MINUTES` | `60` | Default minutes before events to trigger reminders |

The default SQLite database lives alongside the codebase; point `SQLITE_DB_PATH` elsewhere for production deployments.

## Next Steps

- Flesh out domain models for seed batches, tasks, and events.
- Implement background scheduling and reminder delivery services.
- Introduce authentication once multi-user needs arise.
