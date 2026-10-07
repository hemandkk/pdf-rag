from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from app.core.config import settings
from app.schemas.search import (
    SearchRequest,
    SearchResponse,
    SearchResultResponse,
)
from app.services.retrieval_service import (
    RetrievalService,
)


router = APIRouter(
    prefix="/documents",
    tags=["Search"],
)


@router.post(
    "/search",
    response_model=SearchResponse,
)
def search_documents(
    request: SearchRequest,
) -> SearchResponse:
    try:
        retrieval_service = RetrievalService()

        results = retrieval_service.debug_search(
            query=request.query,
            top_k=request.top_k,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return SearchResponse(
        query=request.query,
        threshold=settings.RAG_SIMILARITY_THRESHOLD,
        results=[
            SearchResultResponse(
                document_id=item.result.document_id,
                page_number=item.result.page_number,
                chunk_index=item.result.chunk_index,
                text=item.result.text,
                similarity=item.result.similarity,
                accepted=item.accepted,
            )
            for item in results
        ],
    )