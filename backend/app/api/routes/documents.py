from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.document_repository import (
    DocumentRepository,
)
from app.repositories.knowledge_base_repository import (
    KnowledgeBaseRepository,
)
from app.schemas.document import DocumentResponse
from app.services.chunk_service import ChunkService
from app.services.document_service import (
    DocumentService,
)
from app.services.embedding_service import (
    EmbeddingService,
)
from app.services.pdf_service import PDFService
from app.services.rag_ingestion_service import (
    RagIngestionService,
)
from app.services.vector_service import VectorService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


def get_document_service(
    db: Session = Depends(get_db),
) -> DocumentService:
    document_repository = (
        DocumentRepository(db)
    )

    knowledge_base_repository = (
        KnowledgeBaseRepository(db)
    )

    pdf_service = PDFService()

    chunk_service = ChunkService()

    embedding_service = (
        EmbeddingService()
    )

    vector_service = VectorService()

    rag_ingestion_service = (
        RagIngestionService(
            pdf_service=pdf_service,
            chunk_service=chunk_service,
            embedding_service=embedding_service,
            vector_service=vector_service,
            document_repository=document_repository,
        )
    )

    return DocumentService(
        document_repository=document_repository,
        knowledge_base_repository=(
            knowledge_base_repository
        ),
        rag_ingestion_service=(
            rag_ingestion_service
        ),
    )


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile = File(...),
    service: DocumentService = Depends(
        get_document_service
    ),
) -> DocumentResponse:
    try:
        return service.upload(file)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def list_documents(
    service: DocumentService = Depends(
        get_document_service
    ),
) -> list[DocumentResponse]:
    try:
        return service.list_all()

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: str,
    service: DocumentService = Depends(
        get_document_service
    ),
) -> DocumentResponse:
    try:
        return service.get(document_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc