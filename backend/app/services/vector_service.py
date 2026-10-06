from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb

from app.core.config import settings
from app.services.chunk_service import DocumentChunk


@dataclass
class SearchResult:
    text: str
    document_id: str
    page_number: int
    chunk_index: int
    similarity: float


class VectorService:
    COLLECTION_NAME = "pdf_documents"

    def __init__(self) -> None:
        vector_db_path = Path(
            settings.VECTOR_DB_DIR
        )

        vector_db_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(vector_db_path)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                metadata={
                    "hnsw:space": "cosine",
                },
            )
        )

    def add_chunks(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:

        if not chunks:
            return

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match "
                "number of embeddings."
            )

        self.collection.add(
            ids=[
                chunk.chunk_id
                for chunk in chunks
            ],
            embeddings=embeddings,
            documents=[
                chunk.text
                for chunk in chunks
            ],
            metadatas=[
                {
                    "document_id": chunk.document_id,
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index,
                }
                for chunk in chunks
            ],
        )

    def search(
        self,
        query_embedding: list[float],
        document_id: str,
        top_k: int = 5,
    ) -> list[SearchResult]:

        results: dict[str, Any] = (
            self.collection.query(
                query_embeddings=[
                    query_embedding
                ],
                n_results=top_k,
                where={
                    "document_id": document_id,
                },
                include=[
                    "documents",
                    "metadatas",
                    "distances",
                ],
            )
        )

        documents = results.get(
            "documents"
        )

        metadatas = results.get(
            "metadatas"
        )

        distances = results.get(
            "distances"
        )

        if (
            not documents
            or not metadatas
            or not distances
        ):
            return []

        search_results: list[
            SearchResult
        ] = []

        for text, metadata, distance in zip(
            documents[0],
            metadatas[0],
            distances[0],
            strict=True,
        ):
            search_results.append(
                SearchResult(
                    text=text,
                    document_id=str(
                        metadata[
                            "document_id"
                        ]
                    ),
                    page_number=int(
                        metadata[
                            "page_number"
                        ]
                    ),
                    chunk_index=int(
                        metadata[
                            "chunk_index"
                        ]
                    ),
                    similarity=1.0 - float(distance),
                )
            )

        return search_results

    def count(self) -> int:
        return self.collection.count()