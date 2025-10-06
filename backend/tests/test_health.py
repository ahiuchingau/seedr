import os
import django
import pytest
from httpx import ASGITransport, AsyncClient

from seedr.asgi import application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seedr.settings")
django.setup()


@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "timestamp" in body


@pytest.mark.asyncio
async def test_root_endpoint():
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Seedr backend is running"
    assert payload["docs_url"] == "/api/v1/docs"
    assert payload["health_url"] == "/api/v1/health"
