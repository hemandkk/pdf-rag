from pathlib import Path

import fitz
# import pymupdf  # Future-proof way


class PDFService:
    @staticmethod
    def extract_text(file_path: str) -> tuple[str, int]:
        """
        Extract text from a PDF.

        Returns:
            tuple[str, int]:
                - extracted text
                - number of pages
        """

        pdf_path = Path(file_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        document = fitz.open(file_path)

        try:
            pages = []

            for page in document:
                text = page.get_text()

                if text.strip():
                    pages.append(text.strip())

            full_text = "\n\n".join(pages)

            return full_text, len(document)

        finally:
            document.close()