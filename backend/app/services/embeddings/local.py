from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.services.embeddings.base import EmbeddingProvider


class LocalEmbeddingProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self.model = SentenceTransformer(
            settings.LOCAL_EMBEDDING_MODEL
        )

    @property
    def provider_name(self) -> str:
        return "local"

    @property
    def model_name(self) -> str:
        return settings.LOCAL_EMBEDDING_MODEL

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        embeddings = self.model.encode_document(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        return embeddings.tolist()

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        embedding = self.model.encode_query(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        return embedding.tolist()