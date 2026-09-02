from fastapi import FastAPI
from pydantic import BaseModel

from ai.cynthia import ask_cynthia
from backend.database import (
    init_db,
    save_message,
    get_messages,
    save_memory,
    get_memories,
)

app = FastAPI(title="Cynlith API")

init_db()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {
        "status": "ok",
        "assistant": "Cynthia"
    }


@app.post("/chat", response_model=ChatResponse)
def chat_with_cynthia(request: ChatRequest):
    history = get_messages()
    memories = get_memories()

    memory_context = "\n".join(
        f"{item['key']}: {item['value']}"
        for item in memories
    )

    enhanced_message = request.message

    if memory_context:
        enhanced_message = (
            f"Known learner information:\n{memory_context}\n\n"
            f"Learner's message:\n{request.message}"
        )

    response = ask_cynthia(
        message=enhanced_message,
        history=history,
    )

    save_message("user", request.message)
    save_message("assistant", response)

    return ChatResponse(response=response)
