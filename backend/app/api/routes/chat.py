"""Chat endpoint for the Cynlith learning companion."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import get_settings
from app.models.chat import ChatRequest, ChatResponse
from app.providers.openai_provider import OpenAIProvider
from app.services.conversation import ConversationService

router = APIRouter(tags=["chat"])


def get_conversation_service() -> ConversationService:
    """Build the stateless conversation service for a request."""
    settings = get_settings()
    provider = OpenAIProvider(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )
    return ConversationService(provider)


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    service: Annotated[ConversationService, Depends(get_conversation_service)],
) -> ChatResponse:
    """Generate a single learning-companion reply without persistence."""
    try:
        answer = service.reply(request.message)
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chat service is not configured.",
        ) from error

    return ChatResponse(response=answer)
