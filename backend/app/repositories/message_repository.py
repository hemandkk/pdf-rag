from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.message import Message


class MessageRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, message: Message) -> Message:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_by_id(
        self,
        message_id: str,
    ) -> Message | None:
        statement = select(Message).where(
            Message.id == message_id
        )

        return self.db.scalar(statement)

    def list_by_conversation(
        self,
        conversation_id: str,
    ) -> list[Message]:
        statement = (
            select(Message)
            .where(
                Message.conversation_id
                == conversation_id
            )
            .order_by(Message.created_at.asc())
        )

        return list(self.db.scalars(statement).all())

    def delete(
        self,
        message: Message,
    ) -> None:
        self.db.delete(message)
        self.db.commit()