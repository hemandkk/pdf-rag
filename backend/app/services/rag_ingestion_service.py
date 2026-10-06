from dataclasses import dataclass

from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.pdf_service import PDFService
from app.services.vector_service import VectorService


@dataclass
class IngestionResult:
    document_id: str
    page_count: int
    character_count: int
    chunk_count: int
    text_preview: str


class RAGIngestionService:
    def __init__(self) -> None:
        self.pdf_service = PDFService()
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    def ingest_document(
        self,
        document_id: str,
        file_path: str,
    ) -> IngestionResult:

        pages = self.pdf_service.extract_pages(
            file_path
        )

        if not pages:
            raise ValueError(
                "No extractable text found in PDF."
            )

        full_text = "\n\n".join(
            page.text
            for page in pages
        )

        chunks = ChunkService.create_chunks(
            document_id=document_id,
            pages=pages,
        )

        if not chunks:
            raise ValueError(
                "No chunks were created from PDF."
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

        self.vector_service.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
        )

        return IngestionResult(
            document_id=document_id,
            page_count=len(pages),
            character_count=len(full_text),
            chunk_count=len(chunks),
            text_preview=full_text[:2000],
        )