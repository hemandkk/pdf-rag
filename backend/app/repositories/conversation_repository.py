from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.conversation import Conversation


class ConversationRepository:
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def create(
        self,
        conversation: Conversation,
    ) -> Conversation:
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_by_id(
        self,
        conversation_id: str,
    ) -> Conversation | None:
        statement = select(Conversation).where(
            Conversation.id == conversation_id
        )

        return self.db.scalar(statement)

    def list_by_knowledge_base(
        self,
        knowledge_base_id: str,
    ) -> list[Conversation]:
        statement = (
            select(Conversation)
            .where(
                Conversation.knowledge_base_id
                == knowledge_base_id
            )
            .order_by(
                Conversation.updated_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def update(
        self,
        conversation: Conversation,
    ) -> Conversation:
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def delete(
        self,
        conversation: Conversation,
    ) -> None:
        self.db.delete(conversation)
        self.db.commit()