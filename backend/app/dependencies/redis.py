from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from redis.asyncio import Redis

from ..core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.redis = None
    try:
        yield
    finally:
        redis: Redis | None = getattr(app.state, "redis", None)
        if redis is not None:
            await redis.close()


async def get_redis(request: Request) -> Redis:
    redis: Redis | None = getattr(request.app.state, "redis", None)
    if redis is None:
        settings = get_settings()
        redis = Redis.from_url(settings.redis_url, decode_responses=True)
        request.app.state.redis = redis
    return redis
