import pytest
from httpx import ASGITransport, AsyncClient

from app.dependencies.redis import get_redis
from app.main import app


class DummyRedis:
    async def ping(self) -> bool:  # pragma: no cover - trivial
        return True


@pytest.mark.asyncio
async def test_health_endpoint():
    async def override_get_redis():
        return DummyRedis()

    app.dependency_overrides[get_redis] = override_get_redis

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    app.dependency_overrides.pop(get_redis, None)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "timestamp" in body


@pytest.mark.asyncio
async def test_root_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Seedr backend is running"
    assert payload["docs_url"] == "/docs"
    assert payload["health_url"].endswith("/health")
