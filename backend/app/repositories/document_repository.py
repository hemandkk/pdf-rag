from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.document import Document


class DocumentRepository:
    def __init__(self, db: Session) -> None:
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
        statement = select(Document).where(
            Document.id == document_id
        )

        return self.db.scalar(statement)

    def get_by_knowledge_base(
        self,
        knowledge_base_id: str,
    ) -> list[Document]:
        statement = (
            select(Document)
            .where(
                Document.knowledge_base_id
                == knowledge_base_id
            )
            .order_by(
                Document.created_at.asc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def update(
        self,
        document: Document,
    ) -> Document:
        self.db.commit()
        self.db.refresh(document)

        return document

    def delete(
        self,
        document: Document,
    ) -> None:
        self.db.delete(document)
        self.db.commit()