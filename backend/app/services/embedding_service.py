from openai import OpenAI

from app.core.config import settings


class EmbeddingService:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.model = settings.EMBEDDING_MODEL

    def create_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )

        return [
            item.embedding
            for item in response.data
        ]

    def create_embedding(
        self,
        text: str,
    ) -> list[float]:

        embeddings = self.create_embeddings(
            [text]
        )

        return embeddings[0]