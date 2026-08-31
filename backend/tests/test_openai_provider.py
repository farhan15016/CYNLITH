"""Mocked unit tests for the OpenAI provider."""

from types import SimpleNamespace

from app.providers import openai_provider


def test_openai_provider_uses_the_responses_api(monkeypatch) -> None:
    calls: dict[str, object] = {}

    class MockResponses:
        def create(self, **kwargs: object) -> SimpleNamespace:
            calls["request"] = kwargs
            return SimpleNamespace(output_text="A triangle has three sides.")

    class MockOpenAI:
        def __init__(self, *, api_key: str) -> None:
            calls["api_key"] = api_key
            self.responses = MockResponses()

    monkeypatch.setattr(openai_provider, "OpenAI", MockOpenAI)
    provider = openai_provider.OpenAIProvider(
        api_key="test-key",
        model="test-model",
    )

    assert provider.generate("What is a triangle?") == "A triangle has three sides."
    assert calls["api_key"] == "test-key"
    assert calls["request"] == {
        "model": "test-model",
        "instructions": openai_provider.CYNLITH_SYSTEM_PROMPT,
        "input": "What is a triangle?",
    }
