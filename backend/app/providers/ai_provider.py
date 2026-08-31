"""Provider interface for text generation."""

from typing import Protocol


class AIProvider(Protocol):
    """Generate a response for a user message."""

    def generate(self, message: str) -> str:
        """Generate a text reply."""
