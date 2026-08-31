"""Mocked tests for the chat endpoint and service."""

import asyncio

import httpx

from app.api.routes.chat import get_conversation_service
from app.main import app
from app.services.conversation import ConversationService


class MockAIProvider:
    """Deterministic provider used to keep tests offline."""

    def __init__(self, reply: str) -> None:
        self.reply_text = reply
        self.messages: list[str] = []

    def generate(self, message: str) -> str:
        self.messages.append(message)
        return self.reply_text


async def post_chat(payload: dict[str, str]) -> httpx.Response:
    """Make an in-process request against the ASGI application."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        return await client.post("/chat", json=payload)


def test_conversation_service_delegates_to_provider() -> None:
    provider = MockAIProvider("A fraction is part of a whole.")
    service = ConversationService(provider)

    assert service.reply("What is a fraction?") == "A fraction is part of a whole."
    assert provider.messages == ["What is a fraction?"]


def test_chat_returns_mocked_provider_reply() -> None:
    provider = MockAIProvider("Photosynthesis converts light into chemical energy.")
    service = ConversationService(provider)
    app.dependency_overrides[get_conversation_service] = lambda: service

    try:
        response = asyncio.run(post_chat({"message": "What is photosynthesis?"}))
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "response": "Photosynthesis converts light into chemical energy."
    }


def test_chat_rejects_an_empty_message() -> None:
    response = asyncio.run(post_chat({"message": ""}))

    assert response.status_code == 422
