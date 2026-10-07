from collections.abc import Iterator
import time

from google import genai
from google.genai import errors

from app.core.config import settings
from app.services.llms.base import LLMProvider, LLMProviderError


class GeminiLLMProvider(LLMProvider):
    MAX_RETRIES = 2
    RETRY_DELAY_SECONDS = 2

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is required when using Gemini."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.model = settings.GEMINI_LLM_MODEL

    def generate(self, prompt: str) -> str:
        last_error: Exception | None = None
        max_attempts = self.MAX_RETRIES + 1

        for attempt in range(1, max_attempts + 1):
            print(
                f"[Gemini] Sending request "
                f"(attempt {attempt}/{max_attempts})"
            )

            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                if not response.text:
                    raise LLMProviderError(
                        "Gemini returned an empty response."
                    )

                print(
                    f"[Gemini] Request succeeded "
                    f"on attempt {attempt}/{max_attempts}"
                )

                return response.text

            except errors.APIError as exc:
                last_error = exc

                status_code = getattr(exc, "code", None)

                print(
                    f"[Gemini] API error on attempt "
                    f"{attempt}/{max_attempts}: "
                    f"{status_code} - {exc}"
                )

                retryable_status_codes = {
                    429,
                    500,
                    502,
                    503,
                    504,
                }

                if status_code not in retryable_status_codes:
                    raise LLMProviderError(
                        f"Gemini API error: {exc}",
                        status_code=status_code,
                    ) from exc

                if attempt == max_attempts:
                    print(
                        "[Gemini] Maximum retry attempts reached."
                    )
                    break

                delay = self.RETRY_DELAY_SECONDS * (
                    2 ** (attempt - 1)
                )

                print(
                    f"[Gemini] Retrying in {delay} seconds..."
                )

                time.sleep(delay)

            except LLMProviderError:
                raise

            except Exception as exc:
                print(
                    f"[Gemini] Unexpected error: {exc}"
                )

                raise LLMProviderError(
                    "An unexpected error occurred while "
                    "communicating with Gemini."
                ) from exc

        raise LLMProviderError(
            "Gemini is temporarily unavailable after "
            f"{max_attempts} attempts. "
            "Please try again in a few moments.",
            status_code=503,
        ) from last_error

    def stream(self, prompt: str) -> Iterator[str]:
        print("[Gemini] stream() entered")
        print(
            "[Gemini] Calling generate_content_stream..."
        )

        try:
            response_stream = (
                self.client.models.generate_content_stream(
                    model=self.model,
                    contents=prompt,
                )
            )

            print(
                "[Gemini] generate_content_stream returned"
            )

            chunk_count = 0

            for chunk in response_stream:
                chunk_count += 1

                print(
                    f"[Gemini] Received chunk #{chunk_count}"
                )

                if chunk.text:
                    print(
                        "[Gemini] Chunk text:",
                        repr(chunk.text),
                    )

                    yield chunk.text

                else:
                    print(
                        f"[Gemini] Chunk #{chunk_count} "
                        "contained no text"
                    )

            print(
                f"[Gemini] Stream completed. "
                f"Total chunks: {chunk_count}"
            )

        except errors.APIError as exc:
            status_code = getattr(exc, "code", None)

            print(
                f"[Gemini] Streaming API error: "
                f"{status_code} - {exc}"
            )

            raise LLMProviderError(
                "Gemini is temporarily unavailable. "
                "Please try again in a few moments.",
                status_code=status_code,
            ) from exc

        except Exception as exc:
            print(
                "[Gemini] Streaming unexpected error:",
                repr(exc),
            )

            raise LLMProviderError(
                "An unexpected error occurred while "
                "communicating with Gemini."
            ) from exc