import pytest
from httpx import ASGITransport, AsyncClient

from app.dependencies.sqlite import get_db
from app.main import app


class DummyCursor:
    def close(self) -> None:  # pragma: no cover - trivial
        return None


class DummyConnection:
    def execute(self, query: str) -> DummyCursor:  # pragma: no cover - trivial
        return DummyCursor()


@pytest.mark.asyncio
async def test_health_endpoint():
    async def override_get_db():
        return DummyConnection()

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    app.dependency_overrides.pop(get_db, None)

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
