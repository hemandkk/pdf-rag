from collections.abc import Iterator
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.constants import DEFAULT_KNOWLEDGE_BASE_ID
from app.db.models.conversation import Conversation
from app.db.models.message import Message
from app.repositories.conversation_repository import (
    ConversationRepository,
)
from app.repositories.message_repository import (
    MessageRepository,
)
from app.schemas.conversation import (
    ConversationDetailResponse,
)
from app.services.rag_service import RAGService


class ConversationService:
    def __init__(
        self,
        db: Session,
        rag_service: RAGService,
    ) -> None:
        self.conversation_repository = (
            ConversationRepository(db)
        )

        self.message_repository = (
            MessageRepository(db)
        )

        self.rag_service = rag_service

    def create(
        self,
        title: str = "New conversation",
    ) -> Conversation:
        conversation = Conversation(
            id=str(uuid4()),
            knowledge_base_id=(
                DEFAULT_KNOWLEDGE_BASE_ID
            ),
            title=title,
        )

        return self.conversation_repository.create(
            conversation
        )

    def get(
        self,
        conversation_id: str,
    ) -> Conversation | None:
        return self.conversation_repository.get_by_id(
            conversation_id
        )

    def list_all(
        self,
    ) -> list[Conversation]:
        return self.conversation_repository.list_by_knowledge_base(
            DEFAULT_KNOWLEDGE_BASE_ID
        )

    def get_detail(
        self,
        conversation_id: str,
    ) -> ConversationDetailResponse | None:
        conversation = self.get(
            conversation_id
        )

        if conversation is None:
            return None

        messages = (
            self.message_repository.list_by_conversation(
                conversation_id
            )
        )

        return ConversationDetailResponse(
            id=conversation.id,
            knowledge_base_id=(
                conversation.knowledge_base_id
            ),
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=messages,
        )

    def _get_history(
        self,
        conversation_id: str,
    ) -> list[dict[str, str]]:
        messages = (
            self.message_repository.list_by_conversation(
                conversation_id
            )
        )

        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

    def stream_message(
        self,
        conversation_id: str,
        question: str,
        top_k: int | None = None,
    ) -> tuple[list, Iterator[str]]:
        conversation = self.get(
            conversation_id
        )

        if conversation is None:
            raise ValueError(
                "Conversation not found."
            )

        if (
            conversation.knowledge_base_id
            != DEFAULT_KNOWLEDGE_BASE_ID
        ):
            raise ValueError(
                "Conversation does not belong to "
                "the default knowledge base."
            )

        history = self._get_history(
            conversation_id
        )

        user_message = Message(
            id=str(uuid4()),
            conversation_id=conversation_id,
            role="user",
            content=question,
        )

        self.message_repository.create(
            user_message
        )

        sources, token_stream = (
            self.rag_service.stream(
                question=question,
                history=history,
                top_k=top_k,
            )
        )

        def wrapped_stream() -> Iterator[str]:
            answer_parts: list[str] = []

            try:
                for token in token_stream:
                    answer_parts.append(token)
                    yield token

                answer = "".join(answer_parts)

                assistant_message = Message(
                    id=str(uuid4()),
                    conversation_id=conversation_id,
                    role="assistant",
                    content=answer,
                )

                self.message_repository.create(
                    assistant_message
                )

            except Exception:
                raise

        return sources, wrapped_stream()