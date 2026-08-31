"""Tests for public system endpoints."""

import asyncio

import httpx
from app.main import app


async def get(path: str) -> httpx.Response:
    """Make an in-process request against the ASGI application."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        return await client.get(path)


def test_root_returns_service_identity() -> None:
    response = asyncio.run(get("/"))

    assert response.status_code == 200
    assert response.json() == {"message": "Cynlith API"}


def test_health_reports_service_liveness() -> None:
    response = asyncio.run(get("/health"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
