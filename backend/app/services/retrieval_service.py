from dataclasses import dataclass

from app.core.config import settings
from app.core.constants import DEFAULT_KNOWLEDGE_BASE_ID
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import (
    SearchResult,
    VectorService,
)


@dataclass
class RetrievalResult:
    result: SearchResult
    accepted: bool


class RetrievalService:
    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    def search(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[SearchResult]:
        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        query_embedding = (
            self.embedding_service.embed_query(
                query
            )
        )

        results = self.vector_service.search(
            query_embedding=query_embedding,
            knowledge_base_id=(
                DEFAULT_KNOWLEDGE_BASE_ID
            ),
            top_k=top_k or settings.RAG_TOP_K,
        )

        threshold = (
            settings.RAG_SIMILARITY_THRESHOLD
        )

        return [
            result
            for result in results
            if result.similarity >= threshold
        ]

    def debug_search(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[RetrievalResult]:
        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        query_embedding = (
            self.embedding_service.embed_query(
                query
            )
        )

        results = self.vector_service.search(
            query_embedding=query_embedding,
            knowledge_base_id=(
                DEFAULT_KNOWLEDGE_BASE_ID
            ),
            top_k=top_k or settings.RAG_TOP_K,
        )

        threshold = (
            settings.RAG_SIMILARITY_THRESHOLD
        )

        return [
            RetrievalResult(
                result=result,
                accepted=(
                    result.similarity >= threshold
                ),
            )
            for result in results
        ]