from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=8000)
    session_id: UUID | None = None
    user_id: UUID | None = None


class Source(BaseModel):
    id: UUID
    title: str
    source: str | None = None


class ChatResponse(BaseModel):
    answer: str
    session_id: UUID
    sources: list[Source]
    latency_ms: int
    model: str
