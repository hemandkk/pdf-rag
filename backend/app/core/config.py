from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "PDF RAG API"
    APP_VERSION: str = "1.0.0"
    CHROMA_DIR: str = "chroma"
    UPLOAD_DIR: str = "uploads"
    VECTOR_DB_DIR: str = "chroma"

    DATABASE_URL: str = "sqlite:///./rag.db"

    MAX_FILE_SIZE_MB: int = 20

    # -------------------------
    #  RAG configuration - Similarity threshold
    # -------------------------
    RAG_TOP_K: int = 5
    RAG_SIMILARITY_THRESHOLD: float = 0.20

    # -------------------------
    # Embedding configuration
    # -------------------------

    EMBEDDING_PROVIDER: str = "local"

    LOCAL_EMBEDDING_MODEL: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    OPENAI_EMBEDDING_MODEL: str = (
        "text-embedding-3-small"
    )

    # -------------------------
    # LLM configuration
    # -------------------------

    LLM_PROVIDER: str = "gemini"

    OPENAI_API_KEY: str | None = None

    OPENAI_LLM_MODEL: str = "gpt-6-luna"

    GEMINI_API_KEY: str | None = None

    GEMINI_LLM_MODEL: str = "gemini-3.8-flash"

    # -------------------------
    # RAG configuration
    # -------------------------

    RAG_TOP_K: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()