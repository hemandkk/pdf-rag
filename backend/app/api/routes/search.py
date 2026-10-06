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
def search_document(
    request: SearchRequest,
) -> SearchResponse:

    try:
        retrieval_service = (
            RetrievalService()
        )

        results = (
            retrieval_service.debug_search(
                document_id=(
                    request.document_id
                ),
                query=request.query,
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

    return SearchResponse(
        document_id=request.document_id,
        query=request.query,
        threshold=(
            settings.RAG_SIMILARITY_THRESHOLD
        ),
        results=[
            SearchResultResponse(
                page_number=(
                    item.result.page_number
                ),
                chunk_index=(
                    item.result.chunk_index
                ),
                text=item.result.text,
                similarity=(
                    item.result.similarity
                ),
                accepted=item.accepted,
            )
            for item in results
        ],
    )