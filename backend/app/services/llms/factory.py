from app.core.config import settings
from app.services.llms.base import LLMProvider
from app.services.llms.gemini import (
    GeminiLLMProvider,
)
from app.services.llms.openai import (
    OpenAILLMProvider,
)


def create_llm_provider() -> LLMProvider:
    provider = settings.LLM_PROVIDER.lower()

    if provider == "openai":
        return OpenAILLMProvider()

    if provider == "gemini":
        return GeminiLLMProvider()

    raise ValueError(
        f"Unsupported LLM provider: {provider}. "
        "Supported providers: openai, gemini."
    )