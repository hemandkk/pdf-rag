from collections.abc import Iterator

from openai import OpenAI

from app.core.config import settings
from app.services.llms.base import LLMProvider


class OpenAILLMProvider(LLMProvider):
    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai."
            )

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.model = settings.OPENAI_LLM_MODEL

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        if not response.output_text:
            raise RuntimeError(
                "OpenAI returned an empty response."
            )

        return response.output_text

    def stream(self, prompt: str) -> Iterator[str]:
        response_stream = self.client.responses.create(
            model=self.model,
            input=prompt,
            stream=True,
        )

        for event in response_stream:
            if event.type == "response.output_text.delta":
                if event.delta:
                    yield event.delta