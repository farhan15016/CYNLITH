from fastapi import FastAPI
from pydantic import BaseModel

from ai.cynthia import ask_cynthia
from backend.memory import add_memory, get_history

app = FastAPI(title="Cynlith API")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {"status": "ok", "assistant": "Cynthia"}


@app.post("/chat", response_model=ChatResponse)
def chat_with_cynthia(request: ChatRequest):
    history = get_history()

    response = ask_cynthia(
        message=request.message,
        history=history,
    )

    add_memory("user", request.message)
    add_memory("assistant", response)

    return ChatResponse(response=response)
