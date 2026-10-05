from fastapi import FastAPI

from app.api.routes.documents import router as documents_router
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


app.include_router(
    documents_router,
    prefix="/api/v1",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "PDF RAG API is running",
    }