from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis

from ...dependencies.redis import get_redis

router = APIRouter()


@router.get("/health", tags=["health"])
async def health(redis: Redis = Depends(get_redis)) -> dict[str, str]:
    try:
        await redis.ping()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis connection failed",
        ) from exc

    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}
