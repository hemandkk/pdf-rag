import uuid
from collections.abc import Iterator

from sqlalchemy.orm import Session

from app.core.constants import DEFAULT_KNOWLEDGE_BASE_ID
from app.db.models.conversation import Conversation
from app.db.models.message import Message
from app.repositories.conversation_repository import (
    ConversationRepository,
)
from app.repositories.message_repository import MessageRepository
from app.schemas.chat import MessageResponse, SourceResponse
from app.schemas.conversation import ConversationDetailResponse
from app.services.rag_service import RAGService


class ConversationService:
    def __init__(
        self,
        db: Session,
        rag_service: RAGService,
    ) -> None:
        self.db = db
        self.rag_service = rag_service

        self.conversation_repository = ConversationRepository(db)
        self.message_repository = MessageRepository(db)

    def create(
        self,
        title: str = "New conversation",
    ) -> Conversation:
        conversation = Conversation(
            id=str(uuid.uuid4()),
            knowledge_base_id=DEFAULT_KNOWLEDGE_BASE_ID,
            title=title,
        )

        return self.conversation_repository.create(
            conversation
        )

    def list_all(self) -> list[Conversation]:
        return (
            self.conversation_repository
            .list_by_knowledge_base(
                DEFAULT_KNOWLEDGE_BASE_ID
            )
        )

    def get_by_id(
        self,
        conversation_id: str,
    ) -> Conversation | None:
        conversation = (
            self.conversation_repository.get_by_id(
                conversation_id
            )
        )

        if conversation is None:
            return None

        if (
            conversation.knowledge_base_id
            != DEFAULT_KNOWLEDGE_BASE_ID
        ):
            return None

        return conversation

    def get_messages(
        self,
        conversation_id: str,
    ) -> list[Message]:
        conversation = self.get_by_id(
            conversation_id
        )

        if conversation is None:
            raise ValueError(
                "Conversation not found."
            )

        return (
            self.message_repository
            .list_by_conversation(
                conversation_id
            )
        )

    def get_detail(
        self,
        conversation_id: str,
    ) -> ConversationDetailResponse | None:
        conversation = self.get_by_id(
            conversation_id
        )

        if conversation is None:
            return None

        messages = (
            self.message_repository
            .list_by_conversation(
                conversation_id
            )
        )

        return ConversationDetailResponse(
            id=conversation.id,
            knowledge_base_id=conversation.knowledge_base_id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=[
                MessageResponse(
                    id=message.id,
                    conversation_id=message.conversation_id,
                    role=message.role,
                    content=message.content,
                    created_at=message.created_at,
                )
                for message in messages
            ],
        )

    def stream_message(
        self,
        conversation_id: str,
        question: str,
        top_k: int,
    ) -> tuple[
        list[SourceResponse],
        Iterator[str],
    ]:
        print("[Conversation] stream_message entered")

        conversation = self.get_by_id(
            conversation_id
        )

        print("[Conversation] conversation lookup completed")

        if conversation is None:
            raise ValueError(
                "Conversation not found."
            )

        question = question.strip()

        print("[Conversation] question validated")

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        existing_messages = (
            self.message_repository
            .list_by_conversation(
                conversation_id
            )
        )

        print(
            "[Conversation] messages loaded:",
            len(existing_messages),
        )

        history = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in existing_messages
        ]

        print("[Conversation] history built")

        user_message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role="user",
            content=question,
        )

        print("[Conversation] saving user message")

        self.message_repository.create(
            user_message
        )

        print("[Conversation] user message saved")

        print("[Conversation] calling RAGService.stream")

        sources, token_stream = (
            self.rag_service.stream(
                question=question,
                top_k=top_k,
                history=history,
            )
        )

        print("[Conversation] RAGService.stream returned")

        return (
            sources,
            self._persist_assistant_message(
                conversation_id=conversation_id,
                token_stream=token_stream,
            ),
        )        

    def _persist_assistant_message(
        self,
        conversation_id: str,
        token_stream: Iterator[str],
    ) -> Iterator[str]:
        print("[Conversation] assistant stream started")

        collected_tokens: list[str] = []

        try:
            for token in token_stream:
                print("[Conversation] received token:", repr(token))

                collected_tokens.append(token)

                yield token

        except Exception as exc:
            print(
                "[Conversation] assistant stream error:",
                repr(exc),
            )
            raise

        finally:
            print("[Conversation] assistant stream finished")

            assistant_content = "".join(
                collected_tokens
            ).strip()

            print(
                "[Conversation] collected assistant content length:",
                len(assistant_content),
            )

            if not assistant_content:
                print(
                    "[Conversation] No assistant content to persist"
                )
                return

            assistant_message = Message(
                id=str(uuid.uuid4()),
                conversation_id=conversation_id,
                role="assistant",
                content=assistant_content,
            )

            print(
                "[Conversation] saving assistant message"
            )

            self.message_repository.create(
                assistant_message
            )

            print(
                "[Conversation] assistant message saved"
            )

            conversation = (
                self.conversation_repository
                .get_by_id(conversation_id)
            )

            if conversation is not None:
                self.conversation_repository.update(
                    conversation
                )

            print(
                "[Conversation] conversation updated"
            )