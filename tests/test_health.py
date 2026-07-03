import pytest


@pytest.mark.asyncio
async def test_liveness(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_readiness(client):
    response = await client.get("/api/v1/health")
    assert response.status_code in (200, 503)
    body = response.json()
    assert "status" in body
    assert "database" in body
