from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=50,
    )


class SearchResultResponse(BaseModel):
    document_id: str
    page_number: int
    chunk_index: int
    text: str
    similarity: float
    accepted: bool


class SearchResponse(BaseModel):
    query: str
    threshold: float
    results: list[SearchResultResponse]