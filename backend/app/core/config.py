from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "PDF RAG API"
    APP_VERSION: str = "1.0.0"

    UPLOAD_DIR: str = "uploads"
    VECTOR_DB_DIR: str = "chroma"

    MAX_FILE_SIZE_MB: int = 20

    OPENAI_API_KEY: str
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()