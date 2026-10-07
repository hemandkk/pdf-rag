from dataclasses import dataclass
from typing import Any

import chromadb

from app.core.config import settings
from app.services.chunk_service import DocumentChunk


@dataclass
class SearchResult:
    chunk_id: str
    document_id: str
    page_number: int
    chunk_index: int
    text: str
    similarity: float


class VectorService:
    COLLECTION_NAME = "pdf_documents"

    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DIR
        )

        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={
                "hnsw:space": "cosine",
            },
        )

    def add_documents(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
        knowledge_base_id: str,
    ) -> None:
        if not chunks:
            return

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match."
            )

        ids: list[str] = []
        documents: list[str] = []
        metadatas: list[dict[str, Any]] = []

        for chunk in chunks:
            ids.append(chunk.chunk_id)
            documents.append(chunk.text)

            metadatas.append(
                {
                    "knowledge_base_id": knowledge_base_id,
                    "document_id": chunk.document_id,
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index,
                }
            )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        knowledge_base_id: str,
        top_k: int,
    ) -> list[SearchResult]:
        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={
                "knowledge_base_id": knowledge_base_id,
            },
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        ids = results.get("ids")
        documents = results.get("documents")
        metadatas = results.get("metadatas")
        distances = results.get("distances")

        if (
            not ids
            or not documents
            or not metadatas
            or not distances
        ):
            return []

        result_ids = ids[0]
        result_documents = documents[0]
        result_metadatas = metadatas[0]
        result_distances = distances[0]

        search_results: list[SearchResult] = []

        for (
            chunk_id,
            text,
            metadata,
            distance,
        ) in zip(
            result_ids,
            result_documents,
            result_metadatas,
            result_distances,
            strict=True,
        ):
            if metadata is None:
                continue

            similarity = 1.0 - float(distance)

            search_results.append(
                SearchResult(
                    chunk_id=str(chunk_id),
                    document_id=str(
                        metadata["document_id"]
                    ),
                    page_number=int(
                        metadata["page_number"]
                    ),
                    chunk_index=int(
                        metadata["chunk_index"]
                    ),
                    text=str(text),
                    similarity=similarity,
                )
            )

        return search_results

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        self.collection.delete(
            where={
                "document_id": document_id,
            }
        )