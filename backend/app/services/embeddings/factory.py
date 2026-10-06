from app.core.config import settings
from app.services.embeddings.base import EmbeddingProvider
from app.services.embeddings.local import (
    LocalEmbeddingProvider,
)
from app.services.embeddings.openai import (
    OpenAIEmbeddingProvider,
)


def create_embedding_provider() -> EmbeddingProvider:
    provider = settings.EMBEDDING_PROVIDER.lower()

    if provider == "local":
        return LocalEmbeddingProvider()

    if provider == "openai":
        return OpenAIEmbeddingProvider()

    raise ValueError(
        f"Unsupported embedding provider: {provider}. "
        "Supported providers: local, openai."
    )