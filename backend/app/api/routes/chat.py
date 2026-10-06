from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    SourceResponse,
)
from app.services.rag_service import (
    RAGService,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat_with_document(
    request: ChatRequest,
) -> ChatResponse:

    try:
        rag_service = RAGService()

        answer, search_results = (
            rag_service.answer_question(
                document_id=(
                    request.document_id
                ),
                question=request.question,
                top_k=request.top_k,
            )
        )

    except Exception as exc:
        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=str(exc),
        ) from exc

    sources = [
        SourceResponse(
            page_number=result.page_number,
            chunk_index=result.chunk_index,
            text=result.text,
            similarity=result.similarity,
        )
        for result in search_results
    ]

    return ChatResponse(
        document_id=request.document_id,
        question=request.question,
        answer=answer,
        sources=sources,
    )