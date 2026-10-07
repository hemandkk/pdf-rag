from datetime import datetime

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime


class SourceResponse(BaseModel):
    document_id: str
    filename: str
    page_number: int
    chunk_index: int
    text: str
    similarity: float


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]