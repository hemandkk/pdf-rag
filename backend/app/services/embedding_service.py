from app.services.embeddings.base import EmbeddingProvider
from app.services.embeddings.factory import (
    create_embedding_provider,
)


class EmbeddingService:
    def __init__(
        self,
        provider: EmbeddingProvider | None = None,
    ) -> None:

        self.provider = (
            provider
            if provider is not None
            else create_embedding_provider()
        )

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        return self.provider.embed_documents(
            texts
        )

    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        return self.provider.embed_query(
            text
        )