from pathlib import Path

import fitz


class PDFPage:
    def __init__(
        self,
        page_number: int,
        text: str,
    ) -> None:
        self.page_number = page_number
        self.text = text


class PDFService:
    @staticmethod
    def extract_pages(
        file_path: str,
    ) -> list[PDFPage]:
        """
        Extract text from a PDF page by page.

        Page numbers are 1-based so they match what users
        see in the PDF viewer.
        """

        pdf_path = Path(file_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        document = fitz.open(file_path)

        try:
            pages: list[PDFPage] = []

            for index, page in enumerate(document):
                text = page.get_text().strip()

                if not text:
                    continue

                pages.append(
                    PDFPage(
                        page_number=index + 1,
                        text=text,
                    )
                )

            return pages

        finally:
            document.close()

    @staticmethod
    def extract_text(
        file_path: str,
    ) -> tuple[str, int]:
        """
        Backward-compatible helper that returns the
        complete extracted text and page count.
        """

        pages = PDFService.extract_pages(file_path)

        full_text = "\n\n".join(
            page.text
            for page in pages
        )

        return full_text, len(pages)