"""Request and response schemas for chat."""

from typing import Annotated

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """A single user message for the learning companion."""

    message: Annotated[str, Field(min_length=1, max_length=4_000)]


class ChatResponse(BaseModel):
    """A single assistant reply."""

    response: str
