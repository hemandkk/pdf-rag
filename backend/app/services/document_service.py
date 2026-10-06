from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models.document import Document
from app.repositories.document_repository import (
    DocumentRepository,
)


class DocumentService:
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.repository = (
            DocumentRepository(db)
        )

    def create_processing_document(
        self,
        document_id: str,
        filename: str,
        stored_filename: str,
        file_path: str,
    ) -> Document:

        document = Document(
            id=document_id,
            filename=filename,
            stored_filename=stored_filename,
            file_path=file_path,
            embedding_provider=(
                settings.EMBEDDING_PROVIDER
            ),
            embedding_model=(
                self._get_embedding_model()
            ),
            status="processing",
        )

        return self.repository.create(
            document
        )

    def mark_ready(
        self,
        document: Document,
        page_count: int,
        character_count: int,
        chunk_count: int,
    ) -> Document:

        document.page_count = page_count
        document.character_count = (
            character_count
        )
        document.chunk_count = chunk_count
        document.status = "ready"
        document.error_message = None

        return self.repository.update(
            document
        )

    def mark_failed(
        self,
        document: Document,
        error_message: str,
    ) -> Document:

        document.status = "failed"
        document.error_message = (
            error_message
        )

        return self.repository.update(
            document
        )

    def get_by_id(
        self,
        document_id: str,
    ) -> Document | None:

        return self.repository.get_by_id(
            document_id
        )

    def list_all(
        self,
    ) -> list[Document]:

        return self.repository.list_all()

    @staticmethod
    def _get_embedding_model() -> str:

        provider = (
            settings.EMBEDDING_PROVIDER.lower()
        )

        if provider == "local":
            return (
                settings.LOCAL_EMBEDDING_MODEL
            )

        if provider == "openai":
            return (
                settings.OPENAI_EMBEDDING_MODEL
            )

        return "unknown"