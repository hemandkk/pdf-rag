from dataclasses import dataclass

from app.repositories.document_repository import DocumentRepository
from app.services.vector_service import SearchResult


@dataclass
class EnrichedSource:
    document_id: str
    filename: str
    page_number: int
    chunk_index: int
    text: str
    similarity: float


class SourceEnrichmentService:
    def __init__(
        self,
        document_repository: DocumentRepository,
    ) -> None:
        self.document_repository = document_repository

    def enrich(
        self,
        results: list[SearchResult],
    ) -> list[EnrichedSource]:
        if not results:
            return []

        document_ids = list(
            dict.fromkeys(
                result.document_id
                for result in results
            )
        )

        documents = self.document_repository.get_by_ids(
            document_ids
        )

        documents_by_id = {
            document.id: document
            for document in documents
        }

        enriched_sources: list[EnrichedSource] = []

        for result in results:
            document = documents_by_id.get(result.document_id)

            if document is None:
                continue

            enriched_sources.append(
                EnrichedSource(
                    document_id=result.document_id,
                    filename=document.filename,
                    page_number=result.page_number,
                    chunk_index=result.chunk_index,
                    text=result.text,
                    similarity=result.similarity,
                )
            )

        return enriched_sources