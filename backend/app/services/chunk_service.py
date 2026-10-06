from dataclasses import dataclass

from app.services.pdf_service import PDFPage


@dataclass
class DocumentChunk:
    chunk_id: str
    document_id: str
    page_number: int
    chunk_index: int
    text: str


class ChunkService:
    DEFAULT_CHUNK_SIZE = 1000
    DEFAULT_CHUNK_OVERLAP = 200

    @classmethod
    def create_chunks(
        cls,
        document_id: str,
        pages: list[PDFPage],
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    ) -> list[DocumentChunk]:

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        chunks: list[DocumentChunk] = []

        global_chunk_index = 0

        for page in pages:

            text = page.text

            start = 0

            while start < len(text):

                end = start + chunk_size

                chunk_text = text[start:end].strip()

                if chunk_text:

                    chunk_id = (
                        f"{document_id}-"
                        f"{global_chunk_index}"
                    )

                    chunks.append(
                        DocumentChunk(
                            chunk_id=chunk_id,
                            document_id=document_id,
                            page_number=page.page_number,
                            chunk_index=global_chunk_index,
                            text=chunk_text,
                        )
                    )

                    global_chunk_index += 1

                if end >= len(text):
                    break

                start = end - chunk_overlap

        return chunks