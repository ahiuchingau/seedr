from datetime import datetime, timezone
import asyncio
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status

from ...dependencies.sqlite import get_db

router = APIRouter()


def _probe_database(connection: sqlite3.Connection) -> None:
    cursor = connection.execute("SELECT 1")
    cursor.close()


@router.get("/health", tags=["health"])
async def health(connection: sqlite3.Connection = Depends(get_db)) -> dict[str, str]:
    try:
        await asyncio.to_thread(_probe_database, connection)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        ) from exc

    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}
