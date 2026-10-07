from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.core.constants import (
    DEFAULT_KNOWLEDGE_BASE_ID,
)
from app.db.models.document import Document
from app.repositories.document_repository import (
    DocumentRepository,
)
from app.repositories.knowledge_base_repository import (
    KnowledgeBaseRepository,
)
from app.services.rag_ingestion_service import (
    RagIngestionService,
)


class DocumentService:
    def __init__(
        self,
        document_repository: DocumentRepository,
        knowledge_base_repository: KnowledgeBaseRepository,
        rag_ingestion_service: RagIngestionService,
    ) -> None:
        self.document_repository = (
            document_repository
        )

        self.knowledge_base_repository = (
            knowledge_base_repository
        )

        self.rag_ingestion_service = (
            rag_ingestion_service
        )

    def upload(
        self,
        file: UploadFile,
    ) -> Document:
        knowledge_base = (
            self.knowledge_base_repository.get_by_id(
                DEFAULT_KNOWLEDGE_BASE_ID
            )
        )

        if knowledge_base is None:
            raise ValueError(
                "Default knowledge base does not exist."
            )

        self._validate_pdf(file)

        document_id = str(uuid4())

        original_filename = (
            file.filename
            or "document.pdf"
        )

        stored_filename = (
            f"{document_id}.pdf"
        )

        upload_directory = Path(
            settings.UPLOAD_DIR
        )

        upload_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = (
            upload_directory
            / stored_filename
        )

        with file_path.open(
            "wb"
        ) as output_file:
            while True:
                chunk = file.file.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                output_file.write(chunk)

        document = Document(
            id=document_id,
            knowledge_base_id=(
                DEFAULT_KNOWLEDGE_BASE_ID
            ),
            filename=original_filename,
            stored_filename=stored_filename,
            file_path=str(file_path),
            page_count=0,
            character_count=0,
            chunk_count=0,
            embedding_provider=None,
            embedding_model=None,
            status="processing",
            error_message=None,
        )

        document = (
            self.document_repository.create(
                document
            )
        )

        try:
            self.rag_ingestion_service.ingest(
                document
            )

        except Exception as exc:
            document.status = "failed"
            document.error_message = str(exc)

            self.document_repository.update(
                document
            )

            raise

        return document

    def list_all(
        self,
    ) -> list[Document]:
        knowledge_base = (
            self.knowledge_base_repository.get_by_id(
                DEFAULT_KNOWLEDGE_BASE_ID
            )
        )

        if knowledge_base is None:
            raise ValueError(
                "Default knowledge base does not exist."
            )

        return (
            self.document_repository
            .get_by_knowledge_base(
                DEFAULT_KNOWLEDGE_BASE_ID
            )
        )

    def get(
        self,
        document_id: str,
    ) -> Document:
        document = (
            self.document_repository.get_by_id(
                document_id
            )
        )

        if document is None:
            raise ValueError(
                "Document not found."
            )

        if (
            document.knowledge_base_id
            != DEFAULT_KNOWLEDGE_BASE_ID
        ):
            raise ValueError(
                "Document does not belong "
                "to the default knowledge base."
            )

        return document

    @staticmethod
    def _validate_pdf(
        file: UploadFile,
    ) -> None:
        filename = (
            file.filename
            or ""
        )

        content_type = (
            file.content_type
            or ""
        )

        if not filename.lower().endswith(
            ".pdf"
        ):
            raise ValueError(
                "Only PDF files are supported."
            )

        if content_type not in {
            "application/pdf",
            "application/octet-stream",
            "",
        }:
            raise ValueError(
                "Uploaded file must be a PDF."
            )