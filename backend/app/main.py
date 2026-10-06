from fastapi import FastAPI

from app.api.routes.chat import (
    router as chat_router,
)
from app.api.routes.documents import (
    router as documents_router,
)
from app.api.routes.search import (
    router as search_router,
)
from app.core.config import settings
from app.db.database import Base
from app.db.database import engine
from app.db.models import Document


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


app.include_router(
    documents_router,
    prefix="/api/v1",
)

app.include_router(
    chat_router,
    prefix="/api/v1",
)

app.include_router(
    search_router,
    prefix="/api/v1",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "PDF RAG API is running",
    }