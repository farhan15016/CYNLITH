from fastapi import FastAPI
from pydantic import BaseModel
from ollama import chat

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
    result = chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Cynthia, the AI learning companion for Cynlith. "
                    "Explain concepts clearly, encourage curiosity, and help "
                    "the learner understand rather than simply giving answers."
                ),
            },
            {
                "role": "user",
                "content": request.message,
            },
        ],
    )

    return ChatResponse(response=result["message"]["content"])
