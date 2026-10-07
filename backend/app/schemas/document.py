from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str
    knowledge_base_id: str
    filename: str
    stored_filename: str
    file_path: str
    page_count: int
    character_count: int
    chunk_count: int
    embedding_provider: str | None
    embedding_model: str | None
    status: str
    error_message: str | None
    created_at: datetime
    updated_at: datetime