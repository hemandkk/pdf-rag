import json
from collections.abc import Iterator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session


from app.services.llms.base import LLMProviderError
from app.db.database import get_db
from app.repositories.document_repository import DocumentRepository
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService
from app.services.retrieval_service import RetrievalService
from app.services.source_enrichment_service import (
    SourceEnrichmentService,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


retrieval_service = RetrievalService()
llm_service = LLMService()


def create_rag_service(
    db: Session,
) -> RAGService:
    document_repository = DocumentRepository(db)

    source_enrichment_service = SourceEnrichmentService(
        document_repository=document_repository,
    )

    return RAGService(
        retrieval_service=retrieval_service,
        llm_service=llm_service,
        source_enrichment_service=source_enrichment_service,
    )


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
) -> ChatResponse:
    rag_service = create_rag_service(db)

    try:
        return rag_service.chat(
            question=request.question,
            top_k=request.top_k,
        )

    except LLMProviderError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


@router.post("/stream")
def chat_stream(
    request: ChatRequest,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    rag_service = create_rag_service(db)

    sources, token_stream = rag_service.stream(
        question=request.question,
        top_k=request.top_k,
    )

    def event_stream() -> Iterator[str]:
        try:
            for token in token_stream:
                payload = json.dumps(
                    {"text": token},
                    ensure_ascii=False,
                )

                yield (
                    "event: token\n"
                    f"data: {payload}\n\n"
                )

            sources_payload = json.dumps(
                {
                    "sources": [
                        source.model_dump()
                        for source in sources
                    ]
                },
                ensure_ascii=False,
            )

            yield (
                "event: sources\n"
                f"data: {sources_payload}\n\n"
            )

            yield (
                "event: done\n"
                "data: {}\n\n"
            )

        except Exception as exc:
            error_payload = json.dumps(
                {"message": str(exc)},
                ensure_ascii=False,
            )

            yield (
                "event: error\n"
                f"data: {error_payload}\n\n"
            )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )