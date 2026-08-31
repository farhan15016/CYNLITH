"""Stateless orchestration for a single conversation turn."""

from app.providers.ai_provider import AIProvider


class ConversationService:
    """Delegate a learner message to the configured AI provider."""

    def __init__(self, provider: AIProvider) -> None:
        self._provider = provider

    def reply(self, message: str) -> str:
        """Return the provider's reply for one user message."""
        return self._provider.generate(message)
