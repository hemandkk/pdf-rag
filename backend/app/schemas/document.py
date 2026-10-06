from datetime import datetime

from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    page_count: int
    character_count: int
    chunk_count: int
    status: str
    text_preview: str


class DocumentResponse(BaseModel):
    id: str
    filename: str
    page_count: int
    character_count: int
    chunk_count: int
    embedding_provider: str
    embedding_model: str
    status: str
    error_message: str | None
    created_at: datetime
    updated_at: datetime


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]