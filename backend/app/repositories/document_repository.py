from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.document import Document


class DocumentRepository:
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def create(
        self,
        document: Document,
    ) -> Document:

        self.db.add(document)

        self.db.commit()

        self.db.refresh(document)

        return document

    def get_by_id(
        self,
        document_id: str,
    ) -> Document | None:

        statement = select(
            Document
        ).where(
            Document.id == document_id
        )

        return self.db.scalar(
            statement
        )

    def list_all(
        self,
    ) -> list[Document]:

        statement = (
            select(Document)
            .order_by(
                Document.created_at.desc()
            )
        )

        return list(
            self.db.scalars(
                statement
            ).all()
        )

    def update(
        self,
        document: Document,
    ) -> Document:

        self.db.add(document)

        self.db.commit()

        self.db.refresh(document)

        return document