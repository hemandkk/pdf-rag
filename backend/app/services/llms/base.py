from abc import ABC, abstractmethod


class LLMProviderError(Exception):
    """Raised when an LLM provider cannot generate a response."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def stream(self, prompt: str):
        raise NotImplementedError