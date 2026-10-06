from pathlib import Path
from typing import Any

import chromadb

from app.core.config import settings
from app.services.chunk_service import DocumentChunk


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
        top_k: int = 5,
        document_id: str | None = None,
    ) -> dict[str, Any]:

        where = None

        if document_id:
            where = {
                "document_id": document_id,
            }

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )

    def count(self) -> int:
        return self.collection.count()