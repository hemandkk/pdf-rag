from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.knowledge_base_repository import (
    KnowledgeBaseRepository,
)
from app.schemas.knowledge_base import (
    KnowledgeBaseCreate,
    KnowledgeBaseResponse,
    KnowledgeBaseUpdate,
)
from app.services.knowledge_base_service import (
    KnowledgeBaseService,
)


router = APIRouter(
    prefix="/knowledge-bases",
    tags=["Knowledge Bases"],
)


def get_knowledge_base_service(
    db: Session = Depends(get_db),
) -> KnowledgeBaseService:
    repository = KnowledgeBaseRepository(db)

    return KnowledgeBaseService(
        repository
    )


@router.post(
    "",
    response_model=KnowledgeBaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_knowledge_base(
    data: KnowledgeBaseCreate,
    service: KnowledgeBaseService = Depends(
        get_knowledge_base_service
    ),
) -> KnowledgeBaseResponse:
    return service.create(data)


@router.get(
    "",
    response_model=list[KnowledgeBaseResponse],
)
def list_knowledge_bases(
    service: KnowledgeBaseService = Depends(
        get_knowledge_base_service
    ),
) -> list[KnowledgeBaseResponse]:
    return service.list_all()


@router.get(
    "/{knowledge_base_id}",
    response_model=KnowledgeBaseResponse,
)
def get_knowledge_base(
    knowledge_base_id: str,
    service: KnowledgeBaseService = Depends(
        get_knowledge_base_service
    ),
) -> KnowledgeBaseResponse:
    try:
        return service.get(
            knowledge_base_id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{knowledge_base_id}",
    response_model=KnowledgeBaseResponse,
)
def update_knowledge_base(
    knowledge_base_id: str,
    data: KnowledgeBaseUpdate,
    service: KnowledgeBaseService = Depends(
        get_knowledge_base_service
    ),
) -> KnowledgeBaseResponse:
    try:
        return service.update(
            knowledge_base_id,
            data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{knowledge_base_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_knowledge_base(
    knowledge_base_id: str,
    service: KnowledgeBaseService = Depends(
        get_knowledge_base_service
    ),
) -> None:
    try:
        service.delete(
            knowledge_base_id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc