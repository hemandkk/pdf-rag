import json
from collections.abc import Iterator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.conversation import (
    ConversationCreate,
    ConversationDetailResponse,
    ConversationResponse,
)
from app.services.conversation_service import (
    ConversationService,
)
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService
from app.services.retrieval_service import (
    RetrievalService,
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


def get_conversation_service(
    db: Session = Depends(get_db),
) -> ConversationService:
    retrieval_service = RetrievalService()
    llm_service = LLMService()

    rag_service = RAGService(
        retrieval_service=retrieval_service,
        llm_service=llm_service,
    )

    return ConversationService(
        db=db,
        rag_service=rag_service,
    )


@router.post(
    "",
    response_model=ConversationResponse,
)
def create_conversation(
    request: ConversationCreate,
    service: ConversationService = Depends(
        get_conversation_service
    ),
) -> ConversationResponse:
    try:
        return service.create(
            title=request.title,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[ConversationResponse],
)
def list_conversations(
    service: ConversationService = Depends(
        get_conversation_service
    ),
) -> list[ConversationResponse]:
    return service.list_all()


@router.get(
    "/{conversation_id}",
    response_model=ConversationDetailResponse,
)
def get_conversation(
    conversation_id: str,
    service: ConversationService = Depends(
        get_conversation_service
    ),
) -> ConversationDetailResponse:
    conversation = service.get_detail(
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return conversation


@router.post(
    "/{conversation_id}/messages/stream"
)
def stream_message(
    conversation_id: str,
    question: str,
    top_k: int = 5,
    service: ConversationService = Depends(
        get_conversation_service
    ),
) -> StreamingResponse:
    try:
        sources, token_stream = (
            service.stream_message(
                conversation_id=conversation_id,
                question=question,
                top_k=top_k,
            )
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

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