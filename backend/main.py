from fastapi import FastAPI
from pydantic import BaseModel

from ai.cynthia import ask_cynthia


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
    response = ask_cynthia(request.message)
    return ChatResponse(response=response)
