from uuid import uuid4

from app.db.models.knowledge_base import KnowledgeBase
from app.repositories.knowledge_base_repository import (
    KnowledgeBaseRepository,
)
from app.schemas.knowledge_base import (
    KnowledgeBaseCreate,
    KnowledgeBaseUpdate,
)


class KnowledgeBaseService:
    def __init__(
        self,
        repository: KnowledgeBaseRepository,
    ) -> None:
        self.repository = repository

    def create(
        self,
        data: KnowledgeBaseCreate,
    ) -> KnowledgeBase:
        knowledge_base = KnowledgeBase(
            id=str(uuid4()),
            name=data.name,
            description=data.description,
        )

        return self.repository.create(
            knowledge_base
        )

    def get(
        self,
        knowledge_base_id: str,
    ) -> KnowledgeBase:
        knowledge_base = self.repository.get_by_id(
            knowledge_base_id
        )

        if knowledge_base is None:
            raise ValueError(
                "Knowledge base not found."
            )

        return knowledge_base

    def list_all(self) -> list[KnowledgeBase]:
        return self.repository.list_all()

    def update(
        self,
        knowledge_base_id: str,
        data: KnowledgeBaseUpdate,
    ) -> KnowledgeBase:
        knowledge_base = self.get(
            knowledge_base_id
        )

        if data.name is not None:
            knowledge_base.name = data.name

        if data.description is not None:
            knowledge_base.description = (
                data.description
            )

        return self.repository.update(
            knowledge_base
        )

    def delete(
        self,
        knowledge_base_id: str,
    ) -> None:
        knowledge_base = self.get(
            knowledge_base_id
        )

        self.repository.delete(
            knowledge_base
        )