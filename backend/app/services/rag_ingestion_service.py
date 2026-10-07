from app.db.models.document import Document
from app.repositories.document_repository import (
    DocumentRepository,
)
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.pdf_service import PDFService
from app.services.vector_service import VectorService


class RagIngestionService:
    def __init__(
        self,
        pdf_service: PDFService,
        chunk_service: ChunkService,
        embedding_service: EmbeddingService,
        vector_service: VectorService,
        document_repository: DocumentRepository,
    ) -> None:
        self.pdf_service = pdf_service
        self.chunk_service = chunk_service
        self.embedding_service = embedding_service
        self.vector_service = vector_service
        self.document_repository = document_repository

    def ingest(
        self,
        document: Document,
    ) -> Document:
        pages = self.pdf_service.extract_pages(
            document.file_path
        )

        document.page_count = len(pages)

        document.character_count = sum(
            len(page.text)
            for page in pages
        )

        chunks = self.chunk_service.create_chunks(
            document_id=document.id,
            pages=pages,
        )

        document.chunk_count = len(chunks)

        if not chunks:
            document.status = "failed"
            document.error_message = (
                "No text could be extracted "
                "from the PDF."
            )

            self.document_repository.update(
                document
            )

            raise ValueError(
                "No text could be extracted "
                "from the PDF."
            )

        texts = [
            chunk.text
            for chunk in chunks
        ]

        embeddings = (
            self.embedding_service.embed_documents(
                texts
            )
        )

        document.embedding_provider = (
            self.embedding_service.provider_name
        )

        document.embedding_model = (
            self.embedding_service.model_name
        )

        self.vector_service.add_documents(
            chunks=chunks,
            embeddings=embeddings,
            knowledge_base_id=(
                document.knowledge_base_id
            ),
        )

        document.status = "completed"
        document.error_message = None

        self.document_repository.update(
            document
        )

        return document