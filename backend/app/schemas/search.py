from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    document_id: str

    query: str = Field(
        min_length=1,
        max_length=2000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class SearchResultResponse(BaseModel):
    page_number: int
    chunk_index: int
    text: str
    similarity: float
    accepted: bool


class SearchResponse(BaseModel):
    document_id: str
    query: str
    threshold: float
    results: list[SearchResultResponse]