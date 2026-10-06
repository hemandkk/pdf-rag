from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    document_id: str

    question: str = Field(
        min_length=1,
        max_length=2000,
    )

    top_k: int | None = Field(
        default=None,
        ge=1,
        le=10,
    )


class SourceResponse(BaseModel):
    page_number: int
    chunk_index: int
    text: str
    similarity: float


class ChatResponse(BaseModel):
    document_id: str
    question: str
    answer: str
    sources: list[SourceResponse]