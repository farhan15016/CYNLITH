"""OpenAI Responses API implementation of the AI provider."""

from openai import OpenAI

from app.providers.ai_provider import AIProvider

CYNLITH_SYSTEM_PROMPT = (
    "You are Cynlith, a supportive learning companion. Help learners understand "
    "concepts through clear, accurate explanations. Encourage curiosity, ask a "
    "brief clarifying question when needed, and use examples that fit the learner's "
    "question. Do not claim to have completed work the learner must do."
)


class OpenAIProvider(AIProvider):
    """Generate learning-companion replies with the OpenAI Responses API."""

    def __init__(self, *, api_key: str | None, model: str) -> None:
        self._api_key = api_key
        self._model = model

    def generate(self, message: str) -> str:
        """Generate a reply from the configured OpenAI model."""
        if not self._api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")

        client = OpenAI(api_key=self._api_key)
        response = client.responses.create(
            model=self._model,
            instructions=CYNLITH_SYSTEM_PROMPT,
            input=message,
        )
        if not response.output_text:
            raise RuntimeError("OpenAI returned no output text")

        return response.output_text
