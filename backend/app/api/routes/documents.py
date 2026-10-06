import uuid
from pathlib import Path

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.schemas.document import (
    DocumentListResponse,
)
from app.schemas.document import (
    DocumentResponse,
)
from app.schemas.document import (
    DocumentUploadResponse,
)
from app.services.document_service import (
    DocumentService,
)
from app.services.rag_ingestion_service import (
    RAGIngestionService,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> DocumentUploadResponse:

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required.",
        )

    file_extension = Path(
        file.filename
    ).suffix.lower()

    if file_extension != ".pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    upload_directory = Path(
        settings.UPLOAD_DIR
    )

    upload_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    document_id = str(
        uuid.uuid4()
    )

    stored_filename = (
        f"{document_id}.pdf"
    )

    file_path = (
        upload_directory
        / stored_filename
    )

    max_file_size = (
        settings.MAX_FILE_SIZE_MB
        * 1024
        * 1024
    )

    total_size = 0

    try:
        with file_path.open(
            "wb"
        ) as destination:

            while chunk := await file.read(
                1024 * 1024
            ):

                total_size += len(chunk)

                if total_size > max_file_size:

                    destination.close()

                    if file_path.exists():
                        file_path.unlink()

                    raise HTTPException(
                        status_code=(
                            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
                        ),
                        detail=(
                            f"PDF size cannot exceed "
                            f"{settings.MAX_FILE_SIZE_MB} MB."
                        ),
                    )

                destination.write(chunk)

    finally:
        await file.close()

    document_service = (
        DocumentService(db)
    )

    document = (
        document_service.create_processing_document(
            document_id=document_id,
            filename=file.filename,
            stored_filename=stored_filename,
            file_path=str(file_path),
        )
    )

    try:
        ingestion_service = (
            RAGIngestionService()
        )

        result = (
            ingestion_service.ingest_document(
                document_id=document_id,
                file_path=str(file_path),
            )
        )

        document_service.mark_ready(
            document=document,
            page_count=result.page_count,
            character_count=(
                result.character_count
            ),
            chunk_count=result.chunk_count,
        )

    except Exception as exc:

        document_service.mark_failed(
            document=document,
            error_message=str(exc),
        )

        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                f"Unable to process PDF: {str(exc)}"
            ),
        ) from exc

    return DocumentUploadResponse(
        document_id=document.id,
        filename=document.filename,
        page_count=document.page_count,
        character_count=(
            document.character_count
        ),
        chunk_count=document.chunk_count,
        status=document.status,
        text_preview=result.text_preview,
    )


@router.get(
    "",
    response_model=DocumentListResponse,
)
def list_documents(
    db: Session = Depends(get_db),
) -> DocumentListResponse:

    document_service = (
        DocumentService(db)
    )

    documents = (
        document_service.list_all()
    )

    return DocumentListResponse(
        documents=[
            DocumentResponse.model_validate(
                document,
                from_attributes=True,
            )
            for document in documents
        ]
    )


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: str,
    db: Session = Depends(get_db),
) -> DocumentResponse:

    document_service = (
        DocumentService(db)
    )

    document = (
        document_service.get_by_id(
            document_id
        )
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return DocumentResponse.model_validate(
        document,
        from_attributes=True,
    )