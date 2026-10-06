from app.services.llms.base import (
    LLMProvider,
)
from app.services.llms.factory import (
    create_llm_provider,
)


class LLMService:
    def __init__(
        self,
        provider: LLMProvider | None = None,
    ) -> None:

        self.provider = (
            provider
            if provider is not None
            else create_llm_provider()
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        return self.provider.generate(
            prompt
        )