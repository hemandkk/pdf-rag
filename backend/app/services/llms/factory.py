from app.core.config import settings
from app.services.llms.base import LLMProvider


def create_llm_provider() -> LLMProvider:
    provider = settings.LLM_PROVIDER.lower()

    if provider == "openai":
        from app.services.llms.openai import OpenAILLMProvider

        return OpenAILLMProvider()

    if provider == "gemini":
        from app.services.llms.gemini import GeminiLLMProvider

        return GeminiLLMProvider()

    raise ValueError(
        f"Unsupported LLM provider: {provider}. "
        "Supported providers: openai, gemini."
    )