from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    page_count: int
    character_count: int
    text_preview: str