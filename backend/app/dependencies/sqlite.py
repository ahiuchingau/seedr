from __future__ import annotations

import sqlite3
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request

from ..core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.db = None
    try:
        yield
    finally:
        connection: sqlite3.Connection | None = getattr(app.state, "db", None)
        if connection is not None:
            connection.close()


async def get_db(request: Request) -> sqlite3.Connection:
    connection: sqlite3.Connection | None = getattr(request.app.state, "db", None)
    if connection is None:
        settings = get_settings()
        db_path = Path(settings.sqlite_db_path).expanduser()
        db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(db_path, check_same_thread=False)
        connection.execute("PRAGMA foreign_keys=ON;").close()
        request.app.state.db = connection
    return connection
