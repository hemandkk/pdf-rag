from collections.abc import Iterator

from app.services.llms.factory import create_llm_provider


class LLMService:
    def __init__(self) -> None:
        self.provider = create_llm_provider()

    def generate(self, prompt: str) -> str:
        return self.provider.generate(prompt)

    def stream(self, prompt: str) -> Iterator[str]:
        return self.provider.stream(prompt)