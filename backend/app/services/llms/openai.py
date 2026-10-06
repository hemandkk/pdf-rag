from openai import OpenAI

from app.core.config import settings
from app.services.llms.base import (
    LLMProvider,
)


class OpenAILLMProvider(LLMProvider):
    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required "
                "when LLM_PROVIDER=openai."
            )

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.model = (
            settings.OPENAI_LLM_MODEL
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = (
            self.client.responses.create(
                model=self.model,
                input=prompt,
            )
        )

        return response.output_text