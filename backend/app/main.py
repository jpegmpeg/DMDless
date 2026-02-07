from datetime import datetime
from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.dm_engine import format_dm_reply

app = FastAPI(title="DMDless API", version="0.1.0")


class ChatMessage(BaseModel):
    player_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    reply: str
    timestamp: str
    conversation_id: str


class ConversationState:
    def __init__(self) -> None:
        self.history: Dict[str, List[str]] = {}

    def record(self, conversation_id: str, line: str) -> None:
        self.history.setdefault(conversation_id, []).append(line)

    def summarize(self, conversation_id: str) -> str:
        lines = self.history.get(conversation_id, [])
        if not lines:
            return "No prior context."
        return " ".join(lines[-4:])


state = ConversationState()


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage) -> ChatResponse:
    conversation_id = f"party-{message.player_id}"
    state.record(conversation_id, f"Player {message.player_id}: {message.message}")
    context = state.summarize(conversation_id)
    reply = format_dm_reply(message.message, context)
    state.record(conversation_id, reply)
    return ChatResponse(
        reply=reply,
        timestamp=datetime.utcnow().isoformat() + "Z",
        conversation_id=conversation_id,
    )
