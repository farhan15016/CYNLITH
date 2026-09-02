from fastapi import FastAPI
from pydantic import BaseModel

from ai.cynthia import ask_cynthia
from backend.memory import load_memory, save_memory


app = FastAPI(title="Cynlith API")

conversation_history: list[dict] = load_memory()


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
    global conversation_history

    response = ask_cynthia(
        message=request.message,
        history=conversation_history,
    )

    conversation_history.append({
        "role": "user",
        "content": request.message,
    })

    conversation_history.append({
        "role": "assistant",
        "content": response,
    })

    save_memory(conversation_history)

    return ChatResponse(response=response)
