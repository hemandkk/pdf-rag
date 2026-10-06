import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import settings
from app.schemas.document import DocumentUploadResponse
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

    document_id = str(uuid.uuid4())

    file_path = (
        upload_directory
        / f"{document_id}.pdf"
    )

    max_file_size = (
        settings.MAX_FILE_SIZE_MB
        * 1024
        * 1024
    )

    total_size = 0

    try:
        with file_path.open("wb") as destination:

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

    except Exception as exc:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to process PDF: {str(exc)}",
        ) from exc

    return DocumentUploadResponse(
        document_id=result.document_id,
        filename=file.filename,
        page_count=result.page_count,
        character_count=result.character_count,
        text_preview=result.text_preview,
    )