from collections.abc import Iterator

from google import genai

from app.core.config import settings
from app.services.llms.base import LLMProvider


class GeminiLLMProvider(LLMProvider):
    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is required when LLM_PROVIDER=gemini."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_LLM_MODEL

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text

    def stream(self, prompt: str) -> Iterator[str]:
        response_stream = self.client.models.generate_content_stream(
            model=self.model,
            contents=prompt,
        )

        for chunk in response_stream:
            if chunk.text:
                yield chunk.text