from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.knowledge_base import KnowledgeBase


class KnowledgeBaseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        knowledge_base: KnowledgeBase,
    ) -> KnowledgeBase:
        self.db.add(knowledge_base)
        self.db.commit()
        self.db.refresh(knowledge_base)

        return knowledge_base

    def get_by_id(
        self,
        knowledge_base_id: str,
    ) -> KnowledgeBase | None:
        statement = select(KnowledgeBase).where(
            KnowledgeBase.id == knowledge_base_id
        )

        return self.db.scalar(statement)

    def list_all(self) -> list[KnowledgeBase]:
        statement = (
            select(KnowledgeBase)
            .order_by(
                KnowledgeBase.updated_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def update(
        self,
        knowledge_base: KnowledgeBase,
    ) -> KnowledgeBase:
        self.db.commit()
        self.db.refresh(knowledge_base)

        return knowledge_base

    def delete(
        self,
        knowledge_base: KnowledgeBase,
    ) -> None:
        self.db.delete(knowledge_base)
        self.db.commit()